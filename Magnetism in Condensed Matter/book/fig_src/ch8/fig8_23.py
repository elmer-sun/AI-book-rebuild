# -*- coding: utf-8 -*-
# 图 8.23 La1-xSrxMnO3 (x=0.175) 庞磁电阻（Tokura 等 1994）：
# (a) 不同磁场下 rho-T 曲线（峰降低、峰位右移） (b) 等温 rho-B 曲线（负磁电阻）
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from mplstyle import save_fig

fig, axs = plt.subplots(1, 2, figsize=(9.4, 3.8))


def seg(ax, pts, d0, d1):
    """PCHIP curve with solid/dotted/solid segmentation between d0 and d1."""
    px, py = zip(*pts)
    f = PchipInterpolator(px, py)
    xs = np.linspace(px[0], px[-1], 700)
    ys = f(xs)
    m1, m2 = xs <= d0, xs >= d1
    ax.plot(xs[m1], ys[m1], 'k-', lw=1.3)
    mid = (xs > d0) & (xs < d1)
    ax.plot(xs[mid], ys[mid], ':', lw=1.9, color='k', dash_capstyle='round')
    ax.plot(xs[m2], ys[m2], 'k-', lw=1.3)


# ---------------------------------------------------------------- (a)
ax = axs[0]
curves_a = [
    ('B = 0T', [(200, 0.18), (225, 0.22), (250, 0.33), (258, 0.45), (265, 0.8),
                (273, 1.6), (281, 3.0), (288, 4.9), (291, 5.3), (296, 5.25),
                (302, 5.05), (315, 4.6), (330, 4.3), (350, 4.0), (375, 3.72),
                (400, 3.5)], 258, 296, (317, 5.38)),
    ('3T',     [(200, 0.18), (235, 0.25), (262, 0.4), (275, 0.7), (288, 1.6),
                (300, 3.3), (310, 4.4), (318, 4.38), (330, 4.2), (350, 3.9),
                (375, 3.6), (400, 3.32)], 275, 315, (322, 4.52)),
    ('8T',     [(200, 0.19), (240, 0.28), (270, 0.45), (295, 0.85), (315, 1.9),
                (330, 3.0), (338, 3.32), (348, 3.3), (365, 3.15), (385, 2.95),
                (400, 2.82)], 298, 342, (352, 3.5)),
    ('15T',    [(200, 0.20), (245, 0.3), (280, 0.5), (305, 0.85), (330, 1.8),
                (348, 2.55), (358, 2.8), (370, 2.8), (385, 2.7), (400, 2.6)],
     318, 362, (376, 2.95)),
]
for lab, pts, d0, d1, (lx, ly) in curves_a:
    seg(ax, pts, d0, d1)
    ax.text(lx, ly, lab, fontsize=9)
ax.text(204, 5.5, '(a)', fontsize=11)
ax.text(204, 5.02, r'$x$ = 0.175', fontsize=10)
ax.set_xlim(200, 400)
ax.set_ylim(0, 5.75)
ax.set_xticks([200, 300, 400])
ax.set_xticks([250, 350], minor=True)
ax.set_yticks([0, 2, 4])
ax.set_xlabel('Temperature (K)', fontsize=11, labelpad=1)
ax.set_ylabel(r'Resistivity ($10^{-2}\,\Omega$ cm)', fontsize=10.5, labelpad=2)

# ---------------------------------------------------------------- (b)
ax = axs[1]
curves_b = [
    ('78K',  [(0, 0.05), (15, 0.05)], None, None, (0.45, 0.17)),
    ('254K', [(0, 0.45), (0.7, 0.36), (1.5, 0.30), (3, 0.26), (6, 0.23),
              (10, 0.215), (15, 0.21)], None, None, (0.45, 0.60)),
    ('274K', [(0, 1.2), (0.8, 0.9), (1.8, 0.7), (3, 0.6), (5, 0.53),
              (8, 0.48), (12, 0.45), (15, 0.44)], None, None, (0.45, 1.38)),
    ('284K', [(0, 2.0), (0.6, 1.45), (1.5, 1.05), (3, 0.85), (5, 0.74),
              (8, 0.66), (12, 0.61), (15, 0.59)], 0, 0.9, (0.45, 2.18)),
    ('294K', [(0, 4.8), (0.4, 3.6), (1, 2.6), (2, 1.95), (3, 1.65), (5, 1.42),
              (8, 1.28), (12, 1.2), (15, 1.17)], 0, 1.6, (2.7, 2.02)),
    ('304K', [(0, 4.9), (0.5, 3.7), (1.2, 2.7), (2.5, 1.95), (4, 1.6),
              (6, 1.45), (10, 1.32), (15, 1.25)], 0, 1.9, (2.7, 2.5)),
    ('330K', [(0, 5.0), (0.8, 4.2), (2, 3.2), (3.5, 2.5), (5, 2.2), (8, 2.0),
              (12, 1.88), (15, 1.83)], 0, 1.5, (3.0, 3.3)),
    ('343K', [(0, 5.15), (1, 4.5), (2.5, 3.6), (4, 3.05), (6, 2.65), (9, 2.35),
              (12, 2.15), (15, 2.05)], None, None, (3.4, 3.85)),
]
for lab, pts, d0, d1, (lx, ly) in curves_b:
    if d0 is None:
        px, py = zip(*pts)
        f = PchipInterpolator(px, py)
        xs = np.linspace(px[0], px[-1], 500)
        ax.plot(xs, f(xs), 'k-', lw=1.3)
    else:
        seg(ax, pts, d0, d1)
    ax.text(lx, ly, lab, fontsize=8.5)
ax.text(0.25, 5.5, '(b)', fontsize=11)
ax.text(14.75, 5.32, r'$x$ = 0.175', fontsize=10, ha='right')
ax.set_xlim(0, 15)
ax.set_ylim(0, 5.75)
ax.set_xticks([0, 5, 10, 15])
ax.set_yticks([0, 2, 4])
ax.set_xlabel('Magnetic field (T)', fontsize=11, labelpad=1)
ax.set_ylabel(r'Resistivity ($10^{-2}\,\Omega$ cm)', fontsize=10.5, labelpad=2)

for ax in axs:
    ax.tick_params(labelsize=9.5)

fig.subplots_adjust(left=0.075, right=0.985, bottom=0.135, top=0.975, wspace=0.30)
save_fig(fig, 'ch8', 'fig8_23')
