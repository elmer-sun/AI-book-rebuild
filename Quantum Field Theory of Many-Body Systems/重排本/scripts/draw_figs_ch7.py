# -*- coding: utf-8 -*-
# 批次 B6：文小刚《多体量子场论》第7章插图 7.1–7.18（黑白矢量重绘）
# 依据：原书转换/pages/p291–p347（书页 276–332，pNNN = 书页 + 15）
#   7.6 在 p295（书页 280），7.17 在 p333（书页 318）——两幅为 MinerU 漏抓图。
# 输出：figures/fig_{key}.pdf + figures/preview/fig_{key}.png
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, Polygon

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
    'hatch.linewidth': 0.5,
})

BASE = r"E:\AI整理书籍\文小刚\重排本"
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

GRAY = '0.82'    # 中灰填充（原书阴影）
DARK = '0.72'    # 深灰填充


def save(key):
    for ext, kw in (('pdf', {}), ('png', {'dpi': 160})):
        plt.savefig(os.path.join(FIGDIR if ext == 'pdf' else PREVDIR,
                                 f'fig_{key}.{ext}'),
                    bbox_inches='tight', pad_inches=0.03, **kw)
    plt.close()


def arr(ax, p, q, lw=1.1, ms=11, style='-|>', color='black', **kw):
    """自绘箭头（合同要求 annotate + arrowstyle '-|>'）。"""
    ax.annotate('', xy=q, xytext=p,
                arrowprops=dict(arrowstyle=style, lw=lw,
                                mutation_scale=ms, color=color,
                                shrinkA=0, shrinkB=0, **kw))


def ax_spine(ax, p, q, lw=1.0):
    ax.plot([p[0], q[0]], [p[1], q[1]], color='black', lw=lw,
            solid_capstyle='butt', zorder=3)


def bare(ax):
    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)


def new_ax(fig, rect, xlim, ylim, aspect=None):
    ax = fig.add_axes(rect)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    if aspect == 'equal':
        ax.set_aspect('equal')
    ax.set_axis_off()
    return ax


# ---------------------------------------------------------------- 7.1
def fig_7_1():
    """挖去 r=0 的平面 + 磁通管；回路 A（不可缩, n_w=1）与 B（可缩）。p291"""
    fig = plt.figure(figsize=(4.6, 2.7))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96], (0, 10), (0, 5.9), 'equal')

    # 透视平面（平行四边形）
    P = [(0.4, 1.15), (7.6, 1.15), (9.6, 4.6), (2.4, 4.6)]
    ax.add_patch(Polygon(P, closed=True, facecolor='white',
                         edgecolor='black', lw=0.9))

    # 磁通管：中心黑盘 + 竖直粗线 + 大箭头 + Φ
    cx, cy = 4.85, 2.62
    ax.add_patch(Ellipse((cx, cy), 0.62, 0.2, facecolor='black',
                         edgecolor='black', zorder=5))
    ax.plot([cx, cx], [cy + 0.05, 5.05], color='black', lw=2.2, zorder=4)
    arr(ax, (cx, 4.5), (cx, 5.55), lw=2.2, ms=17)
    ax.text(cx + 0.42, 5.18, r'$\Phi$', fontsize=13)

    # 回路 A：绕黑盘的大透视椭圆，前端(下方)箭头向右
    ax.add_patch(Ellipse((cx, cy), 4.15, 1.25, facecolor='none',
                         edgecolor='black', lw=1.1, zorder=3))
    t = np.linspace(np.deg2rad(250), np.deg2rad(290), 30)
    ax.plot(cx + 2.07 * np.cos(t), cy + 0.62 * np.sin(t) - 0.02,
            color='black', lw=1.1, zorder=3.5)
    arr(ax, (cx - 0.30, cy - 0.62), (cx + 0.16, cy - 0.625), lw=1.3, ms=13)
    ax.text(cx - 2.75, cy - 0.1, 'A', fontsize=13)

    # 回路 B：右上方小可缩圆
    bx, by = 7.05, 3.42
    ax.add_patch(Ellipse((bx, by), 1.35, 0.42, facecolor='none',
                         edgecolor='black', lw=1.1, zorder=3))
    arr(ax, (bx - 0.28, by - 0.21), (bx + 0.22, by - 0.213), lw=1.3, ms=13)
    ax.text(bx + 0.92, by - 0.05, 'B', fontsize=13)
    save('7.1')


# ---------------------------------------------------------------- 7.2
def fig_7_2():
    """环面上的两个不可缩回路 A 与 B。p292"""
    fig = plt.figure(figsize=(4.6, 2.2))
    ax = new_ax(fig, [0.02, 0.02, 0.96, 0.96], (0, 10), (0, 4.8), 'equal')
    cx, cy = 5.0, 2.75

    # 外轮廓（顶面）
    ax.add_patch(Ellipse((cx, cy), 8.6, 3.1, facecolor='white',
                         edgecolor='black', lw=1.0, zorder=1))
    # 中洞（白色填充打穿）+ 远侧内壁（下弯曲线与两端短线）
    a2, b2 = 2.0, 0.60
    ax.add_patch(Ellipse((cx, cy + 0.28), 2 * a2, 2 * b2, facecolor='white',
                         edgecolor='black', lw=1.0, zorder=2))
    t = np.linspace(0, np.pi, 60)
    ax.plot(cx + (a2 - 0.25) * np.cos(t + np.pi),
            cy + 0.40 - 0.26 * np.sin(t),
            color='black', lw=1.0, zorder=3)
    ax.plot([cx - a2 - 0.18, cx - a2 + 0.22], [cy + 0.52, cy + 0.44],
            color='black', lw=1.0, zorder=3)
    ax.plot([cx + a2 - 0.22, cx + a2 + 0.18], [cy + 0.44, cy + 0.52],
            color='black', lw=1.0, zorder=3)

    # 回路 A（环向，绕中洞一周，画在最上层）
    ax.add_patch(Ellipse((cx, cy + 0.10), 5.9, 1.95, facecolor='none',
                         edgecolor='black', lw=1.1, zorder=5))
    ax.text(cx - 3.42, cy + 0.02, 'A', fontsize=13)

    # 回路 B：绕管截面的小竖椭圆（左半虚、右半实），位于前下方
    bx, by = cx - 0.05, cy - 1.22
    ax.add_patch(Ellipse((bx, by), 0.85, 1.80, facecolor='none',
                         edgecolor='black', lw=1.0, ls=(0, (4, 3)),
                         zorder=5))
    t = np.linspace(-np.pi / 2, np.pi / 2, 50)
    ax.plot(bx + 0.425 * np.cos(t), by + 0.90 * np.sin(t),
            color='black', lw=1.3, zorder=5)
    ax.text(bx + 0.60, by - 1.02, 'B', fontsize=13)
    save('7.2')


# ---------------------------------------------------------------- 7.3
def fig_7_3():
    """粒子束穿过一排磁通管。p292"""
    fig = plt.figure(figsize=(5.6, 2.9))
    ax = new_ax(fig, [0.01, 0.02, 0.98, 0.96], (0, 11.6), (0, 6), 'equal')
    th = np.deg2rad(20)
    y0 = 3.0

    # 左侧 5 条竖直虚线（入射波前）
    for k in range(5):
        x = 0.9 + k * 1.05
        ax.plot([x, x], [0.4, 5.6], color='black', lw=1.0,
                ls=(0, (5, 3)))
    # 入射束流：水平虚线 + 实心箭头
    ax.plot([0.35, 5.55], [y0, y0], color='black', lw=1.1, ls=(0, (5, 3)))
    arr(ax, (5.0, y0), (5.62, y0), lw=1.4, ms=14)

    # 管列：5 个阴影圆
    for k in range(5):
        ax.add_patch(Circle((6.35, 0.95 + k * 1.02), 0.24,
                            facecolor=GRAY, edgecolor='black', lw=0.8))
    # 间距 a 标注（最下两管之间）
    arr(ax, (7.0, 0.95), (7.0, 1.97), style='<|-|>', lw=1.0, ms=9)
    ax.text(7.22, 1.28, r'$a$', fontsize=12)

    # 右侧参考水平虚线 + 偏转束流（θ 角）
    ax.plot([7.1, 11.3], [y0, y0], color='black', lw=1.0, ls=(0, (5, 3)))
    xe = 10.75
    ax.plot([7.25, xe], [y0 + 0.06, y0 + 0.06 + (xe - 7.25) * np.tan(th)],
            color='black', lw=1.1, ls=(0, (5, 3)))
    arr(ax, (xe - 0.7, y0 + 0.06 + (xe - 0.7 - 7.25) * np.tan(th)),
        (xe, y0 + 0.06 + (xe - 7.25) * np.tan(th)), lw=1.4, ms=14)
    # θ 角标注
    ax.plot([9.0, 9.0], [y0, y0 + (9.0 - 7.25) * np.tan(th) - 0.28],
            color='black', lw=0.8, ls=(0, (3, 2)))
    ax.text(9.18, y0 + 0.22, r'$\theta$', fontsize=12)

    # 右侧 4 条倾斜虚线（出射波前，与竖直方向成 θ）
    for k in range(4):
        x = 7.6 + k * 1.0
        dx = 1.35 * np.tan(th)
        ax.plot([x, x + dx], [5.6, 0.4], color='black', lw=1.0,
                ls=(0, (5, 3)))
    save('7.3')


# ---------------------------------------------------------------- 7.4
def _cut_plane(ax, x0, y0, s=1.0, shade=True, label_O=False, label_A=False):
    """带切缝的平面：上半阴影，虚线切缝，中心小洞。"""
    # 平面（透视平行四边形）
    w, d, dx = 4.4 * s, 1.05 * s, 2.2 * s   # 半宽 / 前后深 / 透视错位
    ym = y0 + d                              # 切缝高度
    yb = y0                                  # 前边
    yt = y0 + 2 * d + 0.75 * s               # 后边
    P = [(x0 - w + dx * 0.25, yb), (x0 + w - dx * 0.25, yb),
         (x0 + w + dx * 0.75, yt), (x0 - w - dx * 0.75, yt)]
    if shade:
        # 上半（阴影），边界与平面斜边相裁
        def edge_x(Pa, Pb, y):
            t = (Pa[1] - y) / (Pa[1] - Pb[1])
            return Pa[0] + t * (Pb[0] - Pa[0])
        xl = edge_x(P[3], P[0], ym)
        xr = edge_x(P[2], P[1], ym)
        ax.add_patch(Polygon([(xl, ym), (xr, ym), P[2], P[3]],
                             closed=True, facecolor=GRAY,
                             edgecolor='black', lw=0.9, zorder=1))
    ax.add_patch(Polygon(P, closed=True, facecolor='none',
                         edgecolor='black', lw=0.9, zorder=2))
    # 切缝：虚线（左段到洞、洞、右段），端点止于平面斜边
    def edge_x(Pa, Pb, y):
        t = (Pa[1] - y) / (Pa[1] - Pb[1])
        return Pa[0] + t * (Pb[0] - Pa[0])

    xl = edge_x(P[3], P[0], ym)
    xr = edge_x(P[2], P[1], ym)
    hx = x0
    ax.plot([xl, hx - 0.32 * s], [ym, ym], color='black', lw=1.2,
            ls=(0, (4, 2.4)), zorder=3)
    ax.plot([hx + 0.32 * s, xr], [ym, ym], color='black', lw=1.2,
            ls=(0, (4, 2.4)), zorder=3)
    ax.add_patch(Ellipse((hx, ym), 0.64 * s, 0.2 * s, facecolor='white',
                         edgecolor='black', lw=0.9, zorder=4))
    if label_O:
        ax.text(hx - 0.15 * s, ym - 0.42 * s, 'O', fontsize=12)
    if label_A:
        ax.text(xr - 0.1 * s, ym - 0.42 * s, 'A', fontsize=12)
    return (x0, ym, P)


def _cone(ax, cx, ytop, h=3.6, rb=1.35, seam=True, label_O=False,
          label_A=False):
    """圆锥：顶点小椭圆 O、两条母线、完整底椭圆、前母线（接缝 A）。"""
    ry = rb * 0.34
    ax.add_patch(Ellipse((cx, ytop + h), 0.5, 0.16, facecolor='white',
                         edgecolor='black', lw=0.9, zorder=5))
    ax.plot([cx - 0.25, cx - rb], [ytop + h, ytop + ry],
            color='black', lw=1.0, zorder=3)
    ax.plot([cx + 0.25, cx + rb], [ytop + h, ytop + ry],
            color='black', lw=1.0, zorder=3)
    ax.add_patch(Ellipse((cx, ytop + ry), 2 * rb, 2 * ry * 0.62,
                         facecolor='none', edgecolor='black', lw=1.0,
                         zorder=3))   # 完整底椭圆
    if seam:
        ax.plot([cx, cx + rb * 0.12], [ytop + h, ytop + ry - 0.28],
                color='black', lw=1.0, zorder=4)
        if label_A:
            ax.text(cx + rb * 0.3, ytop + ry - 0.62, 'A', fontsize=12)
    if label_O:
        ax.text(cx + 0.42, ytop + h + 0.05, 'O', fontsize=12)


def fig_7_4():
    """V_- 空间：切缝平面 → 锥。p293"""
    fig = plt.figure(figsize=(6.2, 2.1))
    ax = new_ax(fig, [0.01, 0.02, 0.98, 0.96], (0, 13.6), (0, 4.6), 'equal')
    _cut_plane(ax, 5.0, 0.45, s=0.82, shade=True, label_O=True, label_A=True)
    _cone(ax, 11.7, 0.42, h=3.3, rb=1.5, seam=True, label_O=True,
          label_A=True)
    save('7.4')


# ---------------------------------------------------------------- 7.5
def _cone_loop(ax, cx, ytop, h=3.3, rb=1.5, loops=(0.42,)):
    """圆锥 + 环绕回路（前面实线，后面虚线）；loops = 高度比列表（0=顶,1=底）。"""
    ry = rb * 0.34
    ax.add_patch(Ellipse((cx, ytop + h), 0.5, 0.16, facecolor='white',
                         edgecolor='black', lw=0.9, zorder=5))
    ax.plot([cx - 0.25, cx - rb], [ytop + h, ytop + ry],
            color='black', lw=1.0, zorder=3)
    ax.plot([cx + 0.25, cx + rb], [ytop + h, ytop + ry],
            color='black', lw=1.0, zorder=3)
    th = np.linspace(0, np.pi, 60)
    ax.plot(cx + rb * np.cos(th), ytop + ry - ry * 0.62 * np.sin(th),
            color='black', lw=1.0, zorder=3)      # 底椭圆前弧（实线）
    ax.plot(cx + rb * np.cos(th), ytop + ry + ry * 0.62 * np.sin(th),
            color='black', lw=0.9, ls=(0, (4, 3)), zorder=2.2)  # 底后弧（虚线）
    # 接缝
    ax.plot([cx, cx + rb * 0.12], [ytop + h, ytop + ry - 0.28],
            color='black', lw=1.0, zorder=4)
    # 回路椭圆（背面虚线 + 正面实线）
    for f in loops:
        yc = ytop + ry + f * (h - ry)
        wdt = rb * (1 - f) * 1.0
        hy = ry * (1 - f) * 1.05
        t = np.linspace(0, 2 * np.pi, 100)
        ax.plot(cx + wdt * np.cos(t), yc + hy * np.sin(t), color='black',
                lw=0.9, ls=(0, (4, 3)), zorder=2.2)
        m = (t > np.pi) & (t < 2 * np.pi)
        ax.plot(cx + wdt * np.cos(t[m]), yc + hy * np.sin(t[m]),
                color='black', lw=1.2, zorder=4.5)


def fig_7_5():
    """V_- 空间中 n_w = 1 与 n_w = 2 的回路。p294"""
    fig = plt.figure(figsize=(6.4, 4.3))
    # ---- 上排：n_w = 1
    ax = new_ax(fig, [0.00, 0.53, 0.56, 0.46], (-0.2, 9.0), (-0.45, 3.9),
                'equal')
    _, ym, P = _cut_plane(ax, 4.4, 0.45, s=0.72, shade=True)
    # 回路：越过洞的半椭圆 + 两端切缝下的短脚
    ax.plot([2.95, 2.95], [ym - 0.28, ym], color='black', lw=1.3)
    ax.plot([5.85, 5.85], [ym - 0.28, ym], color='black', lw=1.3)
    t = np.linspace(0, np.pi, 60)
    ax.plot(4.4 + 1.45 * np.cos(t), ym + 0.80 * np.sin(t),
            color='black', lw=1.3)
    arr(ax, (4.52, ym + 0.79), (4.95, ym + 0.775), lw=1.4, ms=13)
    ax.text(1.25, -0.3, r'$n_w = 1$', fontsize=13)

    ax = new_ax(fig, [0.55, 0.53, 0.45, 0.46], (0, 6.6), (0, 4.5), 'equal')
    _cone_loop(ax, 3.3, 0.35, h=3.5, rb=1.5, loops=(0.45,))

    # ---- 下排：n_w = 2
    ax = new_ax(fig, [0.00, 0.02, 0.56, 0.46], (-0.2, 9.0), (-0.45, 4.3),
                'equal')
    _, ym, P = _cut_plane(ax, 4.4, 0.65, s=0.72, shade=True)
    # 两个越洞弧（箭头朝左）+ 各自切缝下短脚 + 两个嵌套虚线框
    # 左弧（跨洞，左移方向）
    t = np.linspace(0, np.pi, 60)
    ax.plot(3.85 + 1.15 * np.cos(t), ym + 0.60 * np.sin(t),
            color='black', lw=1.3)
    arr(ax, (4.05, ym + 0.585), (3.65, ym + 0.575), lw=1.4, ms=13)
    ax.plot([2.70, 2.70], [ym - 0.26, ym], color='black', lw=1.3)
    ax.plot([5.00, 5.00], [ym - 0.26, ym], color='black', lw=1.3)
    # 右弧（跨洞，左移方向）
    ax.plot(5.05 + 1.05 * np.cos(t), ym + 0.50 * np.sin(t),
            color='black', lw=1.3)
    arr(ax, (5.25, ym + 0.485), (4.85, ym + 0.48), lw=1.4, ms=13)
    ax.plot([4.00, 4.00], [ym - 0.20, ym], color='black', lw=1.3)
    ax.plot([6.10, 6.10], [ym - 0.20, ym], color='black', lw=1.3)
    # 虚线框（绕洞下方折返）
    for xa, xb, dep in ((2.70, 5.00, 0.55), (4.00, 6.10, 0.30)):
        ax.plot([xa, xa, xb, xb], [ym, ym - dep, ym - dep, ym],
                color='black', lw=1.0, ls=(0, (4, 2.6)))
    ax.text(1.3, -0.32, r'$n_w = 2$', fontsize=13)

    ax = new_ax(fig, [0.55, 0.02, 0.45, 0.46], (0, 6.6), (0, 4.5), 'equal')
    _cone_loop(ax, 3.3, 0.35, h=3.5, rb=1.5, loops=(0.45, 0.75))
    save('7.5')


# ---------------------------------------------------------------- 7.6
def fig_7_6():
    """两任意子在二维谐振子势阱中的能级与简并度。p295（漏抓图）"""
    fig = plt.figure(figsize=(6.0, 4.1))
    ax = fig.add_axes([0.10, 0.20, 0.88, 0.78])
    ax.set_xlim(0, 6.8)
    ax.set_ylim(-0.15, 6.9)
    ax.set_axis_off()
    # 坐标轴
    ax_spine(ax, (0, 0), (0, 6.55), lw=1.2)
    ax_spine(ax, (0, 0), (6.6, 0), lw=1.2)
    ax.text(-0.42, 6.3, r'$E$', fontsize=13)

    cols = [0.9, 2.5, 4.15, 5.75]           # 各列中心
    wdt = 0.62                               # 能级线半长
    lev1 = {E: E for E in (1, 2, 3, 4, 5, 6)}
    lev2 = {1: 1, 3: 3, 5: 5}
    lev3 = {1.12: 1, 2.25: 1, 3.40: 2, 4.50: 2, 5.62: 3}
    lev4 = {2: 2, 4: 4, 6: 6}
    data = [lev1, lev2, lev3, lev4]

    def draw_col(xc, lv):
        for E, D in lv.items():
            ax.plot([xc - wdt, xc + wdt], [E, E], color='black', lw=1.3)
            ax.text(xc, E + 0.14, rf'$D = {D}$', fontsize=11.5,
                    ha='center', va='bottom')

    for xc, lv in zip(cols, data):
        draw_col(xc, lv)

    # 演化箭头（列2→列3、列3→列4）
    def arw(p, q):
        arr(ax, p, q, lw=1.1, ms=11)

    arw((cols[1] + wdt + 0.05, 5), (cols[2] - wdt - 0.10, 5.52))
    arw((cols[1] + wdt + 0.05, 5), (cols[2] - wdt - 0.10, 4.60))
    arw((cols[1] + wdt + 0.05, 3), (cols[2] - wdt - 0.10, 3.32))
    arw((cols[1] + wdt + 0.05, 3), (cols[2] - wdt - 0.10, 2.32))
    arw((cols[1] + wdt + 0.05, 1), (cols[2] - wdt - 0.10, 1.06))
    arw((cols[2] + wdt + 0.05, 5.62), (cols[3] - wdt - 0.10, 6.0))
    arw((cols[2] + wdt + 0.05, 4.50), (cols[3] - wdt - 0.10, 4.06))
    arw((cols[2] + wdt + 0.05, 3.40), (cols[3] - wdt - 0.10, 3.94))
    arw((cols[2] + wdt + 0.05, 2.25), (cols[3] - wdt - 0.10, 2.06))
    arw((cols[2] + wdt + 0.05, 1.12), (cols[3] - wdt - 0.10, 1.94))

    labs = [('Two-dimensional', 'oscillator'),
            ('Two', 'bosons', r'$\theta = 0$'),
            ('Two', 'anyons', r'$\theta = 2\pi/3$'),
            ('Two', 'fermions', r'$\theta = \pi$')]
    for xc, lab in zip(cols, labs):
        for k, s in enumerate(lab):
            ax.text(xc, -0.62 - 0.42 * k, s, fontsize=11.5, ha='center')
    save('7.6')


# ---------------------------------------------------------------- 7.7
def _loop_rect(ax, xa, xb, y0):
    """绕两粒子的圆角矩形交换回路，返回路径点列。"""
    xa_, xb_ = xa - 0.62, xb + 0.62
    yb, yt, r = y0 - 0.95, y0 + 0.95, 0.42
    seg = []
    # 左边直线（下→上）
    seg += [[xa_, yb + r], [xa_, yt - r]]
    # 左上圆角（180°→90°）
    t = np.linspace(np.pi, np.pi / 2, 12)
    seg += np.column_stack([xa_ + r + r * np.cos(t),
                            yt - r + r * np.sin(t)]).tolist()
    # 上边直线（左→右）
    seg += [[xa_ + r, yt], [xb_ - r, yt]]
    # 右上圆角（90°→0°）
    t = np.linspace(np.pi / 2, 0, 12)
    seg += np.column_stack([xb_ - r + r * np.cos(t),
                            yt - r + r * np.sin(t)]).tolist()
    # 右边直线（上→下）
    seg += [[xb_, yt - r], [xb_, yb + r]]
    # 右下圆角（0°→-90°）
    t = np.linspace(0, -np.pi / 2, 12)
    seg += np.column_stack([xb_ - r + r * np.cos(t),
                            yb + r + r * np.sin(t)]).tolist()
    # 下边直线（右→左）
    seg += [[xb_ - r, yb], [xa_ + r, yb]]
    # 左下圆角（-90°→180°）
    t = np.linspace(-np.pi / 2, -np.pi, 12)
    seg += np.column_stack([xa_ + r + r * np.cos(t),
                            yb + r + r * np.sin(t)]).tolist()
    return np.array(seg)


def fig_7_7():
    """交换回路 C_1 与 C_-1 可经绕轴转动连续相互变换。p296"""
    fig = plt.figure(figsize=(6.2, 2.0))
    ax = new_ax(fig, [0.01, 0.03, 0.98, 0.94], (0, 13.2), (0, 4.2), 'equal')

    def panel(x0, C_lab, top_dx, bot_dx, axis=False, rot=False):
        xa, xb, y0 = x0 + 0.8, x0 + 3.3, 2.1
        if axis:
            ax.plot([xa - 1.35, xb + 1.35], [y0, y0], color='black', lw=0.9)
        ax.add_patch(Circle((xa, y0), 0.14, facecolor='black'))
        ax.add_patch(Circle((xb, y0), 0.14, facecolor='black'))
        # 圆角矩形回路
        seg = _loop_rect(ax, xa, xb, y0)
        ax.plot(seg[:, 0], seg[:, 1], color='black', lw=1.2)
        # 箭头：上边与下边
        if top_dx > 0:
            arr(ax, (x0 + 1.55, y0 + 0.95), (x0 + 2.05, y0 + 0.95), lw=1.5, ms=15)
        else:
            arr(ax, (x0 + 2.05, y0 + 0.95), (x0 + 1.55, y0 + 0.95), lw=1.5, ms=15)
        if bot_dx > 0:
            arr(ax, (x0 + 1.55, y0 - 0.95), (x0 + 2.05, y0 - 0.95), lw=1.5, ms=15)
        else:
            arr(ax, (x0 + 2.05, y0 - 0.95), (x0 + 1.55, y0 - 0.95), lw=1.5, ms=15)
        ax.text((xa + xb) / 2, y0 - 0.12, C_lab, fontsize=13)
        if rot:  # 旋转指示小椭圆
            ex = xa - 1.15
            t = np.linspace(0.15 * np.pi, 1.9 * np.pi, 60)
            ax.plot(ex + 0.30 * np.cos(t), y0 + 0.78 * np.sin(t),
                    color='black', lw=0.9)
            arr(ax, (ex + 0.10, y0 - 0.72), (ex + 0.22, y0 - 0.44),
                lw=1.1, ms=10)

    panel(0.3, r'$C_1$', +1, -1)
    panel(6.9, r'$C_{-1}$', -1, +1, axis=True, rot=True)
    save('7.7')


# ---------------------------------------------------------------- 7.8
def fig_7_8():
    """通量-电荷束缚态绕行一周的相位 = 两项之和。p296"""
    fig = plt.figure(figsize=(6.4, 1.75))
    ax = new_ax(fig, [0.01, 0.04, 0.98, 0.92], (0, 14.2), (0, 3.9), 'equal')

    def bs(x, y, dot=True):
        """束缚态：⊗（通量）+ 右上实心点（电荷）。"""
        ax.add_patch(Circle((x, y), 0.30, facecolor='white',
                            edgecolor='black', lw=1.0, zorder=4))
        d = 0.30 / np.sqrt(2)
        ax.plot([x - d, x + d], [y - d, y + d], color='black', lw=1.0,
                zorder=5)
        ax.plot([x - d, x + d], [y + d, y - d], color='black', lw=1.0,
                zorder=5)
        if dot:
            ax.add_patch(Circle((x + 0.46, y + 0.42), 0.12,
                                facecolor='black', zorder=5))

    def flux(x, y):
        """裸 ⊗（通量，无电荷点）。"""
        bs(x, y, dot=False)

    def arc(x1, x2, yb, h, lw=1.2):
        t = np.linspace(0, np.pi, 60)
        xx = np.linspace(x1, x2, 60)
        yy = yb + h * np.sin(t)
        ax.plot(xx, yy, color='black', lw=lw)
        return xx, yy

    # 左：大弧，从右侧束缚态上方跨到左侧，箭头指向左下
    bs(3.6, 1.15)
    bs(6.3, 1.15)
    arc(2.0, 6.6, 1.35, 1.85)
    arr(ax, (2.06, 2.16), (1.68, 1.72), lw=1.4, ms=14)
    ax.text(7.75, 1.35, r'=', fontsize=20)

    # 项一：⊗ 在左、· 在右
    flux(9.5, 1.05)
    ax.add_patch(Circle((10.4, 1.05), 0.12, facecolor='black', zorder=5))
    arc(8.35, 10.65, 1.25, 1.15)
    arr(ax, (8.42, 1.62), (8.10, 1.30), lw=1.4, ms=14)
    ax.text(11.15, 1.02, r'+', fontsize=18)

    # 项二：· 在左、⊗ 在右
    ax.add_patch(Circle((12.15, 1.05), 0.12, facecolor='black', zorder=5))
    flux(13.5, 1.05)
    arc(11.65, 13.75, 1.25, 1.15)
    arr(ax, (11.72, 1.62), (11.40, 1.30), lw=1.4, ms=14)
    save('7.8')


# ---------------------------------------------------------------- 7.9
def fig_7_9():
    """霍尔电阻 ρ_xy 随 B 的变化（经典线性段 + 量子平台）。p298"""
    fig = plt.figure(figsize=(4.6, 3.6))
    ax = fig.add_axes([0.13, 0.13, 0.84, 0.84])
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 8.6)
    ax.set_axis_off()
    ax_spine(ax, (0.4, 0.4), (0.4, 8.3), lw=1.1)
    ax_spine(ax, (0.4, 0.4), (10.3, 0.4), lw=1.1)
    ax.text(0.05, 8.45, r'$\rho_{xy}$', fontsize=13)
    ax.text(9.95, 0.0, r'$B$', fontsize=13)

    from scipy.interpolate import CubicSpline
    pts = np.array([(0.4, 0.4), (1.5, 1.5), (2.2, 2.2), (2.9, 2.62),
                    (3.6, 2.78), (4.6, 2.86), (5.2, 3.35), (5.8, 3.85),
                    (6.6, 4.02), (7.6, 4.1), (8.2, 4.75), (8.7, 5.9),
                    (9.1, 7.1), (9.35, 8.15)], float)
    cs = CubicSpline(pts[:, 0], pts[:, 1])
    x = np.linspace(0.4, 9.35, 400)
    ax.plot(x, cs(x), color='black', lw=1.5)

    # 经典区域圆圈
    ax.add_patch(Circle((1.35, 1.35), 1.15, facecolor='none',
                        edgecolor='black', lw=0.9))
    ax.text(0.55, -0.55, 'Classical', fontsize=12.5)
    ax.text(5.0, 5.35, 'Quantum', fontsize=12.5)
    save('7.9')


# ---------------------------------------------------------------- 7.10
def fig_7_10():
    """第零朗道能级中的圆形轨道 + 单轨道波函数。p301"""
    fig = plt.figure(figsize=(6.3, 2.6))
    # 左：同心圆轨道
    ax = new_ax(fig, [0.00, 0.02, 0.44, 0.96], (0, 5.6), (0, 4.6), 'equal')
    cx, cy = 2.15, 2.2
    rs = np.arange(0.62, 2.12, 0.25)
    for r in rs:
        ax.add_patch(Circle((cx, cy), r, facecolor='none',
                            edgecolor='black', lw=0.9))
    ax.text(3.55, 3.95, r'Area = $2\pi l_B^2$', fontsize=11.5)
    # 6 支细箭头自标注处扇形展开指向各环形面积（外圈→内圆），互不交叉
    mids = [0.30] + [(r0 + r1) / 2 for r0, r1 in zip(rs[:-1], rs[1:])]
    tip_ang = np.deg2rad(133)
    for k, rm_ in enumerate(mids[::-1]):        # 外圈箭头在上、内圆箭头在下
        tp = (cx + rm_ * np.cos(tip_ang), cy + rm_ * np.sin(tip_ang))
        st = (3.72 - 0.12 * k, 3.70 - 0.24 * k)
        arr(ax, st, tp, lw=0.8, ms=9)

    # 右：|psi_m| 在 r_m 处的峰
    ax = fig.add_axes([0.47, 0.14, 0.51, 0.84])
    ax.set_xlim(-0.4, 4.4)
    ax.set_ylim(0, 1.55)
    ax.set_axis_off()
    ax.set_aspect(1.6)
    ax_spine(ax, (0, 0), (0, 1.42), lw=1.1)
    ax_spine(ax, (0, 0), (4.25, 0), lw=1.1)
    ax.text(-0.32, 1.48, r'$|\psi_m|$', fontsize=12, ha='left')
    rm = 2.9
    x = np.linspace(0.2, 4.2, 400)
    y = 0.72 * np.exp(-((x - rm) / 0.50) ** 4)
    ax.plot(x, y, color='black', lw=1.3)
    # l_B 宽度标注
    for xe in (rm - 0.30, rm + 0.30):
        ax.plot([xe, xe], [0.56, 0.84], color='black', lw=0.9)
    arr(ax, (rm - 1.05, 0.70), (rm - 0.33, 0.70), lw=1.0, ms=10)
    arr(ax, (rm + 1.05, 0.70), (rm + 0.33, 0.70), lw=1.0, ms=10)
    ax.text(rm, 0.70, r'$l_B$', fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='none', pad=1))
    ax.text(rm, -0.13, r'$r_m$', fontsize=12, ha='center', va='top')
    save('7.10')


# ---------------------------------------------------------------- 7.11
def fig_7_11():
    """nu=1 液滴：填充前 m 个轨道（粗线）+ 密度分布。p301"""
    fig = plt.figure(figsize=(6.3, 2.5))
    # 左：同心圆（外圈细线、内 m 圈粗线）
    ax = new_ax(fig, [0.00, 0.02, 0.44, 0.96], (0, 5.6), (0, 4.6), 'equal')
    cx, cy = 2.35, 2.35
    for r in (2.25, 2.08):
        ax.add_patch(Circle((cx, cy), r, facecolor='none',
                            edgecolor='black', lw=0.9))
    for r in (1.86, 1.62, 1.38, 1.14):
        ax.add_patch(Circle((cx, cy), r, facecolor='none',
                            edgecolor='black', lw=2.0))
    rm = 1.86
    arr(ax, (cx, cy), (cx + rm * 0.72, cy + rm * 0.72), lw=0.9, ms=10)
    ax.text(cx + rm * 0.72 + 0.42, cy + rm * 0.72 + 0.18, r'$r_m$',
            fontsize=12)
    # 右：密度平台 + 边缘下降
    ax = fig.add_axes([0.47, 0.14, 0.51, 0.84])
    ax.set_xlim(-0.3, 4.5)
    ax.set_ylim(0, 1.55)
    ax.set_axis_off()
    ax.set_aspect(1.6)
    ax_spine(ax, (0, 0), (0, 1.42), lw=1.1)
    ax_spine(ax, (0, 0), (4.35, 0), lw=1.1)
    ax.text(-0.24, 1.48, r'$\rho$', fontsize=12)
    ax.text(4.28, -0.12, r'$r$', fontsize=12, va='top')
    x = np.linspace(0, 4.2, 400)
    y = np.where(x < 3.1, 0.68, 0.68 * 0.5 *
                 (1 + np.cos(np.clip((x - 3.1) / 0.9, 0, 1) * np.pi)))
    y = np.where(x > 4.0, 0.0, y)
    ax.plot(x, y, color='black', lw=1.3)
    ax.text(1.1, 0.76, r'$\nu = 1$', fontsize=11.5)
    for xe in (3.32, 3.86):
        ax.plot([xe, xe], [0.95, 1.28], color='black', lw=0.9)
    arr(ax, (2.85, 1.12), (3.29, 1.12), lw=1.0, ms=10)
    arr(ax, (4.35, 1.12), (3.91, 1.12), lw=1.0, ms=10)
    ax.text(3.59, 1.12, r'$l_B$', fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='none', pad=1))
    save('7.11')


# ---------------------------------------------------------------- 7.12
def fig_7_12():
    """nu=1/3 液滴的密度分布（边缘振荡）。p302"""
    fig = plt.figure(figsize=(5.0, 2.6))
    ax = fig.add_axes([0.11, 0.15, 0.87, 0.83])
    ax.set_xlim(-0.3, 6.1)
    ax.set_ylim(-0.15, 1.45)
    ax.set_axis_off()
    ax.set_aspect(2.6)
    ax_spine(ax, (0, -0.1), (0, 1.36), lw=1.1)
    ax_spine(ax, (0, -0.1), (5.95, -0.1), lw=1.1)
    ax.text(-0.26, 1.38, r'$\rho$', fontsize=12)
    ax.text(5.86, -0.2, r'$r$', fontsize=12, va='top')

    rho0 = 0.62
    xs = [0.0, 1.9, 2.3, 2.6, 2.9, 3.15, 3.45, 3.7, 3.95, 4.2, 4.5, 4.95,
          5.4, 5.75]
    ys = [rho0, rho0, rho0 - 0.10, rho0 + 0.06, rho0 + 0.08, rho0 - 0.16,
          rho0 + 0.02, rho0 + 0.24, rho0 + 0.10, rho0 - 0.08, 0.14,
          0.05, 0.01, 0.0]
    from scipy.interpolate import PchipInterpolator
    cs = PchipInterpolator(xs, ys)
    x = np.linspace(0, 5.75, 500)
    y = np.clip(cs(x), -0.06, 1.2)
    y[x < 0.15] = rho0
    y = np.clip(y, 0, 1.2)
    ax.plot(x, y, color='black', lw=1.3)
    ax.text(1.0, rho0 + 0.10, r'$\nu = 1/3$', fontsize=11.5)
    # l_B 标注（在大峰顶部两侧）
    for xe in (3.72, 4.28):
        ax.plot([xe, xe], [0.95, 1.26], color='black', lw=0.9)
    arr(ax, (3.30, 1.10), (3.69, 1.10), lw=1.0, ms=10)
    arr(ax, (4.70, 1.10), (4.31, 1.10), lw=1.0, ms=10)
    ax.text(4.00, 1.10, r'$l_B$', fontsize=12, ha='center', va='center',
            bbox=dict(facecolor='white', edgecolor='none', pad=1))
    save('7.12')


# ---------------------------------------------------------------- 7.13
def fig_7_13():
    """电子电荷 + 测试电荷中和背景电荷（等离子体类比）。p305"""
    fig = plt.figure(figsize=(6.0, 2.0))
    ax = fig.add_axes([0.02, 0.05, 0.96, 0.93])
    ax.set_xlim(0, 12.6)
    ax.set_ylim(-0.9, 2.6)
    ax.set_axis_off()
    ax.set_aspect(2.4)
    base, top = 0.0, 1.15

    xs = np.linspace(0, 12.4, 700)

    def sm(x, a, b):
        """S 形上升 0→1。"""
        t = np.clip((x - a) / (b - a), 0, 1)
        return 0.5 - 0.5 * np.cos(t * np.pi)

    y = top * (sm(xs, 0.8, 2.3) - sm(xs, 9.4, 10.9))
    # 中间下探的准空穴凹陷
    dip_c, dip_w = 5.55, 0.45
    dip = -top * np.exp(-((xs - dip_c) / dip_w) ** 4) * \
        (np.abs(xs - dip_c) < 1.0)
    y = y + dip
    ax.plot(xs, y + 0.3, color='black', lw=1.3)
    ax.plot([0, 12.4], [0.3, 0.3], color='black', lw=0.8)
    # 凹陷区灰色填充（顶=平台线）
    m = (np.abs(xs - dip_c) < 1.0) & (y < top - 0.01)
    ax.fill_between(xs[m], (y + 0.3)[m], (top + 0.3) * np.ones(m.sum()),
                    color=GRAY, lw=0)
    # 左右参考横线 + 高度双箭头
    ax.plot([0.5, 2.1], [top + 0.3, top + 0.3], color='black', lw=1.1)
    ax.plot([10.6, 12.2], [top + 0.3, top + 0.3], color='black', lw=1.1)
    arr(ax, (0.85, 0.3), (0.85, top + 0.3), style='<|-|>', lw=0.9, ms=8)
    ax.text(1.65, 2.28, "Background\n'charge' density", fontsize=10.5,
            ha='center', va='bottom')
    ax.text(dip_c, 2.28, "Test\n'charge'", fontsize=10.5,
            ha='center', va='bottom')
    ax.text(dip_c, -0.12, 'Charge $1/m$\nquasiparticle', fontsize=10.5,
            ha='center', va='top')
    save('7.13')


# ---------------------------------------------------------------- 7.14
def _droplet(ax, xc, base=0.0, w=2.6, top=0.55, edge=0.55):
    """液滴轮廓：S 上升-平台-S 下降，返回 (xs, ys)。"""
    xs = np.linspace(xc - w / 2, xc + w / 2, 500)
    t1, t2 = xc - w / 2 + edge, xc + w / 2 - edge

    def sm(x, a, b, up=True):
        t = np.clip((x - a) / (b - a), 0, 1)
        v = 0.5 - 0.5 * np.cos(t * np.pi)
        return v if up else 1 - v

    y = top * (sm(xs, xc - w / 2, t1) * sm(xs, t2, xc + w / 2, up=False))
    return xs, y


def fig_7_14():
    """分级 nu=2/7 与 nu=2/5 态（四个液滴密度图）。p308"""
    fig = plt.figure(figsize=(6.6, 2.9))
    pos = [[0.005, 0.52, 0.475, 0.46], [0.52, 0.52, 0.475, 0.46],
           [0.005, 0.02, 0.475, 0.46], [0.52, 0.02, 0.475, 0.46]]

    def frame(ax):
        ax.set_xlim(-0.25, 4.35)
        ax.set_ylim(-0.28, 1.25)
        ax.set_axis_off()
        ax.set_aspect(2.3)
        ax.plot([-0.1, 3.4], [0, 0], color='black', lw=0.8)

    mode = ['dips', 'bumps', 'band_dn', 'band_up']
    for ax_pos, md in zip(pos, mode):
        ax = fig.add_axes(ax_pos)
        frame(ax)
        xc = 1.55
        xs, y = _droplet(ax, xc)
        ax.plot(xs, y, color='black', lw=1.2)
        top = 0.55
        if md == 'dips':
            for x0 in (0.75, 1.3, 1.85, 2.4):
                m = np.abs(xs - x0) < 0.22
                yd = top - 0.16 * np.exp(-((xs[m] - x0) / 0.10) ** 2)
                ax.plot(xs[m], yd, color='black', lw=1.1)
                ax.fill_between(xs[m], yd, top, color=GRAY, lw=0)
            ax.plot([3.02, 3.95], [top, top], color='black', lw=1.0)
            ax.text(3.5, top - 0.13, r'$\nu = 1/3$', fontsize=10.5,
                    ha='center')
        elif md == 'bumps':
            for x0 in (0.75, 1.3, 1.85, 2.4):
                m = np.abs(xs - x0) < 0.30
                yb = top + 0.13 * np.exp(-((xs[m] - x0) / 0.12) ** 2)
                ax.plot(xs[m], yb, color='black', lw=1.1)
                ax.fill_between(xs[m], top, yb, color=GRAY, lw=0)
            ax.plot([3.02, 3.95], [top, top], color='black', lw=1.0)
            ax.text(3.5, top - 0.13, r'$\nu = 1/3$', fontsize=10.5,
                    ha='center')
        elif md == 'band_dn':
            m = np.abs(xs - xc) < 0.98
            yd = top - 0.10 * (0.5 + 0.5 *
                               np.cos(np.clip((np.abs(xs[m] - xc)) / 0.98,
                                              0, 1) * np.pi))
            ax.plot(xs[m], yd, color='black', lw=1.1)
            ax.fill_between(xs[m], yd, top, color=GRAY, lw=0)
            ax.text(xc, 0.20, r'$\nu = 2/7$', fontsize=10.5, ha='center')
            ax.plot([3.02, 3.95], [top, top], color='black', lw=1.0)
            ax.text(3.5, top - 0.13, r'$\nu = 1/3$', fontsize=10.5,
                    ha='center')
        else:
            m = np.abs(xs - xc) < 1.05
            yb = top + 0.10 * (0.5 + 0.5 *
                               np.cos(np.clip((np.abs(xs[m] - xc)) / 1.05,
                                              0, 1) * np.pi))
            ax.plot(xs[m], yb, color='black', lw=1.1)
            ax.fill_between(xs[m], top, yb, color=GRAY, lw=0)
            ax.text(xc, 0.80, r'$\nu = 2/5$', fontsize=10.5, ha='center')
            ax.plot([3.02, 3.95], [top, top], color='black', lw=1.0)
            ax.text(3.5, top - 0.13, r'$\nu = 1/3$', fontsize=10.5,
                    ha='center')
    save('7.14')


# ---------------------------------------------------------------- 7.15
def fig_7_15():
    """头三个朗道能级在光滑势 V(r) 下的能级（角动量 m）。p325"""
    fig = plt.figure(figsize=(6.4, 3.0))
    ax = fig.add_axes([0.07, 0.16, 0.60, 0.82])
    ax.set_xlim(-1.7, 10.3)
    ax.set_ylim(-0.45, 4.3)
    ax.set_axis_off()
    ax.set_aspect(1.05)
    # 坐标轴
    ax_spine(ax, (0, -0.25), (0, 4.1), lw=1.1)
    ax_spine(ax, (-0.25, -0.25), (10.1, -0.25), lw=1.1)
    ax.text(-0.5, 3.95, r'$E$', fontsize=13)
    ax.text(9.85, -0.42, r'$m$', fontsize=13)
    for k in range(4):
        ax.text(k, -0.58, str(k), fontsize=11, ha='center')
    ax.text(3.5, -0.58, r'$\cdots$', fontsize=11, ha='center')
    # 化学势 mu（虚线）
    ax.plot([-0.25, 10.1], [1.05, 1.05], color='black', lw=0.9,
            ls=(0, (5, 3)))
    ax.text(-0.62, 1.05, r'$\mu$', fontsize=13, va='center')

    m_edge = 6.2   # 边缘起始
    for base, fill, m0 in ((0.55, True, 0.0),
                           (1.78, False, -1.1),
                           (3.0, False, -1.1)):
        # 平段 + 上升曲线
        xs = np.linspace(m0, 8.6, 300)
        rise = np.clip(xs - m_edge, 0, None) ** 2 * 0.135
        ys = base + rise
        ax.plot(xs, ys, color='black', lw=0.9, zorder=2)
        # 珠子
        if fill:
            ms_ = np.arange(0, 5.9, 0.55)
            for m_ in ms_:
                ax.add_patch(Circle((m_, base), 0.105, facecolor='black',
                                    zorder=4))
            # 上升段的实心珠子（越过化学势前）
            for m_ in (6.35, 6.85, 7.35, 7.85):
                y_ = base + (m_ - m_edge) ** 2 * 0.135
                ax.add_patch(Circle((m_, y_), 0.105, facecolor='black',
                                    zorder=4))
            # 边缘激发的空心珠子
            for m_ in (8.45, 9.0):
                y_ = base + (m_ - m_edge) ** 2 * 0.135
                ax.add_patch(Circle((m_, y_), 0.105, facecolor='white',
                                    edgecolor='black', lw=1.0, zorder=4))
        else:
            ms_ = np.arange(m0, 5.9, 0.55)
            for m_ in ms_:
                ax.add_patch(Circle((m_, base), 0.105, facecolor='white',
                                    edgecolor='black', lw=1.0, zorder=4))
            for m_ in (6.35, 6.95, 7.55):
                y_ = base + (m_ - m_edge) ** 2 * 0.135
                ax.add_patch(Circle((m_, y_), 0.105, facecolor='white',
                                    edgecolor='black', lw=1.0, zorder=4))
    # omega_c 双箭头（顶两行之间）
    arr(ax, (2.3, 1.78), (2.3, 3.0), style='<|-|>', lw=1.0, ms=9)
    ax.text(2.48, 2.39, r'$\omega_c$', fontsize=12)
    # Bulk excitation 箭头
    arr(ax, (1.0, 0.72), (1.0, 1.6), lw=1.0, ms=10)
    ax.text(1.25, 0.80, 'Bulk excitation', fontsize=10.5)
    # Edge excitation 弯箭头
    ax.annotate('', xy=(8.45, 1.55), xytext=(7.0, 0.95),
                arrowprops=dict(arrowstyle='-|>', lw=1.0, mutation_scale=10,
                                color='black',
                                connectionstyle='arc3,rad=-0.35'))
    ax.text(4.25, 0.80, 'Edge excitation', fontsize=10.5)

    # 右侧小图：圆形轨道，r_m 与 k 方向
    ax2 = fig.add_axes([0.70, 0.10, 0.28, 0.86])
    ax2.set_xlim(-1.6, 1.6)
    ax2.set_ylim(-1.6, 1.6)
    ax2.set_aspect('equal')
    ax2.set_axis_off()
    ax2.add_patch(Circle((0, 0), 1.25, facecolor='none',
                         edgecolor='black', lw=1.0))
    arr(ax2, (0, 0), (0.66, -0.66), lw=0.9, ms=10)
    ax2.text(0.82, -0.62, r'$r_m$', fontsize=11.5)
    t = np.linspace(np.deg2rad(-75), np.deg2rad(-25), 30)
    ax2.plot(1.42 * np.cos(t), 1.42 * np.sin(t), color='black', lw=0.9)
    arr(ax2, (1.42 * np.cos(np.deg2rad(-40)), 1.42 * np.sin(np.deg2rad(-40))),
        (1.42 * np.cos(np.deg2rad(-27)), 1.42 * np.sin(np.deg2rad(-27))),
        lw=0.9, ms=10)
    ax2.text(1.12, -1.35, r'$k$', fontsize=11.5)
    save('7.15')


# ---------------------------------------------------------------- 7.16
def fig_7_16():
    """(a) 手征费米液体 E(k)（只有右移）(b) 一般费米液体（左右移）。p326"""
    fig = plt.figure(figsize=(6.3, 2.3))
    # ---- (a)
    ax = fig.add_axes([0.055, 0.14, 0.40, 0.82])
    ax.set_xlim(-0.25, 2.9)
    ax.set_ylim(-0.3, 2.5)
    ax.set_axis_off()
    ax.set_aspect(0.85)
    ax_spine(ax, (0, -0.15), (0, 2.3), lw=1.0)
    ax_spine(ax, (-0.15, -0.15), (2.75, -0.15), lw=1.0)
    ax.text(-0.2, 2.32, r'$E$', fontsize=12)
    ax.text(2.68, -0.3, r'$k$', fontsize=12, va='top')
    kF, EF = 1.55, 1.35
    x = np.linspace(0, 2.35, 300)
    y = 0.18 + 0.09 * x + 0.30 * x ** 2.4
    ax.plot(x, y, color='black', lw=1.0)
    m = y >= EF
    ax.plot(x[m], y[m], color='black', lw=2.0)
    ax.plot([0.55, 2.15], [EF, EF], color='black', lw=0.8, ls=(0, (4, 3)))
    ax.plot([kF, kF], [-0.15, EF + 0.35], color='black', lw=0.8,
            ls=(0, (4, 3)))
    ax.text(kF, -0.32, r'$k_F$', fontsize=11, ha='center', va='top')
    ax.text(0.62, 0.42, 'Filled', fontsize=11)
    ax.text(1.68, 1.78, 'Right\nmover', fontsize=11)
    ax.text(-0.62, 2.42, '(a)', fontsize=12)

    # ---- (b)
    ax = fig.add_axes([0.50, 0.14, 0.46, 0.82])
    ax.set_xlim(-2.9, 2.9)
    ax.set_ylim(-0.5, 2.6)
    ax.set_axis_off()
    ax.set_aspect(0.85)
    ax_spine(ax, (0, -0.25), (0, 2.4), lw=1.0)
    ax_spine(ax, (-2.6, -0.25), (2.6, -0.25), lw=1.0)
    ax.text(0.12, 2.32, r'$E$', fontsize=12)
    ax.text(2.5, -0.42, r'$k$', fontsize=12, va='top')
    kF = 1.35
    EF = 0.42 + 0.42 * kF ** 2
    x = np.linspace(-2.05, 2.05, 300)
    y = 0.42 + 0.42 * x ** 2
    ax.plot(x, y, color='black', lw=1.0)
    m = y >= EF
    xt = np.where(m, x, np.nan)      # 断开左右两支，避免中段连线
    ax.plot(xt, y, color='black', lw=2.0)
    ax.plot([-1.9, 1.9], [EF, EF], color='black', lw=0.8, ls=(0, (4, 3)))
    for s in (-1, 1):
        ax.plot([s * kF, s * kF], [-0.25, EF + 0.3], color='black', lw=0.8,
                ls=(0, (4, 3)))
        ax.text(s * kF, -0.42, ('-' if s < 0 else '') + r'$k_F$',
                fontsize=11, ha='center', va='top')
    ax.text(-2.35, 1.72, 'Left\nmover', fontsize=11)
    ax.text(1.42, 1.72, 'Right\nmover', fontsize=11)
    ax.text(0, 0.85, 'Filled', fontsize=11, ha='center')
    ax.text(-2.72, 2.42, '(b)', fontsize=12)
    save('7.16')


# ---------------------------------------------------------------- 7.17
def fig_7_17():
    """六电子体系前 22 个轨道的能谱 H_V（M=45..51 零能态简并度
    1,1,2,3,5,7,11）。p333（漏抓图）"""
    rng = np.random.RandomState(11)
    fig = plt.figure(figsize=(4.9, 3.7))
    ax = fig.add_axes([0.13, 0.13, 0.85, 0.84])
    ax.set_xlim(34.2, 54.2)
    ax.set_ylim(-0.06, 1.06)
    # 框 + 刻度
    for s in ax.spines.values():
        s.set_visible(True)
        s.set_linewidth(0.9)
    ax.set_xticks(range(35, 55), minor=True)
    ax.set_xticks([40, 50])
    ax.set_yticks([0, 1])
    ax.set_yticks(np.arange(0.1, 1.0, 0.1), minor=True)
    ax.tick_params(direction='in', which='both', length=4)
    ax.tick_params(which='minor', length=2.2)
    ax.set_xlabel(r'$M$', fontsize=12)
    ax.set_ylabel('Energy', fontsize=12)

    top_of = {35: 1.0, 36: 1.0, 37: .99, 38: .98, 39: .96, 40: .93,
              41: .90, 42: .86, 43: .80, 44: .74, 45: .68, 46: .62,
              47: .56, 48: .51, 49: .47, 50: .43, 51: .39, 52: .36,
              53: .33}
    bot_of = {35: .53, 36: .48, 37: .45, 38: .42, 39: .39, 40: .36,
              41: .34, 42: .31, 43: .28, 44: .26, 45: .24, 46: .22,
              47: .20, 48: .19, 49: .18, 50: .17, 51: .16, 52: .155,
              53: .15}
    cnt = {35: 6, 36: 8, 37: 9, 38: 10, 39: 12, 40: 14, 41: 16, 42: 18,
           43: 20, 44: 22, 45: 24, 46: 26, 47: 28, 48: 30, 49: 32,
           50: 33, 51: 34, 52: 35, 53: 36}
    zero = {45: 1, 46: 1, 47: 2, 48: 3, 49: 5, 50: 7, 51: 11}

    for M in range(35, 54):
        lo, hi = bot_of[M], top_of[M]
        n = cnt[M]
        Es = np.sort(rng.uniform(lo, hi, n))
        ax.hlines(Es, M - 0.38, M + 0.38, color='black', lw=1.1)
        if M in zero:
            Es0 = 0.004 + 0.0085 * np.arange(zero[M])
            ax.hlines(Es0, M - 0.38, M + 0.38, color='black', lw=1.1)
    save('7.17')


# ---------------------------------------------------------------- 7.18
def fig_7_18():
    """(a) 同一 FQH 态两边缘间准粒子隧穿 (b) 不同 FQH 态边缘间电子隧穿。
    p347"""
    fig = plt.figure(figsize=(6.0, 2.3))
    # ---- (a) 左右两个三角（灰），中心点接触
    ax = new_ax(fig, [0.01, 0.05, 0.47, 0.90], (0, 9.4), (0, 4.3), 'equal')
    ax.add_patch(Polygon([(1.5, 3.6), (5.0, 2.15), (1.5, 0.7)], closed=True,
                         facecolor=GRAY, edgecolor='black', lw=0.8))
    ax.add_patch(Polygon([(8.5, 3.6), (5.0, 2.15), (8.5, 0.7)], closed=True,
                         facecolor=GRAY, edgecolor='black', lw=0.8))
    arr(ax, (0.8, 0.7), (0.8, 3.6), style='<|-|>', lw=0.9, ms=9)
    ax.text(0.45, 2.15, r'$V$', fontsize=12, ha='right', va='center')
    arr(ax, (5.0, 3.0), (5.0, 2.25), lw=1.1, ms=11)
    ax.text(4.7, 2.62, r'$I$', fontsize=12, ha='right')
    ax.text(5.85, 2.42, 'FQH', fontsize=11)
    ax.text(0.75, 3.95, '(a)', fontsize=12)

    # ---- (b) 上下两个三角（灰），中心点接触
    ax = new_ax(fig, [0.51, 0.05, 0.47, 0.90], (0, 9.4), (0, 4.3), 'equal')
    ax.add_patch(Polygon([(2.2, 3.85), (7.2, 3.85), (4.7, 2.15)],
                         closed=True, facecolor=GRAY, edgecolor='black',
                         lw=0.8))
    ax.add_patch(Polygon([(2.2, 0.55), (7.2, 0.55), (4.7, 2.15)],
                         closed=True, facecolor=GRAY, edgecolor='black',
                         lw=0.8))
    arr(ax, (1.2, 0.55), (1.2, 3.85), style='<|-|>', lw=0.9, ms=9)
    ax.text(0.85, 2.2, r'$V$', fontsize=12, ha='right', va='center')
    arr(ax, (4.7, 3.1), (4.7, 2.25), lw=1.1, ms=11)
    ax.text(4.4, 2.72, r'$I$', fontsize=12, ha='right')
    ax.text(5.05, 3.3, 'FQH', fontsize=11)
    ax.text(5.05, 1.15, 'FQH', fontsize=11)
    ax.text(0.75, 3.95, '(b)', fontsize=12)
    save('7.18')


if __name__ == '__main__':
    for k, f in sorted(globals().items()):
        if k.startswith('fig_7_') and callable(f):
            f()
            print('done', k)
