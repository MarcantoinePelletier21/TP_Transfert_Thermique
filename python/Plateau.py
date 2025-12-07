import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
from data_analyzer import load_npz

warnings.filterwarnings("ignore", message="Mean of empty slice")

AVG_WINDOW = "1D"
GROUPS = [
    [2, 3, 4],
    [6, 7, 8],
    [10, 11, 12],
    [14, 15, 16, 17, 18],
    [20, 21, 22],
    [24, 25, 26, 27, 28]
]

USE_DATE_FILTER = True
DATE_START = "2024-02-02"
DATE_END = "2024-02-10"

time, T_out, RH_out, low, mid, top = load_npz(r"dataverse_files\DataSet.npz")

df_time = pd.DataFrame({"time": pd.to_datetime(time)}).set_index("time")

station_means = {}
for i in range(29):
    mean_i = np.nanmean(np.vstack([low[:, i], mid[:, i], top[:, i]]), axis=0)
    station_means[i+1] = mean_i

df = df_time.copy()
for s in range(1, 30):
    df[f"S{s}"] = station_means[s]

if USE_DATE_FILTER:
    df = df.loc[DATE_START:DATE_END]
    print(f"\nFiltre temporel appliqué : {DATE_START} → {DATE_END}")
    print(f"Nombre de points restants : {len(df)}")

df_avg = df.copy() if AVG_WINDOW == 0 else df.resample(AVG_WINDOW).mean()

print("\n=== Moyennes des groupes ===")
group_means_numeric = []
for g_idx, group in enumerate(GROUPS, start=1):
    cols = [f"S{i}" for i in group]
    val = df_avg[cols].mean(axis=1).mean()
    group_means_numeric.append(val)
    print(f"Groupe {g_idx} ({group}) : {val:.2f} °C")

plt.figure(figsize=(14, 6))

if len(GROUPS) == 0:
    for s in range(1, 30):
        plt.plot(df_avg.index, df_avg[f"S{s}"], linewidth=1.2, label=f"S{s}")
    plt.ylabel("Température [°C]", fontsize=12, fontweight="bold")

else:
    for g_idx, group in enumerate(GROUPS, start=1):
        cols = [f"S{i}" for i in group]
        plt.plot(df_avg.index, df_avg[cols].mean(axis=1),
                 linewidth=2.0, label=f"Groupe {g_idx}: S {group}")
    plt.ylabel("Température moyenne [°C]", fontsize=12, fontweight="bold")

plt.xlabel("Temps", fontsize=12, fontweight="bold")
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=12))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
plt.gcf().autofmt_xdate()
plt.grid(True)
plt.legend(ncol=2)
plt.tight_layout()
plt.show()
