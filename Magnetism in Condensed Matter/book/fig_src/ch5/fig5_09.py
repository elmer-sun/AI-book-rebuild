# -*- coding: utf-8 -*-
# 图 5.9 反铁磁体 chi 平行/垂直 随温度：T_N 以下 chi_perp 常数、chi_parallel 上升，T_N 以上合并下降
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.5, 3.2)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])
ax.plot(1, 0, ">k", transform=ax.transAxes, clip_on=False, ms=5)
ax.plot(0, 1, "^k", transform=ax.transAxes, clip_on=False, ms=5)

CH = 0.8                      # chi_perp level
TN = 1.0
TH = -0.467                   # Curie-Weiss theta above T_N (chi = peak*(TN-th)/(T-th))
xperp = np.linspace(0, TN, 50)
xpara = np.linspace(0, TN, 200)
xhigh = np.linspace(TN, 3.25, 200)

ax.plot(xperp, np.full_like(xperp, CH), 'k-', lw=1.4)
ax.plot(xpara, CH * xpara**2, 'k-', lw=1.4)
ax.plot(xhigh, CH * (TN - TH) / (xhigh - TH), 'k-', lw=1.4)
ax.axvline(TN, ls=':', lw=0.8, color='0.35', ymax=0.99)

ax.set_xlim(0, 3.35)
ax.set_ylim(0, 1.05)
ax.set_xticks([TN]); ax.set_xticklabels([r'$T_N$'])
ax.set_yticks([])
ax.text(3.38, -0.02, '$T$', ha='left', va='top', fontsize=12)
ax.text(-0.10, 1.07, r'$\chi$', ha='center', va='bottom', fontsize=12)
ax.text(0.14, CH + 0.035, r'$\chi_\perp$', fontsize=12)
ax.text(0.40, 0.28, r'$\chi_\parallel$', fontsize=12)

save_fig(fig, 'ch5', 'fig5_09')
