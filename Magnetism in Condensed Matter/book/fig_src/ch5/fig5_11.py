# -*- coding: utf-8 -*-
# 图 5.11 反铁磁相与自旋翻转跳跃相的能量随磁场曲线，交点 B_spin-flop
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.7, 3.3)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.plot(1, 0, ">k", transform=ax.transAxes, clip_on=False, ms=5)
ax.plot(0, 1, "^k", transform=ax.transAxes, clip_on=False, ms=5)

B = np.linspace(0, 3.4, 300)
E_af = np.full_like(B, -1.0)
E_sf = -0.75 - 0.05165 * B**2          # crossing at B = 2.2
Bsf = 2.2

ax.plot(B, E_af, 'k-', lw=1.3)
ax.plot(B, E_sf, 'k-', lw=1.3)
ax.plot([Bsf, Bsf], [-1.42, 0], ls=':', lw=0.8, color='0.35')

ax.set_xlim(0, 3.5)
ax.set_ylim(-1.45, 0.28)
ax.set_xticks([Bsf])
ax.set_xticklabels([r'$B_{\mathrm{spin\!-\!\mathrm{flop}}}$'], fontsize=10)
ax.set_yticks([0, -1.0])
ax.set_yticklabels(['0', r'$-AM^2-\Delta$'])
ax.tick_params(axis='x', length=0)
ax.tick_params(axis='y', length=3)
for tlab in ax.get_yticklabels():
    tlab.set_fontsize(10)
ax.text(3.53, -0.035, '$B$', ha='left', va='center', fontsize=12)
ax.text(-0.08, 0.30, '$E$', ha='center', va='bottom', fontsize=12)
ax.text(2.42, -0.90, 'antiferromagnetic\nphase', fontsize=10.5, ha='left', va='center')
ax.text(2.62, -1.28, 'spin-flop\nphase', fontsize=10.5, ha='left', va='center')

ax.tick_params(top=False, right=False)
fig.subplots_adjust(left=0.19, right=0.96)
save_fig(fig, 'ch5', 'fig5_11')
