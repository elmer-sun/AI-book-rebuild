# -*- coding: utf-8 -*-
# 图 3.12 脉冲 NMR 的自由感应衰减（FID）信号：三个相近频率干涉成拍，
# 包络以 T2 指数衰减。s(t) = Σ Ai cos(wi t) exp(-t/T2)
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

fig, ax = plt.subplots(figsize=(4.9, 2.3))
plt.subplots_adjust(left=0.11, right=0.97, bottom=0.19, top=0.95)

t = np.linspace(0, 4, 6000)
s = (np.cos(2*np.pi*20.0*t) + 0.75*np.cos(2*np.pi*22.2*t)
     + 0.55*np.cos(2*np.pi*24.6*t)) * np.exp(-t/1.3)

ax.plot(t, s, 'k-', lw=0.5)
ax.axhline(0, color='k', lw=0.9)

ax.set_xlim(-0.05, 4.35)
ax.set_ylim(-2.6, 2.6)
ax.set_xticks([]); ax.set_yticks([])
for sp in ('top', 'right', 'bottom', 'left'):
    ax.spines[sp].set_visible(False)
ax.spines['left'].set_position(('data', 0))
ax.spines['bottom'].set_position(('data', 0))
ax.plot(4.35, 0, '>k', clip_on=False, ms=5)
ax.plot(0, 2.6, '^k', clip_on=False, ms=5)

ax.text(-0.06, 0.5, 'signal', transform=ax.transAxes, rotation=90,
        ha='right', va='center', fontsize=12)
ax.text(1.0, -0.13, '$t$', transform=ax.transAxes, ha='right', va='top', fontsize=12)

save_fig(fig, 'ch3', 'fig3_12')
