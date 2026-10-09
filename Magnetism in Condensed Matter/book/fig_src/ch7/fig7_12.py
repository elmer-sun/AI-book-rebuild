# -*- coding: utf-8 -*-
# 图 7.12 RKKY 函数 F(x)=(sin x - x cos x)/x^4（式 7.89），纵轴 10^3 F(x)
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.6, 3.2)

x = np.linspace(0.6, 4.4 * np.pi, 4000)
F = (np.sin(x) - x * np.cos(x)) / x**4 * 1e3
ax.plot(x, F, 'k-', lw=1.3)

# nπ 处竖直点状网格线与零线
for n in range(1, 5):
    ax.plot([n * np.pi] * 2, [-5.8, 6.6], 'k:', lw=0.7)
ax.plot([0, 4.4 * np.pi], [0, 0], 'k:', lw=0.7)

ax.set_xlim(0, 4.45 * np.pi)
ax.set_ylim(-5.8, 6.6)
ax.set_xticks([n * np.pi for n in range(5)],
              ['0', r'$\pi$', r'$2\pi$', r'$3\pi$', r'$4\pi$'])
ax.set_yticks([-5, 0, 5])
ax.spines[['top', 'right']].set_visible(False)
ax.tick_params(top=False, right=False)
ax.plot(1.0, 0, '>k', ms=5, clip_on=False, transform=ax.transAxes)
ax.plot(0.0, 1.0, '^k', ms=5, clip_on=False, transform=ax.transAxes)
ax.set_xlabel('$x$', fontsize=12, labelpad=1)
ax.set_ylabel(r'$10^{3}\times F(x)$', fontsize=12)

save_fig(fig, 'ch7', 'fig7_12')
