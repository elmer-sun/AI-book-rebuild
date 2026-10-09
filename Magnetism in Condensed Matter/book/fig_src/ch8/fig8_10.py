# -*- coding: utf-8 -*-
# 图 8.10 MEM(TCNQ)2 摩尔磁化率（Lovett 等 2000）：自旋能隙/SP 转变 + 高温宽极大
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.3, 3.3)

ctrl = [(3, 0.60), (3.6, 0.47), (4.2, 0.39), (5, 0.335), (5.8, 0.302),
        (6.5, 0.292), (7.2, 0.296), (8, 0.315), (9, 0.36), (10, 0.43),
        (11, 0.51), (12, 0.62), (13, 0.76), (14, 0.92), (15, 1.10),
        (16, 1.32), (17, 1.60), (18, 1.88), (18.5, 2.02), (19, 2.10),
        (19.5, 2.13), (20, 2.155), (21, 2.20), (22, 2.25), (24, 2.33),
        (26, 2.40), (28, 2.46), (30, 2.51), (33, 2.56), (36, 2.60),
        (40, 2.645), (45, 2.675), (50, 2.70), (55, 2.715), (60, 2.725),
        (65, 2.728), (70, 2.72), (75, 2.71), (80, 2.69), (90, 2.64),
        (100, 2.58), (110, 2.51), (120, 2.43), (130, 2.35), (140, 2.27),
        (150, 2.19), (160, 2.11), (170, 2.03), (180, 1.96), (190, 1.89),
        (200, 1.82), (210, 1.75), (220, 1.68), (230, 1.61), (240, 1.55),
        (250, 1.49), (260, 1.43), (270, 1.38), (280, 1.34), (290, 1.32),
        (300, 1.30)]
p = PchipInterpolator([q[0] for q in ctrl], [q[1] for q in ctrl])
T = np.logspace(np.log10(3), np.log10(300), 400)
ax.semilogx(T, p(T), 'k-', lw=1.0)
ax.semilogx(T, p(T), 'o', mfc='white', mec='k', ms=3.2, markevery=9)

# dotted: uniform Heisenberg-chain model, extrapolated down to T_SP
Tm = np.linspace(3, 20, 60)
ax.semilogx(Tm, 1.90 + 0.23 * ((Tm - 3) / 17.0) ** 1.15, 'k:', lw=1.3)

ax.set_xlim(2.8, 310)
ax.set_ylim(0, 3.0)
ax.set_xticks([3, 10, 30, 100])
ax.set_xticklabels(['3', '10', '30', '100'])
ax.set_yticks([0, 1, 2, 3])
ax.set_yticks([0.5, 1.5, 2.5], minor=True)
ax.set_xlabel(r'$T$ (K)', fontsize=12, labelpad=1)
ax.set_ylabel(r'$\chi_m$ ($10^{-8}$ m$^3$ mol$^{-1}$)', fontsize=12)

save_fig(fig, 'ch8', 'fig8_10')
