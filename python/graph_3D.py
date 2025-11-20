import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

# -----------------------------
# Higher resolution
# -----------------------------
nx, ny, nz = 32, 8, 8  # much finer grid

# Physical dimensions
L, W, H = 32.0, 4.0, 2.0

# Coordinates of voxel centers
i = np.arange(nx)
j = np.arange(ny)
k = np.arange(nz)

Xc = (i + 0.5) / nx * L
Yc = (j + 0.5) / ny * W
Zc = (k + 0.5) / nz * H

X, Y, Z = np.meshgrid(Xc, Yc, Zc, indexing="ij")

# -----------------------------
# 1) Longitudinal factor f_x
# -----------------------------
f_x = np.piecewise(
    X,
    [
        (X >= 0) & (X < 5),
        (X >= 5) & (X < 10),
        (X >= 10) & (X < 15),
        (X >= 15) & (X < 27),
        (X >= 27)
    ],
    [1.0, 0.8, 0.6, 0.3, 0.6]
)

# -----------------------------
# 2) Width factor f_y (INVERTED)
# centre stays hottest
# y≈0 becomes coldest now
# y≈3 becomes medium
# -----------------------------
f_y = np.zeros_like(Y)

mask_hot   = (Y >= 1.0) & (Y < 3.0)   # unchanged
mask_cold  = (Y >= 0.0) & (Y < 1.0)   # INVERTED: now coldest
mask_med   = (Y >= 3.0)               # INVERTED: now medium

f_y[mask_hot]  = 1.0
f_y[mask_med]  = 0.8
f_y[mask_cold] = 0.5

# -----------------------------
# 3) Height factor f_z (hot bottom, cold top)
# -----------------------------
f_z = 1.0 - Z / 5*H
f_z = np.clip(f_z, 0.0, 1.0)

# -----------------------------
# Combined temperature
# -----------------------------
T = f_x * f_y * f_z

# Normalize 0→1
T_min, T_max = T.min(), T.max()
T_norm = (T - T_min) / (T_max - T_min)

# -----------------------------
# Voxels
# -----------------------------
filled = np.ones_like(T, dtype=bool)
cmap = plt.get_cmap("inferno")
colors = cmap(T_norm)

fig = plt.figure(figsize=(12, 7))
ax = fig.add_subplot(111, projection="3d")

ax.voxels(
    filled,
    facecolors=colors,
    edgecolor="none",
    alpha=0.9
)

ax.set_box_aspect((L, W, H))
ax.set_axis_off()
# ax.set_title("3D Voxel Temperature Field (High Resolution)", pad=10)

norm = Normalize(vmin=0.0, vmax=1.0)
sm = ScalarMappable(norm=norm, cmap=cmap)
sm.set_array([])

cbar = fig.colorbar(sm, ax=ax, shrink=0.6)
cbar.set_label("Temperature Relative [%]")

plt.tight_layout()
plt.show()
