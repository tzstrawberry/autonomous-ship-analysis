"""
Synthetic sensor data generator for the research vessel.
Synthetischer Sensordaten-Generator für das Forschungsschiff.

Idea / Idee:
We don't have real ship data, so we fabricate one "test trip" that
looks like an onboard log. Crucially, the anemometer outputs only
APPARENT wind (just like a real one), and the battery outputs only
VOLTAGE and CURRENT (just like a real BMS). True wind and electrical
power are derived later in the pipeline -- not stored here.

Wir haben keine echten Schiffsdaten, also erzeugen wir eine
"Testfahrt", die wie ein Bordlog aussieht. Wichtig: das Anemometer
liefert NUR scheinbaren Wind (wie in echt), die Batterie nur SPANNUNG
und STROM (wie ein echtes BMS). Wahrer Wind und Leistung werden
später in der Pipeline berechnet.
"""

import numpy as np
import pandas as pd


def simulate_trip(duration_s: int = 3600, freq_hz: int = 10, seed: int = 42) -> pd.DataFrame:
    # default_rng is the modern NumPy RNG; seeding makes runs reproducible.
    # default_rng ist der moderne NumPy-Zufallsgenerator; Seed = reproduzierbar.
    rng = np.random.default_rng(seed)

    n = int(duration_s * freq_hz)    # total number of samples  # Gesamtzahl der Abtastwerte
    t = np.arange(n) / freq_hz       # time in seconds since start  # Zeit in Sekunden seit Start

    # ---- 1) Ship kinematics / Schiffskinematik ----
    # Speed over ground oscillates gently around 2.5 m/s (~5 knots).
    # Geschwindigkeit schwankt sanft um 2,5 m/s (~5 Knoten).
    # A real inland vessel doesn't drive at constant speed -> sine wave.
    # Ein echtes Binnenschiff fährt nicht mit konstanter Geschwindigkeit -> Sinuswelle. 
    sog = 2.5 + 0.5 * np.sin(2 * np.pi * t / 600)

    # Course over ground: roughly heading east (90°), meandering a bit.
    # Kurs über Grund: grob Richtung Osten (90°), mit etwas Schwankung.
    cog_deg = 90.0 + 10.0 * np.sin(2 * np.pi * t / 800)
    cog_rad = np.deg2rad(cog_deg)

    # Integrate position step by step (flat-earth ok for short trips).
    # Position aufintegrieren (flache Erde reicht für kurze Strecken).
    dt = 1.0 / freq_hz
    dx = sog * np.sin(cog_rad) * dt   # east displacement per step [m]  # Ostverschiebung pro Schritt [m]
    dy = sog * np.cos(cog_rad) * dt   # north displacement per step [m] # Nordverschiebung pro Schritt [m]
    x = np.cumsum(dx)
    y = np.cumsum(dy)

    # Convert local meters to lat/lon around Berlin Mitte.
    # Umrechnung von lokalen Metern in lat/lon um Berlin Mitte.
    # 1 degree of latitude ≈ 111,320 m everywhere;   
    # 1 degree of longitude shrinks by cos(latitude).
    lat0, lon0 = 52.520, 13.405
    lat = lat0 + y / 111_320.0
    lon = lon0 + x / (111_320.0 * np.cos(np.deg2rad(lat0)))

    # ---- 2) IMU / Inertialsensor ----
    # Inland water = small motions. Add tiny Gaussian noise on top.
    # Binnenwasser = kleine Bewegungen. Fügen Sie zusätzlich ein kleines Gaußsches Rauschen hinzu.
    roll  = 1.0 * np.sin(2 * np.pi * t / 7.0)  + rng.normal(0, 0.1, n)
    pitch = 0.5 * np.sin(2 * np.pi * t / 11.0) + rng.normal(0, 0.1, n)
    yaw   = cog_deg + rng.normal(0, 0.2, n)    # heading ≈ course on a river

    # ---- 3) Wind ----
    # We DEFINE a constant true wind (4 m/s coming FROM west = 270°)
    # and compute what the anemometer on the moving ship would see.
    # Wir DEFINIEREN einen wahren Wind und rechnen, was das Anemometer
    # auf dem fahrenden Schiff messen würde.
    true_ws = 4.0
    true_wd_from = 270.0
    twd_to = (true_wd_from + 180.0) % 360.0     # direction wind blows TO  # Richtung, in die der Wind weht
    twx = true_ws * np.sin(np.deg2rad(twd_to))  # east component  # Ostkomponente
    twy = true_ws * np.cos(np.deg2rad(twd_to))  # north component # Nordkomponente

    # Ship velocity vector in earth frame.
    # Schiffsgeschwindigkeitsvektor im Erdkoordinatensystem.
    svx = sog * np.sin(cog_rad)
    svy = sog * np.cos(cog_rad)

    # Apparent wind = true wind − ship velocity.
    # Scheinbarer Wind = Wahrer Wind − Schiffsgeschwindigkeit.
    # This is the physics: a moving ship "feels" extra headwind.
    # Das ist die Physik: Ein bewegtes Schiff "fühlt" zusätzlichen Gegenwind.
    awx = twx - svx
    awy = twy - svy
    aws = np.hypot(awx, awy) + rng.normal(0, 0.1, n)  # add sensor noise

    # Apparent wind angle relative to the bow, in [-180, 180].
    # Scheinbarer Windwinkel relativ zum Bug, in [-180, 180].
    aw_dir_to = np.rad2deg(np.arctan2(awx, awy)) % 360.0
    awa = (aw_dir_to - cog_deg + 180.0) % 360.0 - 180.0

    # ---- 4) Battery / Batterie ----
    # Real BMS gives voltage and current separately; power = U * I later.
    # Ein echtes BMS liefert Spannung und Strom separat; Leistung = U * I später.
    voltage = 48.0 + rng.normal(0, 0.2, n)                                       # V
    current = 30.0 + 10.0 * np.sin(2 * np.pi * t / 300) + rng.normal(0, 1, n)    # A

    # ---- 5) Logging volume / Datenvolumen ----
    # ~1 kB per sample, varies a bit. Used later for "GB per hour" KPI.
    # ~1 kB pro Sample, variiert etwas. Später für KPI "GB pro Stunde" verwendet.
    bytes_logged = rng.integers(800, 1200, n)

    return pd.DataFrame({
        "t": t, "lat": lat, "lon": lon,
        "sog": sog, "cog": cog_deg,
        "roll": roll, "pitch": pitch, "yaw": yaw,
        "aws": aws, "awa": awa,
        "voltage": voltage, "current": current,
        "bytes_logged": bytes_logged,
    })