"""
True wind from apparent wind / Wahrer Wind aus scheinbarem Wind.

Physics / Physik:
    v_apparent = v_true - v_ship    (in earth frame / im Erdsystem)
=>  v_true     = v_apparent + v_ship

We add the ship velocity vector back to the apparent wind vector.
Wir addieren den Schiffsgeschwindigkeitsvektor zum scheinbaren Wind.
"""

import numpy as np
import pandas as pd


def true_wind(df: pd.DataFrame) -> pd.DataFrame:
    cog = np.deg2rad(df["cog"].values)

    # Ship velocity in the earth frame (east, north).
    # Schiffsgeschwindigkeitsvektor im Erdkoordinatensystem (Ost, Nord).
    svx = df["sog"].values * np.sin(cog)
    svy = df["sog"].values * np.cos(cog)

    # Apparent wind direction relative to the earth frame:
    # "where the wind goes TO" = ship heading + apparent angle.
    # Scheinbare Windrichtung relativ zum Erdkoordinatensystem:
    # "wohin der Wind weht" = Schiffskurs + scheinbarer Winkel.
    aw_dir_to = np.deg2rad((df["cog"].values + df["awa"].values) % 360.0)
    awx = df["aws"].values * np.sin(aw_dir_to)
    awy = df["aws"].values * np.cos(aw_dir_to)

    # Vector addition: true wind = apparent wind + ship velocity.
    # Vektoraddition: wahrer Wind = scheinbarer Wind + Schiffsgeschwindigkeit.
    twx = awx + svx
    twy = awy + svy

    # Convert back to speed + direction.
    # Zurückrechnen in Geschwindigkeit + Richtung.
    tws = np.hypot(twx, twy)
    twd_to = np.rad2deg(np.arctan2(twx, twy)) % 360.0
    # Meteorology reports the direction the wind comes FROM, not goes TO.
    # Meteorologie: Windrichtung = woher der Wind kommt.
    twd_from = (twd_to + 180.0) % 360.0

    out = df.copy()
    out["tws"] = tws
    out["twd"] = twd_from
    return out