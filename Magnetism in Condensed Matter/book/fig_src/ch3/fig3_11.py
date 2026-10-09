# -*- coding: utf-8 -*-
# 图 3.11 吸收速率随泵浦强度 W 的饱和：dE/dt = n0 hw W / (1 + 2 W T1)（式 3.25）
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

fig, ax = plt.subplots(figsize=(4.8, 3.1))
plt.subplots_adjust(left=0.34, right=0.97, bottom=0.10, top=0.97)

W = np.linspace(0, 2.5, 500)          # 单位 1/T1
y = 2 * W / (1 + 2 * W)               # 单位 n0 hw / 2T1（饱和值取 1）

ax.plot(W, y, 'k-', lw=1.5)                       # 实线：饱和曲线
ax.plot([0, 2.5], [1, 1], 'k:', lw=1.3)           # 水平渐近线（饱和值）
ax.plot([0, 0.8], [0, 1.6], 'k:', lw=1.3)         # 初始斜率 n0 hw W

ax.set_xlim(0, 2.5)
ax.set_ylim(0, 1.62)
ax.set_xticks([]); ax.set_yticks([1.0])
ax.set_yticklabels([r'$n_0\hbar\omega/2T_1$'])
ax.tick_params(axis='y', length=3.5, pad=3, top=False, right=False)
for sp in ('top', 'right'):
    ax.spines[sp].set_visible(False)
ax.spines['left'].set_position(('data', 0))
ax.spines['bottom'].set_position(('data', 0))
ax.plot(2.5, 0, '>k', clip_on=False, ms=5)
ax.plot(0, 1.62, '^k', clip_on=False, ms=5)

ax.text(-0.03, 1.52, r'$\mathrm{d}E/\mathrm{d}t$', ha='right', fontsize=12)
ax.text(0.42, 1.50, r'$n_0\hbar\omega W$', ha='left', fontsize=12)

save_fig(fig, 'ch3', 'fig3_11')
