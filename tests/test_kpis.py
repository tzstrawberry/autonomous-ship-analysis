from bka.simulate import simulate_trip
from bka.wind import true_wind
from bka.kpis import summarize, trip_distance_km, energy_wh


def test_summary_has_all_keys():
    df = true_wind(simulate_trip(duration_s=60))
    s = summarize(df)
    assert {"duration_h", "distance_km", "energy_wh",
            "wh_per_km", "gb_per_h"} <= s.keys()


def test_distance_positive():
    # A moving ship over 60 s must cover > 0 km.
    # Ein sich bewegendes Schiff muss in 60 s > 0 km zurücklegen.
    assert trip_distance_km(simulate_trip(duration_s=60)) > 0


def test_energy_positive():
    # 48 V * ~30 A over 60 s -> definitely > 0 Wh.
    # 48 V * ~30 A über 60 s -> definitiv > 0 Wh.
    assert energy_wh(simulate_trip(duration_s=60)) > 0