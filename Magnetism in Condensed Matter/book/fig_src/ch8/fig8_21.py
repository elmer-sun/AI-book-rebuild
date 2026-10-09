# -*- coding: utf-8 -*-
# 图 8.21 被交换各向异性（exchange bias）沿 +B 方向移动的磁滞回线：
# 回线右移，上升支位于 B>0 处，B_ex 由点线引出
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

fig, ax = new_fig(3.8, 3.1)

Ms = 0.85
Bu, Bd = 1.25, 0.95          # ascending / descending switching fields
w = 0.045

# ascending branch: -Ms plateau -> sigmoid rise at Bu -> +Ms plateau
x1 = np.linspace(-3.2, Bu - 4 * w, 60)
x2 = np.linspace(Bu - 4 * w, Bu + 4 * w, 200)
x3 = np.linspace(Bu + 4 * w, 4.2, 60)
ax.plot(x1, -Ms * np.ones_like(x1), 'k-', lw=1.3)
ax.plot(x2, Ms * np.tanh((x2 - Bu) / w), 'k-', lw=1.3)
ax.plot(x3, Ms * np.ones_like(x3), 'k-', lw=1.3)
# descending branch: +Ms plateau out to the right, drop at Bd
ax.plot([Bd, 4.2], [Ms, Ms], 'k-', lw=1.3)
ax.plot([Bd, Bd], [-Ms, Ms], 'k-', lw=1.3)

# M = 0 baseline (dashed) doubling as the B axis, with arrow
ax.plot([-3.3, 4.35], [0, 0], ls=(0, (6, 3, 1, 3)), color='0.25', lw=0.8)
ax.annotate('', xy=(4.55, 0), xytext=(4.25, 0),
            arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))
ax.text(4.72, 0, r'$B$', fontsize=13, va='center', ha='left')
# M axis
ax.plot([0, 0], [-1.25, 1.15], 'k-', lw=0.9)
ax.annotate('', xy=(0, 1.3), xytext=(0, 1.12),
            arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))
ax.text(0, 1.42, r'$M$', fontsize=13, ha='center', va='bottom')

# B_ex marker
ax.plot([Bu, Bu], [-Ms, -1.13], ':', color='k', lw=1.1)
ax.plot([Bu, Bu], [-0.045, 0.045], 'k-', lw=0.8)
ax.text(Bu, -1.33, r'$B_{\mathrm{ex}}$', fontsize=12, ha='center', va='top')

ax.set_xlim(-3.5, 5.15)
ax.set_ylim(-1.62, 1.62)
ax.axis('off')

fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98)
save_fig(fig, 'ch8', 'fig8_21')
