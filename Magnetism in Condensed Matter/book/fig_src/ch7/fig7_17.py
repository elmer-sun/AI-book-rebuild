# -*- coding: utf-8 -*-
# 图 7.17 Kondo 电阻率极小：rho = a T^5 - b ln T，粗线为总电阻率
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

a, b = 0.002, 0.08
T = np.linspace(0.25, 2.6, 400)
r5 = a * T**5
rl = -b * np.log(T)
rt = r5 + rl

fig, ax = new_fig(3.9, 3.0)

ax.plot(T, rt, 'k-', lw=1.9)
ax.plot(T, r5, 'k-', lw=0.9)
ax.plot(T, rl, 'k-', lw=0.9)

ax.text(2.18, 0.135, r'$T^5$', fontsize=12, ha='left')
ax.text(0.42, 0.135, r'$-\ln T$', fontsize=12, ha='left')

ax.set_xlim(0, 2.75)
ax.set_ylim(-0.07, 0.30)
ax.axis('off')
ax.annotate('', xy=(2.75, -0.02), xytext=(0, -0.02),
            arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))
ax.annotate('', xy=(0.02, 0.30), xytext=(0.02, -0.07),
            arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))
ax.text(2.72, -0.075, '$T$', fontsize=12, ha='right', va='top')
ax.text(-0.08, 0.28, r'$\rho$', fontsize=12, ha='right', va='top')

save_fig(fig, 'ch7', 'fig7_17')
