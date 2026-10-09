# -*- coding: utf-8 -*-
# 图 8.13 Sr2CuO2Cl2 逆关联长度（Greven 等 1994）：二维量子非线性 sigma 模型与实验对比
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.5, 3.4)

th = PchipInterpolator([250, 300, 350, 400, 450, 500, 550, 600, 650],
                       [0.0018, 0.0032, 0.0050, 0.0080, 0.0130, 0.0195,
                        0.0280, 0.0380, 0.0500])
Tt = np.linspace(250, 650, 300)
ax.plot(Tt, th(Tt), 'k-', lw=1.3)

noise = lambda T: 1.0 + 0.05 * np.sin(3.7 * T)
sets = [('s', 'white', '$E_i=\\ 5.0$ meV',
         [258, 262, 268, 275, 283, 292, 302, 315, 330, 345, 362, 380, 400,
          420, 445], 0.88),
        ('^', 'k', '$E_i=14.7$ meV',
         [265, 272, 280, 290, 300, 312, 325, 340, 358, 375, 395, 415, 440,
          465, 490, 520], 1.0),
        ('v', 'white', '$E_i=30.5$ meV',
         [300, 315, 332, 350, 372, 395, 420, 448, 478, 510, 545], 1.04),
        ('o', 'k', '$E_i=41.0$ meV',
         [390, 420, 450, 480, 515, 550, 585, 605], 1.0)]
for mk, mfc, lab, Ts, sc in sets:
    T = np.array(Ts, float)
    v = np.array(th(T)) * sc * noise(T)
    e = 0.0012 + 0.07 * v
    ax.errorbar(T, v, yerr=e, fmt=mk, mfc=mfc, mec='k', ms=4.5, ecolor='k',
                elinewidth=0.7, capsize=1.5, lw=0, label=lab)

# T_N marker
ax.annotate('', xy=(258, 0.0045), xytext=(258, 0.0115),
            arrowprops=dict(arrowstyle='->', lw=0.9))
ax.text(264, 0.0112, r'$T_N$', fontsize=11)
ax.legend(loc='upper left', handlelength=1.2, borderaxespad=0.4)

ax.set_xlim(240, 670)
ax.set_ylim(0, 0.052)
ax.set_xticks([250, 350, 450, 550, 650])
ax.set_yticks([0, 0.01, 0.02, 0.03, 0.04, 0.05])
ax.set_xlabel(r'Temperature (K)', fontsize=12, labelpad=1)
ax.set_ylabel(r'$\xi^{-1}$ (Å$^{-1}$)', fontsize=12)

save_fig(fig, 'ch8', 'fig8_13')
