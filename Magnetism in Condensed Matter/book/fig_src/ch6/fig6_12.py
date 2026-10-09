# -*- coding: utf-8 -*-
# 图 6.12 一维自旋链磁振子色散 omega = (8JS/hbar) sin^2(qa/2)：q=0 处切线水平
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

fig, ax = plt.subplots(figsize=(3.4, 3.0))
for sp in ax.spines.values():
    sp.set_visible(False)
ax.set_xticks([])
ax.set_yticks([])

q = np.linspace(0, 1, 200)          # q in units of pi/a
w = np.sin(np.pi * q / 2) ** 2      # omega / (8JS/hbar)
ax.plot(q, w, 'k-', lw=1.7)
ax.plot([1, 1], [0, 1.0], 'k:', lw=0.9)

# axes arrows
ax.annotate('', xy=(1.42, 0), xytext=(-0.03, 0),
            arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))
ax.annotate('', xy=(0, 1.30), xytext=(0, -0.03),
            arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))
# vertical double arrow marking the zone-boundary frequency
ax.annotate('', xy=(1.15, 1.0), xytext=(1.15, 0.0),
            arrowprops=dict(arrowstyle='<->', lw=1.0, color='k'))
ax.text(1.22, 0.5, r'$8JS/\hbar$', ha='left', va='center', fontsize=12)

ax.text(0, 1.36, r'$\omega$', ha='center', va='bottom', fontsize=12)
ax.text(1.46, 0.0, r'$q$', ha='left', va='center', fontsize=12)
ax.text(-0.04, -0.1, r'$0$', ha='right', va='top', fontsize=11)
ax.text(1.0, -0.1, r'$\pi/a$', ha='center', va='top', fontsize=11)

ax.set_xlim(-0.08, 1.58)
ax.set_ylim(-0.16, 1.44)

save_fig(fig, 'ch6', 'fig6_12')
