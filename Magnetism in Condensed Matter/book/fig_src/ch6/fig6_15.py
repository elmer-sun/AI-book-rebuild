# -*- coding: utf-8 -*-
# 图 6.15 有机铁磁体自发磁化 M/Ms vs T/TC：数据点+整体拟合实线；
# 虚线 = 布洛赫 T^{3/2} 径向高温外推，点线 = 临界律 (Tc-T)^beta 向低温外推
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import PchipInterpolator
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.6, 3.5)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

# ---- data points (digitized from the original; organic ferromagnet, Tc~0.67 K, beta~0.36)
t = np.array([0.20, 0.33, 0.44, 0.53, 0.60, 0.66, 0.72,
              0.78, 0.81, 0.83, 0.85, 1.01, 1.02])
M = np.array([0.97, 0.93, 0.88, 0.83, 0.76, 0.69, 0.62,
              0.52, 0.45, 0.42, 0.40, 0.00, 0.00])
err = np.full_like(M, 0.012)
err[7] = 0.02    # 0.78
err[8] = 0.055   # 0.81, large error bar
err[10] = 0.03   # 0.85
ax.errorbar(t, M, yerr=err, fmt='ko', ms=4.2, lw=0.8, mfc='k', capsize=0,
            zorder=5)

# ---- main smooth curve: data + critical-law anchors diving to zero at Tc
BETA = 0.36
tc_t = np.array([0.88, 0.90, 0.92, 0.94, 0.96, 0.98, 1.00])
tc_M = 0.774 * (1 - tc_t) ** BETA
ta = np.concatenate(([0.0], t[:11], tc_t))
Ma = np.concatenate(([1.0], M[:11], tc_M))
srt = np.argsort(ta)
f = PchipInterpolator(ta[srt], Ma[srt])
tt = np.linspace(0, 1.0, 300)
ax.plot(tt, f(tt), 'k-', lw=1.5)

# ---- dashed: spin-wave (Bloch) law extrapolated to high T
tb = np.linspace(0.40, 0.76, 60)
ax.plot(tb, 1 - 0.335 * tb ** 1.5, 'k--', lw=0.9)
# ---- dotted: critical power law extrapolated to low T
td = np.linspace(0.55, 0.91, 60)
ax.plot(td, 0.774 * (1 - td) ** BETA, 'k:', lw=1.1)

# ---- annotations
ax.text(0.13, 1.12, r'$1-aT^{3/2}$', fontsize=11)
ax.text(0.04, 0.875, 'spin-wave region', fontsize=11)
ax.text(0.845, 0.155, 'critical\nregion', fontsize=11, ha='center')
ax.text(1.02, 0.30, r'$(T_{\mathrm{C}}-T)^{\beta}$', fontsize=11,
        ha='left')

ax.set_xlim(0, 1.15)
ax.set_ylim(-0.04, 1.27)
ax.set_xticks([0, 0.5, 1.0])
ax.set_yticks([0, 0.5, 1.0])
ax.set_xticklabels(['0', '0.5', '1'])
ax.set_yticklabels(['0', '0.5', '1'])
ax.tick_params(top=False, right=False)
ax.plot(1.0, 0.0, '>k', transform=ax.transAxes, clip_on=False, ms=5)
ax.plot(0.0, 1.0, '^k', transform=ax.transAxes, clip_on=False, ms=5)
ax.text(0.56, -0.155, r'$T/T_{\mathrm{C}}$', ha='center', va='top',
        fontsize=12)
ax.text(-0.10, 0.63, r'$M/M_{\mathrm{s}}$', ha='right', va='center',
        fontsize=12, rotation=90)

save_fig(fig, 'ch6', 'fig6_15')
