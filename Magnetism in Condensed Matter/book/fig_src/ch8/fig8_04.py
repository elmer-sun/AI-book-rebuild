# -*- coding: utf-8 -*-
# 图 8.4 Au1-xFeX 磁相图（Coles 等 1978）：SG/CG/SP/F/F+CG（P=顺磁按图注补标）
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.0, 4.6)

def smooth(pts, n=200):
    p = PchipInterpolator([q[0] for q in pts], [q[1] for q in pts])
    x = np.linspace(pts[0][0], pts[-1][0], n)
    return x, p(x)

# SG lower boundary (low-concentration nearly linear rise)
x, y = smooth([(0, 0), (2, 10), (4, 20), (6, 27), (8, 30.5),
               (10, 33.5), (12, 36.5), (14, 40), (15.7, 43)])
ax.plot(x, y, 'k-', lw=1.2)
# vertical CG / F+CG line
ax.plot([15.7, 15.7], [0, 43], 'k-', lw=1.0)
# steep CG/F+CG -> F boundary (solid)
x, y = smooth([(15.7, 43), (16, 46), (16.5, 52), (17, 62), (17.5, 70),
               (18, 80), (19, 100), (20, 125), (21, 150), (21.5, 165),
               (21.9, 180), (22.2, 192)])
ax.plot(x, y, 'k-', lw=1.2)
# SP boundary (dashed, left/above the solid steep line)
x, y = smooth([(8.5, 33), (10, 38), (11, 44), (12, 52), (13, 66), (14, 84),
               (15, 105), (16, 128), (17, 148), (18, 165), (18.6, 178),
               (19.2, 190)])
ax.plot(x, y, 'k--', lw=1.0, dashes=(5, 3))
# low-temperature F+CG / F boundary descending from the junction
x, y = smooth([(15.7, 43), (16.5, 40), (17.5, 32), (18.5, 26), (20, 17),
               (21.5, 12), (23, 8.5), (23.8, 7)])
ax.plot(x, y, 'k-', lw=1.0)

# experimental points (simplified two families: filled / open)
sg = [(2, 10.5), (2.8, 15), (3.6, 19), (4.4, 22), (5.2, 24.5), (6, 26.5),
      (6.8, 28.5), (7.6, 30), (8.4, 31.5), (9.2, 32.5), (10, 34), (11, 35.5),
      (12, 37), (13, 38.5), (14, 40.5), (15, 42)]
ax.plot([p[0] for p in sg], [p[1] for p in sg], 'ko', ms=4.5)
fill_c = [(15.5, 45), (16.1, 46.5), (19.6, 163)]
ax.plot([p[0] for p in fill_c], [p[1] for p in fill_c], 'ko', ms=4.5)
fill_t = [(12.8, 85), (13.1, 100), (14.6, 104), (15.0, 107)]
ax.plot([p[0] for p in fill_t], [p[1] for p in fill_t], 'k^', ms=5.5)
fill_s = [(17, 127), (19.4, 127), (16.9, 88)]
ax.plot([p[0] for p in fill_s], [p[1] for p in fill_s], 'ks', ms=5)
open_s = [(19.4, 159), (21, 175)]
ax.plot([p[0] for p in open_s], [p[1] for p in open_s], 'ks', ms=5, mfc='white')
ax.plot([18.6], [167], 'kx', ms=7, mew=1.5)
open_t = [(16.0, 43), (16.4, 42), (15.9, 51)]
ax.plot([p[0] for p in open_t], [p[1] for p in open_t], 'k^', ms=5.5, mfc='white')
open_t2 = [(18.3, 27.5), (19.2, 23.5), (22.0, 10)]
ax.plot([p[0] for p in open_t2], [p[1] for p in open_t2], 'k^', ms=5.5, mfc='white')
desc_s = [(16.8, 38), (17.5, 31), (18.1, 25), (23.3, 7)]
ax.plot([p[0] for p in desc_s], [p[1] for p in desc_s], 'ks', ms=5)

# region labels (P added per caption definition)
ax.text(4.3, 13, 'SG', fontsize=12, ha='center')
ax.text(12.3, 13, 'CG', fontsize=12, ha='center')
ax.text(17.5, 13, 'F+CG', fontsize=12, ha='center')
ax.text(14.1, 52, 'SP', fontsize=12, ha='center')
ax.text(21, 115, 'F', fontsize=12, ha='center')
ax.text(4.5, 140, 'P', fontsize=12, ha='center')

ax.set_xlim(0, 24.5)
ax.set_ylim(0, 195)
ax.set_xticks([0, 4, 8, 12, 16, 20, 24])
ax.set_yticks([40, 80, 120, 160, 180])
ax.set_xlabel(r'$C$ (at.%Fe)', fontsize=12, labelpad=1)
ax.set_ylabel(r'$T$ (K)', fontsize=12)

save_fig(fig, 'ch8', 'fig8_04')
