# -*- coding: utf-8 -*-
# 图 7.11 三维抗磁磁化率 chi_q（横轴在顶部、纵轴向下；q=0 取朗道值 -chi_P/3，q=2k_F 处扭折）
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.0, 3.2)

# 曲线：q<2k_F 缓慢上升，x=1 处扭折（斜率变小），q 大时渐近 0（x=2 约 -0.1）
x1 = np.linspace(0, 1, 200)
y1 = -1.0 / 3 + 0.01 * x1 + 0.1333 * x1**2
x2 = np.linspace(1, 2.35, 200)
y2 = -0.19 * np.exp(-(x2 - 1) / 1.8)
ax.plot(x1, y1, 'k-', lw=1.5)
ax.plot(x2, y2, 'k-', lw=1.5)

# 顶部横轴（向右）与向下纵轴
ax.annotate('', xy=(2.42, 0), xytext=(-0.02, 0),
            arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))
ax.annotate('', xy=(0, -0.80), xytext=(0, -0.02),
            arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))
for xt in [0, 1, 2]:
    ax.plot([xt, xt], [0, 0.028], 'k-', lw=0.9)
ax.text(0, 0.055, '0', ha='center', va='bottom', fontsize=11)
ax.text(1, 0.055, '1', ha='center', va='bottom', fontsize=11)
ax.text(2, 0.055, '2', ha='center', va='bottom', fontsize=11)
ax.text(2.30, 0.16, r'$q/2k_{\mathrm{F}}$', ha='center', va='bottom',
        fontsize=12)

# 纵轴标注
ax.text(-0.09, -1.0 / 3, r'$-\chi_{\mathrm{P}}/3$', ha='right', va='center',
        fontsize=12)
ax.plot([0, 0.028], [-1.0 / 3] * 2, 'k-', lw=0.9)
ax.text(-0.14, -0.42, r'$\chi_{\mathbf{q}}$', ha='center', va='center',
        fontsize=12, rotation=90)

# q = 2k_F 点线（自顶轴向下穿过曲线直至标注）
ax.plot([1, 1], [0, -0.73], 'k:', lw=0.9)
ax.text(1.0, -0.755, r'$q=2k_{\mathrm{F}}$', ha='center', va='top',
        fontsize=12)

ax.set_xlim(-0.62, 2.6)
ax.set_ylim(-0.88, 0.30)
ax.axis('off')

save_fig(fig, 'ch7', 'fig7_11')
