import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from data_analyzer import load_npz
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

HEIGHTS = ("Low", "Mid", "Top")

class DataGrapherApp:
    def __init__(self, master, npz_path):
        self.master = master
        self.master.title("Thermal Data Grapher")

        # ========== Load data ==========
        (self.time,
         self.T_out,
         self.RH_out,
         self.low,
         self.mid,
         self.top) = load_npz(npz_path)

        # ========== UI layout ==========
        self.create_controls()
        self.create_plot_area()

    # ------------------------------------------------------------------ UI
    def create_controls(self):
        ctrl_frame = ttk.Frame(self.master)
        ctrl_frame.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        # Heights checkbuttons
        heights_frame = ttk.LabelFrame(ctrl_frame, text="Heights")
        heights_frame.pack(fill=tk.X, pady=5)

        self.height_vars = {}
        for h in HEIGHTS:
            var = tk.BooleanVar(value=(h == "Low"))  # Low checked by default
            cb = ttk.Checkbutton(heights_frame, text=h, variable=var)
            cb.pack(anchor="w")
            self.height_vars[h] = var

        # --- External temperature ---
        ext_frame = ttk.LabelFrame(ctrl_frame, text="External")
        ext_frame.pack(fill=tk.X, pady=5)

        self.var_Text = tk.BooleanVar(value=False)
        cb_ext = ttk.Checkbutton(ext_frame, text="T_ext", variable=self.var_Text)
        cb_ext.pack(anchor="w")

        # Stations listbox
        stations_frame = ttk.LabelFrame(ctrl_frame, text="Stations")
        stations_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.station_listbox = tk.Listbox(
            stations_frame,
            selectmode=tk.MULTIPLE,
            exportselection=False,
            height=10
        )
        self.station_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # scrollbar for stations
        sb = ttk.Scrollbar(stations_frame, orient=tk.VERTICAL,
                           command=self.station_listbox.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.station_listbox.configure(yscrollcommand=sb.set)

        # populate 1..29
        for i in range(1, 30):
            self.station_listbox.insert(tk.END, f"S{i}")

        # Time range
        time_frame = ttk.LabelFrame(ctrl_frame, text="Time range (optional)")
        time_frame.pack(fill=tk.X, pady=5)

        ttk.Label(time_frame, text="Start:").grid(row=0, column=0, sticky="e")
        ttk.Label(time_frame, text="End:").grid(row=1, column=0, sticky="e")

        self.entry_start = ttk.Entry(time_frame, width=22)
        self.entry_end = ttk.Entry(time_frame, width=22)
        self.entry_start.grid(row=0, column=1, padx=2, pady=2)
        self.entry_end.grid(row=1, column=1, padx=2, pady=2)

        ttk.Label(
            time_frame,
            text="Format ex.: 2025-11-01 12:00"
        ).grid(row=2, column=0, columnspan=2, pady=2)

        # Buttons
        btn_frame = ttk.Frame(ctrl_frame)
        btn_frame.pack(fill=tk.X, pady=5)

        plot_btn = ttk.Button(btn_frame, text="Plot", command=self.update_plot)
        plot_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

        save_btn = ttk.Button(btn_frame, text="Save figure", command=self.save_figure)
        save_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def create_plot_area(self):
        plot_frame = ttk.Frame(self.master)
        plot_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(8, 4))
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    # ------------------------------------------------------------------ Data helpers
    def get_selected_heights(self):
        heights = [h for h, var in self.height_vars.items() if var.get()]
        return heights

    def get_selected_stations(self):
        sel = self.station_listbox.curselection()
        if not sel:
            return []
        stations = [i + 1 for i in sel]
        return stations

    def get_time_mask(self):
        t = self.time
        mask = np.ones(t.shape[0], dtype=bool)

        start_str = self.entry_start.get().strip()
        end_str = self.entry_end.get().strip()

        if start_str:
            start = pd.to_datetime(start_str, errors="coerce", dayfirst=False)
            if pd.isna(start):
                messagebox.showerror("Error", f"Cannot parse start time: {start_str}")
                return None
            start = np.datetime64(start)
            mask &= t >= start

        if end_str:
            end = pd.to_datetime(end_str, errors="coerce", dayfirst=False)
            if pd.isna(end):
                messagebox.showerror("Error", f"Cannot parse end time: {end_str}")
                return None
            end = np.datetime64(end)
            mask &= t <= end

        if not mask.any():
            messagebox.showwarning("Warning", "No data points in selected time range.")
            return None

        return mask

    def get_array_for_height(self, height):
        if height == "Low":
            return self.low
        if height == "Mid":
            return self.mid
        if height == "Top":
            return self.top
        raise ValueError("Unknown height")

    # ------------------------------------------------------------------ Plot logic
    def update_plot(self):
        heights = self.get_selected_heights()
        stations = self.get_selected_stations()
        mask = self.get_time_mask()

        if not heights and not self.var_Text.get():
            messagebox.showerror("Error", "Select at least one height or T_ext.")
            return

        if not stations and not self.var_Text.get():
            messagebox.showerror("Error", "Select at least one station or T_ext.")
            return

        if mask is None:
            return

        self.ax.clear()
        t_sel = self.time[mask]

        # --- Plot stations ---
        for h in heights:
            arr = self.get_array_for_height(h)
            for s in stations:
                y = arr[mask, s - 1]
                label = f"{h}-S{s}"
                self.ax.plot(t_sel, y, label=label)

        # --- Plot external temperature ---
        if self.var_Text.get():
            y_ext = self.T_out[mask]
            self.ax.plot(t_sel, y_ext, label="T_ext", linewidth=2.5)

        # Axis labels
        self.ax.set_xlabel("Temps", fontsize=18, fontweight="bold")
        self.ax.set_ylabel("Température [°C]", fontsize=18, fontweight="bold")

        # Ticks (graduations)
        self.ax.tick_params(axis="both", labelsize=15)

        # Legend
        self.ax.legend(fontsize=14, frameon=True)

        # Time axis formatting
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=12))
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d\n%H:%M"))
        self.fig.autofmt_xdate()

        self.ax.grid(True)
        self.canvas.draw()

    def save_figure(self):
        filetypes = [
            ("PNG", "*.png"),
            ("PDF", "*.pdf"),
            ("SVG", "*.svg"),
            ("All files", "*.*"),
        ]
        path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=filetypes,
            title="Save figure as..."
        )
        if not path:
            return

        try:
            self.fig.savefig(path, dpi=300, bbox_inches="tight")
            messagebox.showinfo("Saved", f"Figure saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", f"Error while saving figure:\n{e}")

def main():
    npz_path = r"dataverse_files\DataSet.npz"

    root = tk.Tk()
    app = DataGrapherApp(root, npz_path)
    root.mainloop()

if __name__ == "__main__":
    main()
