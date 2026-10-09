# -*- coding: utf-8 -*-
# 图 6.4 水的相图：固-液近竖直线、液-气饱和曲线、三相点/临界点、路径 A/B/C
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.ticker import NullLocator, FixedLocator, FixedFormatter
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.6, 3.7)

# liquid-gas saturation curve: ln P = 24.57 - 4958/T (fits 611.7 Pa @ 273.16 K, 2.21e7 Pa @ 647.1 K)
Tsat = np.linspace(273.16, 647.1, 200)
Psat = np.exp(24.57 - 4958.0 / Tsat)
# solid-gas sublimation curve: ln P = 28.81 - 6116/T
Tsub = np.linspace(230.6, 273.16, 100)
Psub = np.exp(28.81 - 6116.0 / Tsub)
# solid-liquid: nearly vertical, melting point drops ~3.54 K per decade of P
Psl = np.logspace(np.log10(611.7), 9, 100)
Tsl = 273.16 - 3.54 * (np.log10(Psl) - np.log10(611.7))

ax.plot(Tsat, Psat, 'k-', lw=1.2)
ax.plot(Tsub, Psub, 'k-', lw=1.2)
ax.plot(Tsl, Psl, 'k-', lw=1.2)
ax.plot([273.16], [611.7], 'ko', ms=4)
ax.plot([647.1], [2.2064e7], 'ko', ms=4)

# region labels
ax.text(315, 1.3e8, 'liquid', ha='center', va='center', fontsize=11)
ax.text(145, 2.0e5, 'solid', ha='center', va='center', fontsize=11)
ax.text(705, 1.1e4, 'gas', ha='center', va='center', fontsize=11)
ax.text(283, 470, 'triple point', ha='left', va='center', fontsize=11)
ax.text(658, 5.2e6, 'critical point', ha='left', va='center', fontsize=11)

# path A: horizontal double arrow crossing the solid-liquid line
ax.annotate('', xy=(340, 8e6), xytext=(215, 8e6),
            arrowprops=dict(arrowstyle='<->', lw=1.2, color='k'))
ax.text(202, 8e6, 'A', ha='right', va='center', fontsize=12)
# path B: slanted double arrow crossing the saturation curve
ax.annotate('', xy=(585, 1.6e5), xytext=(445, 3.2e6),
            arrowprops=dict(arrowstyle='<->', lw=1.2, color='k'))
ax.text(598, 1.1e5, 'B', ha='left', va='center', fontsize=12)
# path C: large arc passing to the right of the critical point (gas -> liquid)
# cubic Bezier in (T, log10 P); tail stays above the 'critical point' text
def bez(p0, p1, p2, p3, n=160):
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 3 * p0 + 3 * (1 - t) ** 2 * t * p1
            + 3 * (1 - t) * t ** 2 * p2 + t ** 3 * p3)

C0, C1, C2, C3 = np.array([640., 6.90]), np.array([800., 7.15]), \
    np.array([590., 9.00]), np.array([480., 9.03])
pts = bez(C0, C1, C2, C3)
ax.plot(pts[:, 0], 10 ** pts[:, 1], 'k-', lw=1.5)
# arrowheads at both ends, pointing outward along the path tangent
ax.annotate('', xy=(C0[0], 10 ** C0[1]),
            xytext=(C0[0] + 32, 10 ** (C0[1] + 0.11)),
            arrowprops=dict(arrowstyle='-|>', lw=1.5, color='k',
                            mutation_scale=20, shrinkA=0, shrinkB=0))
ax.annotate('', xy=(C3[0], 10 ** C3[1]),
            xytext=(C3[0] + 32, 10 ** (C3[1] - 0.11)),
            arrowprops=dict(arrowstyle='-|>', lw=1.5, color='k',
                            mutation_scale=20, shrinkA=0, shrinkB=0))
ax.text(768, 2.5e7, 'C', ha='center', va='center', fontsize=12)

ax.set_yscale('log')
ax.set_xlim(0, 880)
ax.set_ylim(10, 2e9)
ax.xaxis.set_major_locator(FixedLocator([273, 647]))
ax.xaxis.set_major_formatter(FixedFormatter(['273', '647']))
ax.xaxis.set_minor_locator(NullLocator())
yt = [1e1, 1e2, 1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9]
ax.yaxis.set_major_locator(FixedLocator(yt))
ax.yaxis.set_major_formatter(
    FixedFormatter([r'$10^{%d}$' % i for i in range(1, 10)]))
ax.set_xlabel(r'$T$ (K)', fontsize=12)
ax.set_ylabel(r'$P$ (Pa)', fontsize=12)

save_fig(fig, 'ch6', 'fig6_04')
