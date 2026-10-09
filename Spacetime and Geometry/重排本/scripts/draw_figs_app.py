# -*- coding: utf-8 -*-
"""
《时空与几何》(Carroll, Spacetime and Geometry) 中文重排工程
附录插图重绘：E.1, H.1-H.5, I.1  黑白教材风矢量图
产物: figures/fig_{key}.pdf + figures/preview/fig_{key}.png
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

FIGDIR = r'E:\AI整理书籍\卡罗尔\重排本\figures'
PREV = os.path.join(FIGDIR, 'preview')
os.makedirs(PREV, exist_ok=True)

GRAY = '0.55'


# ---------------- 通用小工具 ----------------

def save(fig, key):
    fig.savefig(os.path.join(FIGDIR, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV, 'fig_%s.png' % key),
                dpi=300, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


def arr(ax, p0, p1, lw=1.1, ms=8, color='k', style='-|>', zorder=5):
    """带箭头的线段（轴线用）"""
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, linewidth=lw,
                                color=color, mutation_scale=ms),
                zorder=zorder)


def qbez(p0, m, p1, n=100):
    """二次 Bezier：过端点 p0,p1 与指定中点 m（控制曲线鼓出量最直观）"""
    p0, m, p1 = map(lambda p: np.asarray(p, float), (p0, m, p1))
    c = 2 * m - (p0 + p1) / 2.0
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * p0 + 2 * t * (1 - t) * c + t ** 2 * p1


def cbez(p0, c0, c1, p1, n=100):
    """三次 Bezier"""
    p0, c0, c1, p1 = map(lambda p: np.asarray(p, float), (p0, c0, c1, p1))
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 3 * p0 + 3 * t * (1 - t) ** 2 * c0
            + 3 * t ** 2 * (1 - t) * c1 + t ** 3 * p1)


def hourglass(ax, cx, cy, hw, hh, zorder=4):
    """小光锥（沙漏）图标：上锥浅灰、下锥深灰"""
    ax.add_patch(Polygon([(cx, cy), (cx - hw, cy + hh), (cx + hw, cy + hh)],
                         closed=True, facecolor='0.82', edgecolor='k',
                         lw=0.7, zorder=zorder))
    ax.add_patch(Polygon([(cx, cy), (cx - hw, cy - hh), (cx + hw, cy - hh)],
                         closed=True, facecolor='0.55', edgecolor='k',
                         lw=0.7, zorder=zorder))


# ---------------- 图 E.1  (书页 456 / p471) ----------------

def fig_E_1():
    fig, ax = plt.subplots(figsize=(3.3, 3.4))
    ax.set_aspect('equal')
    ax.axis('off')

    d = (1.05, -0.68)        # 斜投影深度向量（陡斜样式，同原书）
    sep = 1.05               # 两张类空面之间的竖直间隔
    A1 = np.array([0.2, 1.35])            # 顶面左角
    A2 = A1 + (1.8, 1.27)
    A3 = A1 + (2.85, 0.59)
    A4 = A1 + d
    B1 = A1 - (0, sep)
    B2, B3, B4 = A2 - (0, sep), A3 - (0, sep), A4 - (0, sep)

    top = Polygon([A1, A2, A3, A4], closed=True, facecolor='0.66',
                  alpha=0.82, edgecolor='k', lw=1.0, zorder=2)
    bot = Polygon([B1, B2, B3, B4], closed=True, facecolor='0.66',
                  alpha=0.82, edgecolor='k', lw=1.0, zorder=2)
    ax.add_patch(top)
    ax.add_patch(bot)
    # 连接两个超曲面的（类时）竖直棱
    for p, q in [(A1, B1), (A2, B2), (A3, B3), (A4, B4)]:
        ax.plot([p[0], q[0]], [p[1], q[1]], color='k', lw=1.0, zorder=3)

    ax.text(2.35, 1.90, r'$\Sigma_2$', fontsize=12, ha='center', zorder=4)
    ax.text(2.35, 0.72, r'$\Sigma_1$', fontsize=12, ha='center', zorder=4)
    ax.text(0.62, 0.75, r'$R$', fontsize=12, ha='center', zorder=4)

    ax.set_xlim(-0.15, 3.55)
    ax.set_ylim(-0.85, 2.95)
    save(fig, 'E.1')


# ---------------- 图 H.1  (书页 472 / p487) ----------------

def fig_H_1():
    fig, ax = plt.subplots(figsize=(3.6, 2.6))
    xa, xb = -2.45, 2.45
    x = np.linspace(xa, xb, 400)
    y = np.arctan(2.2 * x)
    ax.plot(x, y, color='k', lw=1.7, zorder=4)

    for y0 in (np.pi / 2, -np.pi / 2):
        ax.plot([xa, xb], [y0, y0], color='k', lw=1.0, ls=(0, (5, 3)), zorder=2)

    arr(ax, (0, -2.85), (0, 3.85))                 # 竖轴（原书纵轴上下大幅延伸）
    arr(ax, (xa, 0), (2.75, 0))                    # 横轴
    ax.text(0.16, 3.62, r'arctan $x$', ha='left', va='center', fontsize=11)
    ax.text(2.72, -0.30, r'$x$', ha='center', fontsize=12)
    ax.text(0.12, 2.22, r'$\dfrac{\pi}{2}$', ha='left', va='center')
    ax.text(0.12, -2.28, r'$-\dfrac{\pi}{2}$', ha='left', va='center')

    ax.set_xlim(-2.75, 3.0)
    ax.set_ylim(-3.05, 4.2)
    ax.axis('off')
    save(fig, 'H.1')


# ---------------- 图 H.2  (书页 473 / p488) ----------------

def fig_H_2():
    fig, ax = plt.subplots(figsize=(2.9, 4.0))
    ax.set_aspect('equal')
    ax.axis('off')

    arr(ax, (0, -3.8), (0, 3.9))                   # t 轴
    arr(ax, (-0.35, 0), (6.1, 0))                  # r 轴
    ax.text(0.18, 3.75, r'$t$', ha='left', fontsize=12)
    ax.text(5.95, -0.45, r'$r$', ha='center', fontsize=12)

    # u = constant（灰、斜率 +1，自 t 轴向右上）
    for u, ln in [(-0.2, 4.0), (-1.3, 4.4), (-2.4, 4.4), (-3.5, 4.3)]:
        ax.plot([0, ln], [u, u + ln], color=GRAY, lw=1.1, zorder=2)
    # v = constant（黑、斜率 -1，自 t 轴向右下）
    for v0, ln in [(2.4, 4.2), (1.2, 4.15), (-0.9, 3.55), (-2.1, 2.85)]:
        ax.plot([0, ln], [v0, v0 - ln], color='k', lw=1.4, zorder=3)

    ax.text(4.15, 3.95, r'$u=\mathrm{constant}$', ha='left', fontsize=11)
    ax.text(4.05, -3.40, r'$v=\mathrm{constant}$', ha='left', fontsize=11)

    ax.set_xlim(-0.65, 6.6)
    ax.set_ylim(-5.3, 4.5)
    save(fig, 'H.2')


# ---------------- 图 H.3  (书页 475 / p490) ----------------

def fig_H_3():
    fig, ax = plt.subplots(figsize=(3.4, 3.05))
    ax.set_aspect('equal')
    ax.axis('off')

    a = 0.85          # 圆柱半径（半宽）
    ry = 0.20         # 椭圆半短轴
    yb, yt = 0.45, 2.55          # 下、上椭圆中心高
    x0 = -0.31        # R = 0 母线
    xd = 0.26         # R = pi 虚线母线
    th = np.linspace(0, 2 * np.pi, 200)

    # ---- 阴影区（Minkowski 区，沙漏形）----
    A = (x0, 2.01)    # T = pi
    B = (x0, 0.95)    # T = -pi
    C = (xd, 1.52)    # 腰点（T = 0, R = pi）
    D = (-a, 1.52)    # 左轮廓
    x0v = x0
    AR = cbez(A, (x0v, 1.70), (0.90, 1.62), C)
    BR = cbez(B, (x0v, 1.32), (0.88, 1.40), C)
    AL = cbez(A, (x0v, 1.72), (-0.88, 1.66), D)
    BL = cbez(B, (x0v, 1.30), (-0.88, 1.38), D)
    poly = np.vstack([AR, BR[::-1], BL, AL[::-1]])
    ax.add_patch(Polygon(poly, closed=True, facecolor='0.84',
                         edgecolor='none', zorder=2))
    ax.plot(AR[:, 0], AR[:, 1], 'k-', lw=1.2, zorder=3)
    ax.plot(BR[:, 0], BR[:, 1], 'k-', lw=1.2, zorder=3)
    ax.plot(AL[:, 0], AL[:, 1], 'k-', lw=1.2, zorder=3)
    ax.plot(BL[:, 0], BL[:, 1], 'k-', lw=1.2, zorder=3)
    # 背面重叠的深灰透镜带（虚线为圆柱背面）
    Dup, Ddn = (-a, 1.62), (-a, 1.42)
    LT = qbez(Dup, (-0.25, 1.635), C)
    LB = qbez(Ddn, (-0.25, 1.405), C)
    ax.add_patch(Polygon(np.vstack([LT, LB[::-1]]), closed=True,
                         facecolor='0.58', edgecolor='none', zorder=2.5))
    ax.plot(LT[:, 0], LT[:, 1], 'k--', lw=0.9, dashes=(4, 3), zorder=3)
    ax.plot(LB[:, 0], LB[:, 1], 'k--', lw=0.9, dashes=(4, 3), zorder=3)

    # ---- 圆柱轮廓 ----
    ax.plot(a * np.cos(th), yb + ry * np.sin(th), 'k-', lw=1.1, zorder=4)
    ax.plot(a * np.cos(th), yt + ry * np.sin(th), 'k-', lw=1.1, zorder=4)
    ax.plot([-a, -a], [yb, yt], 'k-', lw=1.1, zorder=4)
    ax.plot([a, a], [yb, yt], 'k-', lw=1.1, zorder=4)
    # R = 0 实线母线 与 R = pi 虚线母线
    ax.plot([x0, x0], [yb + 0.19, yt - 0.19], 'k-', lw=1.0, zorder=3.5)
    ax.plot([xd, xd], [yb + 0.20, yt + 0.19], 'k--', lw=0.9,
            dashes=(4, 3), zorder=3.5)

    # ---- 点与标注 ----
    dot = dict(ms=3.6, color='k', zorder=6)
    for p in [A, B, C, (x0, yt - ry * np.sqrt(1 - (x0 / a) ** 2)),
              (xd, yt - ry * np.sqrt(1 - (xd / a) ** 2))]:
        ax.plot(p[0], p[1], 'o', **dot)
    ax.text(0.18, 2.60, r'$R=0$', ha='right', fontsize=11, zorder=6)
    ax.text(0.42, 2.88, r'$R=\pi$', ha='left', fontsize=11, zorder=6)
    ax.text(-0.22, 2.09, r'$T=\pi$', ha='left', fontsize=11, zorder=6)
    ax.text(-0.20, 0.87, r'$T=-\pi$', ha='left', fontsize=11, zorder=6)

    # T 方向灰箭头
    arr(ax, (-1.18, 1.05), (-1.18, 2.05), lw=3.0, ms=22, color=GRAY)
    ax.text(-1.18, 2.20, r'$T$', ha='center', fontsize=12, color=GRAY)

    ax.set_xlim(-1.60, 1.80)
    ax.set_ylim(0.05, 3.10)
    save(fig, 'H.3')


# ---------------- 图 H.4  (书页 475 / p490) ----------------

def fig_H_4():
    fig, ax = plt.subplots(figsize=(3.9, 3.7))
    ax.set_aspect('equal')
    ax.axis('off')

    ip, im = (0, 1.65), (0, -1.65)     # i+, i-
    i0 = (1.7, 0.0)
    H = 1.65

    # ---- 类光无穷远 I±（外边界，向右鼓出）----
    SIp = qbez(ip, (1.02, 1.16), i0)
    SIm = qbez(im, (1.02, -1.16), i0)
    ax.plot(SIp[:, 0], SIp[:, 1], 'k-', lw=1.3, zorder=3)
    ax.plot(SIm[:, 0], SIm[:, 1], 'k-', lw=1.3, zorder=3)

    # ---- t = constant 线（自 R=0 轴出发，缓降汇入 i0）----
    for y0 in (0.64 * H, 0.31 * H):
        cu = qbez((0, y0), (0.85, 0.44 * y0), i0)
        cl = qbez((0, -y0), (0.85, -0.44 * y0), i0)
        ax.plot(cu[:, 0], cu[:, 1], 'k-', lw=0.9, zorder=2)
        ax.plot(cl[:, 0], cl[:, 1], 'k-', lw=0.9, zorder=2)
    ax.plot([0, i0[0]], [0, i0[1]], 'k-', lw=0.9, zorder=2)   # t = 0

    # ---- r = constant 世界线（i- 到 i+，向右鼓出的弧）----
    arcs = []
    for cx in (0.65, 1.36):
        arc = cbez(im, (cx, -0.75), (cx, 0.75), ip)
        arcs.append(arc)
        ax.plot(arc[:, 0], arc[:, 1], 'k-', lw=0.9, zorder=2)

    # ---- R = 0 边界 ----
    ax.plot([0, 0], [im[1], ip[1]], 'k-', lw=1.3, zorder=3)

    # ---- 光锥小图标（骑在内侧 r=const 弧上）----
    hourglass(ax, 0.50, 0.66, 0.15, 0.30)

    # ---- 点与标注 ----
    dot = dict(ms=3.6, color='k', zorder=6)
    for p in (ip, im, i0):
        ax.plot(p[0], p[1], 'o', **dot)
    ax.text(0, 1.80, r'$i^{+}$', ha='center', fontsize=12)
    ax.text(0, -1.90, r'$i^{-}$', ha='center', fontsize=12)
    ax.text(1.79, 0.03, r'$i^{0}$', ha='left', fontsize=12)
    ax.text(1.10, 1.02, r'$\mathcal{I}^{+}$', ha='left', fontsize=12)
    ax.text(1.10, -1.10, r'$\mathcal{I}^{-}$', ha='left', fontsize=12)

    # R = 0 引线标注
    ax.text(-0.16, 0.56, r'$R=0$', ha='right', fontsize=11)
    ax.plot([-0.13, 0.0], [0.62, 0.76], 'k-', lw=0.7)

    # t / r = constant 引线标注（原书位于图外右下角）
    tgt_t = qbez((0, -0.64 * H), (0.85, -0.44 * 0.64 * H), i0)
    tgt_t = tgt_t[int(0.32 * len(tgt_t))]
    tgt_r = arcs[0][int(0.26 * len(arcs[0]))]
    ax.text(0.85, -1.28, r'$t=\mathrm{constant}$', ha='left', fontsize=11)
    ax.plot([0.83, tgt_t[0]], [-1.22, tgt_t[1]], 'k-', lw=0.7)
    ax.text(0.85, -1.55, r'$r=\mathrm{constant}$', ha='left', fontsize=11)
    ax.plot([0.83, tgt_r[0]], [-1.49, tgt_r[1]], 'k-', lw=0.7)

    # ---- 左侧小坐标系（T,t / R,r）----
    arr(ax, (-1.85, -0.55), (-1.85, 0.55), ms=7)
    arr(ax, (-2.00, -0.38), (-0.72, -0.38), ms=7)
    ax.text(-1.76, 0.48, r'$T,t$', ha='left', fontsize=11)
    ax.text(-0.95, -0.56, r'$R,r$', ha='center', fontsize=11)

    ax.set_xlim(-2.25, 2.80)
    ax.set_ylim(-2.05, 2.0)
    save(fig, 'H.4')


# ---------------- 图 H.5  (书页 478 / p493) ----------------

def fig_H_5():
    fig, ax = plt.subplots(figsize=(3.8, 2.85))
    ax.set_aspect('equal')
    ax.axis('off')

    ip, i0 = (0, 1.7), (1.7, 0.0)

    # 奇点 T = 0（底边虚线）与 R = 0 左边线
    ax.plot([0, i0[0]], [0, 0], 'k--', lw=1.1, dashes=(5, 3), zorder=3)
    ax.plot([0, 0], [0, ip[1]], 'k-', lw=1.3, zorder=3)

    # I+ 外边界
    SIp = qbez(ip, (0.93, 0.95), i0)
    ax.plot(SIp[:, 0], SIp[:, 1], 'k-', lw=1.3, zorder=3)

    # 共动世界线（r = const，自奇点竖直出发，汇入 i+）
    for xa, c1x in [(0.49, 0.44), (0.99, 0.88)]:
        wl = cbez((xa, 0), (xa, 0.50), (c1x, 1.16), ip)
        ax.plot(wl[:, 0], wl[:, 1], 'k-', lw=1.0, zorder=2)

    # t = constant 线（自 R=0 出发缓降汇入 i0）
    for y0 in (0.62 * 1.7, 0.30 * 1.7):
        cu = qbez((0, y0), (0.85, 0.46 * y0), i0)
        ax.plot(cu[:, 0], cu[:, 1], 'k-', lw=0.9, zorder=2)

    # 光锥小图标
    hourglass(ax, 0.44, 0.20, 0.13, 0.15)
    hourglass(ax, 1.07, 0.20, 0.13, 0.15)

    # 点与标注
    dot = dict(ms=3.6, color='k', zorder=6)
    for p in (ip, i0):
        ax.plot(p[0], p[1], 'o', **dot)
    ax.text(0, 1.80, r'$i^{+}$', ha='center', fontsize=12)
    ax.text(1.79, 0.02, r'$i^{0}$', ha='left', fontsize=12)
    ax.text(0.71, -0.14, r'$i^{-}$', ha='center', fontsize=12)
    ax.text(1.06, 0.93, r'$\mathcal{I}^{+}$', ha='left', fontsize=12)

    # 左侧小坐标系
    arr(ax, (-0.80, -0.42), (-0.80, 0.58), ms=7)
    arr(ax, (-1.02, -0.32), (0.05, -0.32), ms=7)
    ax.text(-0.70, 0.52, r'$T$', ha='left', fontsize=12)
    ax.text(0.10, -0.48, r'$R$', ha='left', fontsize=12)

    ax.set_xlim(-1.15, 2.05)
    ax.set_ylim(-0.60, 1.95)
    save(fig, 'H.5')


# ---------------- 图 I.1  (书页 480 / p495) ----------------

def fig_I_1():
    fig = plt.figure(figsize=(4.8, 1.75))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 1.35, 2.0],
                          left=0.02, right=0.98, top=0.96, bottom=0.04,
                          wspace=0.25)

    # ---- n = 1 ----
    ax = fig.add_subplot(gs[0])
    ax.set_aspect('equal')
    ax.axis('off')
    ax.plot([0, 1.7], [0, 0], 'k-', lw=1.6, zorder=3)
    for x in (0, 1.7):
        ax.plot(x, 0, 'ko', ms=3.4, zorder=4)
    ax.text(1.70, -0.30, r'$\eta_1$', ha='center', fontsize=11)
    ax.set_xlim(-0.35, 2.15)
    ax.set_ylim(-0.62, 0.50)

    # ---- n = 2 ----
    ax = fig.add_subplot(gs[1])
    ax.set_aspect('equal')
    ax.axis('off')
    tri = Polygon([(0, 0), (0, 1), (1, 1)], closed=True,
                  facecolor='0.78', edgecolor='k', lw=1.2, zorder=3)
    ax.add_patch(tri)
    ax.plot([1, 1], [0, 1], 'k--', lw=0.9, dashes=(4, 3), zorder=2)
    for p in [(0, 0), (0, 1), (1, 1), (1, 0)]:
        ax.plot(*p, 'ko', ms=3.2, zorder=4)
    arr(ax, (0, -0.12), (0, 1.42))
    arr(ax, (-0.14, 0), (1.5, 0))
    ax.text(0.08, 1.36, r'$\eta_2$', ha='left', fontsize=11)
    ax.text(1.46, -0.18, r'$\eta_1$', ha='center', fontsize=11)
    ax.set_xlim(-0.4, 1.8)
    ax.set_ylim(-0.42, 1.6)

    # ---- n = 3 ----
    ax = fig.add_subplot(gs[2])
    ax.set_aspect('equal')
    ax.axis('off')
    e1 = np.array([-0.66, -0.75])   # eta1：陡峭的左下方向
    e2 = np.array([1.0, -0.30])     # eta2：略向右下
    e3 = np.array([0.0, 1.0])

    def P(x, y, z):
        return x * e1 + y * e2 + z * e3

    # 虚线立方体
    O, X, Y, Z = P(0, 0, 0), P(0, 1, 0), P(1, 0, 0), P(0, 0, 1)
    XZ = P(0, 1, 1)
    YZ = P(1, 0, 1)
    XY = P(1, 1, 0)
    XYZ = P(1, 1, 1)
    edges = [(O, X), (X, XY), (XY, Y), (Y, O),
             (Z, XZ), (XZ, XYZ), (XYZ, YZ), (YZ, Z),
             (O, Z), (X, XZ), (Y, YZ), (XY, XYZ)]
    for pq, q in edges:
        ax.plot([pq[0], q[0]], [pq[1], q[1]], 'k--', lw=0.8,
                dashes=(3, 2.5), zorder=2)
    # 单纯形（四面体）：可见的两面浅灰，背面留白
    T0, T1, T2, T3 = O, Z, XZ, XYZ
    ax.add_patch(Polygon([T1, T2, T3], closed=True, facecolor='0.80',
                         edgecolor='none', zorder=2.5))
    ax.add_patch(Polygon([T0, T2, T3], closed=True, facecolor='0.80',
                         edgecolor='none', zorder=2.5))
    for pp, q in [(T0, T1), (T0, T2), (T0, T3), (T1, T2), (T1, T3), (T2, T3)]:
        ax.plot([pp[0], q[0]], [pp[1], q[1]], 'k-', lw=1.2, zorder=3)
    for pp in (T0, T1, T2, T3):
        ax.plot(pp[0], pp[1], 'o', ms=3.4, color='k', zorder=4)
    # 坐标轴（沿盒三条棱方向）
    arr(ax, (0, -0.05), (0, 1.50))
    arr(ax, (0, 0), 1.55 * e2)
    arr(ax, (0, 0), 1.40 * e1)
    ax.text(0.08, 1.40, r'$\eta_3$', ha='left', fontsize=11)
    ax.text(1.55 * e2[0] + 0.05, 1.55 * e2[1] - 0.18, r'$\eta_2$',
            ha='center', fontsize=11)
    ax.text(1.40 * e1[0] - 0.04, 1.40 * e1[1] - 0.16, r'$\eta_1$',
            ha='center', fontsize=11)
    ax.set_xlim(-1.25, 1.95)
    ax.set_ylim(-1.45, 1.70)

    save(fig, 'I.1')


# ---------------- 主循环 ----------------

if __name__ == '__main__':
    for f in (fig_E_1, fig_H_1, fig_H_2, fig_H_3, fig_H_4, fig_H_5, fig_I_1):
        f()
        print('done:', f.__name__)
