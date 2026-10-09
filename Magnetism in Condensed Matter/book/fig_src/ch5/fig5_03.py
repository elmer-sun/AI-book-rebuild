# -*- coding: utf-8 -*-
# 图 5.3 约化磁化强度 M/Ms 随 T/TC 的平均场曲线族：J=1/2, 1, 3/2, 无穷
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
from scipy.optimize import brentq
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig


def Brillouin(J, x):
    if J == np.inf:
        if abs(x) < 1e-8:
            return x / 3.0
        return 1.0 / np.tanh(x) - 1.0 / x
    g = 2 * J + 1
    if abs(x) < 1e-8:
        return (g + 1) * x / (6 * J)
    return g / (2 * J) / np.tanh(g * x / (2 * J)) - 1.0 / (2 * J) / np.tanh(x / (2 * J))


def M_of_t(J, t):
    a = (3.0 if J == np.inf else 3 * J / (J + 1)) / t   # M = B_J(a*M)
    if t >= 1:
        return 0.0
    if t < 0.1 and np.isfinite(J):
        return 1.0                   # tanh-saturated; deviation < 1e-9
    f = lambda m: Brillouin(J, a * m) - m
    # physical root = largest root: take the LAST sign change on a grid
    mg = np.linspace(1e-6, 1.0 - 1e-9, 400)
    fg = np.array([f(m) for m in mg])
    idx = np.where(np.diff(np.signbit(fg)))[0]
    if len(idx) == 0:
        return 0.0
    i = idx[-1]
    return brentq(f, mg[i], mg[i + 1], xtol=1e-14)


fig, ax = new_fig(4.4, 3.6)

t = np.linspace(0, 1, 500)
for J in (0.5, 1.0, 1.5, np.inf):
    M = np.array([1.0 if ti == 0 else M_of_t(J, ti) for ti in t])
    ax.plot(t, M, 'k-', lw=1.1)

ax.set_xlim(0, 1.16)
ax.set_ylim(0, 1.16)
ax.set_xticks([0, 0.5, 1.0])
ax.set_yticks([0, 0.5, 1.0])
ax.set_xlabel(r'$T/T_C$', fontsize=12, labelpad=1)
ax.set_ylabel(r'$M/M_s$', fontsize=12)
ax.tick_params(top=False, right=False)

# leader-line labels above the curve bundle (as in the book)
lab = {0.5: r'$J=1/2$', 1.0: r'$1$', 1.5: r'$3/2$'}
for J, xt, yt, tt in [(0.5, 0.30, 1.075, 0.24),
                      (1.0, 0.60, 1.075, 0.44),
                      (1.5, 0.80, 1.010, 0.56)]:
    ax.annotate(lab[J], xy=(tt, M_of_t(J, tt)), xytext=(xt, yt),
                fontsize=11, ha='center',
                arrowprops=dict(arrowstyle='-', lw=0.6))
ax.text(0.68, M_of_t(np.inf, 0.68) - 0.055, r'$J=\infty$', fontsize=11,
        ha='center', va='top')

save_fig(fig, 'ch5', 'fig5_03')
