"""
Command-line interface / Kommandozeilen-Schnittstelle.

Two subcommands:
  simulate -> generate a synthetic trip and save as Parquet
  analyze  -> read a Parquet trip, compute KPIs, save plots

Zwei Unterbefehle:
    simulate -> generiert eine synthetische Fahrt und speichert sie als Parquet
    analyze  -> liest eine Parquet-Fahrt, berechnet KPIs, speichert Plots
  
Read/write separation lets us swap the simulator for a real-data
loader later without touching the analysis code.

Lese-/Schreib-Trennung: später echte Daten laden, ohne die Analyse anzufassen.
"""

import argparse
import json
import pandas as pd

from .simulate import simulate_trip
from .wind import true_wind
from .kpis import summarize
from .plots import plot_overview, plot_track


def main():
    p = argparse.ArgumentParser(prog="bka")
    sub = p.add_subparsers(dest="cmd", required=True)

    # --- simulate / simulieren ---
    ps = sub.add_parser("simulate", help="Generate a synthetic trip")
    ps.add_argument("--out", required=True, help="output parquet path")
    ps.add_argument("--duration", type=int, default=3600, help="seconds")
    ps.add_argument("--hz", type=int, default=10, help="sampling rate")
    ps.add_argument("--seed", type=int, default=42)

    # --- analyze / analysieren ---
    pa = sub.add_parser("analyze", help="Compute KPIs and plots")
    pa.add_argument("--in", dest="inp", required=True, help="input parquet path")

    args = p.parse_args()

    if args.cmd == "simulate":
        df = simulate_trip(duration_s=args.duration, freq_hz=args.hz, seed=args.seed)
        df.to_parquet(args.out)
        print(f"Wrote {len(df)} rows -> {args.out}")

    elif args.cmd == "analyze":
        df = pd.read_parquet(args.inp)
        df = true_wind(df)                  # add tws/twd columns  # fügt tws/twd-Spalten hinzu
        print(json.dumps(summarize(df), indent=2))
        plot_overview(df, "overview.png")
        plot_track(df, "track.png")
        print("Saved overview.png, track.png")


if __name__ == "__main__":
    main()