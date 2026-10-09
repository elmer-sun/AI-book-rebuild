# -*- coding: utf-8 -*-
# 图 C.2 类氢径向波函数 R_nl 与径向概率密度 r^2 R^2（σ = Zr/a0 ∈ [0,25]）
# 曲线全部按公式重算；线型按 l：0 实线、1 点线、2 虚线、3 点线
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
from mplstyle import save_fig
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D

s = np.linspace(1e-6, 25.0, 2500)

R = {
    (1, 0): 2.0 * np.exp(-s),
    (2, 0): (2.0 - s) / (2.0 * np.sqrt(2.0)) * np.exp(-s / 2.0),
    (2, 1): s / (2.0 * np.sqrt(6.0)) * np.exp(-s / 2.0),
    (3, 0): (2.0 / (81.0 * np.sqrt(3.0))) * (27.0 - 18.0 * s + 2.0 * s**2) * np.exp(-s / 3.0),
    (3, 1): (4.0 / (81.0 * np.sqrt(6.0))) * s * (6.0 - s) * np.exp(-s / 3.0),
    (3, 2): (4.0 / (81.0 * np.sqrt(30.0))) * s**2 * np.exp(-s / 3.0),
    (4, 0): 0.0625 * (4.0 - 3.0 * s + 0.5 * s**2 - s**3 / 48.0) * np.exp(-s / 4.0),
    (4, 1): 0.0161370 * s * (s**2 / 16.0 - 1.25 * s + 5.0) * np.exp(-s / 4.0),
    (4, 2): 0.0046580 * (0.25 * s**2) * (6.0 - 0.5 * s) * np.exp(-s / 4.0),
    (4, 3): 0.0017590 * (s**3 / 8.0) * np.exp(-s / 4.0),
}

# normalization diagnostic: int R^2 sigma^2 d sigma should be 1
for (n, l), f in R.items():
    norm = np.trapezoid(f**2 * s**2, s)
    print('R%d%d norm = %.6f' % (n, l, norm))

LS = {0: 'solid', 1: 'dotted', 2: 'dashed', 3: 'dotted'}
rows = [
    dict(n=1, title='n = 1',
         ls=[(1, 0)], ylim=(0, 2), yticks=[1, 2],
         rylim=(0, 0.6), ryticks=[0.2, 0.4, 0.6]),
    dict(n=2, title='n = 2',
         ls=[(2, 0), (2, 1)], ylim=(-0.5, 1), yticks=[-0.5, 0, 0.5, 1],
         rylim=(0, 0.2), ryticks=[0.1, 0.2]),
    dict(n=3, title='n = 3',
         ls=[(3, 0), (3, 1), (3, 2)], ylim=(-0.2, 0.4), yticks=[-0.2, 0, 0.2, 0.4],
         rylim=(0, 0.15), ryticks=[0.05, 0.1, 0.15]),
    dict(n=4, title='n = 4',
         ls=[(4, 0), (4, 1), (4, 2), (4, 3)], ylim=(-0.1, 0.2),
         yticks=[-0.1, 0, 0.1, 0.2],
         rylim=(0, 0.1), ryticks=[0.05, 0.1]),
]

fig, axes = plt.subplots(4, 2, figsize=(5.3, 8.6))
fig.subplots_adjust(left=0.085, right=0.985, top=0.955, bottom=0.05,
                    wspace=0.30, hspace=0.72)

for i, cfg in enumerate(rows):
    n = cfg['n']
    axL, axR = axes[i, 0], axes[i, 1]
    handles = []
    for (nn, ll) in cfg['ls']:
        st = LS[ll]
        f = R[(nn, ll)]
        axL.plot(s, f, linestyle=st, color='k', lw=1.2)
        axR.plot(s, s**2 * f**2, linestyle=st, color='k', lw=1.2)
        handles.append(Line2D([], [], linestyle=st, color='k', lw=1.2,
                              label=r'$R_{%d%d}$' % (nn, ll)))
    axL.set_xlim(0, 25.5)
    axR.set_xlim(0, 25.5)
    axL.set_ylim(*cfg['ylim'])
    axR.set_ylim(*cfg['rylim'])
    axL.set_yticks(cfg['yticks'])
    axR.set_yticks(cfg['ryticks'])
    for ax in (axL, axR):
        ax.set_xticks([0, 5, 10, 15, 20, 25])
        ax.set_xlabel(r'$Zr/a_0$')
    axL.set_ylabel(r'$R(r)$')
    axR.set_ylabel(r'$r^2R(r)^2$')
    axL.set_title(cfg['title'], loc='left', fontsize=11, pad=6)
    axL.legend(handles=handles, loc='upper right', handlelength=1.7,
               borderaxespad=0.4)

save_fig(fig, 'chC', 'figC_02')
