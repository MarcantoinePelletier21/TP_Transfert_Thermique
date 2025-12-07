import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
from data_analyzer import load_npz

warnings.filterwarnings("ignore", message="Mean of empty slice")

# ==========================================================
# PARAMÈTRES À MODIFIER
# ==========================================================

# Moyennage temporel :
#    0      = aucun moyennage temporel
#   "1H"    = moyenne horaire
#   "1D"    = moyenne journalière
#   "7D"    = moyenne hebdomadaire
AVG_WINDOW = "1D"

# Groupes de stations (indices 1..29)
GROUPS = [
    [2, 3, 4],
    [6, 7, 8],
    [10, 11, 12],
    [14, 15, 16, 17, 18],
    [20, 21, 22],
    [24, 25, 26, 27, 28]
]

# ==========================================================
# FILTRE TEMPOREL
# ==========================================================

USE_DATE_FILTER = True   # mettre False pour désactiver
DATE_START = "2024-02-02"
DATE_END   = "2024-02-10"

# ==========================================================
# LOAD DATA
# ==========================================================

time, T_out, RH_out, low, mid, top = load_npz(
    r"dataverse_files\DataSet.npz"
)

df_time = pd.DataFrame({"time": pd.to_datetime(time)})
df_time = df_time.set_index("time")

# ==========================================================
# 1. CALCUL MOYENNE VERTICALE PAR STATION
# ==========================================================

station_means = {}

for i in range(29):  # stations 0..28
    low_i = low[:, i]
    mid_i = mid[:, i]
    top_i = top[:, i]

    # Moyenne verticale des 3 capteurs
    mean_i = np.nanmean(np.vstack([low_i, mid_i, top_i]), axis=0)
    station_means[i+1] = mean_i

# ==========================================================
# 2. CONSTRUIRE DATAFRAME AVEC S1..S29
# ==========================================================

df = df_time.copy()
for s in range(1, 30):
    df[f"S{s}"] = station_means[s]

# ==========================================================
# 2b. FILTRE TEMPOREL
# ==========================================================

if USE_DATE_FILTER:
    df = df.loc[DATE_START:DATE_END]
    print(f"\nFiltre temporel appliqué : {DATE_START} → {DATE_END}")
    print(f"Nombre de points restants : {len(df)}")

# ==========================================================
# 3. MOYENNAGE TEMPOREL
# ==========================================================

if AVG_WINDOW == 0:
    df_avg = df.copy()
else:
    df_avg = df.resample(AVG_WINDOW).mean()

# ==========================================================
# 4. CALCUL DES MOYENNES DES GROUPES
# ==========================================================

print("\n=== Moyennes des groupes ===")
group_means_numeric = []

for g_idx, group in enumerate(GROUPS, start=1):

    cols = [f"S{i}" for i in group]

    # Moyenne spatiale → puis moyenne temporelle
    group_mean_value = df_avg[cols].mean(axis=1).mean()

    group_means_numeric.append(group_mean_value)

    print(f"Groupe {g_idx} ({group}) : {group_mean_value:.2f} °C")

# ==========================================================
# 5. PLOT
# ==========================================================

plt.figure(figsize=(14, 6))

if len(GROUPS) == 0:
    # tracer les 29 stations
    for s in range(1, 30):
        plt.plot(df_avg.index, df_avg[f"S{s}"], linewidth=1.2, label=f"S{s}")

    plt.ylabel("Température [°C]", fontsize=12, fontweight="bold")

else:
    # tracer un groupe par courbe
    for g_idx, group in enumerate(GROUPS, start=1):

        cols = [f"S{i}" for i in group]
        group_mean = df_avg[cols].mean(axis=1)

        plt.plot(df_avg.index, group_mean, linewidth=2.0,
                 label=f"Groupe {g_idx}: S {group}")

    plt.ylabel("Température moyenne [°C]", fontsize=12, fontweight="bold")

# ==========================================================
# Format axes
# ==========================================================

plt.xlabel("Temps", fontsize=12, fontweight="bold")
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=12))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
plt.gcf().autofmt_xdate()

plt.grid(True)
plt.legend(ncol=2)
plt.tight_layout()
plt.show()
