# -*- coding: utf-8 -*-
# 图 7.2 近自由电子能带：自由电子抛物线（细线）在区边界 pi/a 处劈为两支（粗线）并打开能隙
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

a = 3.4          # pi/a 位置
G = 2 * a        # 倒格矢
U = 0.55         # 微扰强度（能隙 = 2U）
al = 0.9         # E = al * k^2

fig, ax = new_fig(3.7, 3.5)

kf = np.linspace(0, 5.3, 500)
ax.plot(kf, al * kf**2, color='k', lw=0.7)             # 自由电子抛物线

k1 = np.linspace(2.4, a, 200)                           # 下支（区边界左侧）
E1 = al * (k1**2 + (k1 - G)**2) / 2 - np.sqrt(
    (al * (k1**2 - (k1 - G)**2) / 2)**2 + U**2)
ax.plot(k1, E1, 'k-', lw=1.8)

k2 = np.linspace(a, 4.35, 200)                          # 上支（区边界右侧）
E2 = al * (k2**2 + (k2 - G)**2) / 2 + np.sqrt(
    (al * (k2**2 - (k2 - G)**2) / 2)**2 + U**2)
ax.plot(k2, E2, 'k-', lw=1.8)

# 区边界竖直点线
ax.plot([a, a], [0, 16.2], 'k:', lw=0.9)
ax.text(a, -1.35, r'$\pi/a$', ha='center', va='top', fontsize=12)

# 轴
ax.plot([0, 5.55], [0, 0], 'k-', lw=0.8)
ax.plot(5.55, 0, '>k', ms=5, clip_on=False)
ax.plot([0, 0], [0, 16.2], 'k-', lw=0.8)
ax.plot(0, 16.2, '^k', ms=5, clip_on=False)
ax.text(5.65, -0.15, '$k$', fontsize=12, ha='left', va='top')
ax.text(-0.12, 16.2, '$E$', fontsize=12, ha='right', va='center')
ax.text(-0.14, -0.5, '0', fontsize=11, ha='right', va='top')

ax.set_xlim(-0.7, 6.0)
ax.set_ylim(-1.8, 17.0)
ax.axis('off')

save_fig(fig, 'ch7', 'fig7_02')
