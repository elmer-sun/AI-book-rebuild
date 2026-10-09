# -*- coding: utf-8 -*-
# 图 5.5 外场下的平均场 M(T) 曲线族（J=1/2）：B=0 陡降，B 增大曲线压低抹平相变
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
from scipy.optimize import brentq
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig


def M_of_t(t, b):
    if t <= 0 or t < 0.05:
        return 1.0
    if b == 0 and t > 1:
        return 0.0
    f = lambda m: np.tanh((m + b) / t) - m
    lo, hi = 1e-12, 1.0 - 1e-9
    if f(lo) > 0:
        if f(hi) > 0:
            return 1.0        # root within 1e-9 of saturation
        return brentq(f, lo, hi, xtol=1e-13)
    return 0.0


fig, ax = new_fig(4.5, 3.4)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.plot(1, 0, ">k", transform=ax.transAxes, clip_on=False, ms=5)
ax.plot(0, 1, "^k", transform=ax.transAxes, clip_on=False, ms=5)

t = np.linspace(0, 1.5, 600)
bs = [0.0, 0.025, 0.06, 0.13, 0.24, 0.38, 0.71]
for b in bs:
    M = np.array([1.0 if ti == 0 else M_of_t(ti, b) for ti in t])
    ax.plot(t, M, 'k-', lw=1.5 if b == 0 else 0.9)

ax.set_xlim(0, 1.58)
ax.set_ylim(0, 1.12)
ax.set_xticks([0, 0.5, 1.0, 1.5])
ax.set_yticks([0, 0.5, 1.0])
ax.text(1.59, -0.015, r'$T/T_C$', ha='left', va='top', fontsize=12)
ax.text(-0.02, 1.14, r'$M/M_s$', ha='center', va='bottom', fontsize=12)

# B = 0 label with leader
ax.annotate(r'$B=0$', xy=(0.86, 0.83), xytext=(0.50, 0.66), fontsize=11,
            arrowprops=dict(arrowstyle='->', lw=0.7))
# increasing B double arrow across the family
ax.annotate('', xy=(1.28, 0.86), xytext=(0.70, 0.24),
            arrowprops=dict(arrowstyle='<->', lw=0.9))
ax.text(1.06, 0.475, 'increasing $B$', fontsize=11, rotation=38,
        ha='left', va='center', rotation_mode='anchor')

save_fig(fig, 'ch5', 'fig5_05')
