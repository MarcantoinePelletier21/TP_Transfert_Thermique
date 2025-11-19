import pandas as pd
import numpy as np

# ============================================================
# 1) LOAD RAW CSV (ONE TIME) — ROBUST VERSION
# ============================================================

def load_raw_csv(filepath):
    """
    Load the CSV file and return the raw numpy arrays.
    CSV structure:
        col 0 : time (date + hour)
        col 1 : outside temperature
        col 2 : outside relative humidity
        col 3.. : sensors (Low-S1..Low-S29, Mid-S1..Mid-S29, Top-S1..Top-S29)
    """

    # ---- 1) First try: CSV "français" (semicolon + decimal comma) ----
    df = pd.read_csv(filepath, sep=";", decimal=",", engine="python")

    # If we still only have 1 column, fallback to standard CSV (comma)
    if df.shape[1] == 1:
        df = pd.read_csv(filepath)  # sep="," by default

    print("Shape after read_csv:", df.shape)

    if df.shape[1] < 4:
        raise ValueError(
            f"Expected at least 4 columns (time, T_out, RH_out, sensors...), "
            f"but got {df.shape[1]}. Check the CSV separator and header line."
        )

    # ---- 2) Rename first columns for clarity ----
    cols = list(df.columns)
    df = df.rename(columns={
        cols[0]: "time",
        cols[1]: "T_out",
        cols[2]: "RH_out",
    })

    # ---- 3) Parse time column to datetime ----
    # dayfirst=True pour gérer des formats type '31/10/2025 12:00'
    df["time"] = pd.to_datetime(df["time"], dayfirst=True, errors="coerce")

    # ---- 4) Convert to numpy arrays ----
    time = df["time"].to_numpy()
    T_out = df["T_out"].to_numpy(dtype=float)
    RH_out = df["RH_out"].to_numpy(dtype=float)

    # All sensor columns (everything after the first 3)
    sensor_cols = df.columns[3:]
    sensors = df[sensor_cols].to_numpy(dtype=float)

    print("Number of sensor columns:", sensors.shape[1])

    return time, T_out, RH_out, sensors


# ============================================================
# 2) SPLIT SENSORS INTO LOW / MID / TOP (NUMPY)
# ============================================================

def split_sensors(sensors):
    """
    sensors shape = (n_samples, 87)
    Low : 0..28
    Mid : 29..57
    Top : 58..86
    """
    if sensors.shape[1] != 87:
        raise ValueError(
            f"Expected 87 sensor columns (29 Low + 29 Mid + 29 Top), "
            f"but got {sensors.shape[1]}."
        )

    low = sensors[:, 0:29]
    mid = sensors[:, 29:58]
    top = sensors[:, 58:87]
    return low, mid, top


# ============================================================
# 3) SAVE NPZ (ONE TIME)
# ============================================================

def save_npz(output_path, time, T_out, RH_out, low, mid, top):
    np.savez_compressed(
        output_path,
        time=time,
        T_out=T_out,
        RH_out=RH_out,
        low=low,
        mid=mid,
        top=top
    )


# ============================================================
# 4) FAST LOAD NPZ (USE FOR ALL ANALYSIS)
# ============================================================

def load_npz(filepath):
    data = np.load(filepath)
    return (
        data["time"],
        data["T_out"],
        data["RH_out"],
        data["low"],
        data["mid"],
        data["top"]
    )


# ============================================================
# 5) MAIN EXTRACTION (RUN ONLY ONCE)
# ============================================================

if __name__ == "__main__":

    csv_path = r"dataverse_files\DataSet.csv"
    npz_path = r"dataverse_files\DataSet.npz"

    print("Loading CSV...")
    time, T_out, RH_out, sensors = load_raw_csv(csv_path)

    print("Splitting sensors...")
    low, mid, top = split_sensors(sensors)

    print("Saving NPZ...")
    save_npz(npz_path, time, T_out, RH_out, low, mid, top)

    print("DONE. Dataset saved to:", npz_path)
