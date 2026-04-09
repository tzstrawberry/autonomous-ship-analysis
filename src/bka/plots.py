"""Quick-look plots / Schnellauswertungs-Plots."""

import matplotlib.pyplot as plt


def plot_overview(df, out_path: str = "overview.png") -> str:
    """
    Three stacked time series: speed, true wind, power.
    Drei übereinander gestapelte Zeitreihen: Geschwindigkeit, wahrer Wind, Leistung."""
    fig, axes = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axes[0].plot(df["t"] / 60, df["sog"])
    axes[0].set_ylabel("SOG [m/s]")

    if "tws" in df.columns:
        axes[1].plot(df["t"] / 60, df["tws"])
        axes[1].set_ylabel("True wind [m/s]")

    # Power is derived on the fly: voltage * current.
    # Leistung wird on the fly berechnet: Spannung * Strom.
    power = df["voltage"] * df["current"]
    axes[2].plot(df["t"] / 60, power)
    axes[2].set_ylabel("Power [W]")
    axes[2].set_xlabel("Time [min]")

    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)                    # close to free memory / schließen, um Speicher freizugeben
    return out_path


def plot_track(df, out_path: str = "track.png") -> str:
    """Lat/lon ship track. / Lat/lon Schiffsroute."""
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.plot(df["lon"], df["lat"])
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_title("Ship track / Schiffsroute")
    # Equal aspect so the track isn't visually distorted.
    # Gleiches Seitenverhältnis, damit die Route nicht verzerrt dargestellt wird.
    ax.set_aspect("equal", adjustable="datalim")
    fig.tight_layout()
    fig.savefig(out_path, dpi=120)
    plt.close(fig)
    return out_path