import numpy as np, pandas as pd, matplotlib.pyplot as plt, matplotlib.dates as mdates, warnings
from data_analyzer import load_npz

warnings.filterwarnings("ignore", message="Mean of empty slice")
AVG_WINDOW = "1D"

time, T_out, RH_out, low, mid, top = load_npz(r"dataverse_files\DataSet.npz")

mean_low = np.nanmean(low,1)
mean_mid = np.nanmean(mid,1)
mean_top = np.nanmean(top,1)

df = pd.DataFrame({"time":time,"mean_low":mean_low,"mean_mid":mean_mid,"mean_top":mean_top})
df["time"]=pd.to_datetime(df["time"]); df=df.set_index("time")
df_avg=df.resample(AVG_WINDOW).mean()

plt.figure(figsize=(12,4))
plt.plot(df_avg.index,df_avg["mean_low"],label=f"Low ({AVG_WINDOW})",lw=2)
plt.plot(df_avg.index,df_avg["mean_mid"],label=f"Mid ({AVG_WINDOW})",lw=2)
plt.plot(df_avg.index,df_avg["mean_top"],label=f"Top ({AVG_WINDOW})",lw=2)

plt.xlabel("Temps",fontsize=13,fontweight="bold")
plt.ylabel("Température moyenne [°C]",fontsize=13,fontweight="bold")
plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=10))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
plt.gcf().autofmt_xdate()
plt.grid(True); plt.legend(); plt.tight_layout(); plt.show()
