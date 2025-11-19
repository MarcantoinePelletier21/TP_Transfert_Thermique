import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import warnings
from data_analyzer import load_npz

# Ignore empty-slice warnings (some rows fully NaN)
warnings.filterwarnings("ignore", message="Mean of empty slice")

# ===============================
# PARAMÈTRE À MODIFIER ICI
# Exemple :
#   "1H" = moyenne horaire
#   "1D" = moyenne journalière
#   "7D" = moyenne hebdomadaire
#   "30min" = moyenne aux 30 minutes
# ===============================

AVG_WINDOW = "1D"   # <<< CHANGE JUSTE ÇA

# ===============================
# Load dataset
# ===============================

time, T_out, RH_out, low, mid, top = load_npz(
    r"dataverse_files\DataSet.npz"
)

# Moyenne temporelle par timestep (ignore les NaN)
mean_low = np.nanmean(low, axis=1)
mean_mid = np.nanmean(mid, axis=1)
mean_top = np.nanmean(top, axis=1)

# Convertir en DataFrame
df = pd.DataFrame({
    "time": time,
    "mean_low": mean_low,
    "mean_mid": mean_mid,
    "mean_top": mean_top
})

df["time"] = pd.to_datetime(df["time"])
df = df.set_index("time")

# ===============================
# Moyennage flexible
# ===============================

df_avg = df.resample(AVG_WINDOW).mean()

# ===============================
# Plot
# ===============================

plt.figure(figsize=(12, 4))
plt.plot(df_avg.index, df_avg["mean_low"], label=f"Low ({AVG_WINDOW})", linewidth=2)
plt.plot(df_avg.index, df_avg["mean_mid"], label=f"Mid ({AVG_WINDOW})", linewidth=2)
plt.plot(df_avg.index, df_avg["mean_top"], label=f"Top ({AVG_WINDOW})", linewidth=2)

plt.xlabel("Temps", fontsize=13, fontweight="bold")
plt.ylabel("Température moyenne [°C]", fontsize=13, fontweight="bold")
plt.title(f"Température moyenne — Résolution: {AVG_WINDOW}", fontsize=14, fontweight="bold")

plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=10))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
plt.gcf().autofmt_xdate()

plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
