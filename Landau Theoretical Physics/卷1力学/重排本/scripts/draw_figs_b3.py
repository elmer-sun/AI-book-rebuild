# -*- coding: utf-8 -*-
"""
朗道《力学》重排本插图重绘 批次 B3：图28–图42（黑白教材风矢量图）。
运行后在 figures/ 生成 figN.pdf，figures/preview/ 生成 figN.png。
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Arc, Polygon

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, '..', 'figures')
PREV = os.path.join(OUT, 'preview')
os.makedirs(PREV, exist_ok=True)


# ---------------- 公共小工具 ----------------
def new_ax(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + '.pdf'), bbox_inches='tight',
                pad_inches=0.03)
    fig.savefig(os.path.join(PREV, name + '.png'), dpi=150,
                bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


def arrow(ax, x0, y0, x1, y1, lw=1.2, ms=9):
    """自绘箭头（-|> 实心）"""
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def atom(ax, x, y, r, filled=True, lw=1.0):
    ax.add_patch(Circle((x, y), r, fc='k' if filled else 'w', ec='k',
                        lw=lw, zorder=5))


def seg(ax, x0, y0, x1, y1, lw=1.2, ls='-'):
    ax.plot([x0, x1], [y0, y1], 'k-', lw=lw, ls=ls)


def cr(P, n=30):
    """Catmull-Rom 样条，过点 P (N,2)，平滑采样"""
    P = np.asarray(P, float)
    if len(P) < 3:
        return P
    pts = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    t = np.linspace(0, 1, n, endpoint=False)[:, None]
    for i in range(1, len(pts) - 2):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[i + 1], pts[i + 2]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                          + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    out.append(P[-1][None, :])
    return np.vstack(out)


def hatch_line(ax, x0, x1, y0, y=0, d=0.11, sp=0.14, lw=0.8):
    """地面斜短线（图40）"""
    xs = np.arange(x0, x1 + 1e-9, sp)
    for x in xs:
        seg(ax, x, y, x - d, y - d, lw=lw)


def hatch_arc(ax, cx, cy, r, a0, a1, d=0.16, n=46, lw=0.8):
    """沿圆弧外侧斜短线（图41）"""
    for a in np.linspace(a0, a1, n):
        ca, sa = np.cos(a), np.sin(a)
        x, y = cx + r * ca, cy + r * sa
        nx, ny = ca, sa                      # 外法向
        th = -np.pi / 4                       # 顺时针转45°
        dx = nx * np.cos(th) - ny * np.sin(th)
        dy = nx * np.sin(th) + ny * np.cos(th)
        seg(ax, x, y, x + d * dx, y + d * dy, lw=lw)


# ---------------- 图 28 (p088) 分子 ABA 纵向/横向振动 ----------------
def fig_28():
    fig, ax = new_ax(3.2, 2.75)
    ax.set_xlim(-0.15, 3.45)
    ax.set_ylim(0.05, 5.0)
    xl, xc, xr = 0.5, 1.5, 2.5
    r = 0.055

    # 顶部：平衡位形  3(A)---2(B)---1(A)
    seg(ax, xl, 4.2, xr, 4.2, lw=1.2)
    atom(ax, xl, 4.2, r, True); atom(ax, xc, 4.2, r, False); atom(ax, xr, 4.2, r, True)
    ax.text(xl, 4.42, '3', ha='center', fontsize=10)
    ax.text(xc, 4.42, '2', ha='center', fontsize=10)
    ax.text(xr, 4.42, '1', ha='center', fontsize=10)
    ax.text(1.0, 4.42, '$l$', ha='center', fontsize=10)
    ax.text(2.0, 4.42, '$l$', ha='center', fontsize=10)
    ax.text(xl - 0.02, 3.90, '$A$', ha='center', fontsize=10)
    ax.text(xc, 3.90, '$B$', ha='center', fontsize=10)
    ax.text(xr + 0.02, 3.90, '$A$', ha='center', fontsize=10)

    def row(y, tag):
        seg(ax, xl, y, xr, y, lw=1.2)
        atom(ax, xl, y, r, True); atom(ax, xc, y, r, False); atom(ax, xr, y, r, True)
        ax.text(3.12, y - 0.03, '$%s$' % tag, fontsize=10)

    # a：反对称 x1=x3（左、右原子同向右，B 向左）
    row(3.0, 'a')
    arrow(ax, xl + r, 3.0, 0.75, 3.0, lw=1.1, ms=11)
    arrow(ax, xc - r, 3.0, 1.25, 3.0, lw=1.1, ms=11)
    arrow(ax, xr + r, 3.0, 2.85, 3.0, lw=1.1, ms=11)

    # b：对称 x1=-x3（两 A 原子反向，B 不动）
    row(2.0, 'b')
    arrow(ax, xl - r, 2.0, 0.18, 2.0, lw=1.1, ms=11)
    arrow(ax, xr + r, 2.0, 2.82, 2.0, lw=1.1, ms=11)

    # c：对称弯曲（B 向上，两 A 向下）
    row(1.0, 'c')
    arrow(ax, xl, 1.0 - r, 0.5, 0.52, lw=1.1, ms=11)
    arrow(ax, xc, 1.0 + r, 1.5, 1.48, lw=1.1, ms=11)
    arrow(ax, xr, 1.0 - r, 2.5, 0.52, lw=1.1, ms=11)
    save(fig, 'fig28')


# ---------------- 图 29 (p089) 三角形分子 ABA ----------------
def _v_molecule(ax, ox, oy, tag=None, arrows=None):
    """V 形分子；arrows=(angL,angC,angR) 度，None 则不画"""
    bl, br = 157.0, 27.0
    L = 1.0
    xl, yl = ox + L * np.cos(np.radians(bl)), oy + L * np.sin(np.radians(bl))
    xr, yr = ox + L * np.cos(np.radians(br)), oy + L * np.sin(np.radians(br))
    seg(ax, ox, oy, xl, yl, lw=1.2)
    seg(ax, ox, oy, xr, yr, lw=1.2)
    atom(ax, ox, oy, 0.05, False)
    atom(ax, xl, yl, 0.055, True)
    atom(ax, xr, yr, 0.055, True)
    if arrows:
        aL, aC, aR, lA = arrows
        arrow(ax, xl, yl, xl + lA * np.cos(np.radians(aL)),
              yl + lA * np.sin(np.radians(aL)), lw=1.0, ms=8)
        arrow(ax, xr, yr, xr + lA * np.cos(np.radians(aR)),
              yr + lA * np.sin(np.radians(aR)), lw=1.0, ms=8)
        arrow(ax, ox, oy, ox + 0.42 * np.cos(np.radians(aC)),
              oy + 0.42 * np.sin(np.radians(aC)), lw=1.0, ms=8)
    if tag:
        ax.text(1.72, oy + 0.25, '$%s$' % tag, fontsize=10)


def fig_29():
    fig, ax = new_ax(3.15, 4.0)
    ax.set_xlim(-2.1, 3.1)
    ax.set_ylim(-3.90, 1.75)

    # 顶部：三角形分子与坐标轴
    ox, oy = 0.0, 0.0
    _v_molecule(ax, ox, oy)
    seg(ax, -1.9, 0, 2.72, 0, lw=0.8, ls='--')
    seg(ax, 0, 0, 0, 1.36, lw=0.8, ls='--')
    ax.text(2.83, -0.06, '$X$', fontsize=10)
    ax.text(0.17, 1.28, '$Y$', fontsize=10)
    ax.add_patch(Arc((0, 0), 1.06, 1.06, theta1=27, theta2=157, lw=0.8))
    ax.text(0.28, 0.47, r'$2\alpha$', fontsize=10)
    ax.text(-0.99, 0.56, '$A$', fontsize=10)
    ax.text(-0.94, 0.16, '3', fontsize=10)
    ax.text(0.94, 0.60, '$A$', fontsize=10)
    ax.text(0.94, 0.28, '1', fontsize=10)
    ax.text(0.09, 0.12, '2', fontsize=10)
    ax.text(-0.02, -0.30, '$B$', fontsize=10)

    # a：相对 Y 轴反对称 (x1=x3, y1=-y3)
    _v_molecule(ax, 0, -1.02, 'a', arrows=(295, 180, 38, 0.46))
    # b：相对 Y 轴对称 (x1=-x3, y1=y3)，高频型
    _v_molecule(ax, 0, -2.10, 'b', arrows=(295, 90, 245, 0.46))
    # c：相对 Y 轴对称，弯曲型
    _v_molecule(ax, 0, -3.18, 'c', arrows=(228, 90, 312, 0.46))
    save(fig, 'fig29')


# ---------------- 图 30 (p090) 线性非对称分子 ABC ----------------
def fig_30():
    fig, ax = new_ax(3.0, 0.75)
    ax.set_xlim(-0.2, 3.25)
    ax.set_ylim(-0.55, 0.85)
    xl, xc, xr = 0.5, 1.75, 3.0
    seg(ax, xl, 0, xr, 0, lw=1.2)
    atom(ax, xl, 0, 0.06, True)
    atom(ax, xc, 0, 0.06, False)
    atom(ax, xr, 0, 0.06, False)
    ax.text(xl, 0.24, '3', ha='center', fontsize=10)
    ax.text(xc, 0.24, '2', ha='center', fontsize=10)
    ax.text(xr, 0.24, '1', ha='center', fontsize=10)
    ax.text(1.12, 0.24, '$l_2$', ha='center', fontsize=10)
    ax.text(2.37, 0.24, '$l_1$', ha='center', fontsize=10)
    ax.text(xl, -0.34, '$C$', ha='center', fontsize=10)
    ax.text(xc, -0.34, '$B$', ha='center', fontsize=10)
    ax.text(xr, -0.34, '$A$', ha='center', fontsize=10)
    save(fig, 'fig30')


# ---------------- 图 31 (p095) 色散曲线 I(eps) ----------------
def fig_31():
    fig, ax = new_ax(3.3, 2.25)
    ax.set_xlim(-2.72, 2.95)
    ax.set_ylim(-0.42, 1.62)

    seg(ax, -2.55, 0, 2.75, 0, lw=1.0)              # 横轴
    seg(ax, 0, 0, 0, 1.42, lw=1.0)                  # 纵轴（过峰顶向上）
    e = np.linspace(-2.55, 2.75, 400)
    ax.plot(e, 1.0 / (1.0 + e * e), 'k-', lw=1.3)   # I/I(0)
    # 半高度虚线与 ±lambda 虚线
    seg(ax, -1.0, 0.5, 1.0, 0.5, lw=0.8, ls='--')
    seg(ax, -1.0, 0.5, -1.0, 0, lw=0.8, ls='--')
    seg(ax, 1.0, 0.5, 1.0, 0, lw=0.8, ls='--')
    ax.text(0.06, 1.30, r'$I/I(0)$', fontsize=10)
    ax.text(0.07, 1.03, '1', fontsize=10)
    ax.text(0.07, 0.56, '1/2', fontsize=10)
    ax.text(-1.0, -0.36, r'$-\lambda$', ha='center', fontsize=10)
    ax.text(0.0, -0.36, '0', ha='center', fontsize=10)
    ax.text(1.0, -0.36, r'$\lambda$', ha='center', fontsize=10)
    ax.text(2.78, -0.10, r'$\varepsilon$', fontsize=10)
    save(fig, 'fig31')


# ---------------- 图 32 (p104) 非线性共振振幅曲线 (a)(b)(c) ----------------
def _ax32(ax, eps_lab=True):
    seg(ax, -1.42, 0, 1.42, 0, lw=1.0)
    seg(ax, 0, 0, 0, 1.13, lw=1.0)
    ax.text(0.07, 1.06, '$b$', fontsize=10)
    if eps_lab:
        ax.text(1.47, -0.06, r'$\varepsilon$', fontsize=10)


def fig_32():
    fig = plt.figure(figsize=(3.35, 4.75))
    axs = [fig.add_axes([0, 1 - (i + 1) / 3 + 0.012, 1, 1 / 3 - 0.024])
           for i in range(3)]
    for ax in axs:
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_xlim(-1.62, 1.62)
        ax.set_ylim(-0.20, 1.30)

    # (a) f->0：对称钟形曲线
    ax = axs[0]
    _ax32(ax)
    x = np.linspace(-1.0, 1.0, 300)
    y = 0.75 / (1.0 + (x / 0.44) ** 2)
    ax.plot(x, y, 'k-', lw=1.3)
    ax.text(0.42, 0.90, r'$f\rightarrow 0$', fontsize=10)
    ax.text(1.38, 0.62, '$a$', fontsize=10)

    # (b) f<fk：峰移向正 eps
    ax = axs[1]
    _ax32(ax)
    pts = [(-1.02, 0.028), (-0.84, 0.05), (-0.62, 0.09), (-0.42, 0.155),
           (-0.24, 0.25), (-0.10, 0.36), (0.02, 0.475), (0.13, 0.58),
           (0.23, 0.665), (0.32, 0.72), (0.38, 0.744), (0.45, 0.735),
           (0.53, 0.69), (0.62, 0.615), (0.72, 0.50), (0.82, 0.36),
           (0.92, 0.22), (1.02, 0.10), (1.10, 0.035), (1.15, 0.012)]
    ax.plot(cr(pts)[:, 0], cr(pts)[:, 1], 'k-', lw=1.3)
    ax.text(0.60, 0.86, r'$f<f_k$', fontsize=10)
    ax.text(1.38, 0.55, '$b$', fontsize=10)

    # (c) f>fk：S 形曲线，不稳定段虚线
    ax = axs[2]
    _ax32(ax)
    main = [(-1.16, 0.086), (-0.92, 0.10), (-0.68, 0.135), (-0.45, 0.20),
            (-0.24, 0.29), (-0.05, 0.39), (0.14, 0.50), (0.32, 0.60),
            (0.46, 0.665), (0.56, 0.70), (0.66, 0.742), (0.75, 0.775),
            (0.82, 0.79), (0.875, 0.78), (0.905, 0.73), (0.918, 0.645)]
    ax.plot(cr(main)[:, 0], cr(main)[:, 1], 'k-', lw=1.3)
    mid = [(0.918, 0.645), (0.895, 0.61), (0.85, 0.565), (0.78, 0.51),
           (0.70, 0.445), (0.63, 0.385), (0.585, 0.345), (0.562, 0.315)]
    ax.plot(cr(mid)[:, 0], cr(mid)[:, 1], 'k--', lw=1.3)
    low = [(0.562, 0.315), (0.568, 0.25), (0.595, 0.185), (0.65, 0.135),
           (0.73, 0.10), (0.82, 0.088), (0.918, 0.086), (1.0, 0.075),
           (1.09, 0.062), (1.16, 0.05)]
    ax.plot(cr(low)[:, 0], cr(low)[:, 1], 'k-', lw=1.3)
    seg(ax, 0.562, 0.66, 0.562, 0.33, lw=0.8, ls='--')   # B->D
    seg(ax, 0.918, 0.62, 0.918, 0.10, lw=0.8, ls='--')   # C->E
    ax.text(-1.16, 0.17, '$A$', fontsize=10)
    ax.text(0.46, 0.79, '$B$', fontsize=10)
    ax.text(0.97, 0.68, '$C$', fontsize=10)
    ax.text(0.42, 0.32, '$D$', fontsize=10)
    ax.text(0.97, 0.13, '$E$', fontsize=10)
    ax.text(1.20, 0.10, '$F$', fontsize=10)
    ax.text(0.62, 0.99, r'$f>f_k$', fontsize=10)
    ax.text(1.38, 0.55, '$c$', fontsize=10)
    save(fig, 'fig32')


# ---------------- 图 33 (p107) 结合共振 b(eps) ----------------
def fig_33():
    fig, ax = new_ax(3.3, 2.05)
    ax.set_xlim(-2.95, 3.55)
    ax.set_ylim(-0.55, 1.55)

    seg(ax, -2.5, 0, 3.05, 0, lw=1.0)
    seg(ax, 0, 0, 0, 1.05, lw=1.0)
    seg(ax, -1.06, 0, 1.0, 0, lw=0.8, ls='--')      # BC 段 b=0 不稳定
    be = [(-1.06, 0.0), (-1.02, 0.13), (-0.96, 0.25), (-0.86, 0.36),
          (-0.72, 0.44), (-0.52, 0.50), (-0.28, 0.535), (0.0, 0.555),
          (0.3, 0.59), (0.6, 0.615), (0.95, 0.645), (1.3, 0.665),
          (1.7, 0.678), (2.1, 0.685), (2.42, 0.688)]
    ax.plot(cr(be)[:, 0], cr(be)[:, 1], 'k-', lw=1.3)
    cf = [(1.0, 0.0), (1.04, 0.055), (1.12, 0.10), (1.24, 0.135),
          (1.42, 0.16), (1.65, 0.178), (1.95, 0.188), (2.25, 0.191)]
    ax.plot(cr(cf)[:, 0], cr(cf)[:, 1], 'k--', lw=1.3)
    ax.text(0.10, 0.97, '$b$', fontsize=10)
    ax.text(3.13, -0.10, r'$\varepsilon$', fontsize=10)
    ax.text(-2.4, -0.30, '$A$', fontsize=10)
    ax.text(-1.10, -0.30, '$B$', fontsize=10)
    ax.text(0.94, -0.30, '$C$', fontsize=10)
    ax.text(1.88, -0.30, '$D$', fontsize=10)
    ax.text(2.52, 0.63, '$E$', fontsize=10)
    ax.text(2.38, 0.14, '$F$', fontsize=10)
    save(fig, 'fig33')


# ---------------- 图 34 (p108) 三次谐波共振 b(eps) ----------------
def fig_34():
    fig, ax = new_ax(3.0, 2.1)
    ax.set_xlim(-1.35, 1.55)
    ax.set_ylim(-0.28, 1.42)

    seg(ax, -1.05, 0, 1.05, 0, lw=1.0)
    seg(ax, 0, 0, 0, 1.08, lw=1.0)
    up = [(0.30, 0.457), (0.315, 0.55), (0.36, 0.66), (0.43, 0.75),
          (0.52, 0.815), (0.62, 0.85), (0.72, 0.868), (0.81, 0.875)]
    ax.plot(cr(up)[:, 0], cr(up)[:, 1], 'k-', lw=1.3)
    dn = [(0.30, 0.457), (0.345, 0.415), (0.42, 0.388), (0.52, 0.385),
          (0.63, 0.40), (0.74, 0.44), (0.84, 0.515)]
    ax.plot(cr(dn)[:, 0], cr(dn)[:, 1], 'k--', lw=1.3)
    ax.text(-0.16, 1.0, '$b$', fontsize=10)
    ax.text(1.10, -0.10, r'$\varepsilon$', fontsize=10)
    ax.text(0.20, 0.43, '$A$', ha='right', fontsize=10)
    ax.text(0.87, 0.87, '$B$', fontsize=10)
    ax.text(0.90, 0.49, '$C$', fontsize=10)
    save(fig, 'fig34')


# ---------------- 图 35 (p112) 固定系 XYZ 与动系 x1x2x3 ----------------
def fig_35():
    fig, ax = new_ax(3.2, 2.6)
    ax.set_xlim(-1.35, 3.15)
    ax.set_ylim(-0.85, 2.75)

    O = np.array([0.0, 0.0])
    Op = np.array([1.23, 1.11])
    P = np.array([1.21, 1.59])

    # 固定坐标系
    arrow(ax, 0, 0, 0, 2.43, lw=1.0, ms=10)
    arrow(ax, 0, 0, 2.45, 0, lw=1.0, ms=10)
    arrow(ax, 0, 0, -0.70, -0.43, lw=1.0, ms=10)
    ax.text(-0.17, 2.35, '$Z$', fontsize=11)
    ax.text(2.56, -0.13, '$Y$', fontsize=11)
    ax.text(-0.93, -0.56, '$X$', fontsize=11)
    ax.text(-0.02, -0.30, '$O$', fontsize=11)

    # 刚体（不规则"土豆"）
    t = np.linspace(0, 2 * np.pi, 400)
    rr = 1 + 0.13 * np.cos(2 * t - 0.6) + 0.07 * np.cos(3 * t + 1.2) \
        + 0.05 * np.cos(5 * t + 0.4)
    bx = 1.23 + 0.44 * rr * np.cos(t)
    by = 1.30 + 0.60 * rr * np.sin(t)
    ax.plot(bx, by, 'k-', lw=1.3)

    # 动坐标系
    arrow(ax, Op[0], Op[1], 0.72, 2.03, lw=1.0, ms=10)
    arrow(ax, Op[0], Op[1], 2.08, 1.60, lw=1.0, ms=10)
    arrow(ax, Op[0], Op[1], 1.04, 0.47, lw=1.0, ms=10)
    ax.text(0.62, 2.12, '$x_3$', fontsize=11)
    ax.text(2.16, 1.55, '$x_2$', fontsize=11)
    ax.text(0.97, 0.22, '$x_1$', fontsize=11)
    ax.text(Op[0] + 0.16, Op[1] - 0.10, "$O'$", fontsize=11)

    # 矢量 R, r, tau（粗黑斜体）
    arrow(ax, 0, 0, Op[0], Op[1], lw=1.6, ms=11)
    arrow(ax, 0, 0, P[0], P[1], lw=1.6, ms=11)
    arrow(ax, Op[0], Op[1], P[0], P[1], lw=1.6, ms=11)
    ax.text(0.80, 0.36, r'$\boldsymbol{R}$', fontsize=11)
    ax.text(0.44, 0.85, r'$\boldsymbol{\tau}$', fontsize=11)
    ax.text(1.34, 1.30, r'$\boldsymbol{r}$', fontsize=11)
    save(fig, 'fig35')


# ---------------- 图 36 (p117) 等腰三角形分子 ----------------
def fig_36():
    fig, ax = new_ax(2.7, 2.15)
    ax.set_xlim(-1.55, 1.65)
    ax.set_ylim(-0.55, 1.55)

    ax.plot([-0.92, 0.92, 0, -0.92], [0, 0, 1, 0], 'k-', lw=1.4)
    atom(ax, 0, 1, 0.055, False)
    atom(ax, -0.92, 0, 0.055, False)
    atom(ax, 0.92, 0, 0.055, False)
    seg(ax, 0, 1.38, 0, -0.42, lw=0.8, ls='--')      # x2 轴
    seg(ax, -1.35, 0.33, 1.42, 0.33, lw=0.8, ls='--')  # x1 轴
    ax.text(0.10, 1.32, '$x_2$', fontsize=11)
    ax.text(0.86, 0.20, '$x_1$', fontsize=11)
    ax.text(0.10, 0.43, '$h$', fontsize=11)
    ax.text(-0.12, -0.36, '$a$', fontsize=11)
    ax.text(0.13, 1.00, '$m_2$', fontsize=11)
    ax.text(-0.90, -0.30, '$m_1$', ha='center', fontsize=11)
    ax.text(0.94, -0.30, '$m_1$', ha='center', fontsize=11)
    save(fig, 'fig36')


# ---------------- 图 37 (p117) 正三棱锥 4 原子分子 ----------------
def fig_37():
    fig, ax = new_ax(2.2, 2.7)
    ax.set_xlim(-1.30, 1.40)
    ax.set_ylim(-0.62, 2.32)

    A = (0.0, 1.94)          # m2 顶点
    Bk = (0.0, 0.53)         # 后 m1
    Fl = (-0.79, 0.0)        # 前 left m1
    Fr = (0.81, 0.0)         # 前 right m1
    seg(ax, *A, *Fl, lw=1.4); seg(ax, *A, *Fr, lw=1.4)
    seg(ax, *Fl, *Fr, lw=1.4)
    seg(ax, *A, *Bk, lw=0.8); seg(ax, *Bk, *Fl, lw=0.8); seg(ax, *Bk, *Fr, lw=0.8)
    atom(ax, *A, 0.05, False)
    atom(ax, *Bk, 0.05, False)
    atom(ax, *Fl, 0.05, False)
    atom(ax, *Fr, 0.05, False)
    ax.text(0.04, 2.08, '$m_2$', fontsize=11)
    ax.text(0.09, 0.54, '$m_1$', fontsize=11)
    ax.text(-0.81, -0.34, '$m_1$', ha='center', fontsize=11)
    ax.text(0.85, -0.34, '$m_1$', ha='center', fontsize=11)
    ax.text(-0.44, 0.40, '$a$', fontsize=11)
    ax.text(0.42, 0.39, '$a$', fontsize=11)
    ax.text(0.0, 0.13, '$a$', ha='center', fontsize=11)
    save(fig, 'fig37')


# ---------------- 图 38 (p118) 圆锥体的两组坐标轴 ----------------
def fig_38():
    fig, ax = new_ax(2.8, 3.3)
    ax.set_xlim(-1.75, 1.85)
    ax.set_ylim(-0.95, 3.35)

    h, rb, yc = 2.2, 0.86, 2.2
    # 锥面轮廓（两条素线）与底椭圆
    seg(ax, 0, 0, -rb, yc, lw=1.4)
    seg(ax, 0, 0, rb, yc, lw=1.4)
    t = np.linspace(0, 2 * np.pi, 200)
    ax.plot(rb * np.cos(t), yc + 0.28 * np.sin(t), 'k-', lw=1.4)
    # x3 / x3' 轴（锥内虚线，锥外实线）
    seg(ax, 0, 0, 0, yc + 0.28, lw=1.0, ls='--')
    seg(ax, 0, yc + 0.28, 0, 2.92, lw=1.0)
    arrow(ax, 0, 2.92, 0, 3.02, lw=1.0, ms=10)
    ax.text(-0.34, 2.92, '$x_3$', fontsize=11)
    ax.text(0.17, 2.92, "$x_3'$", fontsize=11)
    # x2 轴（过质心 O，锥内虚线）
    seg(ax, -1.17, 1.65, -rb * 0.75, 1.65, lw=1.0)
    seg(ax, -rb * 0.75, 1.65, 0, 1.65, lw=1.0, ls='--')
    arrow(ax, 0, 1.65, 1.32, 1.65, lw=1.0, ms=10)
    ax.text(1.38, 1.50, '$x_2$', fontsize=11)
    # x1 轴（过 O；反向延长为虚线）
    arrow(ax, 0, 1.65, -1.05, 1.13, lw=1.0, ms=10)
    seg(ax, 0, 1.65, 1.12, 2.15, lw=0.9, ls='--')
    ax.text(-1.28, 1.02, '$x_1$', fontsize=11)
    # O' 系
    seg(ax, -1.09, 0, 1.18, 0, lw=1.0)
    arrow(ax, 1.0, 0, 1.18, 0, lw=1.0, ms=10)
    arrow(ax, 0, 0, -1.0, -0.50, lw=1.0, ms=10)
    ax.text(1.30, -0.24, "$x_2'$", fontsize=11)
    ax.text(-1.25, -0.62, "$x_1'$", fontsize=11)
    ax.text(-0.20, 1.76, '$O$', fontsize=11)
    ax.text(0.06, -0.30, "$O'$", fontsize=11)
    save(fig, 'fig38')


# ---------------- 图 39 (p119) 双杆辛亥 OA-AB ----------------
def _rod(ax, p0, p1, w=0.05):
    """双线描细杆（圆头）"""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    d = d / np.linalg.norm(d)
    n = np.array([-d[1], d[0]]) * w
    ax.add_patch(Polygon([p0 + n, p1 + n, p1 - n, p0 - n], closed=True,
                         fc='w', ec='k', lw=1.2, zorder=4,
                         joinstyle='round', capstyle='round'))


def fig_39():
    fig, ax = new_ax(3.05, 2.2)
    ax.set_xlim(-0.45, 2.95)
    ax.set_ylim(-0.55, 2.05)

    phi = np.radians(49)
    A = (np.cos(phi), np.sin(phi))
    B = (2 * np.cos(phi), 0)
    seg(ax, -0.02, 0, 2.55, 0, lw=0.8, ls='--')
    seg(ax, 0, 0, 0, 1.72, lw=0.8, ls='--')
    _rod(ax, (0, 0), A)
    _rod(ax, A, B)
    ax.add_patch(Arc((0, 0), 0.50, 0.50, theta1=0, theta2=49, lw=0.8))
    ax.text(0.34, 0.16, r'$\varphi$', fontsize=11)
    ax.text(0.26, 0.46, '$l$', fontsize=11)
    ax.text(1.07, 0.46, '$l$', fontsize=11)
    ax.text(0.62, 0.93, '$A$', fontsize=11)
    ax.text(-0.17, -0.24, '$O$', fontsize=11)
    ax.text(B[0] - 0.03, -0.28, '$B$', ha='center', fontsize=11)
    ax.text(2.44, -0.26, '$x$', fontsize=11)
    ax.text(-0.20, 1.62, '$y$', fontsize=11)
    save(fig, 'fig39')


# ---------------- 图 40 (p119) 平面上滚动的圆柱 ----------------
def fig_40():
    fig, ax = new_ax(2.9, 2.75)
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-0.75, 2.25)

    ax.add_patch(Circle((0, 1), 1.0, fc='none', ec='k', lw=1.4))
    seg(ax, -1.5, 0, 1.5, 0, lw=1.2)
    hatch_line(ax, -1.42, 1.44, -1.5, y=0, d=0.11, sp=0.15)
    # 中心->切点（R），中心->质心 P（a），P->切点
    seg(ax, 0, 1, 0, 0, lw=0.9)
    ang = np.radians(216)          # 质心方位（自 +x 轴）
    P = np.array([0.47 * np.cos(ang), 1 + 0.47 * np.sin(ang)])
    seg(ax, 0, 1, P[0], P[1], lw=0.9)
    seg(ax, P[0], P[1], 0, 0, lw=0.9)
    ax.text(0.09, 0.52, '$R$', fontsize=11)
    ax.text(-0.27, 0.93, '$a$', fontsize=11)
    ax.add_patch(Arc((0, 1), 0.56, 0.56, theta1=216, theta2=270, lw=0.8))
    ax.text(-0.16, 0.655, r'$\varphi$', fontsize=11)
    save(fig, 'fig40')


# ---------------- 图 41 (p120) 圆柱内滚动于圆柱形曲面 ----------------
def fig_41():
    fig, ax = new_ax(3.3, 1.95)
    ax.set_xlim(-1.62, 1.85)
    ax.set_ylim(-1.72, 0.42)

    R, a = 1.0, 0.275
    contact = np.radians(208)
    C = (R - a) * np.array([np.cos(contact), np.sin(contact)])
    # 大圆弧碗（略过半圆）+ 外侧阴影
    th = np.linspace(np.radians(183), np.radians(357), 300)
    ax.plot(np.cos(th), np.sin(th), 'k-', lw=1.4)
    hatch_arc(ax, 0, 0, 1.0, np.radians(185), np.radians(355), d=0.17, n=48)
    # 小圆柱
    ax.add_patch(Circle(C, a, fc='none', ec='k', lw=1.4))
    # 中心竖直虚线
    seg(ax, 0, 0, 0, -1.0, lw=0.9, ls='--')
    # a 箭头（大头圆心方向，止于小圆边缘）
    u = C / np.linalg.norm(C)
    arrow(ax, 0, 0, *(C - a * u), lw=1.0, ms=10)
    # R 箭头
    aR = np.radians(-39)
    arrow(ax, 0, 0, 0.97 * np.cos(aR), 0.97 * np.sin(aR), lw=1.0, ms=10)
    # phi 弧
    ax.add_patch(Arc((0, 0), 0.60, 0.60, theta1=208, theta2=270, lw=0.8))
    ax.text(-0.19, -0.23, r'$\varphi$', fontsize=11)
    ax.text(-0.60, -0.24, '$a$', fontsize=11)
    ax.text(0.40, -0.18, '$R$', fontsize=11)
    save(fig, 'fig41')


# ---------------- 图 42 (p120) 平面上滚动的匀质圆锥 ----------------
def fig_42():
    fig, ax = new_ax(3.4, 2.1)
    ax.set_xlim(-1.15, 2.75)
    ax.set_ylim(-0.75, 1.25)

    # 坐标系
    arrow(ax, 0, 0, 0, 0.92, lw=1.0, ms=10)
    arrow(ax, 0, 0, -0.52, -0.27, lw=1.0, ms=10)
    ax.text(0.06, 0.85, '$Z$', fontsize=11)
    ax.text(-0.62, -0.20, '$X$', fontsize=11)
    # Y 轴：锥内点划线，锥外实线
    seg(ax, 0, 0, 1.49, 0, lw=0.9, ls=(0, (6, 3, 1, 3)))
    arrow(ax, 1.49, 0, 2.0, 0, lw=1.0, ms=10)
    ax.text(2.08, -0.09, '$Y$', fontsize=11)
    # 圆锥：底椭圆（略倾斜）+ 两条轮廓线
    base = np.array([1.37, 0.05])
    tilt = np.radians(7)
    tt = np.linspace(0, 2 * np.pi, 200)
    ex = base[0] + 0.33 * np.sin(tt) * np.cos(tilt)
    ey = base[1] + 0.33 * np.cos(tt) * np.sin(tilt) \
        + 0.115 * np.cos(tt) * np.cos(tilt)
    # 椭圆参数化：长轴近似竖直
    ex = base[0] + 0.115 * np.cos(tt) * np.cos(tilt) \
        - 0.33 * np.sin(tt) * np.sin(tilt)
    ey = base[1] + 0.115 * np.cos(tt) * np.sin(tilt) \
        + 0.33 * np.sin(tt) * np.cos(tilt)
    # 上、下轮廓端点取椭圆上最左的两点附近
    ax.plot([0, ex[ np.argmax(ey) ]], [0, ey[np.argmax(ey)]], 'k-', lw=1.4)
    ax.plot([0, ex[ np.argmin(ey) ]], [0, ey[np.argmin(ey)]], 'k-', lw=1.4)
    ax.plot(ex, ey, 'k-', lw=1.4)
    # 锥轴（虚线 + 中部箭头 a）及其延长
    ax.plot([0, base[0]], [0, base[1]], 'k--', lw=0.9)
    arrow(ax, 0, 0, 1.02, 0.043, lw=0.9, ms=9)
    seg(ax, base[0], base[1], 1.72, 0.075, lw=0.8)
    ax.text(0.70, 0.10, '$a$', fontsize=11)
    # theta 弧（X 与 Y 之间）
    ax.add_patch(Arc((0, 0), 0.76, 0.76, theta1=207, theta2=352, lw=0.8))
    ax.text(0.02, -0.50, r'$\theta$', fontsize=11)
    # A：底圆最低点
    iA = np.argmin(ey)
    ax.text(ex[iA] - 0.06, ey[iA] - 0.28, '$A$', fontsize=11)
    ax.text(-0.24, 0.06, '$O$', fontsize=11)
    save(fig, 'fig42')


if __name__ == '__main__':
    import sys
    todo = sys.argv[1:] or ['28', '29', '30', '31', '32', '33', '34',
                            '35', '36', '37', '38', '39', '40', '41', '42']
    for k in todo:
        globals()['fig_' + k]()
        print('fig' + k, 'ok')
