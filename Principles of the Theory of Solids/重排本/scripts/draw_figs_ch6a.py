# -*- coding: utf-8 -*-
"""重绘 Ziman《Principles of the Theory of Solids》2nd ed. 第 6 章插图（第一批）。
原书图号连续：Fig. 97-101 (pp.172-180), Fig. 112-118 (pp.190-198)。
输出 figures/fig_{key}.pdf + figures/preview/fig_{key}.png
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle
from matplotlib.path import Path
from scipy.interpolate import PchipInterpolator

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

HATCH = '////'   # 原书斜线方向：自左下到右上


def save(fig, key):
    for ext, dpi in (('pdf', None), ('png', 300)):
        out = os.path.join(FIGDIR if ext == 'pdf' else PREVDIR,
                           f'fig_{key}.{ext}')
        fig.savefig(out, bbox_inches='tight', pad_inches=0.03, dpi=dpi)
    plt.close(fig)
    print('saved fig_%s' % key)


def newax(fig, rect, xlim, ylim):
    ax = fig.add_axes(rect)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis('off')
    ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    return ax


def arrow(ax, x0, y0, x1, y1, lw=1.1, style='-|>', ms=10):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, color='black', lw=lw,
                                mutation_scale=ms, shrinkA=0, shrinkB=0),
                zorder=6)


def dblarrow(ax, x0, y0, x1, y1, lw=1.0, ms=9):
    # 从中心向两端的两支单箭头（避免短箭头时 <|-|> 两端箭头互相重叠）
    xm, ym = 0.5 * (x0 + x1), 0.5 * (y0 + y1)
    arrow(ax, xm, ym, x0, y0, lw=lw, ms=ms)
    arrow(ax, xm, ym, x1, y1, lw=lw, ms=ms)


def stipple(ax, poly, n=1200, seed=0, size=1.2, alpha=0.5, color='0.15'):
    poly = np.asarray(poly)
    rng = np.random.default_rng(seed)
    path = Path(poly)
    (x0, y0), (x1, y1) = poly.min(0), poly.max(0)
    pts = np.empty((n, 2))
    cnt = 0
    while cnt < n:
        cand = rng.uniform((x0, y0), (x1, y1), size=(n * 3, 2))
        ok = cand[path.contains_points(cand)]
        take = min(len(ok), n - cnt)
        pts[cnt:cnt + take] = ok[:take]
        cnt += take
    ax.scatter(pts[:n, 0], pts[:n, 1], s=size, c=color, alpha=alpha,
               linewidths=0, zorder=2)


def ion(ax, x, y, r, sign, lw=1.5):
    ax.add_patch(Circle((x, y), r, fill=False, lw=lw, zorder=4))
    b = 0.45 * r
    ax.plot([x - b, x + b], [y, y], 'k-', lw=lw, zorder=5)
    if sign > 0:
        ax.plot([x, x], [y - b, y + b], 'k-', lw=lw, zorder=5)


# ---------------------------------------------------------------- Fig. 97
def fig_97():
    fig = plt.figure(figsize=(4.7, 1.95))
    ax = newax(fig, [0.005, 0.02, 0.99, 0.96], (-1.05, 5.62), (-1.78, 1.60))
    ax.plot([-0.88, 5.45], [0, 0], 'k-', lw=1.1, zorder=1)
    for i in range(5):
        ax.add_patch(Circle((i, 0), 0.50, facecolor='white', edgecolor='k',
                            lw=1.1, hatch=HATCH, zorder=2))
        ax.plot([i], [0], 'ko', ms=3.6, zorder=5)
    xs = np.array([-0.70, -0.30, 0.0, 1.0, 1.8, 2.3, 2.8, 3.3, 3.8, 4.4,
                   5.3])
    Es = np.array([0.998, 1.0, 0.999, 0.93, 0.31, 0.16, -0.59, -0.97, -1.0,
                   -0.99, -0.90])
    env = PchipInterpolator(xs, Es)
    x = np.linspace(-0.70, 5.3, 1200)
    w = env(x) * np.cos(2 * np.pi * x)
    ax.plot(x, env(x), 'k--', dashes=(5, 3), lw=1.1, zorder=3)
    ax.plot(x, w, 'k-', lw=1.25, zorder=4)
    ax.text(-0.62, 1.22, r'$f\,(\boldsymbol{l},t)$', fontsize=11)
    ax.text(0.30, -1.40, r'$\phi_n(\mathbf{r}-\boldsymbol{l})$', fontsize=11)
    save(fig, 97)


# ---------------------------------------------------------------- Fig. 98
def wannier_profile(u):
    """单一 Wannier 函数剖面：主峰（相邻格点处过零）+ 浅负谷 + 低正包。"""
    u = np.asarray(u, dtype=float)
    a = np.abs(u)
    y = np.zeros_like(u)
    m1 = a <= 1.0
    y[m1] = np.cos(np.pi * a[m1] / 2.0)
    m2 = (a > 1.0) & (a <= 2.35)
    y[m2] = -0.30 * np.sin(np.pi * (a[m2] - 1.0) / 1.35)
    m3 = (a > 2.35) & (a <= 3.8)
    y[m3] = 0.22 * np.sin(np.pi * (a[m3] - 2.35) / 1.45)
    return y


def fig_98():
    fig = plt.figure(figsize=(4.5, 2.15))
    ax = newax(fig, [0.005, 0.02, 0.99, 0.96], (-1.20, 5.60), (-1.25, 1.72))
    ax.plot([-0.95, 5.30], [0, 0], 'k-', lw=1.1, zorder=1)
    for i in range(5):
        ax.add_patch(Circle((i, 0), 0.50, facecolor='white', edgecolor='k',
                            lw=1.1, hatch=HATCH, zorder=2))
        ax.plot([i], [0], 'ko', ms=3.6, zorder=5)
    ax.plot([1, 1], [0, 1.58], 'k-', lw=0.9, zorder=3)
    ax.plot([2, 2], [0, 1.58], 'k--', dashes=(4, 3), lw=0.9, zorder=3)
    u = np.linspace(-3.8, 3.8, 1200)
    m = (u >= -1.0) & (u <= 3.6)
    y = wannier_profile(u[m])
    y = y * np.clip((u[m] + 1.0) / 0.12, 0, 1)   # 从格点 1 的原子处平滑出发
    ax.plot(1 + u[m], y, 'k-', lw=1.25, zorder=4)
    m = (u >= -1.85) & (u <= 3.45)
    ax.plot(2 + u[m], wannier_profile(u[m]), 'k--', dashes=(5, 3), lw=1.15,
            zorder=4)
    dblarrow(ax, 1, -0.85, 2, -0.85)
    ax.text(1.5, -0.68, r'$d$', fontsize=12, ha='center')
    save(fig, 98)


# ---------------------------------------------------------------- Fig. 99
def fig_99():
    rng = np.random.default_rng(7)
    fig = plt.figure(figsize=(3.0, 3.3))
    ax = fig.add_axes([0.10, 0.02, 0.88, 0.96])
    ax.set_xlim(0, 2.3)
    ax.set_ylim(-0.42, 3.05)
    ax.axis('off')
    x0, x1 = 0.15, 2.15
    yc0, yc1 = 2.30, 3.00
    ax.add_patch(Rectangle((x0, yc0), x1 - x0, yc1 - yc0, facecolor='white',
                           edgecolor='k', lw=0.8, zorder=1))
    n = 2600
    pts = rng.uniform((x0 + 0.02, yc0 + 0.02), (x1 - 0.02, yc1 - 0.02),
                      (n, 2))
    keep = rng.uniform(size=n) < 0.55
    ax.scatter(pts[keep, 0], pts[keep, 1], s=0.9, c='k', alpha=0.5,
               linewidths=0, zorder=2)
    ax.plot([x0, x1], [yc0, yc0], 'k-', lw=1.6, zorder=4)
    ax.text(0.5 * (x0 + x1), 0.5 * (yc0 + yc1), 'Conduction band',
            ha='center', va='center', fontsize=10.5, zorder=6)
    # 杂质能级：三条短横线 + 电子（实心点）
    xi = x0 + 0.72
    for k in range(3):
        ax.plot([xi - 0.09, xi + 0.09], [yc0 - 0.07 - 0.065 * k] * 2, 'k-',
                lw=1.0, zorder=5)
    ax.plot([xi], [yc0 - 0.30], 'ko', ms=3.2, zorder=5)
    ax.text(0.5 * (x0 + x1) + 0.16, 1.42, 'Energy gap', ha='center',
            fontsize=10.5)
    yv0, yv1 = 0.0, 0.68
    ax.add_patch(Rectangle((x0, yv0), x1 - x0, yv1 - yv0, facecolor='white',
                           edgecolor='k', lw=1.2, hatch=HATCH, zorder=1))
    save(fig, 99)


# ---------------------------------------------------------------- Fig. 100
def fig_100():
    fig = plt.figure(figsize=(4.8, 2.15))
    # ---- (a) ----
    ax = fig.add_axes([0.0, 0.02, 0.47, 0.92])
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 3.55)
    ax.axis('off')
    ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 3.55)
    t = np.linspace(0, 2 * np.pi, 400)
    rr = 1.30 * (1 + 0.10 * np.sin(3 * t + 0.7) + 0.07 * np.sin(5 * t + 2.1)
                 + 0.05 * np.sin(7 * t + 4.0))
    blob = np.stack([2.0 + rr * np.cos(t),
                     1.85 + 1.12 * rr / 1.30 * np.sin(t)], 1)
    ax.add_patch(Polygon(blob, closed=True, facecolor='white', edgecolor='k',
                         lw=1.1, hatch=HATCH, zorder=1))
    centers = [(1.28, 2.42, 0.42), (1.62, 2.10, 0.46), (1.95, 2.62, 0.40),
               (2.62, 2.72, 0.44), (1.98, 1.72, 0.40), (2.38, 1.52, 0.42),
               (1.28, 1.20, 0.44), (1.86, 0.78, 0.44), (2.72, 1.02, 0.46),
               (3.18, 1.92, 0.44)]
    for (cx, cy, r) in centers:
        ax.add_patch(Circle((cx, cy), r, facecolor='none', edgecolor='k',
                            lw=1.4, zorder=4))
        ax.add_patch(Circle((cx, cy), 0.13, facecolor='white',
                            edgecolor='k', lw=1.1, zorder=5))
        b = 0.065
        ax.plot([cx - b, cx + b], [cy, cy], 'k-', lw=1.0, zorder=6)
        ax.plot([cx, cx], [cy - b, cy + b], 'k-', lw=1.0, zorder=6)
    ax.text(2.0, 0.18, r'$(a)$', ha='center', fontsize=12)
    # ---- (b) ----
    ax = fig.add_axes([0.50, 0.02, 0.48, 0.92])
    ax.set_xlim(-0.62, 1.62)
    ax.set_ylim(-0.62, 3.62)
    ax.axis('off')
    ax.plot([0, 0], [-0.42, 3.42], 'k-', lw=1.6, zorder=3)
    arrow(ax, -0.26, 2.98, -0.26, 3.36, lw=1.1)
    ax.text(-0.36, 3.06, r'$\mathcal{E}$', fontsize=12, ha='right')
    Ec, Ev = 2.05, 1.00
    Nc = np.linspace(0, 1.0, 200)
    Eco = Ec + 1.30 * Nc ** 2
    ax.fill_betweenx(Eco, 0, Nc, facecolor='white', edgecolor='black',
                     lw=0, hatch='---', zorder=1)
    ax.plot(Nc, Eco, 'k-', lw=1.4, zorder=3)
    Nv = np.linspace(0, 1.02, 200)
    Evo = Ev - 1.00 * Nv ** 2 / 1.02
    ax.fill_betweenx(Evo, 0, Nv, facecolor='white', edgecolor='black',
                     lw=0, hatch='---', zorder=1)
    ax.plot(Nv, Evo, 'k-', lw=1.4, zorder=3)
    ax.add_patch(Ellipse((0.33, 1.66), 0.62, 0.115, facecolor='white',
                         edgecolor='k', lw=2.3, zorder=4))
    ax.plot([0, 1.38], [0, 0], 'k-', lw=1.6, zorder=3)
    ax.text(0.60, -0.24, r'$\mathcal{N}\,(\mathcal{E})$', fontsize=11,
            ha='center')
    arrow(ax, 1.02, -0.16, 1.30, -0.16, lw=1.1)
    ax.text(-0.07, Ec, r'$\mathcal{E}_c$', fontsize=11, ha='right',
            va='center')
    ax.text(-0.07, Ev, r'$\mathcal{E}_v$', fontsize=11, ha='right',
            va='center')
    ax.text(0.55, -0.56, r'$(b)$', ha='center', fontsize=12)
    save(fig, 100)


# ---------------------------------------------------------------- Fig. 101
def fig_101():
    fig = plt.figure(figsize=(4.0, 3.75))
    rng = np.random.default_rng(42)
    # ---- (a) ----
    ax = fig.add_axes([0.02, 0.30, 0.96, 0.68])
    ax.set_xlim(-0.85, 5.15)
    ax.set_ylim(-0.85, 4.55)
    ax.axis('off')
    ax.set_aspect('equal', adjustable='datalim')
    ax.set_xlim(-0.85, 5.15)
    ax.set_ylim(-0.85, 4.55)
    for i in range(5):
        for j in range(5):
            if i == 2 and j == 2:
                continue
            sign = 1 if (i + j) % 2 else -1
            ion(ax, j, 4 - i, 0.335, sign)
    cx, cy = 2.0, 2.0
    R, sigma = 1.55, 0.52
    u = rng.uniform(size=6500)
    rcl = sigma * np.sqrt(-2 * np.log(1 - u * (1 - np.exp(-R ** 2 /
                                                           (2 * sigma ** 2)))))
    th = rng.uniform(0, 2 * np.pi, 6500)
    ax.scatter(cx + rcl * np.cos(th), cy + rcl * np.sin(th), s=1.0, c='k',
               alpha=0.5, linewidths=0, zorder=6)
    u2 = rng.uniform(size=2400)
    rc2 = 0.22 * np.sqrt(-2 * np.log(1 - u2))
    th2 = rng.uniform(0, 2 * np.pi, 2400)
    ax.scatter(cx + rc2 * np.cos(th2), cy + rc2 * np.sin(th2), s=1.4, c='k',
               alpha=0.9, linewidths=0, zorder=7)
    ax.text(4.72, 2.0, r'$(a)$', fontsize=12, ha='center', va='center')
    # ---- (b) ----
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.26])
    ax.set_xlim(-1.35, 3.6)
    ax.set_ylim(-1.55, 0.62)
    ax.axis('off')
    ax.plot([-1.0, -1.0], [-1.32, 0.48], 'k-', lw=1.1, zorder=1)
    arrow(ax, -1.0, 0.48, -1.0, 0.60, lw=1.1)
    ax.text(-1.12, -0.32, r'$\mathcal{V}(r)$', fontsize=11, ha='right')
    ax.plot([-1.0, 3.25], [0, 0], 'k-', lw=1.0, zorder=1)
    ax.plot([0.9, 0.9], [-0.045, 0.045], 'k-', lw=1.0)
    arrow(ax, 1.30, 0.20, 2.05, 0.20, lw=1.0)
    ax.text(2.18, 0.20, r'$r$', fontsize=11, va='center')
    xs = np.array([-1.0, -0.30, 0.30, 0.55, 0.66, 0.76, 0.90, 1.04, 1.14,
                   1.25, 1.60, 2.20, 3.25])
    ys = np.array([-0.035, -0.055, -0.11, -0.26, -0.62, -1.05, -1.05, -1.05,
                   -0.62, -0.26, -0.115, -0.065, -0.045])
    xx = np.linspace(-1.0, 3.25, 800)
    yy = PchipInterpolator(xs, ys)(xx)
    ax.plot(xx, yy, 'k-', lw=1.3, zorder=3)
    ax.text(3.42, -0.52, r'$(b)$', fontsize=12, ha='center', va='center')
    save(fig, 101)


# ---------------------------------------------------------------- Fig. 112
def fig_112():
    fig = plt.figure(figsize=(4.2, 4.5))
    # ---- (a) ----
    ax = fig.add_axes([0.01, 0.56, 0.98, 0.42])
    ax.set_xlim(-1.5, 3.55)
    ax.set_ylim(-0.30, 1.22)
    ax.axis('off')
    ax.plot([-1.4, 3.45], [0, 0], 'k-', lw=1.1)
    ax.plot([-1, -1], [0, 0.85], 'k-', lw=0.9)
    ax.plot([1, 1], [0, 0.85], 'k-', lw=0.9)
    ax.plot([3, 3], [0, 0.85], 'k-', lw=0.9)
    arrow(ax, 0, 0, 0, 1.10, lw=1.2)
    ax.text(-0.07, 1.02, r'$\mathcal{E}(\mathbf{k})$', ha='right',
            fontsize=11)
    kk = np.linspace(-1.12, 3.12, 600)
    EE = 0.21 * (1 - np.cos(np.pi * kk))
    ax.plot(kk, EE, 'k-', lw=1.3, zorder=4)
    for k0 in (0.52, 1.45, 2.55):
        ax.plot([k0], [0.21 * (1 - np.cos(np.pi * k0))], 'ko', ms=4, zorder=5)
    arrow(ax, 0.70, 0.34, 0.92, 0.43, lw=1.3)
    arrow(ax, 1.58, 0.225, 1.73, 0.135, lw=1.3)
    arrow(ax, 2.80, 0.365, 2.98, 0.418, lw=1.3)
    arrow(ax, 1.55, 0.72, 2.35, 0.72, lw=1.2)
    ax.text(1.95, 0.78, r'$E$', ha='center', fontsize=12)
    ax.text(-1.07, 0.445, r"$A'$", ha='right', fontsize=12)
    ax.text(1.06, 0.455, r'$A$', ha='left', fontsize=12)
    ax.text(3.07, 0.45, r'$C$', ha='left', fontsize=12)
    ax.text(2.0, -0.09, r'$B$', ha='center', fontsize=12)
    ax.text(0, -0.09, r'$O$', ha='center', fontsize=12)
    ax.text(0.42, -0.18, r'$k$', ha='center', fontsize=12)
    arrow(ax, 0.52, -0.145, 0.80, -0.145, lw=1.0)
    ax.text(0.95, -0.27, r'$(a)$', ha='center', fontsize=12)
    # ---- (b) ----
    ax = fig.add_axes([0.17, 0.015, 0.66, 0.50])
    ax.set_xlim(-0.28, 1.62)
    ax.set_ylim(-0.24, 1.44)
    ax.axis('off')
    ax.plot([0, 0], [0, 1.00], 'k-', lw=1.1)
    arrow(ax, 0, 1.00, 0, 1.10, lw=1.1)
    ax.text(-0.05, 1.00, r'$t$', ha='right', fontsize=12)
    ax.plot([0, 1.45], [0, 0], 'k-', lw=1.1)
    arrow(ax, 1.45, 0, 1.58, 0, lw=1.1)
    ax.text(1.02, -0.10, r'$x$', ha='center', fontsize=12)
    ax.text(-0.03, -0.10, r'$O$', ha='right', fontsize=12)
    ax.plot([1, 1], [0, 1.32], 'k-', lw=0.9)
    tt = np.linspace(0, 1.26, 600)
    xx = 0.5 * (1 - np.cos(np.pi * tt / 0.42))
    ax.plot(xx, tt, 'k-', lw=1.3, zorder=4)
    arrow(ax, 0.40, 0.175, 0.66, 0.243, lw=1.3)
    arrow(ax, 0.63, 0.600, 0.37, 0.668, lw=1.3)
    arrow(ax, 0.86, 1.155, 0.97, 1.21, lw=1.3)
    ax.text(-0.05, 0.84, r'$B$', ha='right', fontsize=12)
    ax.text(1.05, 0.42, r'$A$', ha='left', fontsize=12)
    ax.text(1.05, 1.26, r'$C$', ha='left', fontsize=12)
    ax.text(0.6, -0.20, r'$(b)$', ha='center', fontsize=12)
    save(fig, 112)


# ---------------------------------------------------------------- Fig. 113
def fig_113():
    fig = plt.figure(figsize=(3.8, 2.55))
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.96])
    ax.set_xlim(-0.16, 1.12)
    ax.set_ylim(-0.17, 1.16)
    ax.axis('off')
    arrow(ax, 0, 0, 0, 1.10, lw=1.2)
    ax.text(-0.035, 1.03, r'$\mathcal{E}(\mathbf{k})$', ha='right',
            fontsize=11)
    ax.plot([0, 1.02], [0, 0], 'k-', lw=1.1)
    arrow(ax, 1.02, 0, 1.10, 0, lw=1.1)
    ax.text(0.42, -0.09, r'$k$', ha='center', fontsize=12)
    arrow(ax, 0.48, -0.068, 0.60, -0.068, lw=1.0)
    ax.text(-0.035, -0.06, r'$O$', ha='right', fontsize=12)
    xs = np.array([0, 0.08, 0.18, 0.30, 0.42, 0.52, 0.60, 0.66, 0.73, 0.81])
    ys = np.array([0, 0.012, 0.055, 0.13, 0.235, 0.36, 0.45, 0.487, 0.462,
                   0.405])
    xx = np.linspace(0, 0.79, 400)
    yy = PchipInterpolator(xs, ys)(xx)
    ax.plot(xx, yy, 'k-', lw=1.3, zorder=4)
    arrow(ax, 0.545, 0.398, 0.632, 0.475, lw=1.3)
    arrow(ax, 0.815, 0.408, 0.885, 0.335, lw=1.3)
    ax.text(0.915, 0.305, r'$B$', ha='left', fontsize=12)
    ax.text(0.688, 0.435, r'$A$', ha='left', fontsize=12)
    ax.plot([0.66, 0.66], [-0.02, 0.02], 'k-', lw=1.0)
    ax.plot([0.66, 0.66], [0.487, 0.72], 'k-', lw=0.9)
    ax.text(0.682, 0.595, r'$\mathcal{E}_\mathrm{gap}$', ha='left',
            fontsize=10.5)
    xs2 = np.array([0.66, 0.71, 0.78, 0.87, 0.97, 1.04])
    ys2 = np.array([0.72, 0.762, 0.812, 0.863, 0.905, 0.928])
    xx2 = np.linspace(0.66, 1.04, 300)
    ax.plot(xx2, PchipInterpolator(xs2, ys2)(xx2), 'k-', lw=1.3, zorder=4)
    ax.text(0.675, 0.755, r"$A''$", ha='left', fontsize=12)
    save(fig, 113)


# ---------------------------------------------------------------- Fig. 114
def fig_114():
    fig = plt.figure(figsize=(4.7, 2.0))
    ax = fig.add_axes([0.005, 0.02, 0.99, 0.96])
    ax.set_xlim(-0.75, 4.95)
    ax.set_ylim(-1.30, 1.30)
    ax.axis('off')
    th = np.deg2rad(-33.0)
    u = np.array([np.cos(th), np.sin(th)])
    nv = np.array([-np.sin(th), np.cos(th)])
    L, W = 3.1, 0.36
    for cen, seed in (((0.95, 0.0), 3), ((2.95, 0.0), 4)):
        c1 = cen + L * u
        c2 = cen - L * u
        poly = np.array([c1 + W * nv, c1 - W * nv, c2 - W * nv, c2 + W * nv])
        ax.add_patch(Polygon(poly, closed=True, facecolor='0.94',
                             edgecolor='none', zorder=1))
        stipple(ax, poly, n=1500, seed=seed, size=1.1, alpha=0.45)
        ax.plot([c1[0] + W * nv[0], c2[0] + W * nv[0]],
                [c1[1] + W * nv[1], c2[1] + W * nv[1]], 'k-', lw=1.0, zorder=3)
        ax.plot([c1[0] - W * nv[0], c2[0] - W * nv[0]],
                [c1[1] - W * nv[1], c2[1] - W * nv[1]], 'k-', lw=1.0, zorder=3)
    ax.plot([-0.62, 4.42], [0, 0], 'k-', lw=1.0, zorder=4)
    arrow(ax, 4.42, 0, 4.60, 0, lw=1.0)
    ax.text(4.68, 0, r'$x$', ha='left', va='center', fontsize=12)
    ax.plot([0.75], [0], 'ko', ms=4.6, zorder=6)
    ax.text(0.60, -0.15, r'$O$', ha='right', fontsize=12)
    arrow(ax, 1.30, 0, 1.58, 0, lw=1.0)
    ax.text(1.47, -0.19, r'$A$', ha='center', fontsize=12)
    ax.plot([2.45], [0], 'ko', ms=4.6, zorder=6)
    ax.text(2.28, -0.20, r"$A''$", ha='center', fontsize=12)
    ax.text(2.00, 0.10, r'$d$', ha='center', fontsize=12)
    arrow(ax, 3.30, 0.82, 4.00, 0.82, lw=1.2)
    ax.text(3.22, 0.82, r'$e\mathbf{E}$', ha='right', va='center',
            fontsize=12)
    save(fig, 114)


# ---------------------------------------------------------------- Fig. 115
def fig_115():
    rng = np.random.default_rng(11)
    fig = plt.figure(figsize=(4.5, 2.05))
    ax = fig.add_axes([0.005, 0.02, 0.99, 0.96])
    ax.set_xlim(-0.18, 5.45)
    ax.set_ylim(-0.78, 2.18)
    ax.axis('off')
    x1, x2 = 2.30, 2.95
    yE, top = 0.95, 1.85
    ax.add_patch(Rectangle((-0.05, -0.60), 5.50, 0.60, facecolor='0.93',
                           edgecolor='none', zorder=1))
    gp = rng.uniform((-0.05, -0.60), (5.45, 0.0), (2600, 2))
    ax.scatter(gp[:, 0], gp[:, 1], s=0.9, c='k', alpha=0.4, linewidths=0,
               zorder=1)
    ax.plot([-0.05, 5.45], [0, 0], 'k-', lw=1.2, zorder=3)
    ax.add_patch(Rectangle((x1, 0), x2 - x1, top, facecolor='0.90',
                           edgecolor='k', lw=1.2, zorder=2))
    gb = rng.uniform((x1, 0), (x2, top), (900, 2))
    ax.scatter(gb[:, 0], gb[:, 1], s=0.9, c='k', alpha=0.4, linewidths=0,
               zorder=2)
    ax.plot([0.02, x1], [yE, yE], 'k-', lw=1.0, zorder=4)
    ax.plot([x1, x2], [yE, yE], 'k--', dashes=(4, 3), lw=0.9, zorder=4)
    ax.plot([x2, 4.58], [yE, yE], 'k-', lw=1.0, zorder=4)
    ax.text(4.66, yE, r'$\mathcal{E}$', ha='left', va='center', fontsize=12)
    dblarrow(ax, 0.12, 0.02, 0.12, yE - 0.02, lw=1.0)
    ax.text(0.05, 0.46, r'$\mathcal{E}$', ha='right', va='center',
            fontsize=12)
    dblarrow(ax, 5.22, 0.02, 5.22, top + 0.06, lw=1.0)
    ax.text(5.10, yE + 0.04, r'$\mathcal{V}$', ha='right', va='center',
            fontsize=12)
    per, amp = 0.545, 0.55
    xa = np.linspace(0.30, x1, 700)
    ax.plot(xa, yE + amp * np.cos(2 * np.pi * (xa - x1) / per), 'k-', lw=1.25,
            zorder=5)
    xd = np.linspace(x1, x2, 200)
    ax.plot(xd, yE + amp * np.exp(-(xd - x1) / 0.28), 'k-', lw=1.25,
            zorder=5)
    xt = np.linspace(x2, 4.50, 700)
    ax.plot(xt, yE + 0.22 * np.cos(2 * np.pi * (xt - x2) / 0.52), 'k-',
            lw=1.25, zorder=5)
    for lx, lab in ((x1, r'$x_1$'), (x2, r'$x_2$')):
        ax.text(lx, -0.30, lab, ha='center', va='center', fontsize=12,
                bbox=dict(fc='white', ec='none', pad=1.2), zorder=6)
    arrow(ax, 4.30, -0.30, 4.88, -0.30, lw=1.0)
    ax.text(4.60, -0.52, r'$x$', ha='center', fontsize=12,
            bbox=dict(fc='white', ec='none', pad=1.0), zorder=6)
    save(fig, 115)


# ---------------------------------------------------------------- Fig. 116
def _panel116(ax, s, mode):
    ax.set_xlim(-2.55, 3.05)
    ax.set_ylim(-2.25, 1.62)
    ax.axis('off')
    xb = 0.35
    tilt = {'a': 0.0, 'b': 0.30, 'c': 0.45, 'd': 0.60}[mode]
    ax.plot([-xb, -xb], [-1.55, 1.30], 'k-', lw=1.1)
    ax.plot([xb, xb], [1.30 - tilt, -1.55], 'k-', lw=1.1)
    ax.plot([-xb, xb], [1.30, 1.30 - tilt], 'k-', lw=1.1)
    # n 侧
    ax.plot([-2.35, -xb], [0, 0], 'k-', lw=1.1)
    ax.plot([-xb, xb], [0, 0], 'k--', dashes=(4, 3), lw=0.9)
    for dx in (-2.05, -1.67, -1.29):
        ax.plot([dx], [0.05], 'ko', ms=4.2)
    ax.text(-1.67, 0.36, r'$n$-type', ha='center', fontsize=10)
    ax.plot([-2.35, -xb], [-0.85, -0.85], 'k-', lw=1.1)
    ax.add_patch(Rectangle((-2.35, -1.35), 2.0, 0.50, facecolor='white',
                           edgecolor='k', lw=0.8, hatch=HATCH, zorder=1))
    # p 侧
    ax.plot([xb, 2.25], [0.95 - s, 0.95 - s], 'k-', lw=1.1)
    ax.plot([xb, 2.25], [-s, -s], 'k--', dashes=(4, 3), lw=0.9)
    for dx in (0.78, 1.16, 1.54):
        ax.add_patch(Circle((dx, -s + 0.055), 0.052, facecolor='white',
                            edgecolor='k', lw=1.1, zorder=4))
    ax.plot([xb, 2.25], [-s - 0.48, -s - 0.48], 'k-', lw=1.1)
    ax.add_patch(Rectangle((xb, -s - 0.98), 1.9, 0.50, facecolor='white',
                           edgecolor='k', lw=0.8, hatch=HATCH, zorder=1))
    ax.text(1.10, -s - 0.26, r'$p$-type', ha='center', fontsize=10)
    if mode == 'a':
        ax.text(2.32, -0.02, 'Fermi\nlevel', ha='left', va='center',
                fontsize=9.5)
        arrow(ax, 0, -1.62, 0, -1.28, lw=1.0)
        ax.text(0, -1.80, 'Insulator', ha='center', fontsize=9.5)
    elif mode == 'b':
        ax.plot([xb, 1.30], [0, 0], 'k--', dashes=(4, 3), lw=0.9)
        arrow(ax, 1.30, 0, 1.48, 0, lw=0.9)
        ax.text(1.55, 0, 'Gap', ha='left', va='center', fontsize=10)
        dblarrow(ax, 0.45, -0.03, 0.45, -s + 0.01, lw=0.8, ms=4.5)
        ax.text(0.53, -s / 2 - 0.02, r'$V$', ha='left', va='center', fontsize=10.5)
    elif mode == 'c':
        ax.plot([-xb, 0.50], [0, 0], 'k--', dashes=(4, 3), lw=0.9)
        ax.plot([0.52], [0.02], 'ko', ms=4.2)
        yy = np.linspace(-0.02, -1.12, 200)
        wav = 0.52 + 0.05 * np.sin(2 * np.pi * (yy + 0.02) / 0.20)
        ax.plot(wav, yy, 'k-', lw=1.0, zorder=5)
        arrow(ax, 0.52, -1.00, 0.52, -1.16, lw=1.0)
        ax.text(0.70, -0.28, 'Phonons', ha='left', va='center', fontsize=9.5)
    elif mode == 'd':
        arrow(ax, -0.30, 0.02, 0.50, 0.02, lw=1.1)
        ax.plot([0.72], [0.02], 'ko', ms=4.2)
        dblarrow(ax, 0.58, -0.01, 0.58, -s, lw=0.9)
        ax.text(0.65, -s / 2, r'$V$', ha='left', va='center', fontsize=11)
    ax.text(-2.35, -1.98, r'$(%s)$' % mode, ha='left', fontsize=12)


def fig_116():
    fig = plt.figure(figsize=(4.8, 4.9))
    _panel116(fig.add_axes([0.015, 0.700, 0.475, 0.280]), 0.0, 'a')
    _panel116(fig.add_axes([0.510, 0.700, 0.475, 0.280]), 0.35, 'b')
    ax = fig.add_axes([0.16, 0.372, 0.66, 0.275])
    ax.set_xlim(-0.06, 1.10)
    ax.set_ylim(-0.10, 1.16)
    ax.axis('off')
    ax.plot([0, 0], [0, 1.08], 'k-', lw=1.1)
    ax.plot([0, 1.05], [0, 0], 'k-', lw=1.1)
    ax.text(-0.06, 0.55, 'Current', rotation=90, ha='right', va='center',
            fontsize=10)
    ax.text(1.02, -0.09, 'Voltage', ha='right', fontsize=10)
    vx = np.array([0, 0.05, 0.12, 0.20, 0.28, 0.33, 0.40, 0.48, 0.55, 0.62,
                   0.70, 0.80, 0.90, 0.97])
    vy = np.array([0, 0.10, 0.32, 0.55, 0.68, 0.70, 0.58, 0.36, 0.25, 0.27,
                   0.42, 0.68, 0.95, 1.08])
    xx = np.linspace(0, 0.97, 500)
    yy = PchipInterpolator(vx, vy)(xx)
    solid = PchipInterpolator(vx, vy)
    ax.plot(xx, yy, 'k-', lw=1.3, zorder=4)
    xd = np.linspace(0.335, 0.52, 100)
    ax.plot(xd, 0.685 * (1 - (xd - 0.335) / 0.185) ** 1.15, 'k--',
            dashes=(5, 3), lw=1.0)
    xe = np.array([0.545, 0.62, 0.70, 0.78, 0.845])
    ye = np.array([0.03, 0.09, 0.26, 0.52, 0.80])
    xq = np.linspace(0.545, 0.845, 200)
    ax.plot(xq, PchipInterpolator(xe, ye)(xq), 'k--', dashes=(5, 3), lw=1.0)
    ax.text(0.115, 0.47, r'$(a)$', ha='center', fontsize=12)
    ax.text(0.375, 0.32, r'$(b)$', ha='center', fontsize=12)
    ax.text(0.595, 0.105, r'$(c)$', ha='center', fontsize=12)
    ax.text(0.895, 0.80, r'$(d)$', ha='left', fontsize=12)
    _panel116(fig.add_axes([0.015, 0.020, 0.475, 0.280]), 0.60, 'c')
    _panel116(fig.add_axes([0.510, 0.020, 0.475, 0.280]), 0.85, 'd')
    save(fig, 116)


# ---------------------------------------------------------------- Fig. 117
def fig_117():
    fig = plt.figure(figsize=(4.8, 1.85))
    ax = fig.add_axes([0.005, 0.02, 0.99, 0.96])
    ax.set_xlim(-0.06, 4.42)
    ax.set_ylim(-1.05, 1.28)
    ax.axis('off')
    ext = [(0.10, 1.00), (1.20, 1.00), (2.15, -0.62), (2.58, 0.34),
           (3.00, -0.62), (3.44, 0.34), (3.85, -0.62), (4.42, 0.32)]
    cx, cy = [], []
    for (xa, ya), (xb, yb) in zip(ext[:-1], ext[1:]):
        t = np.linspace(0, 1, 80, endpoint=False)
        s = 0.5 * (1 - np.cos(np.pi * t))
        cx.append(xa + (xb - xa) * t)
        cy.append(ya + (yb - ya) * s)
    cx = np.append(np.array(cx), ext[-1][0])
    cy = np.append(np.array(cy), ext[-1][1])
    yF = 0.52
    ax.fill_between(cx, yF, cy, where=cy < yF, facecolor='white',
                    edgecolor='k', lw=0, hatch='---', zorder=1)
    ax.plot(cx, cy, 'k-', lw=1.3, zorder=3)
    i0 = np.argmax(cy < yF)
    ax.plot([cx[i0], 4.42], [yF, yF], 'k-', lw=1.3, zorder=4)
    ax.plot([1.25, 2.45], [1.0, 1.0], 'k--', dashes=(5, 3), lw=1.1, zorder=4)
    ax.plot([1.30, cx[i0]], [yF, yF], 'k--', dashes=(4, 3), lw=1.0, zorder=4)
    dblarrow(ax, 2.42, yF, 2.42, 1.0, lw=1.0)
    ax.text(2.33, 0.76, 'Work function', ha='right', va='center', fontsize=10)
    ax.text(3.30, 0.60, 'Fermi level', ha='left', va='center', fontsize=10)
    save(fig, 117)


# ---------------------------------------------------------------- Fig. 118
def fig_118():
    fig = plt.figure(figsize=(4.65, 1.9))
    ax = fig.add_axes([0.005, 0.02, 0.99, 0.96])
    ax.set_xlim(-0.15, 4.75)
    ax.set_ylim(-1.0, 1.52)
    ax.axis('off')
    E0 = 0.42
    xs = np.array([1.75, 1.80, 1.88, 1.98, 2.10, 2.24, 2.34])
    ys = np.array([0.05, -0.20, -0.40, -0.56, -0.68, -0.75, -0.78])
    sxx = PchipInterpolator(xs, ys)(np.linspace(xs[0], xs[-1], 100))
    poly = [(0.12, 1.25), (1.75, 1.25), (1.75, 0.05)]
    poly += list(np.stack([np.linspace(xs[0], xs[-1], 100), sxx], 1))
    poly += [(2.34, -0.92), (0.12, -0.92)]
    ax.add_patch(Polygon(poly, closed=True, facecolor='white', edgecolor='k',
                         lw=0, hatch=HATCH, zorder=1))
    ax.plot([0.12, 1.75, 1.75], [1.25, 1.25, 0.05], 'k-', lw=1.3, zorder=3)
    ax.plot(np.linspace(xs[0], xs[-1], 100), sxx, 'k-', lw=1.3, zorder=3)
    for xc in (2.66, 3.36, 4.06):
        xx = np.linspace(xc - 0.42, xc + 0.42, 200)
        yy = -0.92 + 0.77 * np.exp(-((xx - xc) / 0.215) ** 2)
        m = yy > -0.78
        poly2 = list(np.stack([xx[m], yy[m]], 1)) + [(xx[m][-1], -0.92),
                                                     (xx[m][0], -0.92)]
        ax.add_patch(Polygon(poly2, closed=True, facecolor='white',
                             edgecolor='k', lw=0, hatch=HATCH, zorder=1))
        ax.plot(xx[m], yy[m], 'k-', lw=1.3, zorder=3)
    arrow(ax, 0.38, E0, 4.46, E0, lw=1.0)
    ax.plot([0.38, 4.40], [E0, E0], 'k--', dashes=(6, 4), lw=1.0, zorder=4)
    ax.text(0.30, E0, r'$\mathcal{E}_0$', ha='right', va='center',
            fontsize=12)
    ax.text(4.52, E0 - 0.13, r'$z$', ha='left', va='center', fontsize=11)
    xout = np.linspace(0.55, 1.75, 300)
    yout = E0 + 0.33 * np.exp((xout - 1.75) / 0.17)
    xin = np.linspace(1.75, 4.42, 1100)
    Ain = 0.60 * np.exp(-(xin - 1.75) / 1.3)
    yin = E0 + Ain * np.cos(2 * np.pi * (xin - 1.75) / 0.42 - 0.9)
    ax.plot(xout, yout, 'k-', lw=1.25, zorder=5)
    ax.plot(xin, yin, 'k-', lw=1.25, zorder=5)
    ax.text(2.90, 1.04, r'$\psi_0(z)$', ha='center', fontsize=12)
    save(fig, 118)


if __name__ == '__main__':
    for f in (fig_97, fig_98, fig_99, fig_100, fig_101, fig_112, fig_113,
              fig_114, fig_115, fig_116, fig_117, fig_118):
        f()
