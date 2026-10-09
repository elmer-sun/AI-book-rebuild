# -*- coding: utf-8 -*-
# 图 8.25 铁磁体霍尔电阻率示意：低场段斜率 ∝(R0+Re)，饱和(B>mu0 Ms)后斜率 ∝R0
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig

fig, ax = new_fig(2.7, 2.9)

# two straight segments
ax.plot([0, 1.0], [0, 2.3], 'k-', lw=1.7)
ax.plot([1.0, 2.7], [2.3, 3.1], 'k-', lw=1.7)

# axes with arrows through the origin
ax.annotate('', xy=(0, 3.45), xytext=(0, -0.02),
            arrowprops=dict(arrowstyle='-|>', lw=1.0, color='k'))
ax.annotate('', xy=(2.95, 0), xytext=(-0.02, 0),
            arrowprops=dict(arrowstyle='-|>', lw=1.0, color='k'))
ax.text(0.06, 3.55, r'$\rho_{\mathrm{H}}$', fontsize=13, ha='left', va='bottom')
ax.text(3.05, 0, r'$B$', fontsize=13, ha='left', va='center')

# saturation mark
ax.plot([1.0, 1.0], [-0.07, 0.07], 'k-', lw=1.0)
ax.text(1.0, -0.24, r'$\mu_0 M_{\mathrm{s}}$', fontsize=12, ha='center', va='top')

ax.set_xlim(-0.12, 3.35)
ax.set_ylim(-0.72, 3.85)
ax.axis('off')

fig.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.98)
save_fig(fig, 'ch8', 'fig8_25')
