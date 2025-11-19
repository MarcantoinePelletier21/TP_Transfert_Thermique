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
AVG_WINDOW = "1D"     # <---- CHANGE ICI

# Groupes de stations (indices 1..29)
# Laisser vide → affiche les 29 stations séparément


# GROUPS = [[2,3,4],[6,7,8],[10,11,12], [14,15,16,17,18], [20,21,22],[24,25,26,27,28]]  #groupe pour les plateaux P1,2,...,6  
GROUPS = [[4,8,12,16,18,22,25,28],[1,3,5,7,9,11,13,15,19,21,23,27,29], [2,6,10,14,17,20,24,26]]  #groupe pour les sections gauche, droite et milieu p/r au camion

# ==========================================================
# LOAD DATA
# ==========================================================

time, T_out, RH_out, low, mid, top = load_npz(
    r"dataverse_files\DataSet.npz"
)

df_time = pd.DataFrame({"time": pd.to_datetime(time)})
df_time = df_time.set_index("time")


# ==========================================================
# 1. CALCUL DES MOYENNES VERTICALES PAR STATION
# ==========================================================

station_means = {}  # dict: station index -> np.array temps

for i in range(29):  # stations 0..28
    low_i = low[:, i]
    mid_i = mid[:, i]
    top_i = top[:, i]

    # moyenne verticale des 3 capteurs (na.rm)
    mean_i = np.nanmean(np.vstack([low_i, mid_i, top_i]), axis=0)

    station_means[i+1] = mean_i  # index 1..29


# ==========================================================
# 2. Construire DataFrame complet : une colonne par station
# ==========================================================

df = df_time.copy()

for s in range(1, 30):  # 1..29
    df[f"S{s}"] = station_means[s]


# ==========================================================
# 3. Moyennage temporel conditionnel
# ==========================================================

if AVG_WINDOW == 0:
    df_avg = df.copy()
else:
    df_avg = df.resample(AVG_WINDOW).mean()


# ==========================================================
# 4. Plot
# ==========================================================

plt.figure(figsize=(14, 6))

# ---- Cas A : aucun groupe → tracer les 29 stations ----
if len(GROUPS) == 0:

    for s in range(1, 30):
        plt.plot(df_avg.index, df_avg[f"S{s}"], linewidth=1.2, label=f"S{s}")

    plt.title(f"Moyenne verticale par station (fenêtre: {AVG_WINDOW})",
              fontsize=14, fontweight="bold")
    plt.ylabel("Température [°C]", fontsize=12, fontweight="bold")


# ---- Cas B : groupes définis → tracer un groupe par courbe ----
else:

    for g_idx, group in enumerate(GROUPS, start=1):

        # Colonnes correspondantes à ce groupe
        cols = [f"S{i}" for i in group]

        # Moyenne entre les stations du groupe
        group_mean = df_avg[cols].mean(axis=1)

        plt.plot(df_avg.index, group_mean, linewidth=2.0,
                 label=f"Groupe {g_idx}: {group}")

    plt.title(f"Moyennes verticales par groupe (fenêtre: {AVG_WINDOW})",
              fontsize=14, fontweight="bold")
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
