import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from data_analyzer import load_npz
import numpy as np, matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

HEIGHTS = ("Low","Mid","Top")

class DataGrapherApp:
    def __init__(self, master, npz_path):
        self.master = master
        self.master.title("Thermal Data Grapher")
        self.time, self.T_out, self.RH_out, self.low, self.mid, self.top = load_npz(npz_path)
        self.create_controls()
        self.create_plot_area()

    def create_controls(self):
        f = ttk.Frame(self.master); f.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)

        hf = ttk.LabelFrame(f, text="Heights"); hf.pack(fill=tk.X, pady=5)
        self.height_vars = {}
        for h in HEIGHTS:
            v = tk.BooleanVar(value=(h=="Low"))
            ttk.Checkbutton(hf, text=h, variable=v).pack(anchor="w")
            self.height_vars[h] = v

        ef = ttk.LabelFrame(f, text="External"); ef.pack(fill=tk.X, pady=5)
        self.var_Text = tk.BooleanVar(value=False)
        ttk.Checkbutton(ef, text="T_ext", variable=self.var_Text).pack(anchor="w")

        sf = ttk.LabelFrame(f, text="Stations"); sf.pack(fill=tk.BOTH, expand=True, pady=5)
        self.station_listbox = tk.Listbox(sf, selectmode=tk.MULTIPLE, exportselection=False, height=10)
        self.station_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb = ttk.Scrollbar(sf, orient=tk.VERTICAL, command=self.station_listbox.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.station_listbox.configure(yscrollcommand=sb.set)
        for i in range(1,30): self.station_listbox.insert(tk.END, f"S{i}")

        tf = ttk.LabelFrame(f, text="Time range (optional)"); tf.pack(fill=tk.X, pady=5)
        ttk.Label(tf, text="Start:").grid(row=0, column=0, sticky="e")
        ttk.Label(tf, text="End:").grid(row=1, column=0, sticky="e")
        self.entry_start = ttk.Entry(tf, width=22); self.entry_end = ttk.Entry(tf, width=22)
        self.entry_start.grid(row=0, column=1, padx=2, pady=2)
        self.entry_end.grid(row=1, column=1, padx=2, pady=2)
        ttk.Label(tf, text="Format ex.: 2025-11-01 12:00").grid(row=2, column=0, columnspan=2, pady=2)

        bf = ttk.Frame(f); bf.pack(fill=tk.X, pady=5)
        ttk.Button(bf, text="Plot", command=self.update_plot).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)
        ttk.Button(bf, text="Save figure", command=self.save_figure).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=2)

    def create_plot_area(self):
        pf = ttk.Frame(self.master); pf.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.fig, self.ax = plt.subplots(figsize=(8,4))
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
        self.canvas = FigureCanvasTkAgg(self.fig, master=pf)
        self.canvas.draw(); self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, pf); self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def get_selected_heights(self):
        return [h for h,v in self.height_vars.items() if v.get()]

    def get_selected_stations(self):
        sel = self.station_listbox.curselection()
        return [i+1 for i in sel] if sel else []

    def get_time_mask(self):
        t = self.time; m = np.ones(t.shape[0], dtype=bool)
        s = self.entry_start.get().strip(); e = self.entry_end.get().strip()
        if s:
            st = pd.to_datetime(s, errors="coerce")
            if pd.isna(st): messagebox.showerror("Error", f"Cannot parse start time: {s}"); return None
            m &= t >= np.datetime64(st)
        if e:
            et = pd.to_datetime(e, errors="coerce")
            if pd.isna(et): messagebox.showerror("Error", f"Cannot parse end time: {e}"); return None
            m &= t <= np.datetime64(et)
        if not m.any(): messagebox.showwarning("Warning", "No data points in selected time range."); return None
        return m

    def get_array_for_height(self, h):
        if h=="Low": return self.low
        if h=="Mid": return self.mid
        if h=="Top": return self.top
        raise ValueError("Unknown height")

    def update_plot(self):
        H = self.get_selected_heights()
        S = self.get_selected_stations()
        M = self.get_time_mask()
        if M is None: return
        if not H and not self.var_Text.get():
            messagebox.showerror("Error","Select at least one height or T_ext."); return
        if not S and not self.var_Text.get():
            messagebox.showerror("Error","Select at least one station or T_ext."); return

        self.ax.clear()
        t = self.time[M]

        for h in H:
            arr = self.get_array_for_height(h)
            for s in S:
                self.ax.plot(t, arr[M, s-1], label=f"{h}-S{s}")

        if self.var_Text.get():
            self.ax.plot(t, self.T_out[M], label="T_ext", linewidth=2.5)

        self.ax.set_xlabel("Temps", fontsize=18, fontweight="bold")
        self.ax.set_ylabel("Température [°C]", fontsize=18, fontweight="bold")
        self.ax.tick_params(axis="both", labelsize=15)
        self.ax.legend(fontsize=14, frameon=True)
        self.ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=12))
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        self.fig.autofmt_xdate()
        self.ax.grid(True)
        self.canvas.draw()

    def save_figure(self):
        ft = [("PNG","*.png"),("PDF","*.pdf"),("SVG","*.svg"),("All files","*.*")]
        p = filedialog.asksaveasfilename(defaultextension=".png", filetypes=ft)
        if not p: return
        try:
            self.fig.savefig(p, dpi=300, bbox_inches="tight")
            messagebox.showinfo("Saved", f"Figure saved:\n{p}")
        except Exception as e:
            messagebox.showerror("Error", f"Error:\n{e}")

def main():
    root = tk.Tk()
    DataGrapherApp(root, r"dataverse_files\DataSet.npz")
    root.mainloop()

if __name__=="__main__": main()
