# -*- coding: utf-8 -*-
"""
《时空与几何》第 5 章（Schwarzschild 解）插图重绘，第一批：图 5.1 - 5.9。
黑白教材风矢量图；图内文字用原书英文/数学记号。
产物: figures/fig_5.k.pdf + figures/preview/fig_5.k.png
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Polygon, FancyArrowPatch, Circle, Arc

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

BASE = r'E:\AI整理书籍\卡罗尔\重排本'
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)


def _save(fig, key):
    for ext, d in (('pdf', FIGDIR), ('png', PREVDIR)):
        path = os.path.join(d, 'fig_%s.%s' % (key, ext))
        fig.savefig(path, bbox_inches='tight', pad_inches=0.03, dpi=150)
    plt.close(fig)


def _arrow(ax, xy_from, xy_to, lw=1.2, ms=12, color='k', style='-|>', zorder=5):
    ax.annotate('', xy=xy_to, xytext=xy_from, zorder=zorder,
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


# ---------------------------------------------------------------- 图 5.1 ----
def fig_5_1():
    """Foliation of R^3 (minus the origin) by two-spheres: 嵌套球壳."""
    fig, ax = plt.subplots(figsize=(3.2, 3.45))
    ax.set_xlim(-1.85, 1.85)
    ax.set_ylim(-1.75, 1.75)
    ax.set_aspect('equal')
    ax.axis('off')

    R, rs = 1.0, 0.36          # 外球与内球半径
    k = 0.30                   # 赤道椭圆压扁比

    th = np.linspace(0, np.pi, 200)

    # 上半球外缘（凸外表面, 稍深）
    up = np.column_stack([R * np.cos(th), R * np.sin(th)])
    ax.add_patch(Polygon(up, closed=True, fc='0.86', ec='none', zorder=1))
    # 下半球内壁（凹碗内表面, 稍浅）
    low = np.column_stack([R * np.cos(th + np.pi), R * np.sin(th + np.pi)])
    eqf = np.column_stack([R * np.cos(th), -k * R * np.sin(th)])   # 赤道前弧
    bowl = np.vstack([low, eqf[::-1]])
    ax.add_patch(Polygon(bowl, closed=True, fc='0.91', ec='none', zorder=1))

    # 外球轮廓
    ax.add_patch(Circle((0, 0), R, fc='none', ec='k', lw=1.1, zorder=3))
    # 外球赤道：后段虚线, 前段实线
    ax.plot(R * np.cos(th), k * R * np.sin(th), 'k--', lw=0.9, zorder=2)
    ax.plot(eqf[:, 0], eqf[:, 1], 'k-', lw=1.2, zorder=3)

    # x, y 轴（赤道面内, 画在碗面之上、内球之下）
    _arrow(ax, (0, 0), (-1.42, -0.36), lw=1.1, ms=11, zorder=4)
    ax.text(-1.52, -0.40, '$x$', fontsize=12, ha='right', va='top', zorder=6)
    _arrow(ax, (0, 0), (1.02, -1.02), lw=1.1, ms=11, zorder=4)
    ax.text(1.09, -1.06, '$y$', fontsize=12, ha='left', va='top', zorder=6)

    # z 轴（穿出上壳）
    _arrow(ax, (0, 0), (0, 1.42), lw=1.1, ms=11, zorder=4)
    ax.text(0.02, 1.48, '$z$', fontsize=12, ha='left', va='bottom', zorder=6)

    # 内球（画在 z 轴线之后, 遮住轴下段）
    ax.add_patch(Circle((0, 0), rs, fc='0.80', ec='none', zorder=5))
    ax.add_patch(Circle((0, 0), rs, fc='none', ec='0.45', lw=0.7, zorder=6))
    # 内球赤道环（略宽于球, 同一赤道面）
    rr = 0.50
    ax.plot(rr * np.cos(th), 0.30 * rr * np.sin(th), 'k--', lw=0.8, zorder=4)
    ax.plot(rr * np.cos(th), -0.30 * rr * np.sin(th), 'k-', lw=1.0, zorder=7)

    ax.text(-1.02, 0.86, r'$\mathbf{R}^3$', fontsize=13, ha='center', va='center', zorder=6)
    _save(fig, '5.1')


# ---------------------------------------------------------------- 图 5.2 ----
def fig_5_2():
    """Foliation of a wormhole by two-spheres: 双平面 + 喉道."""
    fig, ax = plt.subplots(figsize=(3.4, 3.3))
    ax.set_xlim(-4.6, 4.9)
    ax.set_ylim(-0.35, 9.6)
    ax.set_aspect('equal')
    ax.axis('off')

    def plane(c, a, b, z=2):
        corners = [c - a - b, c + a - b, c + a + b, c - a + b]
        ax.add_patch(Polygon(corners, closed=True, fc='0.85', ec='0.45',
                             lw=0.7, zorder=z))

    a = np.array([3.3, 0.85])
    b = np.array([-1.05, 1.5])
    plane(np.array([0.15, 6.9]), a, b)            # 上平面
    plane(np.array([0.30, 2.1]), a, b)            # 下平面

    # 喉道轮廓 half-width w(y)，中心线从上孔中心滑向下孔中心
    ytop, ybot, waist = 6.75, 2.35, 0.40
    y = np.linspace(ytop, ybot, 240)
    w = waist + 0.98 * np.exp((y - ytop) / 0.60) + 1.15 * np.exp((ybot - y) / 0.85)
    xt, xb = 0.15, 0.30                            # 上、下孔中心 x
    cx = xt + (xb - xt) * (ytop - y) / (ytop - ybot)

    # 喉道白色主体：上孔前弧 + 右侧线 + 下孔前弧 + 左侧线
    ryT, ryB = 0.30 * w[0], 0.28 * w[-1]
    tt = np.linspace(np.pi, 2 * np.pi, 60)
    top_arc = np.column_stack([xt + w[0] * np.cos(tt), ytop + ryT * np.sin(tt)])
    bot_arc = np.column_stack([xb + w[-1] * np.cos(tt), ybot + ryB * np.sin(tt)])
    right = np.column_stack([cx + w, y])
    left = np.column_stack([cx - w, y])[::-1]
    body = np.vstack([top_arc, right, bot_arc[::-1], left])
    ax.add_patch(Polygon(body, closed=True, fc='white', ec='none', zorder=3))
    for sgn in (1, -1):
        ax.plot(cx + sgn * w, y, 'k-', lw=1.1, zorder=4)

    # 喉道上的二维球面（圆环）
    for yc in (5.55, 4.65, 3.75):
        i = np.argmin(np.abs(y - yc))
        rxc = w[i]
        ax.add_patch(Ellipse((cx[i], yc), 2 * rxc, 2 * 0.26 * rxc,
                             fc='none', ec='k', lw=0.8, zorder=5))

    # 上孔（白洞口 + 后壁内弧）
    ax.add_patch(Ellipse((xt, ytop), 2 * w[0], 2 * ryT,
                         fc='white', ec='none', zorder=4))
    ax.add_patch(Arc((xt, ytop - 0.13), 2.15, 0.62, theta1=15, theta2=165,
                     ec='0.55', lw=0.8, zorder=5))
    ax.add_patch(Ellipse((xt, ytop), 2 * w[0], 2 * ryT,
                         fc='none', ec='k', lw=1.0, zorder=6))
    # 下孔
    ax.add_patch(Ellipse((xb, ybot), 2 * w[-1], 2 * ryB,
                         fc='white', ec='none', zorder=4))
    ax.add_patch(Arc((xb, ybot + 0.13), 2.35, 0.66, theta1=195, theta2=345,
                     ec='0.55', lw=0.8, zorder=5))
    ax.add_patch(Ellipse((xb, ybot), 2 * w[-1], 2 * ryB,
                         fc='none', ec='k', lw=1.0, zorder=6))
    _save(fig, '5.2')


# ---------------------------------------------------------------- 图 5.3 ----
def fig_5_3():
    """Orbits around a star: r(lambda). 恒星 + 两条虚线轨道 + 径向箭头."""
    fig, ax = plt.subplots(figsize=(4.3, 2.2))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.2)
    ax.axis('off')

    S = (7.0, 2.75)   # 恒星位置

    # 大轨道（虚线大椭圆, 倾斜, 越出画面）
    c1, a1, b1, ang1 = (5.2, 3.9), 5.6, 1.35, 10.0
    # 内轨道（虚线小椭圆）
    c2, a2, b2, ang2 = (4.0, 1.7), 2.3, 1.15, 30.0

    def ell(c, a, b, ang, n=400):
        t = np.linspace(0, 2 * np.pi, n)
        ca, sa = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        x0, y0 = a * np.cos(t), b * np.sin(t)
        return c[0] + ca * x0 - sa * y0, c[1] + sa * x0 + ca * y0

    for (c, a, b, ang) in ((c1, a1, b1, ang1), (c2, a2, b2, ang2)):
        x, y = ell(c, a, b, ang)
        ax.plot(x, y, 'k--', dashes=(5, 3.2), lw=1.15)

    # 轨道上的运动方向箭头（沿切向）
    def tangential_arrow(c, a, b, ang, t0, t1):
        ca, sa = np.cos(np.radians(ang)), np.sin(np.radians(ang))
        p = lambda t: (c[0] + ca * a * np.cos(t) - sa * b * np.sin(t),
                       c[1] + sa * a * np.cos(t) + ca * b * np.sin(t))
        x0, y0 = p(t0)
        x1, y1 = p(t1)
        _arrow(ax, (x0, y0), (x1, y1), lw=1.0, ms=13)

    tangential_arrow(c1, a1, b1, ang1, 2.50, 2.57)     # 大椭圆左上, 向左下
    tangential_arrow(c1, a1, b1, ang1, 5.50, 5.57)     # 大椭圆右上, 向右上
    tangential_arrow(c2, a2, b2, ang2, 2.30, 2.38)     # 内椭圆左上, 向上

    # 恒星：放射状星芒
    for i in range(12):
        phi = i * np.pi / 6 + 0.22
        L = 0.42 if i % 2 == 0 else 0.24
        ax.plot([S[0], S[0] + L * np.cos(phi)], [S[1], S[1] + L * np.sin(phi)],
                'k-', lw=1.5)
    ax.add_patch(Circle(S, 0.07, fc='k', ec='none', zorder=6))

    # 径向箭头 r(lambda)
    _arrow(ax, S, (4.15, 5.35), lw=2.4, ms=20)          # 左上长箭头
    _arrow(ax, S, (4.55, 1.95), lw=2.4, ms=20)          # 左下
    ax.text(5.20, 1.82, '$r(\\lambda)$', fontsize=12, ha='center', va='top')
    _arrow(ax, S, (9.55, 2.62), lw=2.4, ms=20)          # 右
    ax.text(8.30, 2.42, '$r(\\lambda)$', fontsize=12, ha='center', va='top')
    _arrow(ax, S, (6.82, 1.50), lw=2.4, ms=20)          # 下
    _save(fig, '5.3')


# ------------------------------------------------------- 图 5.4 / 5.5 公用 ----
def _potential_panels(curves_L, label_spec, title, fname):
    """两联有效势图. curves_L: dict L -> (r array, V array).
       label_spec: (panel, text, x_lab, y_lab) 或
                   (panel, text, x_lab, y_lab, L, r_touch) —— 引线连到曲线."""
    fig, axes = plt.subplots(1, 2, figsize=(4.8, 2.30))
    fig.subplots_adjust(left=0.085, right=0.995, bottom=0.13, top=0.99, wspace=0.09)

    for j, ax in enumerate(axes):
        ax.set_facecolor('0.89')
        ax.set_xlim(0, 30)
        ax.set_ylim(0, 0.8)
        ax.set_xticks([0, 10, 20, 30])
        ax.set_yticks([0.2, 0.4, 0.6, 0.8])
        ax.tick_params(direction='in', top=True, right=True, length=4.2,
                       width=0.9, labelsize=9.5, pad=3)
        if j == 1:
            ax.set_yticklabels([])
        for s in ax.spines.values():
            s.set_linewidth(1.0)
        ax.text(0.47, 0.955, title[j], transform=ax.transAxes, ha='center',
                va='top', fontsize=9.5, linespacing=1.45)

    axes[0].text(-0.185, 0.52, '$V(r)$', fontsize=11, ha='right', va='center',
                 transform=axes[0].transAxes)
    for ax in axes:
        ax.text(30, -0.075, '$r$', fontsize=11, ha='right', va='top',
                clip_on=False)

    # 画曲线
    for j in (0, 1):
        for L, (r, V) in curves_L[j].items():
            axes[j].plot(r, V, 'k-', lw=1.35)

    # 标注
    for spec in label_spec:
        j, txt, xl, yl = spec[:4]
        ax = axes[j]
        if len(spec) == 6:
            L, r_t = spec[4], spec[5]
            r_arr, V_arr = curves_L[j][L]
            ytc = float(np.interp(r_t, r_arr, V_arr))
            ax.plot([r_t, xl - 0.5], [ytc, yl], '-', color='0.45', lw=0.7)
        ax.text(xl, yl, txt, fontsize=10, ha='left', va='center')

    _save(fig, fname)


def fig_5_4():
    """Effective potentials in Newtonian gravity (GM=1)."""
    Ls = [1, 2, 3, 4, 5]
    curves = {0: {}, 1: {}}
    for L in Ls:
        # massless: V = L^2/(2 r^2)
        r0 = L / np.sqrt(1.6)
        r = np.linspace(r0, 30, 600)
        curves[0][L] = (r, L**2 / (2 * r**2))
        # massive: V = 1/2 - 1/r + L^2/(2 r^2)
        r0 = (-1 + np.sqrt(1 + 0.6 * L**2)) / 0.6
        r = np.linspace(r0, 30, 600)
        curves[1][L] = (r, 0.5 - 1.0 / r + L**2 / (2 * r**2))

    titles = ['Newtonian gravity\nmassless particles',
              'Newtonian gravity\nmassive particles']
    spec = [
        (0, '$L=5$', 11.0, 0.452, 5, 5.08),
        (0, '$4$',    13.6, 0.388, 4, 4.36),
        (0, '$3$',    16.2, 0.324, 3, 3.56),
        (0, '$2$',    18.8, 0.260, 2, 2.63),
        (0, '$1$',    21.4, 0.196, 1, 1.49),
        (1, '$5$',     7.6, 0.480),
        (1, '$4$',     7.3, 0.360),
        (1, '$3$',     5.4, 0.262),
        (1, '$2$',     4.3, 0.148),
        (1, '$L=1$',   6.2, 0.040),
    ]
    _potential_panels(curves, spec, titles, '5.4')


def fig_5_5():
    """Effective potentials in general relativity (GM=1)."""
    Ls = [1, 2, 3, 4, 5]
    curves = {0: {}, 1: {}}
    for L in Ls:
        # massless GR: V = L^2/(2r^2) - L^2/r^3  (>=0 for r>=2)
        r = np.linspace(2.0, 30, 900)
        curves[0][L] = (r, L**2 / (2 * r**2) - L**2 / r**3)
        # massive GR: V = 1/2 - 1/r + L^2/(2r^2) - L^2/r^3
        curves[1][L] = (r, 0.5 - 1.0 / r + L**2 / (2 * r**2) - L**2 / r**3)

    titles = ['general relativity\nmassless particles',
              'general relativity\nmassive particles']
    spec = [
        (0, '$L=5$', 12.0, 0.262, 5, 5.00),
        (0, '$4$',    14.6, 0.196, 4, 4.50),
        (0, '$3$',    16.4, 0.142, 3, 3.60),
        (0, '$2$',    17.8, 0.096, 2, 3.10),
        (0, '$1$',    19.2, 0.055, 1, 3.02),
        (1, '$5$',    4.55, 0.590),
        (1, '$4$',    5.10, 0.435),
        # 引线按曲线实际高度连接（与原图标签堆叠次序相反, 见报告说明）
        (1, '$3$',    24.4, 0.320, 1, 6.0),
        (1, '$2$',    24.4, 0.258, 2, 6.0),
        (1, '$L=1$',  24.4, 0.196, 1, 6.0),
    ]
    _potential_panels(curves, spec, titles, '5.5')


# ---------------------------------------------------------------- 图 5.6 ----
def fig_5_6():
    """Precessing ellipse rosette (orbits in GR)."""
    fig, ax = plt.subplots(figsize=(4.0, 3.1))
    ax.set_xlim(0, 10)
    ax.set_ylim(0.2, 7.6)
    ax.set_aspect('equal')
    ax.axis('off')

    F = np.array([2.8, 1.9])     # 焦点（行星）
    e, a = 0.72, 3.0
    p = a * (1 - e**2)

    def orbit(w, color, lw):
        phi = np.linspace(0, 2 * np.pi, 500)
        r = p / (1 + e * np.cos(phi - w))
        ax.plot(F[0] + r * np.cos(phi), F[1] + r * np.sin(phi),
                color=color, lw=lw, solid_capstyle='round')

    w0 = np.radians(192)         # 初始近日点方向（左下）
    orbit(w0, 'k', 1.7)                      # "当前"轨道（原书白色椭圆）
    for kk in range(1, 5):
        orbit(w0 + np.radians(18) * kk, '0.55', 1.05)

    # 行星（灰色球体 + 高光）
    ax.add_patch(Circle(F, 0.46, fc='0.74', ec='none', zorder=6))
    clip = Circle(F, 0.46, fc='none', ec='none', zorder=7)
    ax.add_patch(clip)
    hl = Circle((F[0] - 0.11, F[1] + 0.11), 0.46, fc='0.90', ec='none', zorder=7)
    ax.add_patch(hl)
    hl.set_clip_path(clip)
    ax.add_patch(Circle(F, 0.46, fc='none', ec='0.35', lw=0.6, zorder=8))

    # 进动方向箭头（右上方, 逆时针弯箭头）
    ar = FancyArrowPatch((8.45, 4.15), (8.85, 6.45),
                         connectionstyle='arc3,rad=0.40',
                         arrowstyle='-|>', mutation_scale=30,
                         lw=3.6, color='0.25', zorder=9)
    ax.add_patch(ar)
    _save(fig, '5.6')


# ---------------------------------------------------------------- 图 5.7 ----
def fig_5_7():
    """Light cones close up as r -> 2GM (Schwarzschild coordinates)."""
    fig, ax = plt.subplots(figsize=(4.0, 2.55))
    ax.set_xlim(-0.15, 10.4)
    ax.set_ylim(-0.95, 6.7)
    ax.axis('off')

    # 坐标轴
    ax.plot([0.55, 0.55], [-0.45, 6.15], 'k-', lw=1.1)
    _arrow(ax, (0.55, 6.0), (0.55, 6.45), lw=1.1, ms=12)
    ax.text(0.82, 6.22, '$t$', fontsize=12, ha='left', va='center')
    ax.plot([0.30, 10.0], [0, 0], 'k-', lw=1.1)
    _arrow(ax, (10.0, 0), (10.35, 0), lw=1.1, ms=12)
    ax.text(10.30, -0.42, '$r$', fontsize=12, ha='right', va='top')

    # r = 2GM 虚线
    ax.plot([3.0, 3.0], [0, 5.7], 'k--', lw=1.1, dashes=(5, 3.5))
    ax.text(3.0, -0.55, '$2GM$', fontsize=12, ha='center', va='top')

    # 三个光锥（倒立圆锥: 尖朝下, 椭圆口朝上）, 逼近 2GM 逐渐变窄
    yr, ya = 5.05, 3.30                     # 口缘与锥尖高度
    for xc, hw in ((4.15, 0.35), (6.05, 0.75), (8.85, 1.22)):
        ry = 0.28 * hw
        ax.add_patch(Polygon([(xc - hw, yr), (xc + hw, yr), (xc, ya)],
                             closed=True, fc='0.88', ec='k', lw=1.0, zorder=4))
        ax.add_patch(Ellipse((xc, yr), 2 * hw, 2 * ry, fc='0.96', ec='k',
                             lw=1.0, zorder=5))
    _save(fig, '5.7')


# ---------------------------------------------------------------- 图 5.8 ----
def fig_5_8():
    """Beacon falling into a black hole: 信号间隔被拉长."""
    fig, ax = plt.subplots(figsize=(4.25, 3.35))
    ax.set_xlim(-0.15, 10.9)
    ax.set_ylim(-0.85, 8.0)
    ax.axis('off')

    x_t, x_h, x_obs = 1.0, 3.2, 8.4         # t 轴, 2GM, 观测者
    # 坐标轴
    ax.plot([x_t, x_t], [-0.45, 7.45], 'k-', lw=1.1)
    _arrow(ax, (x_t, 7.35), (x_t, 7.75), lw=1.1, ms=12)
    ax.text(x_t + 0.27, 7.55, '$t$', fontsize=12, ha='left', va='center')
    ax.plot([0.75, 10.5], [0, 0], 'k-', lw=1.1)
    _arrow(ax, (10.5, 0), (10.85, 0), lw=1.1, ms=12)
    ax.text(10.8, -0.40, '$r$', fontsize=12, ha='right', va='top')

    ax.plot([x_h, x_h], [0, 7.1], 'k--', lw=1.1, dashes=(5, 3.5))
    ax.text(x_h, -0.55, '$2GM$', fontsize=12, ha='center', va='top')

    # 观测者世界线
    ax.plot([x_obs, x_obs], [0, 7.5], 'k-', lw=1.0)

    # 信标（自由下落）世界线
    s = np.linspace(0, 1.03, 400)
    yb = 7.3 - 7.1 * s
    xb = x_h * (1 + 0.10 * s**0.35 + 0.95 * s**2.6)
    ax.plot(xb, yb, 'k-', lw=2.0)

    # 三个发射事件（等固有时）
    s_ev = np.array([0.686, 0.786, 0.886])
    y_ev = 7.3 - 7.1 * s_ev
    x_ev = x_h * (1 + 0.10 * s_ev**0.35 + 0.95 * s_ev**2.6)

    def curve_pt(sv):
        return (x_h * (1 + 0.10 * sv**0.35 + 0.95 * sv**2.6), 7.3 - 7.1 * sv)

    # 事件刻度（垂直于曲线的短线段）
    for sv in s_ev:
        p0 = np.array(curve_pt(sv))
        p1 = np.array(curve_pt(sv + 0.012))
        tg = p1 - p0
        tg = tg / np.linalg.norm(tg)
        nrm = np.array([-tg[1], tg[0]])
        a_, b_ = p0 - 0.11 * nrm, p0 + 0.11 * nrm
        ax.plot([a_[0], b_[0]], [a_[1], b_[1]], 'k-', lw=1.0)

    # 接收事件与光信号（虚线, 微弯, 凸向左上）
    # 事件自上而下 = 发射越来越晚, 到达次序相同: 顶事件 -> 顶到达
    y_arr = np.array([7.20, 5.40, 3.90])
    for (xe, ye), ya in zip(zip(x_ev, y_ev), y_arr):
        tpar = np.linspace(0, 1, 60)
        cx = xe + 0.55 * (x_obs - xe)
        cy = ye + 0.60 * (ya - ye)
        bx = (1 - tpar)**2 * xe + 2 * (1 - tpar) * tpar * cx + tpar**2 * x_obs
        by = (1 - tpar)**2 * ye + 2 * (1 - tpar) * tpar * cy + tpar**2 * ya
        ax.plot(bx, by, 'k--', lw=1.0, dashes=(4.5, 3.0))
        ax.plot([x_obs - 0.16, x_obs + 0.16], [ya, ya], 'k-', lw=1.0)

    # 标注
    ax.text(0.60 * x_ev[0] + 0.40 * x_ev[1] - 0.85, 0.5 * (y_ev[0] + y_ev[1]),
            '$\\Delta\\tau_1$', fontsize=12, ha='center', va='center')
    ax.text(0.60 * x_ev[1] + 0.40 * x_ev[2] - 0.85, 0.5 * (y_ev[1] + y_ev[2]),
            '$\\Delta\\tau_1$', fontsize=12, ha='center', va='center')
    ax.text(x_obs + 0.28, 0.5 * (3.90 + 5.40), '$\\Delta\\tau_2$',
            fontsize=12, ha='left', va='center')
    ax.text(x_obs + 0.28, 0.5 * (5.40 + 7.20) + 0.15,
            '$\\Delta\\tau_2^{\\prime} > \\Delta\\tau_2$',
            fontsize=12, ha='left', va='center')
    _save(fig, '5.8')


# ---------------------------------------------------------------- 图 5.9 ----
def fig_5_9():
    """Schwarzschild light cones in tortoise coordinates r*."""
    fig, ax = plt.subplots(figsize=(4.3, 2.6))
    ax.set_xlim(0, 10.6)
    ax.set_ylim(-1.75, 6.5)
    ax.axis('off')

    x_axis, y_axis = 3.8, 1.15              # t 轴位置与水平轴高度
    # 坐标轴
    ax.plot([x_axis, x_axis], [y_axis - 0.25, 6.05], 'k-', lw=1.1)
    _arrow(ax, (x_axis, 5.95), (x_axis, 6.35), lw=1.1, ms=12)
    ax.text(x_axis + 0.25, 6.15, '$t$', fontsize=12, ha='left', va='center')
    ax.plot([0.9, 10.1], [y_axis, y_axis], 'k-', lw=1.1)
    _arrow(ax, (10.1, y_axis), (10.45, y_axis), lw=1.1, ms=12)
    ax.text(10.42, y_axis - 0.35, '$r^{*}$', fontsize=12, ha='right', va='top')

    # 两个不退化光锥（沙漏状）, 分别位于 t 轴两侧
    for xc in (2.45, 6.90):
        hw, ry = 1.02, 0.30
        yw = 3.50                            # 腰点
        for sgn in (1, -1):                  # 上、下锥
            ax.add_patch(Polygon([(xc - hw, yw + sgn * 1.12),
                                  (xc + hw, yw + sgn * 1.12),
                                  (xc, yw)],
                                 closed=True, fc='0.88', ec='k', lw=1.0,
                                 zorder=4))
            ax.add_patch(Ellipse((xc, yw + sgn * 1.12), 2 * hw, 2 * ry,
                                 fc='0.96', ec='k', lw=1.0, zorder=5))

    # 指向 r = 2GM (r* = -infinity) 的粗箭头
    _arrow(ax, (5.0, -0.55), (1.3, -0.55), lw=4.5, ms=24, color='0.55')
    ax.text(3.1, -1.05, '$r = 2GM$', fontsize=11, ha='center', va='top')
    ax.text(3.1, -1.62, '$r^{*} = -\\infty$', fontsize=11, ha='center', va='top')
    _save(fig, '5.9')


if __name__ == '__main__':
    for f in (fig_5_1, fig_5_2, fig_5_3, fig_5_4, fig_5_5,
              fig_5_6, fig_5_7, fig_5_8, fig_5_9):
        f()
        print('done:', f.__name__)
