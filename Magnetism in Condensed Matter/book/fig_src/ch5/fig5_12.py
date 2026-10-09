# -*- coding: utf-8 -*-
# 图 5.12 绝对零度反铁磁 M-B 折线：(a) 自旋翻转跳跃+倾转饱和 (b) 自旋翻转直接跳到 Ms
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

fig, axs = plt.subplots(2, 1, figsize=(4.5, 5.4))

# ---------- (a) ----------
ax = axs[0]
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.plot(1, 0, ">k", transform=ax.transAxes, clip_on=False, ms=5)
ax.plot(0, 1, "^k", transform=ax.transAxes, clip_on=False, ms=5)
B1, B2 = 2.0, 3.4
ax.plot([0, B1, B1, B2, 5.6], [0, 0, 0.55, 1.0, 1.0], 'k-', lw=2.0)
ax.plot([0, B2], [1.0, 1.0], ls=':', lw=0.9, color='0.35')
ax.plot([B2, B2], [0, 1.0], ls=':', lw=0.9, color='0.35')
ax.set_xlim(0, 5.7)
ax.set_ylim(0, 1.30)
ax.set_xticks([0, B1, B2]); ax.set_xticklabels(['$0$', '$B_1$', '$B_2$'])
ax.set_yticks([0, 1.0]); ax.set_yticklabels(['$0$', '$M_s$'])
ax.text(5.73, -0.015, '$B$', ha='left', va='top', fontsize=12)
ax.text(-0.10, 1.33, '$M$', ha='center', va='bottom', fontsize=12)
ax.text(0.05, 0.92, '(a)', fontsize=12, transform=ax.transAxes)

# ---------- (b) ----------
ax = axs[1]
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.plot(1, 0, ">k", transform=ax.transAxes, clip_on=False, ms=5)
ax.plot(0, 1, "^k", transform=ax.transAxes, clip_on=False, ms=5)
B3 = 2.6
ax.plot([0, B3, B3, 5.6], [0, 0, 1.0, 1.0], 'k-', lw=2.0)
ax.plot([0, B3], [1.0, 1.0], ls=':', lw=0.9, color='0.35')
ax.set_xlim(0, 5.7)
ax.set_ylim(0, 1.30)
ax.set_xticks([0, B3]); ax.set_xticklabels(['$0$', '$B_3$'])
ax.set_yticks([0, 1.0]); ax.set_yticklabels(['$0$', '$M_s$'])
ax.text(5.73, -0.015, '$B$', ha='left', va='top', fontsize=12)
ax.text(-0.10, 1.33, '$M$', ha='center', va='bottom', fontsize=12)
ax.text(0.05, 0.92, '(b)', fontsize=12, transform=ax.transAxes)

fig.subplots_adjust(left=0.10, right=0.965, top=0.97, bottom=0.07, hspace=0.34)
ax.tick_params(top=False, right=False)
fig.subplots_adjust(left=0.10, right=0.965, top=0.97, bottom=0.07, hspace=0.34)
save_fig(fig, 'ch5', 'fig5_12')
