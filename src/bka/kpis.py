"""
KPI calculations / Berechnung der Kennzahlen.

Implemented KPIs:
  - distance / Distan             [km]   Haversine over lat/lon
  - duration / Dauer              [h]
  - data density / Datendichte    [GB/h] (named in the thesis topic)
  - energy / Energie              [Wh]   trapezoidal integration of P(t) = U(t)*I(t)
  - efficiency / Effizienz        [Wh/km] (named in the thesis topic)
"""

import numpy as np
import pandas as pd


def haversine_m(lat1, lon1, lat2, lon2):
    """
    Great-circle distance in meters between two GPS points.
    Latitude/longitude are spherical coordinates -- naive subtraction
    in degrees is wrong. Haversine is the standard formula.

    Großkreisdistanz in Metern. Lat/Lon sind Kugelkoordinaten,
    naive Subtraktion ist falsch -> Haversine.
    """
    R = 6_371_000.0             # Earth radius in meters / Erdradius in Metern
    p1, p2 = np.deg2rad(lat1), np.deg2rad(lat2)
    dphi = np.deg2rad(lat2 - lat1)
    dlmb = np.deg2rad(lon2 - lon1)
    a = np.sin(dphi / 2) ** 2 + np.cos(p1) * np.cos(p2) * np.sin(dlmb / 2) ** 2
    return 2 * R * np.arcsin(np.sqrt(a))


def trip_distance_km(df: pd.DataFrame) -> float:
    # Sum of segment distances between consecutive GPS points.
    # Summe der Distanzen zwischen aufeinanderfolgenden GPS-Punkten.
    d = haversine_m(
        df["lat"].values[:-1], df["lon"].values[:-1],
        df["lat"].values[1:],  df["lon"].values[1:],
    )
    return float(d.sum() / 1000.0)


def duration_h(df: pd.DataFrame) -> float:
    return float((df["t"].iloc[-1] - df["t"].iloc[0]) / 3600.0)


def data_density_gb_per_h(df: pd.DataFrame) -> float:
    """How much data we log per hour. Total bytes / total hours."""
    gb = df["bytes_logged"].sum() / 1e9
    # max(..., 1e-9) avoids division by zero on a 1-sample dataframe.
    # max(..., 1e-9) vermeidet Division durch Null bei einem DataFrame mit nur einem Sample.
    return gb / max(duration_h(df), 1e-9)


def energy_wh(df: pd.DataFrame) -> float:
    """
    Electrical energy via trapezoidal integration of P(t).
    np.trapezoid handles non-uniform time stamps correctly, which matters
    for real ship logs where samples can be irregular.

    Elektrische Energie via trapezoidale Integration von P(t).
    np.trapezoid behandelt ungleichmäßige Zeitstempel korrekt,
    was für echte Schiffslogs wichtig ist, wo die Abtastzeiten unregelmäßig sein können.
    """
    p = df["voltage"].values * df["current"].values   # power / Leistung [W]
    ws = np.trapezoid(p, df["t"].values)                  # energy / Energy [W*s = J]
    return float(ws / 3600.0)                         # convert to Wh / umrechnen in Wh


def energy_per_km(df: pd.DataFrame) -> float:
    km = trip_distance_km(df)
    return energy_wh(df) / max(km, 1e-9)


def summarize(df: pd.DataFrame) -> dict:
    """
    One-shot KPI dictionary, ready to print as JSON.
    Einmalige Berechnung aller KPIs, bereit zur Ausgabe als JSON.
    """
    return {
        "duration_h":  round(duration_h(df), 3),
        "distance_km": round(trip_distance_km(df), 3),
        "mean_sog_ms": round(float(df["sog"].mean()), 3),
        "mean_tws_ms": round(float(df["tws"].mean()), 3) if "tws" in df else None,
        "energy_wh":   round(energy_wh(df), 1),
        "wh_per_km":   round(energy_per_km(df), 2),
        "gb_per_h":    round(data_density_gb_per_h(df), 4),
    }