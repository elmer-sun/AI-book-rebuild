# -*- coding: utf-8 -*-
# 图 5.7 居里-外斯定律三视图：(a) chi(T) (b) 1/chi(T) (c) chi*T(T)，theta = 0, +-Theta
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

fig, axs = plt.subplots(3, 1, figsize=(4.3, 7.6))


def arrow_axes(ax):
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.plot(1, 0, ">k", transform=ax.transAxes, clip_on=False, ms=5)
    ax.plot(0, 1, "^k", transform=ax.transAxes, clip_on=False, ms=5)


LS = {'p': ':', '0': '-', 'm': '--'}

# ---------- (a) chi vs T ----------
ax = axs[0]
arrow_axes(ax)
ax.text(0.035, 0.955, '(a)', transform=ax.transAxes, fontsize=12, va='top')
x = np.linspace(0.02, 5, 400)
ax.plot(x, 1.0 / x, LS['0'], lw=1.5, color='k')                # theta = 0
ax.plot(np.linspace(1.22, 5, 200), 1.0 / (np.linspace(1.22, 5, 200) - 1),
        LS['p'], lw=1.2, color='k')                            # theta = +Theta
ax.plot(x, 1.0 / (x + 1), LS['m'], lw=1.2, color='k')          # theta = -Theta
ax.axvline(1, ls=':', lw=0.8, color='0.35')
ax.set_xlim(0, 5.2); ax.set_ylim(0, 5.2)
ax.set_xticks([1]); ax.set_xticklabels([r'$\Theta$'])
ax.set_yticks([])
ax.text(5.25, -0.1, '$T$', ha='left', va='top', fontsize=12)
ax.text(-0.12, 5.3, r'$\chi$', ha='center', va='bottom', fontsize=12)
ax.text(2.45, 2.05, r'$\theta=+\Theta$', fontsize=10.5)
ax.text(2.85, 0.72, r'$\theta=0$', fontsize=10.5)
ax.text(3.35, 0.42, r'$\theta=-\Theta$', fontsize=10.5)
ax.text(0.03, 0.93, 'thick: solid' if False else '', transform=ax.transAxes)

# ---------- (b) 1/chi vs T ----------
ax = axs[1]
arrow_axes(ax)
ax.text(0.035, 0.955, '(b)', transform=ax.transAxes, fontsize=12, va='top')
xs = np.linspace(0, 5, 100)
ax.plot(xs, xs, LS['0'], lw=1.5, color='k')
# theta=0 line through origin, dashed into T<0
ax.plot(np.linspace(-1.6, 0, 20), np.linspace(-1.6, 0, 20), '--', lw=0.9, color='k')
# theta=+Theta: zero at +1, dashed extension on T<0
xp = np.linspace(0, 5, 100)
ax.plot(xp, xp - 1, LS['p'], lw=1.2, color='k')
ax.plot(np.linspace(-1.6, 0, 20), np.linspace(-1.6, 0, 20) - 1, '--', lw=0.9, color='k')
# theta=-Theta: zero at -1
xm = np.linspace(-1, 5, 100)
ax.plot(xm, xm + 1, LS['m'], lw=1.2, color='k')
ax.set_xlim(-1.7, 5.2); ax.set_ylim(-1.6, 6.4)
ax.set_xticks([-1, 1]); ax.set_xticklabels([r'$-\Theta$', r'$\Theta$'])
ax.set_yticks([])
ax.text(5.25, -0.15, '$T$', ha='left', va='top', fontsize=12)
ax.text(-0.10, 6.5, r'$1/\chi$', ha='center', va='bottom', fontsize=12)
ax.text(3.30, 5.15, r'$\theta=-\Theta$', fontsize=10.5)
ax.text(3.55, 3.30, r'$\theta=0$', fontsize=10.5)
ax.text(3.75, 1.75, r'$\theta=+\Theta$', fontsize=10.5)

# ---------- (c) chi*T vs T ----------
ax = axs[2]
arrow_axes(ax)
ax.text(0.035, 0.955, '(c)', transform=ax.transAxes, fontsize=12, va='top')
ax.plot(np.linspace(0, 5, 50), np.full(50, 1.0), LS['0'], lw=1.5, color='k')
xp = np.linspace(1.33, 5, 300)
ax.plot(xp, xp / (xp - 1), LS['p'], lw=1.2, color='k')
ax.plot(np.linspace(0, 5, 100), np.linspace(0, 5, 100) /
        (np.linspace(0, 5, 100) + 1), LS['m'], lw=1.2, color='k')
ax.axvline(1, ls=':', lw=0.8, color='0.35')
ax.set_xlim(0, 5.2); ax.set_ylim(0, 3.3)
ax.set_xticks([1]); ax.set_xticklabels([r'$\Theta$'])
ax.set_yticks([])
ax.text(5.25, -0.08, '$T$', ha='left', va='top', fontsize=12)
ax.text(-0.12, 3.4, r'$\chi T$', ha='center', va='bottom', fontsize=12)
ax.text(2.10, 2.50, r'$\theta=+\Theta$', fontsize=10.5)
ax.text(3.85, 1.10, r'$\theta=0$', fontsize=10.5)
ax.text(2.75, 0.48, r'$\theta=-\Theta$', fontsize=10.5)

fig.subplots_adjust(left=0.09, right=0.97, top=0.985, bottom=0.032, hspace=0.24)
save_fig(fig, 'ch5', 'fig5_07')
