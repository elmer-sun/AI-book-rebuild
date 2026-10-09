# -*- coding: utf-8 -*-
# 图 6.17 Co0.92Fe0.08 合金磁振子能谱（Sinclair & Brockhouse 1960），E=A(ka/2pi)^2 重建
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.4, 3.4)

x = np.linspace(0, 0.2, 400)
ax.plot(x, 1.25 * x**2, 'k-', lw=1.5, zorder=2)

# (x, E/eV, x-error bar); three branch symbols
d111 = [(0.030, 0.002, 0.004), (0.052, 0.005, 0.005), (0.068, 0.010, 0.006),
        (0.090, 0.019, 0.009), (0.100, 0.025, 0.010), (0.168, 0.034, 0.012)]
d110 = [(0.040, 0.003, 0.004), (0.078, 0.011, 0.007),
        (0.095, 0.019, 0.009), (0.135, 0.028, 0.011)]
d100 = [(0.062, 0.007, 0.005), (0.112, 0.018, 0.009), (0.152, 0.030, 0.011)]

for d, mk, mfc, lab in [(d111, 'o', 'k', '[111]'),
                        (d110, 'o', 'white', '[110]'),
                        (d100, '^', 'white', '[100]')]:
    d = np.array(d)
    ax.errorbar(d[:, 0], d[:, 1], xerr=d[:, 2], fmt=mk, mfc=mfc, mec='k',
                ms=5.5, elinewidth=1.0, capsize=2.5, capthick=1.0,
                color='k', ls='none', zorder=3, label=lab)

ax.legend(loc='upper left', frameon=True, framealpha=1, edgecolor='k',
          borderpad=0.5, labelspacing=0.35, handlelength=1.0, handletextpad=0.6)

ax.set_xlim(0, 0.2)
ax.set_ylim(0, 0.0375)
ax.set_xticks([0.05, 0.10, 0.15])
ax.set_xticklabels(['0.05', '0.10', '0.15'])
ax.set_yticks([0.01, 0.02, 0.03])
ax.set_xlabel(r'$(ka/2\pi)$')
ax.set_ylabel('Magnon energy, in eV')
fig.tight_layout()
save_fig(fig, 'ch6', 'fig6_17')
