# -*- coding: utf-8 -*-
# 图 6.28 Stoner-Wohlfarth 回线族与多晶平均：
# (a) 小角度族 theta=0/5/15/30 (b) 大角度族 theta=90/45/60/75 (c) 无规取向平均回线
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

NPHI = 6001
PHI = np.linspace(0, 2 * np.pi, NPHI, endpoint=False)


def Efield(phi, h, th):
    return np.sin(phi) ** 2 - 2.0 * h * np.cos(th - phi)


def minima(phi, Ev):
    return np.where((Ev <= np.roll(Ev, 1)) & (Ev <= np.roll(Ev, -1)))[0]


def sweep(th, hs, phi_start):
    Ev = Efield(PHI, hs[0], th)
    cand = minima(PHI, Ev)
    d = np.abs(((PHI[cand] - phi_start + np.pi) % (2 * np.pi)) - np.pi)
    prev = PHI[cand[np.argmin(d)]]
    H, PH = [], []
    for h in hs:
        Ev = Efield(PHI, h, th)
        cand = minima(PHI, Ev)
        if len(cand) == 0:
            continue
        d = np.abs(((PHI[cand] - prev + np.pi) % (2 * np.pi)) - np.pi)
        k = int(np.argmin(d))
        if d[k] > 1.0:
            k = int(np.argmin(Ev[cand]))
        prev = PHI[cand[k]]
        H.append(h)
        PH.append(prev)
    H = np.array(H)
    return H, np.cos(th - np.array(PH))


def with_jumps(H, V):
    X, Y = [H[0]], [V[0]]
    for i in range(1, len(H)):
        if abs(V[i] - Y[-1]) > 0.35:
            X.append(H[i]); Y.append(Y[-1])
        X.append(H[i]); Y.append(V[i])
    return np.array(X), np.array(Y)


def draw_loop(ax, th, lw, ls):
    hd = np.linspace(1.45, -1.45, 1400)
    Hu, Mu = sweep(th, hd, th)
    Hl, Ml = sweep(th, hd[::-1], th + np.pi)
    for H, M in [(Hu, Mu), (Hl, Ml)]:
        X, Y = with_jumps(H, M)
        ax.plot(X, Y, color='k', lw=lw, ls=ls)


fig, axs = plt.subplots(3, 1, figsize=(4.3, 9.8),
                        gridspec_kw=dict(left=0.17, right=0.96,
                                         top=0.985, bottom=0.045, hspace=0.42))

# ---- (a) 小角度族 ----
ax = axs[0]
draw_loop(ax, 0.0, 2.4, '-')
for tv in (5, 15):
    draw_loop(ax, np.deg2rad(tv), 1.0, '-')
draw_loop(ax, np.deg2rad(30), 1.3, '--')
ax.text(0.05, 0.94, '(a)', transform=ax.transAxes, fontsize=13)

# ---- (b) 大角度族 ----
ax = axs[1]
draw_loop(ax, np.pi / 2, 2.4, '-')
for tv in (45, 60):
    draw_loop(ax, np.deg2rad(tv), 1.0, '-')
draw_loop(ax, np.deg2rad(75), 1.3, '--')
ax.text(0.05, 0.94, '(b)', transform=ax.transAxes, fontsize=13)

# ---- (c) 多晶平均回线（对 0-180 度无规取向取平均，两支） ----
ax = axs[2]
hd = np.linspace(1.45, -1.45, 400)
ths = np.deg2rad(np.linspace(0, 180, 361))[:-1]
MU, ML = [], []
for tv in ths:
    Hu, Mu = sweep(tv, hd, tv)
    Hl, Ml = sweep(tv, hd[::-1], tv + np.pi)
    MU.append(Mu)            # 按 h 降序
    ML.append(Ml)            # 按 h 升序
bu = np.array(MU).mean(axis=0)
bl = np.array(ML).mean(axis=0)
ax.plot(hd, bu, 'k-', lw=1.7)
ax.plot(hd[::-1], bl, 'k-', lw=1.7)
ax.text(0.05, 0.94, '(c)', transform=ax.transAxes, fontsize=13)

for ax in axs:
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_xlabel(r'$h$')
    ax.set_ylabel(r'$M/M_s$')

save_fig(fig, 'ch6', 'fig6_28')
