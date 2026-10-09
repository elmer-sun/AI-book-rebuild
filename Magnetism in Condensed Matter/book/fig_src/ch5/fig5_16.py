# -*- coding: utf-8 -*-
# 图 5.16 热中子谱：(a) 速度分布 n(v) (b) 波长分布 n(lambda)，30 K 与 300 K 等面积归一
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

KB = 1.380649e-23
MN = 1.6749275e-27
H = 6.62607015e-34


def nv(v_kms, T):
    v = v_kms * 1e3
    v0 = np.sqrt(2 * KB * T / MN)
    return v**3 * np.exp(-v**2 / v0**2)


def nl(l_A, T):
    lam = l_A * 1e-10
    lc = H / np.sqrt(2 * MN * KB * T)
    return lam**-5.0 * np.exp(-(lc / lam)**2)


fig, axs = plt.subplots(2, 1, figsize=(4.4, 6.0))

# ---------- (a) velocity ----------
ax = axs[0]
xr = (0.001, 8.0)
x = np.linspace(*xr, 2000)
y30 = nv(x, 30); y300 = nv(x, 300)
A30 = np.trapezoid(y30, x); A300 = np.trapezoid(y300, x)
# equal-area normalisation, 30 K peak pinned at 0.95 of the frame height
Sc = 0.95 * A30 / np.max(y30)
ax.plot(x, y30 / A30 * Sc, 'k:', lw=1.4)
ax.plot(x, y300 / A300 * Sc, 'k-', lw=1.4)
ax.set_xlim(0, 8); ax.set_ylim(0, 1.06)
ax.set_xticks([0, 2, 4, 6, 8]); ax.set_yticks([])
ax.set_xlabel(r'$v$ (km s$^{-1}$)', fontsize=11)
ax.set_ylabel(r'$n(v)$', fontsize=11)
ax.text(1.25, 0.88, '30 K', fontsize=10.5, ha='left')
ax.text(3.00, 0.30, '300 K', fontsize=10.5, ha='left')
ax.text(0.04, 0.92, '(a)', fontsize=12, transform=ax.transAxes)

# ---------- (b) wavelength ----------
ax = axs[1]
xr = (0.05, 15.0)
x = np.linspace(*xr, 3000)
y30 = nl(x, 30); y300 = nl(x, 300)
A30 = np.trapezoid(y30, x); A300 = np.trapezoid(y300, x)
Sc = 0.95 * A300 / np.max(y300)
ax.plot(x, y30 / A30 * Sc, 'k:', lw=1.4)
ax.plot(x, y300 / A300 * Sc, 'k-', lw=1.4)
ax.set_xlim(0, 15); ax.set_ylim(0, 1.06)
ax.set_xticks([0, 5, 10, 15]); ax.set_yticks([])
ax.set_xlabel(r'$\lambda$ ($10^{-10}$ m)', fontsize=11)
ax.set_ylabel(r'$n(\lambda)$', fontsize=11)
ax.text(1.55, 0.90, '300 K', fontsize=10.5, ha='left')
ax.text(4.45, 0.38, '30 K', fontsize=10.5, ha='left')
ax.text(0.04, 0.92, '(b)', fontsize=12, transform=ax.transAxes)

fig.subplots_adjust(left=0.10, right=0.965, top=0.975, bottom=0.075, hspace=0.42)
save_fig(fig, 'ch5', 'fig5_16')
