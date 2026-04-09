# Autonomous Ship Data Analysis Pipeline

A Python pipeline that turns sensor recordings of an autonomous inland research vessel into operational and performance KPIs. Since no real ship data is available, a synthetic sensor stream stands in for field data.

> Self-initiated implementation based on a publicly available thesis topic from Technische Universität Berlin. No real project data or proprietary materials are used.
> Reference: <https://www.theses.tu-berlin.de/de/theses/019d0b43-9add-74f0-a093-1d014acca9ec>

## Features
- Synthetic sensor stream: GPS, IMU, anemometer, battery
- True wind from apparent wind via vector subtraction
- KPIs: energy efficiency [Wh/km], data density [GB/h], distance, duration, mean wind
- Quick-look plots and unit tests

## Quickstart
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src

python -m bka.cli simulate --out data/trip.parquet --duration 3600
python -m bka.cli analyze --in data/trip.parquet
pytest -q
```

## Tech Stack
Python · NumPy · Pandas · Matplotlib · PyArrow · pytest

---

# 🇩🇪 Deutsche Version

Eine Python-Pipeline, die Sensordaten eines autonomen Binnenforschungsschiffs in Betriebs- und Leistungskennzahlen überführt. Da keine realen Schiffsdaten vorliegen, wird ein synthetischer Sensorstrom als Platzhalter verwendet.

> Eigenständige Umsetzung eines öffentlich zugänglichen Themenvorschlags der Technischen Universität Berlin. Es werden keine realen Projektdaten oder vertraulichen Informationen verwendet.
> Referenz: <https://www.theses.tu-berlin.de/de/theses/019d0b43-9add-74f0-a093-1d014acca9ec>

## Funktionen
- Synthetischer Sensorstrom: GPS, IMU, Anemometer, Batterie
- Wahrer Wind aus scheinbarem Wind per Vektorsubtraktion
- Kennzahlen: Energieeffizienz [Wh/km], Datendichte [GB/h], Strecke, Dauer, mittlerer Wind
- Schnellauswertungs-Plots und Unit-Tests

## Schnellstart
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=src

python -m bka.cli simulate --out data/trip.parquet --duration 3600
python -m bka.cli analyze --in data/trip.parquet
pytest -q
```

## Technologien
Python · NumPy · Pandas · Matplotlib · PyArrow · pytest
