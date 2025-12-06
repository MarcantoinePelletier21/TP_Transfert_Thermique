import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from data_analyzer import load_npz


# ---------------------------------------------------------------
# Configuration du range temporel
# ---------------------------------------------------------------
START = np.datetime64("2024-01-27 00:00")
END   = np.datetime64("2024-03-04 00:00")

NIGHT_START = 22  # 22:00
NIGHT_END = 7     # 07:00

# ---------------------------------------------------------------
# Interrupteurs
# ---------------------------------------------------------------
SHOW_NIGHT = False     # surligner les nuits
SHOW_COLD  = True       # surligner T_ext < 3°C


def main():
    # -----------------------------------------------------------
    # Charger les données
    # -----------------------------------------------------------
    time, T_out, RH_out, low, mid, top = load_npz(
        r"dataverse_files\DataSet.npz"
    )

    # -----------------------------------------------------------
    # Sélectionner la période désirée
    # -----------------------------------------------------------
    mask = (time >= START) & (time <= END)

    t_sel = time[mask]
    top_S1 = top[mask, 0]      # S1 = colonne 0
    top_S29 = top[mask, 28]    # S29 = colonne 28
    T_ext_sel = T_out[mask]

    mean_S1_S29 = np.nanmean([top_S1, top_S29])
    mean_Text = np.nanmean(T_ext_sel)
    mean_S1 = np.nanmean(top_S1)
    mean_S29 = np.nanmean(top_S29)

    print("Température extérieure moyenne :", mean_Text)
    print("S1 Top moyen :", mean_S1)
    print("S29 Top moyen :", mean_S29)
    print("Température moyenne Top (S1 + S29) :", mean_S1_S29)



    # -----------------------------------------------------------
    # Préparer les données
    # -----------------------------------------------------------
    t_pd = pd.to_datetime(t_sel)

    # -----------------------------------------------------------
    # Création du graphique
    # -----------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 5))

    # Courbes
    ax.plot(t_pd, top_S1, label="Top S1", linewidth=2)
    ax.plot(t_pd, top_S29, label="Top S29", linewidth=2)
    ax.plot(t_pd, T_ext_sel, label="Température extérieure", linewidth=2.5, linestyle = '-', color = "black")

    ax.set_xlabel("Temps", fontsize=16, fontweight="bold")
    ax.set_ylabel("Température [°C]", fontsize=16, fontweight="bold")
  
    ax.tick_params(axis="both", labelsize=13)
    ax.grid(False)

    import matplotlib.patches as mpatches
    legend_patches = []

    # -----------------------------------------------------------
    # Shading des nuits (22h → 7h)
    # -----------------------------------------------------------
    if SHOW_NIGHT:
        night_patch = mpatches.Patch(facecolor="gray", alpha=0.45, label="Nuit (22h–7h)")

        current_day = pd.to_datetime(START).normalize()
        end_day = pd.to_datetime(END)

        while current_day < end_day:
            night_start = current_day + pd.Timedelta(hours=NIGHT_START)
            next_day = current_day + pd.Timedelta(days=1)
            night_end = current_day + pd.Timedelta(hours=24 + NIGHT_END)

            ax.axvspan(night_start, night_end, facecolor="gray", alpha=0.45)

            current_day = next_day

        legend_patches.append(night_patch)

    # -----------------------------------------------------------
    # Shading lorsque T_ext > 3 °C
    # -----------------------------------------------------------
    if SHOW_COLD:
        # CORRECTION : c'est >3°C, donc :
        below_mask = T_ext_sel > -1

        cold_patch = mpatches.Patch(facecolor="gray", alpha=0.45, label="T_ext >-1°C")

        in_zone = False
        start_idx = 0

        for i, val in enumerate(below_mask):
            if val and not in_zone:
                in_zone = True
                start_idx = i
            elif not val and in_zone:
                in_zone = False
                ax.axvspan(t_pd[start_idx], t_pd[i],
                           facecolor="gray", alpha=0.45)

        if in_zone:
            ax.axvspan(t_pd[start_idx], t_pd[-1],
                       facecolor="gray", alpha=0.45)

        legend_patches.append(cold_patch)

    # -----------------------------------------------------------
    # Légende complète
    # -----------------------------------------------------------
    handles, labels = ax.get_legend_handles_labels()

    for patch in legend_patches:
        handles.append(patch)
        labels.append(patch.get_label())

    ax.legend(handles, labels, fontsize=12, loc="lower right",
              frameon=True, facecolor="white", framealpha=1.0)

    # -----------------------------------------------------------
    # Format de l’axe du temps
    # -----------------------------------------------------------
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=8))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
    fig.autofmt_xdate()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
