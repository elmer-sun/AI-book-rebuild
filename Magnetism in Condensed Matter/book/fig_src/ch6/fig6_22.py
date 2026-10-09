# -*- coding: utf-8 -*-
# 图 6.22 Fe/Ni/Co 单晶磁化曲线（Honda & Kaya 1926, Kaya 1928），平滑饱和曲线重建
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

fig, axs = plt.subplots(1, 3, figsize=(6.6, 2.5), sharey=True)


def sat(Bv, Bi):
    return 1.0 - np.exp(-Bv / Bi)


panels = [
    dict(xmax=6.0, xlab=r'$6\times10^{-2}$',
         curves=[(0.15, '(100)', 0.8, 1.045), (0.45, '(110)', 2.2, 1.045),
                 (1.5, '(111)', 4.6, 1.045)]),
    dict(xmax=3.0, xlab=r'$3\times10^{-2}$',
         curves=[(0.10, '(111)', 0.55, 1.045), (0.30, '(110)', 1.5, 1.045),
                 (0.80, '(100)', 2.55, 1.045)]),
]
for ax, p in zip(axs[:2], panels):
    Bv = np.linspace(0, p['xmax'], 400)
    for Bi, lab, xt, yt in p['curves']:
        ax.plot(Bv, sat(Bv, Bi), 'k-', lw=1.4)
        ax.text(xt, yt, lab, ha='center', va='bottom', fontsize=10)
    ax.set_xlim(0, p['xmax'])
    ax.set_ylim(0, 1.14)
    ax.set_xticks([p['xmax']])
    ax.set_xticklabels([p['xlab']])
    ax.set_yticks([0, 1])

# Co: 两支 —— (100) 极陡，(001) 近线性缓慢上升（六方 c 轴难磁化）
ax = axs[2]
Bv = np.linspace(0, 8.0, 400)
ax.plot(Bv, sat(Bv, 0.15), 'k-', lw=1.4)
ax.plot(Bv, 0.80 * np.tanh(Bv / 4.5), 'k-', lw=1.4)
ax.text(1.6, 1.045, '(100)', ha='center', va='bottom', fontsize=10)
ax.text(6.0, 0.86, '(001)', ha='center', va='bottom', fontsize=10)
ax.set_xlim(0, 8.0)
ax.set_ylim(0, 1.14)
ax.set_xticks([8.0])
ax.set_xticklabels([r'$8\times10^{-2}$'])
ax.set_yticks([0, 1])

axs[0].set_ylabel(r'M/M$_0$')
fig.supxlabel(r'B (tesla)', fontsize=11, y=0.02)
fig.subplots_adjust(left=0.09, right=0.955, bottom=0.17, top=0.96, wspace=0.13)
save_fig(fig, 'ch6', 'fig6_22')
