import pandas as pd
import numpy as np

def load_raw_csv(filepath):
    df = pd.read_csv(filepath, sep=";", decimal=",", engine="python")
    if df.shape[1] == 1: df = pd.read_csv(filepath)
    if df.shape[1] < 4: raise ValueError(f"CSV invalide: {df.shape[1]} colonnes")
    cols = list(df.columns)
    df = df.rename(columns={cols[0]: "time", cols[1]: "T_out", cols[2]: "RH_out"})
    df["time"] = pd.to_datetime(df["time"], dayfirst=True, errors="coerce")
    time = df["time"].to_numpy()
    T_out = df["T_out"].to_numpy(float)
    RH_out = df["RH_out"].to_numpy(float)
    sensors = df[df.columns[3:]].to_numpy(float)
    return time, T_out, RH_out, sensors

def split_sensors(sensors):
    if sensors.shape[1] != 87: raise ValueError("87 colonnes requises")
    return sensors[:,0:29], sensors[:,29:58], sensors[:,58:87]

def save_npz(output_path, time, T_out, RH_out, low, mid, top):
    np.savez_compressed(output_path, time=time, T_out=T_out, RH_out=RH_out, low=low, mid=mid, top=top)

def load_npz(filepath):
    d = np.load(filepath)
    return d["time"], d["T_out"], d["RH_out"], d["low"], d["mid"], d["top"]

if __name__ == "__main__":
    csv_path = r"dataverse_files\DataSet.csv"
    npz_path = r"dataverse_files\DataSet.npz"
    time, T_out, RH_out, sensors = load_raw_csv(csv_path)
    low, mid, top = split_sensors(sensors)
    save_npz(npz_path, time, T_out, RH_out, low, mid, top)
    print("DONE:", npz_path)
