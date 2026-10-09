# -*- coding: utf-8 -*-
"""
《时空与几何》(Carroll, Spacetime and Geometry) 第 7 章插图重绘
黑白教材风矢量图, matplotlib Agg 后端。
产物: figures/fig_7.1.pdf ... fig_7.12.pdf  (+ figures/preview/fig_7.*.png 自检图)
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Ellipse, FancyArrowPatch, Polygon, Arc, Circle, PathPatch, Rectangle
from matplotlib.path import Path
import numpy as np

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

OUT = r'E:\AI整理书籍\卡罗尔\重排本\figures'
PRE = os.path.join(OUT, 'preview')
os.makedirs(PRE, exist_ok=True)

GRAY = '0.62'          # 粗灰箭头 (微分同胚弧线)
GRAYC = '0.60'         # 辅助灰曲线


def savefig(fig, key):
    fig.savefig(os.path.join(OUT, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRE, 'fig_%s.png' % key),
                bbox_inches='tight', pad_inches=0.03, dpi=150)
    plt.close(fig)


def arrow(ax, p0, p1, lw=1.1, head=11, color='k', style='-|>'):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle=style, lw=lw,
                                 color=color, mutation_scale=head,
                                 shrinkA=0, shrinkB=0, zorder=5))


def axes_xy(ax, ox, oy, xlen, ylen, ylow=0.35):
    """原书风格: 两条带箭头的坐标轴 (y 轴略向下伸出)."""
    arrow(ax, (ox, oy - ylow), (ox, oy + ylen), lw=1.1)
    arrow(ax, (ox, oy), (ox + xlen, oy), lw=1.1)
    ax.text(ox + 0.22, oy + ylen + 0.05, '$y$', fontsize=12)
    ax.text(ox + xlen + 0.18, oy - 0.28, '$x$', fontsize=12)


def eye(ax, cx, cy, w, ang=0.0, pupil=+0.10):
    """简笔眼睛: 杏仁形轮廓 + 瞳孔 (pupil: 瞳孔沿轴偏移, 正=朝注视方向)."""
    a = np.radians(ang)
    ca, sa = np.cos(a), np.sin(a)

    def R(x, y):
        return (cx + x * ca - y * sa, cy + x * sa + y * ca)

    t1, t2 = R(-w / 2, 0), R(w / 2, 0)
    cu, cd = R(0, 0.30 * w), R(0, -0.30 * w)
    verts = [t1, cu, t2, cd, t1]
    codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3,
             Path.CURVE3, Path.CURVE3]
    path = Path(verts, codes)
    ax.add_patch(PathPatch(path, fill=False, lw=0.9, edgecolor='k'))
    px, py = R(pupil * w / 2, 0)
    ax.add_patch(Circle((px, py), 0.085 * w + 0.02, facecolor='k',
                        edgecolor='none', zorder=6))


# ---------------------------------------------------------------- fig 7.1 --
def fig_7_1():
    """微分同胚 phi 联系背景流形 M_b 与物理流形 M_p."""
    fig, ax = plt.subplots(figsize=(3.6, 2.0))
    ax.set_xlim(0, 10.4); ax.set_ylim(0, 5.6)
    ax.set_aspect('equal'); ax.axis('off')

    ax.add_patch(Ellipse((2.75, 2.6), 3.1, 1.95, fill=False, lw=1.2))
    ax.text(2.75, 3.02, r'$\eta_{\mu\nu}$', ha='center', fontsize=12)
    ax.text(2.75, 2.16, r'$(\phi^* g)_{\mu\nu}$', ha='center', fontsize=12)
    ax.text(0.78, 2.72, r'$M_b$', ha='center', fontsize=12)

    ax.add_patch(Ellipse((7.55, 2.6), 2.8, 1.9, fill=False, lw=1.2))
    ax.text(7.55, 2.45, r'$g_{\alpha\beta}$', ha='center', fontsize=12)
    ax.text(9.45, 3.1, r'$M_p$', ha='center', fontsize=12)

    # 上弧: phi, 左 -> 右
    ax.add_patch(FancyArrowPatch((3.6, 3.95), (6.9, 4.0),
                                 connectionstyle='arc3,rad=0.32',
                                 arrowstyle='-|>', lw=4.5, color=GRAY,
                                 mutation_scale=22))
    ax.text(5.2, 4.85, r'$\phi$', ha='center', fontsize=13)
    # 下弧: phi*, 右 -> 左
    ax.add_patch(FancyArrowPatch((6.9, 1.25), (3.6, 1.3),
                                 connectionstyle='arc3,rad=0.32',
                                 arrowstyle='-|>', lw=4.5, color=GRAY,
                                 mutation_scale=22))
    ax.text(5.2, 0.18, r'$\phi^*$', ha='center', fontsize=13)
    savefig(fig, '7.1')


# ---------------------------------------------------------------- fig 7.2 --
def fig_7_2():
    """单参数微分同胚族 psi_eps, 由背景时空上的矢量场 xi^mu 生成."""
    fig, ax = plt.subplots(figsize=(3.8, 1.9))
    ax.set_xlim(-1.2, 10.4); ax.set_ylim(-0.2, 5.2)
    ax.set_aspect('equal'); ax.axis('off')

    ax.add_patch(Ellipse((3.0, 2.35), 3.0, 1.75, fill=False, lw=1.2))
    ax.text(2.25, 3.85, r'$M_b$', ha='center', fontsize=12)
    ax.add_patch(Ellipse((7.7, 2.35), 2.7, 1.7, fill=False, lw=1.2))
    ax.text(9.35, 2.85, r'$M_p$', ha='center', fontsize=12)

    # 椭圆内的三枚小箭头 (矢量场 xi^mu)
    arrow(ax, (2.0, 2.45), (2.9, 2.76), lw=0.9, head=9)
    arrow(ax, (2.0, 2.35), (2.97, 2.35), lw=0.9, head=9)
    arrow(ax, (2.0, 2.25), (2.9, 1.94), lw=0.9, head=9)
    ax.text(3.5, 2.32, r'$\xi^\mu$', ha='center', fontsize=12)

    # psi_eps 循环弧 (绕椭圆左侧约 285 度, 开口朝右)
    cx, cy, r = 0.78, 2.35, 1.28
    th = np.radians(np.linspace(320.0, -285.0, 240))   # 递减: 320 -> -285(=35)
    ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), color=GRAY, lw=4.0,
            solid_capstyle='butt', zorder=4)
    th1, th2 = np.radians(55.0), np.radians(36.0)
    ax.add_patch(FancyArrowPatch((cx + r * np.cos(th1), cy + r * np.sin(th1)),
                                 (cx + r * np.cos(th2), cy + r * np.sin(th2)),
                                 arrowstyle='-|>', lw=4.0, color=GRAY,
                                 mutation_scale=22, zorder=4))
    ax.text(0.52, 2.42, r'$\psi_\epsilon$', ha='center', fontsize=12)

    # 上弧 (phi o psi_eps): 左 -> 右
    ax.add_patch(FancyArrowPatch((3.9, 3.4), (7.0, 3.45),
                                 connectionstyle='arc3,rad=0.32',
                                 arrowstyle='-|>', lw=4.5, color=GRAY,
                                 mutation_scale=22))
    ax.text(5.45, 4.45, r'$(\phi \circ \psi_\epsilon)$', ha='center',
            fontsize=12)
    # 下弧 (phi o psi_eps)*: 右 -> 左
    ax.add_patch(FancyArrowPatch((7.0, 1.2), (3.95, 1.15),
                                 connectionstyle='arc3,rad=0.32',
                                 arrowstyle='-|>', lw=4.5, color=GRAY,
                                 mutation_scale=22))
    ax.text(5.45, 0.02, r'$(\phi \circ \psi_\epsilon)^*$', ha='center',
            fontsize=12)
    savefig(fig, '7.2')


# ---------------------------------------------------------------- fig 7.3 --
def fig_7_3():
    """偏折测地线 x^mu(lambda) 分解为背景测地线与微扰."""
    fig, ax = plt.subplots(figsize=(4.8, 2.4))
    ax.set_xlim(-3.3, 3.3); ax.set_ylim(-1.75, 1.5)
    ax.set_aspect('equal'); ax.axis('off')

    x0, x1, h = -2.4, 2.45, 0.55
    L = x1 - x0
    # 背景测地线 (虚线直线)
    ax.plot([x0, x1], [0.03, 0.02], 'k--', dashes=(5, 3.5), lw=1.0)
    # 真实路径 x^mu(lambda)
    xx = np.linspace(x0, x1, 300)
    yy = h * np.sin(np.pi * (xx - x0) / L)
    ax.plot(xx, yy, 'k-', lw=1.4)

    # 渐近切线 (细线, 交成 X, 标出偏折角 alpha-hat)
    mt = 0.25
    over = 0.55
    xc = 0.5 * (x0 + x1) + 0.02
    yc = 0.02 + mt * (xc - x0)
    ax.plot([x0 - 0.1, xc + over], [0.02 - mt * 0.1, yc + mt * over],
            'k-', lw=0.7)
    ax.plot([xc - over, x1 + 0.1], [yc - mt * over, 0.02 + mt * 0.1],
            'k-', lw=0.7)
    ang = np.degrees(np.arctan(mt))
    ax.add_patch(Arc((xc, yc), 1.0, 1.0, angle=0,
                     theta1=180 - ang, theta2=180 + ang, lw=0.8))
    ax.text(xc - 0.80, yc - 0.03, r'$\hat\alpha$', ha='center', fontsize=12)

    # 发射体 (左) 与观测者眼睛 (右)
    ax.add_patch(Circle((-2.56, 0.03), 0.12, facecolor='0.75',
                        edgecolor='k', lw=0.8))
    eye(ax, 2.72, 0.02, 0.62, ang=0.0, pupil=-0.12)

    # 微扰位移 x^(1)mu
    xa = 0.62
    ya = h * np.sin(np.pi * (xa - x0) / L)
    arrow(ax, (xa, 0.04), (xa, ya - 0.03), lw=0.9, head=9)
    ax.text(xa + 0.13, 0.20, r'$x^{(1)\mu}$', ha='left', fontsize=9.5)
    ax.text(0.95, 0.70, r'$x^\mu(\lambda)$', ha='left', fontsize=11)
    ax.text(1.78, -0.22, r'$x^{(0)\mu}$', ha='left', fontsize=11)

    # 撞击参数 b 与质量 M
    arrow(ax, (0.02, -0.04), (0.02, -0.92), lw=0.9, head=10, style='<|-|>')
    ax.text(-0.14, -0.52, r'$b$', ha='right', fontsize=12)
    ax.add_patch(Circle((0.02, -1.25), 0.32, facecolor='0.8',
                        edgecolor='k', lw=0.9))
    ax.text(-0.44, -1.02, r'$M$', ha='center', fontsize=12)
    savefig(fig, '7.3')


# ------------------------------------------------- 环形粒子序列 (7.4-7.6) --
def _ring_axes(ax, ox, n_rings, xmax):
    axes_xy(ax, ox, -2.6, 4.8, 4.3, ylow=0.7)
    ax.set_xlim(-0.1, xmax)
    ax.set_ylim(-3.7, 2.6)
    ax.set_aspect('equal')
    ax.axis('off')


def _draw_ring(ax, cxy, X, Y):
    """闭合多边形 (穿过 12 个粒子) + 粒子点 + 中心点."""
    Xc = np.concatenate([X, X[:1]]); Yc = np.concatenate([Y, Y[:1]])
    ax.plot(cxy[0] + Xc, cxy[1] + Yc, 'k-', lw=1.2)
    ax.plot(cxy[0] + X, cxy[1] + Y, 'ko', ms=4, mew=0)
    ax.plot([cxy[0]], [cxy[1]], 'ko', ms=4, mew=0)


def fig_7_4():
    """+ 偏振: 圆环粒子振荡 (圆-纵椭圆-圆-横椭圆-...)."""
    fig, ax = plt.subplots(figsize=(4.8, 1.6))
    R = 1.0
    th = np.radians(np.arange(12) * 30)
    c0, s0 = np.cos(th), np.sin(th)
    seq = [(0, 0), (-1, 0.85), (0, 0), (1, 0.68), (0, 0), (-1, 0.85), (0, 0)]
    centers = [2.3 + 2.75 * k for k in range(7)]
    _ring_axes(ax, 0.6, 7, 19.4)
    for cx, (s, A) in zip(centers, seq):
        X = R * c0 * (1 + 0.5 * A * s)
        Y = R * s0 * (1 - 0.5 * A * s)
        _draw_ring(ax, (cx, 0.0), X, Y)
    savefig(fig, '7.4')


def fig_7_5():
    """x 偏振: 圆环粒子振荡 (圆-+45度椭圆-圆--45度椭圆-...)."""
    fig, ax = plt.subplots(figsize=(4.8, 1.6))
    R, A = 1.0, 0.8
    th = np.radians(np.arange(12) * 30)
    c0, s0 = np.cos(th), np.sin(th)
    seq = [0, 1, 0, -1, 0, 1, 0]
    centers = [2.3 + 2.75 * k for k in range(7)]
    _ring_axes(ax, 0.6, 7, 19.4)
    for cx, s in zip(centers, seq):
        X = R * (c0 + 0.5 * A * s * s0)
        Y = R * (s0 + 0.5 * A * s * c0)
        _draw_ring(ax, (cx, 0.0), X, Y)
    savefig(fig, '7.5')


def fig_7_6():
    """R 偏振: 恒定椭率的椭圆连续旋转 (右手)."""
    fig, ax = plt.subplots(figsize=(4.3, 1.68))
    a, b = 1.38, 0.72
    orients = [90, 45, 0, -45, 90, 45]          # 长轴方位角 (度)
    centers = [2.3 + 2.75 * k for k in range(6)]
    _ring_axes(ax, 0.6, 6, 17.0)
    tt = np.linspace(0, 2 * np.pi, 200)
    td = np.radians(np.arange(8) * 45)
    for cx, phi in zip(centers, orients):
        p = np.radians(phi)

        def rot(x, y):
            return (x * np.cos(p) - y * np.sin(p),
                    x * np.sin(p) + y * np.cos(p))
        Xe, Ye = rot(a * np.cos(tt), b * np.sin(tt))
        ax.plot(cx + Xe, Ye, 'k-', lw=1.2)
        Xd, Yd = rot(a * np.cos(td), b * np.sin(td))
        ax.plot(cx + Xd, Yd, 'ko', ms=4, mew=0)
        ax.plot([cx], [0.0], 'ko', ms=4, mew=0)
    savefig(fig, '7.6')


# ---------------------------------------------------------------- fig 7.7 --
def fig_7_7():
    """弦圈的三种基本振动模式: 呼吸(spin-0), + 与 x (spin-2)."""
    fig, ax = plt.subplots(figsize=(4.8, 1.7))
    ax.set_xlim(0.2, 14.9); ax.set_ylim(0.1, 5.0)
    ax.set_aspect('equal'); ax.axis('off')
    R = 1.3
    dirs4 = [90, 180, 270, 0]
    diag4 = [45, 135, 225, 315]

    def arrows(cx, cy, angles):
        for d in np.radians(angles):
            dx, dy = np.cos(d), np.sin(d)
            # 外向箭头 (形变最大时向外)
            arrow(ax, (cx + 1.50 * R * dx, cy + 1.50 * R * dy),
                  (cx + 1.85 * R * dx, cy + 1.85 * R * dy),
                  lw=1.7, head=12)
            # 内向箭头
            arrow(ax, (cx + 0.85 * R * dx, cy + 0.85 * R * dy),
                  (cx + 0.55 * R * dx, cy + 0.55 * R * dy),
                  lw=1.7, head=12)

    # (a) 呼吸模式: 同心圆涟漪
    cx, cy = 2.4, 2.55
    for s in np.linspace(-1, 1, 9):
        if abs(s) < 1e-6:
            continue
        ax.add_patch(Circle((cx, cy), R * (1 + 0.42 * s), fill=False,
                            lw=0.5, edgecolor='0.65'))
    ax.add_patch(Circle((cx, cy), R, fill=False, lw=1.5, edgecolor='k'))
    arrows(cx, cy, dirs4)

    # (b) + 模式: 同周长椭圆族, 长轴沿坐标轴
    cx, cy = 7.5, 2.55
    for phid in np.linspace(0, 90, 13):
        ph = np.radians(phid)
        aa, bb = R * (1 + 0.42 * np.cos(ph)), R * (1 - 0.42 * np.cos(ph))
        tt = np.linspace(0, 2 * np.pi, 200)
        ax.plot(cx + aa * np.cos(tt), cy + bb * np.sin(tt), color='0.65',
                lw=0.5)
    ax.add_patch(Circle((cx, cy), R, fill=False, lw=1.5, edgecolor='k'))
    arrows(cx, cy, dirs4)

    # (c) x 模式: 同上但旋转 45 度
    cx, cy = 12.6, 2.55
    p45 = np.radians(45)
    for phid in np.linspace(0, 90, 13):
        ph = np.radians(phid)
        aa, bb = R * (1 + 0.42 * np.cos(ph)), R * (1 - 0.42 * np.cos(ph))
        tt = np.linspace(0, 2 * np.pi, 200)
        X, Y = aa * np.cos(tt), bb * np.sin(tt)
        ax.plot(cx + X * np.cos(p45) - Y * np.sin(p45),
                cy + X * np.sin(p45) + Y * np.cos(p45), color='0.65', lw=0.5)
    ax.add_patch(Circle((cx, cy), R, fill=False, lw=1.5, edgecolor='k'))
    arrows(cx, cy, diag4)
    savefig(fig, '7.7')


# ---------------------------------------------------------------- fig 7.8 --
def fig_7_8():
    """(t, x^i) 处引力场扰动由过去光锥上的事件给出."""
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    ax.set_xlim(0, 10.2); ax.set_ylim(0.4, 8.0)
    ax.set_aspect('equal'); ax.axis('off')

    # 平面 (t = const)
    plane = [(0.9, 6.15), (6.2, 7.0), (9.3, 5.2), (4.0, 4.35)]
    ax.add_patch(Polygon(plane, closed=True, facecolor='0.88',
                         edgecolor='0.6', lw=0.7))
    ax.text(1.75, 6.05, r'$t$', fontsize=12)

    apex = (5.4, 6.2)
    bc, bw, bh = (5.2, 2.1), 2.2, 0.5        # 底面椭圆
    # 锥体填充 (轮廓 + 底面下半椭圆弧)
    tarc = np.linspace(np.pi, 2 * np.pi, 80)
    xs = bc[0] + bw * np.cos(tarc)
    ys = bc[1] + bh * np.sin(tarc)
    conex = [apex[0], bc[0] - bw] + list(xs) + [bc[0] + bw]
    coney = [apex[1], bc[1]] + list(ys) + [bc[1]]
    ax.add_patch(Polygon(list(zip(conex, coney)), closed=True,
                         facecolor='0.85', edgecolor='none', zorder=2))
    ax.plot([apex[0], bc[0] - bw], [apex[1], bc[1]], 'k-', lw=0.9, zorder=3)
    ax.plot([apex[0], bc[0] + bw], [apex[1], bc[1]], 'k-', lw=0.9, zorder=3)
    ax.plot(xs, ys, '-', color='0.25', lw=0.9, zorder=3)      # 底面前半
    tup = np.linspace(0, np.pi, 50)
    ax.plot(bc[0] + bw * np.cos(tup), bc[1] + bh * np.sin(tup), '--',
            color='0.55', lw=0.8, zorder=3)                   # 底面后半

    # 顶点 x^i 与平面上另一点 y^i
    ax.plot([apex[0]], [apex[1]], 'ko', ms=3.5)
    ax.text(5.12, 6.5, r'$x^i$', fontsize=12)
    py = (6.7, 6.42)
    ax.plot([py[0]], [py[1]], 'ko', ms=3.5)
    ax.text(6.95, 6.6, r'$y^i$', fontsize=12)
    # 竖直虚线 y^i -> (t_r, y^i)
    pt = (6.7, 3.35)
    ax.plot([py[0], pt[0]], [py[1], pt[1]], 'k--', dashes=(4, 3), lw=0.9,
            zorder=4)
    ax.plot([pt[0]], [pt[1]], 'ko', ms=3.5, zorder=5)
    ax.text(6.92, 3.0, r'$(t_r,\, y^i)$', fontsize=10)
    savefig(fig, '7.8')


# ---------------------------------------------------------------- fig 7.9 --
def fig_7_9():
    """波源 (尺度 delta r) 与距离 r 处的观测者."""
    fig, ax = plt.subplots(figsize=(4.2, 1.7))
    ax.set_xlim(0, 10.4); ax.set_ylim(0, 4.2)
    ax.set_aspect('equal'); ax.axis('off')

    eye(ax, 1.35, 3.0, 0.8, ang=-22, pupil=0.12)
    ax.text(1.4, 3.8, 'observer', ha='center', fontsize=9)

    # 不规则源斑块
    tt = np.linspace(0, 2 * np.pi, 200)
    rr = 0.78 + 0.16 * np.sin(3 * tt + 0.8) + 0.10 * np.sin(5 * tt + 2.0)
    bx, by = 8.1 + 1.15 * rr * np.cos(tt), 1.5 + 0.75 * rr * np.sin(tt)
    ax.add_patch(Polygon(list(zip(bx, by)), closed=True, facecolor='0.82',
                         edgecolor='0.55', lw=0.7))
    ax.text(8.55, 2.55, 'source', ha='center', fontsize=9)

    # 视线与距离 r
    ax.plot([1.62, 8.1], [2.88, 1.42], 'k-', lw=0.8)
    ax.text(4.75, 1.92, r'$r$', ha='center', fontsize=12)

    # 源中心与 delta r 位移
    ax.plot([8.1], [1.42], 'ko', ms=3.5, zorder=6)
    arrow(ax, (8.1, 1.42), (8.85, 1.98), lw=1.7, head=12)
    ax.text(7.55, 0.98, r'$\delta r$', ha='center', fontsize=11)
    savefig(fig, '7.9')


# --------------------------------------------------------------- fig 7.10 --
def fig_7_10():
    """双星系统: 两颗质量 M 的恒星在 x1-x2 平面以半径 R 绕转."""
    fig, ax = plt.subplots(figsize=(4.4, 2.8))
    ax.set_xlim(0, 11.6); ax.set_ylim(0, 7.4)
    ax.set_aspect('equal'); ax.axis('off')

    # 轨道平面 (透视平行四边形)
    plane = [(1.2, 3.4), (7.0, 5.6), (10.8, 3.6), (5.0, 1.4)]
    ax.add_patch(Polygon(plane, closed=True, facecolor='0.82',
                         edgecolor='0.45', lw=0.8))

    # 轨道 (虚线椭圆, 倾斜) 与两星
    cxy, aw, bw, tilt = (5.9, 4.55), 2.4, 1.15, 18.0
    ax.add_patch(Ellipse(cxy, 2 * aw, 2 * bw, angle=tilt, fill=False,
                         lw=1.0, edgecolor='k', linestyle=(0, (4, 3))))
    p = np.radians(tilt)
    ux, uy = np.cos(p), np.sin(p)
    sR = (cxy[0] + aw * ux, cxy[1] + aw * uy)     # 右上星
    sL = (cxy[0] - aw * ux, cxy[1] - aw * uy)     # 左下星

    ax.plot([sL[0], sR[0]], [sL[1], sR[1]], 'k-', lw=0.8)   # 两星连线
    ax.plot([cxy[0]], [cxy[1]], 'ko', ms=3.5)
    for (sx, sy), lab in ((sR, (0.48, 0.30)), (sL, (-0.62, -0.28))):
        ax.add_patch(Circle((sx, sy), 0.28, facecolor='0.85',
                            edgecolor='none', zorder=4))
        ax.add_patch(Circle((sx, sy), 0.16, facecolor='k',
                            edgecolor='none', zorder=5))
        ax.text(sx + lab[0], sy + lab[1], r'$M$', ha='center', fontsize=12)

    ax.text(0.5 * (cxy[0] + sR[0]) + 0.15, 0.5 * (cxy[1] + sR[1]) + 0.10,
            r'$R$', ha='center', fontsize=11)
    ax.text(0.5 * (cxy[0] + sL[0]) - 0.22, 0.5 * (cxy[1] + sL[1]) - 0.28,
            r'$R$', ha='center', fontsize=11)

    # 速度箭头 v (切向, 反向)
    v1 = (-0.87, 0.50)
    arrow(ax, sR, (sR[0] + 1.05 * v1[0], sR[1] + 1.05 * v1[1]), lw=1.2,
          head=11)
    ax.text(sR[0] + 1.25 * v1[0] - 0.05, sR[1] + 1.25 * v1[1] + 0.12,
            r'$v$', ha='center', fontsize=12)
    arrow(ax, sL, (sL[0] - 1.05 * v1[0], sL[1] - 1.05 * v1[1]), lw=1.2,
          head=11)
    ax.text(sL[0] - 1.25 * v1[0] + 0.08, sL[1] - 1.25 * v1[1] - 0.18,
            r'$v$', ha='center', fontsize=12)

    # 坐标轴 x1, x2, x3 (左下前方)
    ox, oy = 3.6, 0.85
    arrow(ax, (ox, oy), (ox, oy + 1.4), lw=0.9, head=10)
    ax.text(ox + 0.12, oy + 1.5, r'$x^3$', fontsize=11)
    arrow(ax, (ox, oy), (ox + 1.45, oy - 0.62), lw=0.9, head=10)
    ax.text(ox + 1.62, oy - 0.60, r'$x^1$', fontsize=11)
    arrow(ax, (ox, oy), (ox - 1.45, oy - 0.62), lw=0.9, head=10)
    ax.text(ox - 1.85, oy - 0.58, r'$x^2$', fontsize=11)
    savefig(fig, '7.10')


# --------------------------------------------------------------- fig 7.11 --
def fig_7_11():
    """引力波干涉仪 schematic: laser, 分束器, 四镜, photodiode."""
    fig, ax = plt.subplots(figsize=(3.5, 3.9))
    ax.set_xlim(0, 10); ax.set_ylim(0, 11.2)
    ax.set_aspect('equal'); ax.axis('off')
    bs = (5.2, 4.0)

    def mirror(cx, cy, horiz_label='above', vertical=False):
        w, h = (0.30, 0.80) if vertical else (0.80, 0.30)
        ax.add_patch(Rectangle((cx - w / 2, cy - h / 2), w, h,
                               facecolor='0.7', edgecolor='k', lw=0.8))

    # 激光器
    ax.add_patch(Rectangle((1.2, 3.65), 1.7, 0.7, facecolor='0.85',
                           edgecolor='k', lw=0.8))
    ax.text(2.05, 4.0, 'laser', ha='center', va='center', fontsize=9)
    ax.plot([2.9, bs[0]], [4.0, bs[1]], 'k-', lw=0.8)

    # 分束器 (斜线)
    ax.plot([bs[0] - 0.28, bs[0] + 0.28], [bs[1] - 0.28, bs[1] + 0.28],
            'k-', lw=1.3)

    # 竖直臂 (向上): 近镜 + 端镜 + L
    ax.plot([bs[0], bs[0]], [bs[1], 10.2], 'k-', lw=0.8)
    mirror(bs[0], 7.3); ax.text(4.55, 7.3, 'mirror', ha='right',
                                fontsize=9)
    mirror(bs[0], 10.2); ax.text(4.55, 10.2, 'mirror', ha='right',
                                 fontsize=9)
    ax.plot([bs[0] + 0.18, 5.95], [7.3, 7.3], color='0.5', lw=0.7)
    ax.plot([bs[0] + 0.18, 5.95], [10.2, 10.2], color='0.5', lw=0.7)
    arrow(ax, (5.95, 7.3), (5.95, 10.2), lw=0.8, head=9, style='<|-|>')
    ax.text(6.2, 8.75, r'$L$', ha='center', fontsize=12)

    # 水平臂 (向右): 近镜 + 端镜 + L
    ax.plot([bs[0], 9.6], [bs[1], bs[1]], 'k-', lw=0.8)
    mirror(6.6, bs[1]); ax.text(6.6, 4.62, 'mirror', ha='center',
                                fontsize=9)
    mirror(9.6, bs[1]); ax.text(9.6, 4.62, 'mirror', ha='center',
                                fontsize=9)
    ax.plot([6.6, 6.6], [bs[1] - 0.18, 3.05], color='0.5', lw=0.7)
    ax.plot([9.6, 9.6], [bs[1] - 0.18, 3.05], color='0.5', lw=0.7)
    arrow(ax, (6.6, 3.05), (9.6, 3.05), lw=0.8, head=9, style='<|-|>')
    ax.text(8.1, 2.78, r'$L$', ha='center', fontsize=12)

    # 探测器
    ax.plot([bs[0], bs[0]], [bs[1], 1.4], 'k-', lw=0.8)
    ax.add_patch(Rectangle((4.05, 0.7), 2.3, 0.7, facecolor='0.85',
                           edgecolor='k', lw=0.8))
    ax.text(5.2, 1.05, 'photodiode', ha='center', va='center', fontsize=8.5)
    savefig(fig, '7.11')


# --------------------------------------------------------------- fig 7.12 --
def fig_7_12():
    """LIGO / LISA 灵敏度曲线与预期波源 (双对数坐标)."""
    fig, ax = plt.subplots(figsize=(4.6, 3.3))

    def region(pts, shade):
        pts = np.array(pts, dtype=float)
        ax.fill(10 ** pts[:, 0], 10 ** pts[:, 1],
                color=shade, lw=0, zorder=1)

    # ---- 灰色区域 (log10 单位) ----
    region([(-4.50, -20.00), (-2.60, -21.85), (-2.25, -22.35),
            (-3.35, -22.45)], '0.62')                    # unresolved galactic binaries
    region([(-3.85, -18.90), (-3.58, -18.52), (-2.33, -23.30),
            (-2.60, -23.72)], '0.82')                    # MBH coalescence
    region([(-2.55, -21.55), (-1.95, -22.15), (-1.70, -23.10),
            (-2.35, -22.70)], '0.72')                    # resolved galactic binaries
    region([(1.20, -21.35), (1.50, -21.05), (2.80, -23.55),
            (2.50, -23.85)], '0.82')                     # NS-NS / BH-BH
    region([(1.95, -20.05), (2.60, -20.20), (3.10, -23.30),
            (2.45, -23.60)], '0.58')                     # SN core collapse

    # ---- LISA 曲线 ----
    lf1 = np.linspace(-4.52, -2.55, 80)
    a1 = -19.7 + (lf1 + 4.52) * (-1.70)
    lf2 = np.linspace(-2.55, 0.0, 500)
    base = -23.05 + (lf2 + 2.55) * 0.95
    amp = 0.06 + 0.20 * (lf2 + 2.55) / 2.55
    phase = 2 * np.pi * (2.6 * (lf2 + 2.55) + 3.4 * (lf2 + 2.55) ** 2)
    a2 = base + amp * np.sin(phase)
    ax.plot(10 ** np.concatenate([lf1, lf2]),
            10 ** np.concatenate([a1, a2]), 'k-', lw=1.1, zorder=3)

    # ---- LIGO 曲线 ----
    lf3 = np.linspace(0.95, 1.55, 30)
    a3 = -20.1 + (lf3 - 0.95) * (-4.83)
    lf4 = np.linspace(1.55, 4.15, 300)
    a4 = -23.05 + 0.75 * (np.maximum(lf4 - 2.0, 0.0)) ** 2 \
        - 0.20 * np.exp(-((lf4 - 1.9) / 0.22) ** 2)
    ax.plot(10 ** np.concatenate([lf3, lf4]),
            10 ** np.concatenate([a3, a4]), 'k-', lw=1.1, zorder=3)

    # ---- 标注与引线 (坐标为 log10 值, 绘制前转换) ----
    lead = dict(lw=0.7, color='k', zorder=4)

    def T(lx, ly, *a, **k):
        ax.text(10 ** lx, 10 ** ly, *a, **k)

    def L(p0, p1):
        ax.plot([10 ** p0[0], 10 ** p1[0]],
                [10 ** p0[1], 10 ** p1[1]], **lead)

    T(-2.85, -18.72, 'Coalescence of\nmassive black holes',
      ha='center', fontsize=9)
    L((-3.18, -19.10), (-3.62, -19.85))
    T(-2.02, -21.05, 'resolved galactic\nbinaries', ha='center', fontsize=9)
    L((-2.32, -21.48), (-2.60, -21.92))
    T(-4.72, -21.95, 'unresolved\ngalactic\nbinaries', ha='left',
      fontsize=9, linespacing=1.3)
    L((-3.98, -21.90), (-3.50, -21.40))
    T(2.38, -18.95, 'NS--NS and BH--BH\ncoalescence', ha='center',
      fontsize=9)
    L((1.92, -19.52), (1.55, -20.65))
    T(3.22, -19.80, 'SN core collapse', ha='left', fontsize=9)
    L((3.16, -20.02), (2.62, -20.80))
    T(-2.15, -23.92, 'LISA', ha='center', fontsize=10)
    T(1.80, -23.92, 'LIGO', ha='center', fontsize=10)

    # ---- 坐标轴 ----
    ax.set_xscale('log'); ax.set_yscale('log')
    ax.set_xlim(10 ** -5.15, 10 ** 4.65)
    ax.set_ylim(10 ** -24.15, 10 ** -17.65)
    ax.set_xticks([1e-4, 1e-2, 1e0, 1e2, 1e4])
    ax.set_xticklabels([r'$10^{-4}$', r'$10^{-2}$', r'$10^{0}$',
                        r'$10^{2}$', r'$10^{4}$'], fontsize=9)
    ax.set_yticks([1e-24, 1e-22, 1e-20, 1e-18])
    ax.set_yticklabels([r'$10^{-24}$', r'$10^{-22}$', r'$10^{-20}$',
                        r'$10^{-18}$'], fontsize=9)
    ax.tick_params(which='minor', length=2.5)
    ax.set_xlabel('frequency (Hz)', fontsize=10)
    ax.set_ylabel('gravitational wave amplitude', fontsize=10)
    for s in ('top', 'right'):
        ax.spines[s].set_visible(False)
    savefig(fig, '7.12')


# ------------------------------------------------------------------ 主流程 --
if __name__ == '__main__':
    for fn in (fig_7_1, fig_7_2, fig_7_3, fig_7_4, fig_7_5, fig_7_6,
               fig_7_7, fig_7_8, fig_7_9, fig_7_10, fig_7_11, fig_7_12):
        fn()
        print('done:', fn.__name__)
