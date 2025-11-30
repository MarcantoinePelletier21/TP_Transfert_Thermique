import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"dataverse_files\intemperies_2min_complet.csv", sep=";")
# df.dropna(subset=["Précipitation (mm)"], inplace=True)

# Convertir la colonne Date en datetime
df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
df.dropna(subset=["Précipitation (mm)", "Date"], inplace=True)
# Mettre la date comme index pour le resample
df = df.set_index("Date")

# Binning horaire → somme des précipitations par heure
df_hourly = df["Précipitation (mm)"].resample("H").sum()

print(df_hourly)
plt.plot(df_hourly.index, df_hourly.values)
plt.show()