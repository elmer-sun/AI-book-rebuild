# -*- coding: utf-8 -*-
# 图 7.15 一维金属能带：(a) 自由电子抛物线填充至 k_F (b) q=2k_F 周期势在费面打开能隙
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

kF = 1.6
G = 2 * kF
U = 0.35

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(4.1, 5.9))


def band_axes(ax, Etop):
    ax.plot([-2.45, 2.75], [0, 0], 'k-', lw=0.8)
    ax.plot(2.75, 0, '>k', ms=5, clip_on=False)
    ax.plot([0, 0], [0, Etop], 'k-', lw=0.8)
    ax.plot(0, Etop, '^k', ms=5, clip_on=False)
    ax.text(2.85, -0.16, '$k$', fontsize=12, ha='left', va='top')
    ax.text(0, Etop + 0.18, '$E(k)$', fontsize=12, ha='center', va='bottom')
    ax.text(-0.12, -0.16, '0', fontsize=11, ha='right', va='top')
    for s in (-1, 1):
        ax.plot([s * kF] * 2, [0, 3.25], 'k:', lw=0.9)
        ax.text(s * kF, -0.2, ('$-k_{\\mathrm{F}}$' if s < 0
                               else '$k_{\\mathrm{F}}$'),
                ha='center', va='top', fontsize=12)
    ax.plot([-2.45, 2.45], [kF**2] * 2, 'k:', lw=0.9)   # E_F
    ax.set_xlim(-2.9, 3.15)
    ax.set_ylim(-0.55, Etop + 0.25)
    ax.axis('off')


# ---- (a) 自由电子抛物线，|k|<kF 加粗 ----
kk = np.linspace(-2.7, 2.7, 700)
ax1.plot(kk, kk**2, 'k-', lw=0.9)
kb = np.linspace(-kF, kF, 200)
ax1.plot(kb, kb**2, 'k-', lw=2.2)
band_axes(ax1, 3.55)

# ---- (b) 能隙：下支加粗，上支变细 ----
klo = np.linspace(0.0, kF, 200)
Elo = (klo**2 + (klo - G)**2) / 2 - np.sqrt(
    ((klo**2 - (klo - G)**2) / 2)**2 + U**2)
khi = np.linspace(kF, 2.75, 300)
Ehi = (khi**2 + (khi - G)**2) / 2 + np.sqrt(
    ((khi**2 - (khi - G)**2) / 2)**2 + U**2)
for s in (1, -1):
    ax2.plot(s * klo, Elo, 'k-', lw=2.2)
    ax2.plot(s * khi, Ehi, 'k-', lw=0.9)
band_axes(ax2, 3.85)

fig.subplots_adjust(left=0.03, right=0.985, top=0.985, bottom=0.015,
                    hspace=0.09)
save_fig(fig, 'ch7', 'fig7_15')
