# -*- coding: utf-8 -*-
# 图 8.16 三幅量子相变/掺杂相图：(a) CePd2Si2 温-压 (b) 有机超导体温-压
# (c) La2-xSrxCuO4 温-掺杂
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.interpolate import PchipInterpolator
from mplstyle import save_fig

fig, axs = plt.subplots(1, 3, figsize=(10.6, 3.5))

# ---------------------------------------------------------------- (a)
ax = axs[0]
tn = PchipInterpolator([0, 2, 4, 6, 8, 10, 12, 14, 15, 16, 17, 18, 19, 20, 21],
                       [10.3, 10.0, 9.4, 8.7, 7.9, 7.15, 6.3, 5.4, 4.9, 4.3, 3.7, 3.0, 2.3, 1.6, 1.05])
p = np.arange(0, 21.1, 1.0)
ax.plot(p, tn(p), 'o', ms=4, color='k', lw=0)
sc = [(22.5, 0.5), (24, 0.85), (26, 1.1), (28, 1.3), (30, 1.25), (32, 0.95), (33.5, 0.5)]
sx, sy = zip(*sc)
ax.plot(sx, sy, '^', ms=4.5, color='k', lw=0)
ax.text(20, 10.1, r'CePd$_2$Si$_2$', fontsize=10.5, ha='center')
ax.text(5, 3.4, 'AF', fontsize=11)
ax.text(28, 5.0, 'M', fontsize=11, ha='center')
ax.text(28, 0.42, 'S', fontsize=11, ha='center')
ax.text(0.04, 0.94, '(a)', transform=ax.transAxes, fontsize=11)
ax.set_xlim(0, 40)
ax.set_ylim(-0.4, 11.4)
ax.set_xticks([0, 10, 20, 30, 40])
ax.set_yticks([0, 5, 10])
ax.set_xlabel('Pressure (kbar)', fontsize=11, labelpad=1)
ax.set_ylabel(r'$T$ (K)', fontsize=11, labelpad=2)
ax.set_title(r'', fontsize=1)

# ---------------------------------------------------------------- (b)
ax = axs[1]
ax.plot([0.13, 0.13], [0, 27.5], ':', color='k', lw=1.1)
ax.plot(0.13, 27.5, 'o', ms=4.2, color='k', lw=0)
ax.plot(0.13, 12, '*', ms=7.5, color='k', lw=0)
ax.plot(0.13, 0, 'o', ms=4.2, color='k', lw=0)
ax.plot(0.45, 11, 's', ms=4, color='k', mfc='w', lw=0)
tri = [(0.52, 10.4), (0.65, 8.8), (0.78, 7.3), (0.90, 4.6), (0.97, 2.2)]
tx, ty = zip(*tri)
ax.plot(tx, ty, '^', ms=4.5, color='k', lw=0)
# "1 kbar" scale bar
ax.plot([0.42, 0.62], [20, 20], 'k-', lw=0.9)
ax.plot([0.42, 0.42], [19.5, 20.5], 'k-', lw=0.9)
ax.plot([0.62, 0.62], [19.5, 20.5], 'k-', lw=0.9)
ax.text(0.52, 21.2, '1 kbar', fontsize=9, ha='center')
ax.text(0.20, 15, 'AF', fontsize=11)
ax.text(0.55, 15, 'M', fontsize=11, ha='center')
ax.text(0.50, 4.3, 'S', fontsize=11, ha='center')
handles = [
    Line2D([], [], ls='none', marker='o', ms=4.2, color='k',
           label=r'$\kappa$-ET$_2$Cu[N(CN)$_2$]Cl'),
    Line2D([], [], ls='none', marker='*', ms=7, color='k',
           label=r'$\kappa$-ET$_2$Cu[N(CN)$_2$]Br'),
    Line2D([], [], ls='none', marker='s', ms=4, mfc='w', color='k',
           label=r'$\kappa$-ET$_2$Cu(CN)[N(CN)$_2$]'),
    Line2D([], [], ls='none', marker='^', ms=4.5, color='k',
           label=r'$\kappa$-ET$_2$Cu(NCS)$_2$'),
]
ax.legend(handles=handles, loc='upper left', bbox_to_anchor=(0.0, 0.865),
          handletextpad=0.3, borderaxespad=0.0, fontsize=6.6)
ax.text(0.04, 0.96, '(b)', transform=ax.transAxes, fontsize=11)
ax.set_xlim(0, 1.05)
ax.set_ylim(-1.2, 43)
ax.set_xticks([])
ax.set_yticks([0, 10, 20, 30, 40])
ax.set_xlabel('Pressure', fontsize=11, labelpad=1)
ax.set_ylabel(r'$T$ (K)', fontsize=11, labelpad=2)

# ---------------------------------------------------------------- (c)
ax = axs[2]
tet = PchipInterpolator([0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.21],
                        [500, 455, 410, 360, 305, 250, 195, 140, 95, 55, 20, 0])
xt = np.linspace(0, 0.21, 200)
ax.plot(xt, tet(xt), ':', color='k', lw=1.1)
ax.plot([0.005, 0.028], [310, 60], ':', color='k', lw=1.1)
ax.text(0.100, 322, 'tetragonal', fontsize=9, rotation=-52, ha='center')
ax.text(0.019, 185, 'orthorhombic', fontsize=9, rotation=78, ha='center')
afx = [0.0, 0.0, 0.002, 0.008, 0.015, 0.022, 0.03]
afy = [300, 230, 160, 95, 50, 20, 5]
ax.plot(afx, afy, '^', ms=4.5, color='k', lw=0)
sgx = [0.105, 0.115, 0.13, 0.15, 0.17, 0.19, 0.20, 0.215]
sgy = [5, 9, 13, 17, 20, 23, 24, 21]
ax.plot(sgx, sgy, 's', ms=4, color='k', lw=0)
scx = [0.05, 0.06, 0.08, 0.10, 0.12, 0.14, 0.16, 0.18, 0.20, 0.22, 0.25, 0.28, 0.30]
scy = [0, 2, 10, 18, 27, 34, 38, 36.5, 31, 24, 14, 6, 1]
ax.plot(scx, scy, 'o', ms=4.2, color='k', lw=0)
ax.plot([0.012, 0.062], [75, 75], 'k-', lw=0.8)
ax.text(0.068, 71, 'AF', fontsize=11)
ax.text(0.072, 40, 'SG', fontsize=11)
ax.text(0.152, 8, 'S', fontsize=11, ha='center')
ax.text(0.13, 455, r'La$_{2-x}$Sr$_x$CuO$_4$', fontsize=10, ha='center')
ax.text(0.04, 0.94, '(c)', transform=ax.transAxes, fontsize=11)
ax.set_xlim(-0.005, 0.42)
ax.set_ylim(-14, 545)
ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4])
ax.set_xticklabels(['0.0', '0.1', '0.2', '0.3', '0.4'])
ax.set_yticks([0, 200, 400])
ax.set_xlabel(r'Sr concentration, $x$', fontsize=11, labelpad=1)
ax.set_ylabel(r'$T$ (K)', fontsize=11, labelpad=2)

for ax in axs:
    ax.tick_params(labelsize=9.5)

fig.subplots_adjust(left=0.055, right=0.99, bottom=0.14, top=0.98, wspace=0.30)
save_fig(fig, 'ch8', 'fig8_16')
