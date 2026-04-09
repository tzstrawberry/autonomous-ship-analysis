from bka.simulate import simulate_trip
from bka.wind import true_wind


def test_true_wind_recovers_injected_value():
    """
    End-to-end check: the simulator injects a constant 4 m/s wind from
    270°. The wind.py module should recover roughly the same values.
    If vector math is wrong anywhere in the chain, this test fails.

    End-to-End-Check: Der Simulator injiziert einen konstanten Wind von 4 m/s
    aus 270°. Das Modul wind.py sollte ungefähr die gleichen Werte zurückliefern.
    Wenn irgendwo in der Kette die Vektorrechnung falsch ist, schlägt dieser Test fehl.
    """
    df = true_wind(simulate_trip(duration_s=300, seed=0))
    assert abs(df["tws"].mean() - 4.0) < 0.5
    # Angle comparison wraps around 360°, so use the (x+180)%360-180 trick.
    # Winkelvergleich: 360°-Wraparound, daher der (x+180)%360-180-Trick.
    assert abs(((df["twd"].mean() - 270.0 + 180) % 360) - 180) < 10