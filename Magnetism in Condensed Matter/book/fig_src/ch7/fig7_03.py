# -*- coding: utf-8 -*-
# 图 7.3 (a) 费米函数 f(E) (b) 态密度 g(E)∝E^(1/2) (c) 乘积 f(E)g(E)
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

mu = 1.0
Ts = [0.01, 0.05, 0.1]

fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.75))


def style(ax):
    ax.spines[['top', 'right']].set_visible(False)
    ax.plot(1.0, 0, '>k', ms=4.5, clip_on=False, transform=ax.transAxes)
    ax.plot(0.0, 1.0, '^k', ms=4.5, clip_on=False, transform=ax.transAxes)
    ax.tick_params(top=False, right=False)
    ax.set_xticks([0, mu], ['0', r'$\mu$'])
    ax.set_xlim(0, 2.1)
    ax.set_xlabel('$E$', fontsize=12, labelpad=1)


# ---- (a) f(E) ----
ax = axs[0]
E = np.linspace(0, 2.1, 800)
ax.plot(E, (E < mu) * 1.0, 'k-', lw=1.9)
for T in Ts:
    ax.plot(E, 1.0 / (np.exp((E - mu) / T) + 1), 'k-', lw=0.85)
style(ax)
ax.set_yticks([0, 1])
ax.set_ylim(0, 1.13)
ax.set_ylabel('$f(E)$', fontsize=12)

# ---- (b) g(E) ----
ax = axs[1]
E = np.linspace(0, 2.1, 400)
ax.plot(E, np.sqrt(E), 'k-', lw=1.4)
style(ax)
ax.set_yticks([])
ax.set_ylim(0, 1.75)
ax.text(1.22, 0.72, r'$\propto E^{1/2}$', fontsize=11)
ax.set_ylabel('$g(E)$', fontsize=12)

# ---- (c) f*g ----
ax = axs[2]
ax.plot(E, np.sqrt(E) * (E < mu), 'k-', lw=1.9)
for T in Ts:
    ax.plot(E, np.sqrt(E) / (np.exp((E - mu) / T) + 1), 'k-', lw=0.85)
style(ax)
ax.set_yticks([])
ax.set_ylim(0, 1.13)

fig.subplots_adjust(wspace=0.42, left=0.07, right=0.985,
                    bottom=0.14, top=0.97)
save_fig(fig, 'ch7', 'fig7_03')
