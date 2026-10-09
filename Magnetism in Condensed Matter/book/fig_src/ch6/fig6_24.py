# -*- coding: utf-8 -*-
# 图 6.24 磁滞回线示意：M_s、M_r 与矫顽场 H_c（坐标轴过原点）
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

fig, ax = plt.subplots(figsize=(4.2, 3.3))
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

Hc, w, a, norm = 0.40, 0.36, 0.05, 1.075
H = np.linspace(-1.55, 1.55, 900)
Mup = (np.tanh((H + Hc) / w) + a * H) / norm
Mdn = (np.tanh((H - Hc) / w) + a * H) / norm
ax.plot(H, Mup, 'k-', lw=1.6)
ax.plot(H, Mdn, 'k-', lw=1.6)

XL, XR = -1.62, 1.62
YB, YT = -1.24, 1.30
ax.set_xlim(XL, XR)
ax.set_ylim(YB, YT)
# 过原点的箭头轴
ax.annotate('', xy=(0, YT - 0.02), xytext=(0, YB),
            arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                            shrinkA=0, shrinkB=0))
ax.annotate('', xy=(XR - 0.03, 0), xytext=(XL, 0),
            arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0,
                            shrinkA=0, shrinkB=0))
ax.text(0.05, YT - 0.02, '$M$', ha='left', va='top', fontsize=13)
ax.text(XR - 0.05, 0.05, '$H$', ha='right', va='bottom', fontsize=13)

Mr = np.tanh(Hc / w) / norm
# M_s、M_r 刻度与左侧标注
for yv, lab in [(1.0, r'$M_s$'), (Mr, r'$M_r$')]:
    ax.plot([-0.035, 0.0], [yv, yv], 'k-', lw=0.9)
    ax.text(-0.06, yv, lab, ha='right', va='center', fontsize=12)
# H_c 刻度（回线在 M=0 处的翻转场）与下方标注
ax.plot([Hc, Hc], [0.0, -0.035], 'k-', lw=0.9)
ax.text(Hc - 0.03, -0.07, r'$H_c$', ha='right', va='top', fontsize=12)

fig.tight_layout()
save_fig(fig, 'ch6', 'fig6_24')
