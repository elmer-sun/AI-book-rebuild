# -*- coding: utf-8 -*-
# 图 6.27 Stoner-Wohlfarth 单畴粒子（theta 为场与易轴夹角）：
# (a) theta=90 回线 (b) theta=90 能量面+最低能量轨迹 (c) theta=30 回线 (d) theta=30 能量面
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from mplstyle import save_fig

NPHI = 6001
PHI = np.linspace(0, 2 * np.pi, NPHI, endpoint=False)


def Efield(phi, h, th):
    """约化能量 E/K = sin^2(phi) - 2 h cos(theta - phi)，h = H/H_k = M_s H / 2K"""
    return np.sin(phi) ** 2 - 2.0 * h * np.cos(th - phi)


def minima(phi, Ev):
    idx = np.where((Ev <= np.roll(Ev, 1)) & (Ev <= np.roll(Ev, -1)))[0]
    return idx


def sweep(th, hs, phi_start):
    """沿 h 序列连续追踪一个极小分支，遇到分支消失即跳到全局极小。
    返回 (h, phi, M, E)，跳变处插入竖直连接点。"""
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
        if d[k] > 1.0:                      # 分支消失 -> 跳变
            k = int(np.argmin(Ev[cand]))
        prev = PHI[cand[k]]
        H.append(h)
        PH.append(prev)
    H = np.array(H)
    PH = np.array(PH)
    M = np.cos(th - PH)
    E = Efield(PH, H, th)
    return H, PH, M, E


def with_jumps(H, V):
    """在跳变处插入同 h 的竖直段。"""
    X, Y = [H[0]], [V[0]]
    for i in range(1, len(H)):
        if abs(V[i] - Y[-1]) > 0.35:
            X.append(H[i]); Y.append(Y[-1])
        X.append(H[i]); Y.append(V[i])
    return np.array(X), np.array(Y)


def traj_points(H, P, E):
    """把 (h,phi,E) 轨迹画到 phi∈[0,2pi] 曲面上：环绕处断开，跳变处竖直连接。"""
    Pm = np.mod(P, 2 * np.pi)
    Xp, Xh, Xe = [Pm[0]], [H[0]], [E[0]]
    for i in range(len(H) - 1):
        dPr = abs(Pm[i + 1] - Pm[i])
        if dPr > np.pi:                   # phi 0<->2pi 环绕：断开
            Xp.append(np.nan); Xh.append(H[i + 1]); Xe.append(E[i + 1])
        elif abs(E[i + 1] - E[i]) > 0.3:  # 分支消失跳变：竖直连接
            Xp.append(Pm[i + 1]); Xh.append(H[i + 1]); Xe.append(E[i])
        Xp.append(Pm[i + 1]); Xh.append(H[i + 1]); Xe.append(E[i + 1])
    return np.array(Xp), np.array(Xh), np.array(Xe)


def loop(ax, th):
    hd = np.linspace(1.45, -1.45, 1400)
    Hu, Pu, Mu, _ = sweep(th, hd, th)
    Hl, Pl, Ml, _ = sweep(th, hd[::-1], th + np.pi)
    for H, M in [(Hu, Mu), (Hl, Ml)]:
        X, Y = with_jumps(H, M)
        ax.plot(X, Y, 'k-', lw=1.6)
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_xlabel(r'$h$')
    ax.set_ylabel(r'$M/M_s$')


fig = plt.figure(figsize=(4.8, 13.2))
gs = fig.add_gridspec(4, 1, height_ratios=[1, 1.45, 1, 1.45],
                      left=0.17, right=0.96, top=0.985, bottom=0.026,
                      hspace=0.38)

# ---------------- (a) theta = 90 loop ----------------
ax = fig.add_subplot(gs[0])
loop(ax, np.pi / 2)
ax.text(0.05, 0.94, '(a)', transform=ax.transAxes, fontsize=13)

# ---------------- (b) theta = 90 energy surface ----------------
ax = fig.add_subplot(gs[1], projection='3d')
th = np.pi / 2
hg = np.linspace(-2, 2, 33)
pg = np.linspace(0, 2 * np.pi, 241)
for h in hg:
    ax.plot(pg, np.full_like(pg, h), Efield(pg, h, th), 'k-', lw=0.45)
for hswe, p0 in [(np.linspace(2, -2, 900), th),
                 (np.linspace(-2, 2, 900), th + np.pi)]:
    Ht, Pt, Mt, Et = sweep(th, hswe, p0)
    Xp, Xh, Xe = traj_points(Ht, Pt, Et)
    ax.plot(Xp, Xh, Xe, 'k-', lw=2.4)
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-2, 2)
ax.set_xticks([0, np.pi, 2 * np.pi])
ax.set_xticklabels(['0', r'$\pi$', r'$2\pi$'])
ax.set_yticks([-2, -1, 0, 1, 2])
ax.set_xlabel(r'$\phi$', labelpad=12)
ax.set_ylabel('$h$', labelpad=14)
ax.view_init(elev=26, azim=-60)
ax.grid(False)
for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.pane.set_facecolor('white')
    axis.pane.set_edgecolor('none')
ax.set_zticks([])
ax.zaxis.set_visible(False)
# 左侧 Energy 竖直箭头
ax.annotate('', xy=(0.055, 0.62), xytext=(0.055, 0.28),
            xycoords='axes fraction',
            arrowprops=dict(arrowstyle='-|>', color='k', lw=1.2))
ax.text2D(0.075, 0.64, 'Energy', transform=ax.transAxes,
          ha='left', va='center', fontsize=11)
ax.text2D(0.06, 0.95, '(b)', transform=ax.transAxes, fontsize=13)

# ---------------- (c) theta = 30 loop ----------------
ax = fig.add_subplot(gs[2])
loop(ax, np.deg2rad(30))
ax.text(0.05, 0.94, '(c)', transform=ax.transAxes, fontsize=13)

# ---------------- (d) theta = 30 energy surface ----------------
ax = fig.add_subplot(gs[3], projection='3d')
th = np.deg2rad(30)
for h in hg:
    ax.plot(pg, np.full_like(pg, h), Efield(pg, h, th), 'k-', lw=0.45)
for hswe, p0 in [(np.linspace(2, -2, 900), th),
                 (np.linspace(-2, 2, 900), th + np.pi)]:
    Ht, Pt, Mt, Et = sweep(th, hswe, p0)
    Xp, Xh, Xe = traj_points(Ht, Pt, Et)
    ax.plot(Xp, Xh, Xe, 'k-', lw=2.4)
ax.set_xlim(0, 2 * np.pi)
ax.set_ylim(-2, 2)
ax.set_xticks([0, np.pi, 2 * np.pi])
ax.set_xticklabels(['0', r'$\pi$', r'$2\pi$'])
ax.set_yticks([-2, -1, 0, 1, 2])
ax.set_xlabel(r'$\phi$', labelpad=12)
ax.set_ylabel('$h$', labelpad=14)
ax.view_init(elev=26, azim=-60)
ax.grid(False)
for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
    axis.pane.set_facecolor('white')
    axis.pane.set_edgecolor('none')
ax.set_zticks([])
ax.zaxis.set_visible(False)
# 左侧 Energy 竖直箭头
ax.annotate('', xy=(0.055, 0.62), xytext=(0.055, 0.28),
            xycoords='axes fraction',
            arrowprops=dict(arrowstyle='-|>', color='k', lw=1.2))
ax.text2D(0.075, 0.64, 'Energy', transform=ax.transAxes,
          ha='left', va='center', fontsize=11)
ax.text2D(0.06, 0.95, '(d)', transform=ax.transAxes, fontsize=13)

save_fig(fig, 'ch6', 'fig6_27')
