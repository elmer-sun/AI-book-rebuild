# -*- coding: utf-8 -*-
# 图 3.7 序参量 Q 附近的绝热势能面：(a) E=1/2 k Q^2（单一极小）
# (b) E=1/2 k Q^2 - γQ^3 型失稳：两条相交于 Q=0 的抛物线，极小在 ∓Q0
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

fig, axs = plt.subplots(1, 2, figsize=(6.4, 3.0))
plt.subplots_adjust(left=0.06, right=0.985, bottom=0.13, top=0.92, wspace=0.42)

for ax, tag in zip(axs, '(a),(b)'.split(',')):
    ax.set_xticks([]); ax.set_yticks([])
    ax.tick_params(top=False, right=False)
    for sp in ('top', 'right'):
        ax.spines[sp].set_visible(False)
    ax.text(0.03, 1.04, '$E(Q)$', transform=ax.transAxes, ha='left')
    ax.text(1.0, -0.10, '$Q$', transform=ax.transAxes, ha='right', va='top')
    ax.text(0.03, 0.90, tag, transform=ax.transAxes, ha='left')

# (a) 单一极小，与横轴相切于 Q=0
ax = axs[0]
ax.spines['left'].set_position(('data', 0))
ax.spines['bottom'].set_position(('data', 0))
q = np.linspace(-1.05, 1.05, 400)
ax.plot(q, q**2, 'k-', lw=1.4)
ax.set_xlim(-1.18, 1.18)
ax.set_ylim(-0.10, 1.22)
ax.plot(1.18, 0, '>k', clip_on=False, ms=5)
ax.plot(0, 1.22, '^k', clip_on=False, ms=5)

# (b) 两抛物线交于原点（失稳点），极小在 ∓Q0
ax = axs[1]
ax.spines['left'].set_position(('data', 0))
ax.spines['bottom'].set_position(('data', 0))
q = np.linspace(-1.40, 1.40, 500)
Q0 = 0.5
ax.plot(q, (q - Q0)**2 - Q0**2, 'k-', lw=1.5)
ax.plot(q, (q + Q0)**2 - Q0**2, color='0.35', lw=1.2, ls=(0, (4, 2.4)))
ax.set_xlim(-1.50, 1.50)
ax.set_ylim(-0.46, 1.22)
ax.plot(1.50, 0, '>k', clip_on=False, ms=5)
ax.plot(0, 1.22, '^k', clip_on=False, ms=5)
ax.set_xticks([-Q0, Q0])
ax.set_xticklabels(['$-Q_0$', '$Q_0$'])
ax.tick_params(axis='x', length=3.5, pad=1, top=False, right=False)

save_fig(fig, 'ch3', 'fig3_07')
