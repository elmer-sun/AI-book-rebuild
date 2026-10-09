# -*- coding: utf-8 -*-
# 图 8.15 LiHoF4 量子相变相图（Bitko 等 1996）：横场下铁磁临界线，
# 实线含核超精细相互作用、虚线仅电子自旋，实心圆为实验数据点
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.0, 3.4)

# solid curve: transverse-field Ising mean field incl. hyperfine coupling
ts = [0, 0.2, 0.4, 0.6, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.55]
Hs = [51, 47, 43, 39.5, 37, 35.8, 34, 31, 27.5, 23, 15.5, 6, 0]
f = PchipInterpolator(ts, Hs)
tt = np.linspace(0, 1.55, 400)
ax.plot(tt, f(tt), 'k-', lw=1.2)
# dashed curve: electronic spins only, merges into the solid near T = 0.9 K
td = np.linspace(0, 0.9, 100)
ax.plot(td, PchipInterpolator([0, 0.3, 0.6, 0.8, 0.9], [39, 38, 36.8, 36.2, 35.8])(td),
        'k--', lw=1.0, dashes=(5, 3))

# experimental points
pts = [(0, 51), (0.1, 49.5), (0.2, 47), (0.3, 44), (0.4, 42), (0.5, 40.5),
       (0.6, 39), (0.8, 37), (1.0, 34), (1.2, 30), (1.3, 27), (1.45, 23)]
px, py = zip(*pts)
ye = [0.7] * 9 + [1.0, 2.5, 2.5]
xe = [0] * 10 + [0.05, 0.04]
ax.errorbar(px, py, yerr=ye, xerr=xe, fmt='o', ms=4.2, color='k',
            ecolor='k', elinewidth=0.8, capsize=2.2, capthick=0.8, lw=0)

ax.text(0.50, 45.5, 'Paramagnet', fontsize=11)
ax.text(0.22, 13.5, 'Ferromagnet', fontsize=11)
ax.text(1.58, 55, r'LiHoF$_4$', fontsize=11, ha='right')

ax.set_xlim(-0.03, 1.68)
ax.set_ylim(-3, 63)
ax.set_xticks([0, 0.4, 0.8, 1.2, 1.6])
ax.set_yticks([0, 20, 40, 60])
ax.set_xlabel(r'$T$ (K)', fontsize=12, labelpad=1)
ax.set_ylabel(r'$H_0$ (kOe)', fontsize=12, labelpad=2)
ax.tick_params(labelsize=10)

fig.subplots_adjust(left=0.14, right=0.97, bottom=0.13, top=0.97)
save_fig(fig, 'ch8', 'fig8_15')
