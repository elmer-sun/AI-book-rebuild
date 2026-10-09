# -*- coding: utf-8 -*-
# 图 8.19 Fe/Cr/Fe 多层膜巨磁电阻（Baibich 等 1988）：三条对称阶梯曲线，
# 平台电阻比随 Cr 层减薄而增大；纵轴下部有断轴记号
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.6, 3.6)

B = np.linspace(-4.5, 4.5, 2000)


def curve(Bc, plat, w):
    return plat + (1 - plat) * 0.5 * (1 + np.tanh((np.abs(B) - Bc) / w))


ax.plot(B, curve(0.9, 0.85, 0.13), 'k-', lw=1.1)
ax.plot(B, curve(1.0, 0.65, 0.16), 'k-', lw=1.1)
ax.plot(B, curve(1.6, 0.42, 0.25), 'k-', lw=1.1)

# sample labels
ax.text(1.75, 0.865, r'$(\mathrm{Fe}\,30\,\mathrm{\AA}/\mathrm{Cr}\,18\,\mathrm{\AA})_{30}$',
        fontsize=9.5, va='center')
ax.text(1.85, 0.665, r'$(\mathrm{Fe}\,30\,\mathrm{\AA}/\mathrm{Cr}\,12\,\mathrm{\AA})_{35}$',
        fontsize=9.5, va='center')
ax.text(2.45, 0.515, r'$(\mathrm{Fe}\,30\,\mathrm{\AA}/\mathrm{Cr}\,9\,\mathrm{\AA})_{40}$',
        fontsize=9.5, va='center')

# Hs arrows
for x0, y0, y1, lab, dx in [(0.86, 0.90, 0.985, r'$H_{\mathrm{s}}$', -0.72),
                            (1.04, 0.705, 0.795, r'$H_{\mathrm{s}}$', -0.70),
                            (1.66, 0.505, 0.60, r'$H_{\mathrm{s}}$', -0.68)]:
    ax.annotate('', xy=(x0, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', lw=1.0, color='k'))
    ax.text(x0 + dx, 0.5 * (y0 + y1), lab, fontsize=10, va='center')

# axes: left + bottom spines with arrows
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xlim(-4.7, 4.7)
ax.set_ylim(0.465, 1.045)
ax.set_xticks([-4, -3, -2, -1, 0, 1, 2, 3, 4])
ax.set_yticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0])
ax.set_xlabel('Magnetic field (T)', fontsize=11.5, labelpad=1)
ax.text(0.02, 1.015, r'$R/R(H=0)$', transform=ax.transAxes,
        fontsize=11.5, ha='left')
ax.tick_params(labelsize=10, top=False, right=False)

# axis-end arrowheads (drawn in axes-fraction-safe way)
ax.annotate('', xy=(1.005, 0.0), xytext=(0.995, 0.0),
            xycoords='axes fraction',
            arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))
ax.annotate('', xy=(0.0, 1.005), xytext=(0.0, 0.995),
            xycoords='axes fraction',
            arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))

# break mark on the left spine just below the 0.5 tick
import matplotlib.transforms as mtrans
tr = mtrans.blended_transform_factory(ax.transData, ax.transAxes)
xl = ax.get_xlim()[0]
for y0, y1 in [(0.0135, 0.030), (0.021, 0.0375)]:
    ax.plot([xl - 0.06, xl + 0.10], [y0, y1], 'k-', lw=0.9, transform=tr,
            clip_on=False)

fig.subplots_adjust(left=0.11, right=0.975, bottom=0.115, top=0.94)
save_fig(fig, 'ch8', 'fig8_19')
