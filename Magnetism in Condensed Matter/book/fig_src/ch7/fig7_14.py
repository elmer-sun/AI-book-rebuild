# -*- coding: utf-8 -*-
# 图 7.14 一、二、三维电子气 chi_q 对比：1D 在 q=2k_F 发散，2D 扭折，3D 膝状转折
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
from scipy.interpolate import PchipInterpolator
import matplotlib.pyplot as plt
from mplstyle import new_fig, save_fig


def L1(x):
    return 0.5 / x * np.log(np.abs((1 + x) / (1 - x)))


def L3(x):
    x = np.asarray(x, dtype=float)
    r = np.empty_like(x)
    s = x < 1e-6
    r[s] = 1.0
    xs = x[~s]
    r[~s] = 0.5 + (1 - xs**2) / (4 * xs) * np.log(np.abs((1 + xs) / (1 - xs)))
    return r


def L2_num(x, nk=600, nth=2001):
    """2D Lindhard（数值积分），返回 g(x)，g(0)=1."""
    q = 2.0 * x
    k = np.linspace(1e-6, 1.0, nk)
    c0 = np.clip((1.0 - k**2 - q**2) / (2 * k * q), -1.0, 1.0)
    th0 = np.arccos(c0)
    t = np.linspace(-1, 1, nth)
    th = th0[:, None] * t[None, :]
    den = -q * q - 2 * k[:, None] * q * np.cos(th) + 1j * 1e-6
    val = np.real(1.0 / den).mean(axis=1) * (2 * th0)
    Pi = 4.0 / (4 * np.pi**2) * np.trapezoid(k * val, k)
    return Pi / (-0.5 / np.pi)      # Pi(0) = -N(0)/2（本归一化下）


xs = np.concatenate([np.linspace(1.001, 1.05, 10),
                     np.linspace(1.08, 2.3, 60)])
gs = np.array([L2_num(x) for x in xs])
print('check g2d(2) =', L2_num(2.0))
f2 = PchipInterpolator(xs, gs)

fig, ax = new_fig(4.3, 3.4)

xp = np.linspace(1e-6, 1.0, 120)
ax.plot(xp, np.ones_like(xp), 'k-', lw=1.3)          # 2D 平台
xp = np.linspace(1.0, 2.3, 300)
ax.plot(xp, np.clip(f2(xp), 0, 2.8), 'k-', lw=1.3)   # 2D
xp = np.linspace(1e-6, 2.3, 500)
ax.plot(xp, np.clip(L1(xp), 0, 2.8), 'k-', lw=1.3)   # 1D（尖峰出图顶）
ax.plot(xp, L3(xp), 'k-', lw=1.3)                    # 3D

ax.plot([1, 1], [0, 2.72], 'k:', lw=0.9)

ax.text(0.80, 1.72, '1D', fontsize=12)
ax.text(0.72, 1.03, '2D', fontsize=12)
ax.text(0.63, 0.48, '3D', fontsize=12)

ax.set_xlim(0, 2.35)
ax.set_ylim(0, 2.72)
ax.set_xticks([0, 1, 2])
ax.set_yticks([0, 0.5, 1.0], ['0', r'$\chi_{\mathrm{P}}/2$',
                              r'$\chi_{\mathrm{P}}$'])
ax.spines[['top', 'right']].set_visible(False)
ax.tick_params(top=False, right=False)
ax.plot(1.0, 0, '>k', ms=5, clip_on=False, transform=ax.transAxes)
ax.plot(0.0, 1.0, '^k', ms=5, clip_on=False, transform=ax.transAxes)
ax.set_xlabel(r'$q/2k_{\mathrm{F}}$', fontsize=12, labelpad=1)
ax.set_ylabel(r'$\chi_{\mathbf{q}}$', fontsize=12)

save_fig(fig, 'ch7', 'fig7_14')
