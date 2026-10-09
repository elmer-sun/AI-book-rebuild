# -*- coding: utf-8 -*-
# 图 7.10 三维 Lindhard 顺磁磁化率 chi_q 随 q/2k_F 的变化（q=2k_F 处扭折）
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig


def L3(x):
    x = np.asarray(x, dtype=float)
    r = np.empty_like(x)
    s = x < 1e-6
    r[s] = 1.0
    xs = x[~s]
    r[~s] = 0.5 + (1 - xs**2) / (4 * xs) * np.log(np.abs((1 + xs) / (1 - xs)))
    return r


fig, ax = new_fig(4.0, 3.3)

x = np.linspace(1e-6, 2.3, 1200)
ax.plot(x, L3(x), 'k-', lw=1.5)

# 水平渐近参考线（带右向箭头）
ax.annotate('', xy=(2.3, 0.065), xytext=(0.0, 0.065),
            arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))

# q = 2k_F 点线与标注
ax.plot([1, 1], [0, 1.0], 'k:', lw=0.9)
ax.text(1.0, 1.05, r'$q=2k_{\mathrm{F}}$', ha='center', va='bottom',
        fontsize=12)

ax.set_xlim(0, 2.35)
ax.set_ylim(-0.055, 1.24)
ax.set_xticks([0, 1, 2])
ax.set_yticks([0, 0.5, 1.0], ['0', r'$\chi_{\mathrm{P}}/2$',
                              r'$\chi_{\mathrm{P}}$'])
ax.spines[['top', 'right']].set_visible(False)
ax.tick_params(top=False, right=False)
ax.plot(1.0, 0, '>k', ms=5, clip_on=False, transform=ax.transAxes)
ax.plot(0.0, 1.0, '^k', ms=5, clip_on=False, transform=ax.transAxes)
ax.set_xlabel(r'$q/2k_{\mathrm{F}}$', fontsize=12, labelpad=1)
ax.set_ylabel(r'$\chi_{\mathbf{q}}$', fontsize=12)

save_fig(fig, 'ch7', 'fig7_10')
