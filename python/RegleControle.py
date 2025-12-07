import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from data_analyzer import load_npz
import matplotlib.patches as mpatches

START = np.datetime64("2024-01-27 00:00")
END   = np.datetime64("2024-03-04 00:00")
NIGHT_START, NIGHT_END = 22, 7

SHOW_NIGHT = False
SHOW_COLD  = True

def main():
    time, T_out, RH_out, low, mid, top = load_npz(r"dataverse_files\DataSet.npz")

    mask = (time >= START) & (time <= END)
    t_sel = time[mask]
    top_S1 = top[mask, 0]
    top_S29 = top[mask, 28]
    T_ext_sel = T_out[mask]

    mean_S1_S29 = np.nanmean([top_S1, top_S29])
    print("Température extérieure moyenne :", np.nanmean(T_ext_sel))
    print("S1 Top moyen :", np.nanmean(top_S1))
    print("S29 Top moyen :", np.nanmean(top_S29))
    print("Température moyenne Top (S1 + S29) :", mean_S1_S29)

    t_pd = pd.to_datetime(t_sel)
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(t_pd, top_S1, label="Top S1", linewidth=2)
    ax.plot(t_pd, top_S29, label="Top S29", linewidth=2)
    ax.plot(t_pd, T_ext_sel, label="Température extérieure",
            linewidth=2.5, linestyle='-', color="black")

    ax.set_xlabel("Temps", fontsize=16, fontweight="bold")
    ax.set_ylabel("Température [°C]", fontsize=16, fontweight="bold")
    ax.tick_params(axis="both", labelsize=13)
    ax.grid(False)

    legend_patches = []

    if SHOW_NIGHT:
        p = mpatches.Patch(facecolor="gray", alpha=0.45, label="Nuit (22h–7h)")
        current_day = pd.to_datetime(START).normalize()
        end_day = pd.to_datetime(END)
        while current_day < end_day:
            night_start = current_day + pd.Timedelta(hours=NIGHT_START)
            night_end   = current_day + pd.Timedelta(hours=24 + NIGHT_END)
            ax.axvspan(night_start, night_end, facecolor="gray", alpha=0.45)
            current_day += pd.Timedelta(days=1)
        legend_patches.append(p)

    if SHOW_COLD:
        below_mask = T_ext_sel > -1
        p = mpatches.Patch(facecolor="gray", alpha=0.45, label="T_ext > -1°C")
        in_zone = False
        start_idx = 0
        for i, val in enumerate(below_mask):
            if val and not in_zone:
                in_zone = True
                start_idx = i
            elif not val and in_zone:
                in_zone = False
                ax.axvspan(t_pd[start_idx], t_pd[i], facecolor="gray", alpha=0.45)
        if in_zone:
            ax.axvspan(t_pd[start_idx], t_pd[-1], facecolor="gray", alpha=0.45)
        legend_patches.append(p)

    handles, labels = ax.get_legend_handles_labels()
    for patch in legend_patches:
        handles.append(patch)
        labels.append(patch.get_label())
    ax.legend(handles, labels, fontsize=12, loc="lower right",
              frameon=True, facecolor="white", framealpha=1.0)

    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=8))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
    fig.autofmt_xdate()

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
