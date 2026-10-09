# -*- coding: utf-8 -*-
# 图 5.2 铁磁平均场图解法（B=0）：布里渊曲线与三条过原点直线
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

fig, ax = new_fig(4.6, 3.4)

# axes cross at the origin, arrows at the ends (as in the book)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_position('zero')
ax.spines['bottom'].set_position('zero')
ax.set_xticks([])
ax.set_yticks([])
ax.plot(3.15, 0, ">k", clip_on=False, ms=5)
ax.plot(0, 1.9, "^k", clip_on=False, ms=5)

x = np.linspace(-3.05, 3.05, 400)
ax.plot(x, np.tanh(x), 'k-', lw=1.4)                     # B_J(y), J=1/2
for m in (2.2, 1.0, 0.5):
    ax.plot(x, m * x, 'k-', lw=0.9)
for s in (1, -1):
    ax.axhline(s, ls=':', lw=0.8, color='0.35')

ax.set_xlim(-3.1, 3.15)
ax.set_ylim(-1.9, 1.9)
ax.text(3.18, -0.07, '$y$', ha='left', va='top', fontsize=13)
ax.text(-0.08, 1.95, '$M/M_s$', ha='center', va='bottom', fontsize=13)
ax.text(0.44, 1.70, r'$T{>}T_C$', ha='center', va='center', fontsize=9.5)
ax.text(1.27, 1.70, r'$T{=}T_C$', ha='center', va='center', fontsize=9.5)
ax.text(2.55, 1.70, r'$T{<}T_C$', ha='center', va='center', fontsize=9.5)
ax.text(-0.42, 1.03, '1', ha='right', va='center', fontsize=10)
ax.text(-0.42, -1.05, '$-1$', ha='right', va='center', fontsize=10)

save_fig(fig, 'ch5', 'fig5_02')
