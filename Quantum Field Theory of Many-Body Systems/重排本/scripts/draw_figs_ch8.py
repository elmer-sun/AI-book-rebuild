# -*- coding: utf-8 -*-
"""
B5 批次（下）：文小刚《多体量子场论》第8章 8.1–8.7 共 7 幅插图重绘（黑白矢量）。
输出: figures/fig_8.x.pdf + figures/preview/fig_8.x.png
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import (Circle, Ellipse, FancyBboxPatch, Rectangle,
                                Polygon)

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
    'hatch.linewidth': 0.55,
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

LW = 1.1
LW_AX = 0.9
DASH = (4, 2.4)
GRAY = '0.82'


def save(fig, key):
    fig.savefig(os.path.join(FIGDIR, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREVDIR, 'fig_%s.png' % key),
                bbox_inches='tight', pad_inches=0.03, dpi=170)
    plt.close(fig)
    print('fig_%s done' % key)


def arrow(ax, p0, p1, lw=1.0, ms=12, style='-|>'):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, lw=lw, color='k',
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def catmull_rom(pts, n=28, closed=False):
    if closed:
        pts = list(pts) + [pts[0], pts[1], pts[2]]
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = (np.array(P[j], float) for j in (i - 1, i, i + 1, i + 2))
        for j in range(n):
            s = j / n
            s2, s3 = s * s, s * s * s
            pt = 0.5 * ((2 * p1) + (-p0 + p2) * s
                        + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s2
                        + (-p0 + 3 * p1 - 3 * p2 + p3) * s3)
            out.append(pt)
    out.append(np.array(P[-2], float))
    return np.array(out)


def newax(w, h):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_axis_off()
    return fig, ax


# ------------------------------------------------------------- 8.1 水的相图
def fig_8_1():
    fig, ax = newax(3.5, 3.0)
    # 坐标轴
    ax.plot([0, 0], [0, 4.25], color='k', lw=LW_AX)
    ax.plot([0, 5.65], [0, 0], color='k', lw=LW_AX)
    ax.text(-0.28, 3.9, r'$P$', ha='center', va='center', fontsize=11.5)
    ax.text(5.5, -0.32, r'$T$', ha='center', va='center', fontsize=11.5)
    tp = (1.40, 1.53)     # 三相点
    cp = (3.45, 2.49)     # 临界点
    # 升华曲线（三相点 -> T 轴）
    ax.plot([tp[0], 0.70], [tp[1], 0.0], color='k', lw=1.5)
    # 熔化曲线（三相点 -> 上方，略右倾）
    ax.plot([tp[0], 1.56], [tp[1], 4.15], color='k', lw=1.5)
    # 汽化曲线（三相点 -> 临界点，微弯）
    t = np.linspace(0, 1, 60)
    vx = (1 - t) ** 2 * tp[0] + 2 * (1 - t) * t * 2.05 + t ** 2 * cp[0]
    vy = (1 - t) ** 2 * tp[1] + 2 * (1 - t) * t * 2.42 + t ** 2 * cp[1]
    ax.plot(vx, vy, color='k', lw=1.5)
    ax.add_patch(Circle(cp, 0.105, fc='k', ec='k', zorder=4))
    # 绕过临界点的虚线路径（两端箭头）
    pts = [(3.12, 3.32), (3.95, 3.18), (4.44, 2.86), (4.44, 2.28),
           (4.10, 1.86), (3.97, 1.64)]
    P = catmull_rom(pts)
    ax.plot(P[:, 0], P[:, 1], color='k', lw=1.0, ls='--', dashes=DASH)
    arrow(ax, pts[1], pts[0], lw=1.0, ms=11)          # 指向 Water 端
    arrow(ax, pts[-2], pts[-1], lw=1.0, ms=11)        # 指向 Vapor 端
    ax.text(2.75, 3.67, 'Water', ha='center', va='center', fontsize=11.5)
    ax.text(0.70, 1.75, 'Ice', ha='center', va='center', fontsize=11.5)
    ax.text(3.65, 0.73, 'Vapor', ha='center', va='center', fontsize=11.5)
    ax.set_xlim(-0.55, 6.0)
    ax.set_ylim(-0.62, 4.42)
    ax.set_aspect('equal')
    save(fig, '8.1')


# ------------------------------------- 8.2 圆周上量子化的粒子波（7 个波长）
def fig_8_2():
    fig, ax = newax(2.9, 2.9)
    n, A = 7, 0.17
    th = np.linspace(0, 2 * np.pi, 2400)
    r = 1 + A * np.sin(n * th)
    wx, wy = r * np.cos(th), r * np.sin(th)
    # 波峰与圆之间的透镜区域画斜线
    for k in range(n):
        t0, t1 = 2 * k * np.pi / n, (2 * k + 1) * np.pi / n
        m = (th >= t0) & (th <= t1)
        ts = th[m]
        lens_x = np.concatenate([r[m] * np.cos(ts), np.cos(ts[::-1])])
        lens_y = np.concatenate([r[m] * np.sin(ts), np.sin(ts[::-1])])
        ax.fill(lens_x, lens_y, facecolor='white', edgecolor='none',
                hatch='///', zorder=1)
    ax.plot(np.cos(th), np.sin(th), color='k', lw=1.25, zorder=3)
    ax.plot(wx, wy, color='k', lw=1.05, zorder=2)
    ax.set_xlim(-1.32, 1.32)
    ax.set_ylim(-1.32, 1.32)
    ax.set_aspect('equal')
    save(fig, '8.2')


# ------------------------------- 8.3 环面上的隧穿：Ux, Uy 与两链接回路
W, H = 1.5, 2.3          # 盒子正面尺寸
DX, DY = 0.5, 0.46       # 背面偏移


def _box(ax, ox):
    """线框长方体（12 条棱）。"""
    x0, x1, y0, y1 = ox, ox + W, 0, H
    xb0, xb1, yb0, yb1 = ox + DX, ox + W + DX, DY, H + DY
    for (a, b, c, d) in [(x0, y0, x1, y0), (x1, y0, x1, y1),
                         (x1, y1, x0, y1), (x0, y1, x0, y0),
                         (xb0, yb0, xb1, yb0), (xb1, yb0, xb1, yb1),
                         (xb1, yb1, xb0, yb1), (xb0, yb1, xb0, yb0),
                         (x0, y0, xb0, yb0), (x1, y0, xb1, yb0),
                         (x0, y1, xb0, yb1), (x1, y1, xb1, yb1)]:
        ax.plot([a, c], [b, d], color='k', lw=0.75, zorder=1)


def _chevron(ax, x0, x1, ytop, ymid):
    """浅 V 世界线，两个箭头指向中央拐点。"""
    ax.plot([x0, (x0 + x1) / 2, x1], [ytop, ymid, ytop],
            color='k', lw=1.25, zorder=3)
    xm = (x0 + x1) / 2
    arrow(ax, (x0 + 0.45 * (xm - x0), ytop + 0.45 * (ymid - ytop)),
          (x0 + 0.72 * (xm - x0), ytop + 0.72 * (ymid - ytop)),
          lw=1.25, ms=11)
    arrow(ax, (x1 - 0.45 * (x1 - xm), ytop + 0.45 * (ymid - ytop)),
          (x1 - 0.72 * (x1 - xm), ytop + 0.72 * (ymid - ytop)),
          lw=1.25, ms=11)


def _ymark(ax, x0, x1, y0, x2, y2):
    """y 方向隧穿的折线世界线：横段向右箭头 + 斜段向上箭头。"""
    ax.plot([x0, x1], [y0, y0], color='k', lw=1.25, zorder=3)
    ax.plot([x1, x2], [y0, y2], color='k', lw=1.25, zorder=3)
    arrow(ax, (x0 + 0.30 * (x1 - x0), y0), (x0 + 0.78 * (x1 - x0), y0),
          lw=1.25, ms=11)
    f0, f1 = 0.42, 0.72
    arrow(ax, (x1 + f0 * (x2 - x1), y0 + f0 * (y2 - y0)),
          (x1 + f1 * (x2 - x1), y0 + f1 * (y2 - y0)), lw=1.25, ms=11)


def fig_8_3():
    fig, ax = newax(10.6, 3.6)
    ox = [0.0, 2.95, 5.9, 8.85]
    for i, o in enumerate(ox):
        _box(ax, o)
        ax.text(o - 0.28, H + DY + 0.22, '(%s)' % 'abcd'[i],
                ha='center', va='center', fontsize=12)
    # (a) x 方向隧穿：横跨盒子的浅 V，右端伸出盒外
    _chevron(ax, ox[0] + 0.24, ox[0] + 1.74, 1.49, 1.26)
    # (b) y 方向隧穿：折线
    _ymark(ax, ox[1] + 0.78, ox[1] + 1.05, 1.20, ox[1] + 1.26, 1.66)
    # (c) 四次隧穿：两条浅 V + 两个 y 折线
    _chevron(ax, ox[2] + 0.20, ox[2] + 1.32, 1.63, 1.36)
    _chevron(ax, ox[2] + 0.20, ox[2] + 1.32, 0.78, 0.64)
    _ymark(ax, ox[2] + 0.55, ox[2] + 0.75, 1.63, ox[2] + 0.92, 2.00)
    _ymark(ax, ox[2] + 0.53, ox[2] + 0.73, 0.78, ox[2] + 0.90, 1.16)
    # (d) 两个相互链接的回路
    cx, cy = ox[3] + 0.78, 1.18
    R1x, R1y = 0.56, 0.50
    ph = np.linspace(np.deg2rad(122), np.deg2rad(122 - 360), 500)
    wob = 1 + 0.035 * np.sin(3 * ph + 1.0) + 0.02 * np.sin(5 * ph + 0.3)
    lx = cx + R1x * np.cos(ph) * wob
    ly = cy + R1y * np.sin(ph) * wob
    ax.plot(lx, ly, color='k', lw=1.25, zorder=2)
    # 大回路箭头（顺时针）：左上向右、左下向左、右下向左
    for adeg in (128, 232, 305):
        a = np.deg2rad(adeg)
        p = np.array([cx + R1x * np.cos(a), cy + R1y * np.sin(a)])
        tg = np.array([R1y * np.sin(a), -R1x * np.cos(a)])   # 顺时针切向
        tg = tg / np.linalg.norm(tg)
        arrow(ax, p - 0.13 * tg, p + 0.13 * tg, lw=1.25, ms=12)
    # 小回路（豆形，逆时针）：顶点在上方，穿过大回路顶部
    pts = [(0.05, 0.78), (0.22, 0.60), (0.32, 0.30), (0.29, 0.02),
           (0.14, -0.24), (0.0, -0.30), (-0.14, -0.24), (-0.28, 0.02),
           (-0.32, 0.32), (-0.22, 0.58), (-0.06, 0.72)]
    P = catmull_rom([(cx + px, cy + py) for px, py in pts], closed=True)
    ax.plot(P[:, 0], P[:, 1], color='k', lw=1.25, zorder=3)
    arrow(ax, (cx - 0.30, cy + 0.18), (cx - 0.285, cy + 0.05), lw=1.25, ms=12)
    arrow(ax, (cx + 0.285, cy + 0.05), (cx + 0.30, cy + 0.18), lw=1.25, ms=12)
    # 共用坐标架（(a)(b) 之间）：t 竖直向上；底部 y 斜箭头 + x 横箭头
    tx = ox[1] - 0.62
    arrow(ax, (tx, 1.05), (tx, 2.55), lw=1.0, ms=12)
    ax.text(tx - 0.02, 2.78, r'$t$', ha='center', va='center', fontsize=11.5)
    fx = ox[1] - 0.72
    arrow(ax, (fx, 0.28), (fx + 0.30, 0.56), lw=1.0, ms=11)
    ax.text(fx + 0.40, 0.60, r'$y$', ha='left', va='center', fontsize=11.5)
    arrow(ax, (fx, 0.10), (fx + 0.52, 0.10), lw=1.0, ms=11)
    ax.text(fx + 0.58, 0.10, r'$x$', ha='left', va='center', fontsize=11.5)
    ax.set_xlim(-0.65, 11.05)
    ax.set_ylim(-0.35, 3.15)
    ax.set_aspect('equal')
    save(fig, '8.3')


# --------------------------- 8.4 一维晶体经过杂质（窄带噪声示意图）
def _panel_84(ax, ox, dots, xdim, ximp, tag):
    y = 0.0
    ax.plot([ox - 0.35, ox + 5.05], [y, y], color='k', lw=0.9, zorder=1)
    for dx in dots:
        ax.add_patch(Circle((ox + dx, y), 0.105, fc='k', ec='k', zorder=3))
    # 杂质 ×
    s = 0.09
    ax.plot([ox + ximp - s, ox + ximp + s], [y - 0.22 - s, y - 0.22 + s],
            color='k', lw=1.0)
    ax.plot([ox + ximp - s, ox + ximp + s], [y - 0.22 + s, y - 0.22 - s],
            color='k', lw=1.0)
    # 电流 I 箭头
    arrow(ax, (ox + 1.55, 0.52), (ox + 2.95, 0.52), lw=1.1, ms=12)
    ax.text(ox + 2.25, 0.72, r'$I$', ha='center', va='center', fontsize=11.5)
    # 电压 V 标注（两端竖线 + 向外双箭头）
    for sgn, xe in ((-1, ox), (1, ox + xdim)):
        ax.plot([xe, xe], [y - 0.06, y - 0.78], color='k', lw=0.9)
    yv = -0.62
    va = 0.42 * xdim
    arrow(ax, (ox + xdim / 2 - 0.35, yv), (ox, yv), lw=1.0, ms=11)
    arrow(ax, (ox + xdim / 2 + 0.35, yv), (ox + xdim, yv), lw=1.0, ms=11)
    ax.plot([ox + xdim / 2 - 0.35, ox + xdim / 2 - 0.02], [yv, yv], color='k', lw=1.0)
    ax.plot([ox + xdim / 2 + 0.02, ox + xdim / 2 + 0.35], [yv, yv], color='k', lw=1.0)
    ax.text(ox + xdim / 2, yv, r'$V$', ha='center', va='center', fontsize=11.5,
            bbox=dict(fc='white', ec='none', pad=1.5))
    ax.text(ox - 0.62, 0.78, tag, ha='center', va='center', fontsize=12)


def fig_8_4():
    fig, ax = newax(9.4, 2.1)
    _panel_84(ax, 0.0, np.arange(0.30, 5.0, 0.86), 4.75, 2.45, '(a)')
    _panel_84(ax, 4.85, np.array([0.30, 0.97, 1.95, 2.62, 3.60, 4.27]),
              4.75, 2.28, '(b)')
    ax.set_xlim(-1.0, 10.3)
    ax.set_ylim(-1.05, 1.05)
    ax.set_aspect('equal')
    save(fig, '8.4')


# ------------------------- 8.5 FQH 流体流经收缩区（背散射 -> 窄带噪声）
def fig_8_5():
    fig, ax = newax(5.6, 3.3)
    xh = 2.55            # 半宽
    yt, yb = 1.72, -1.72
    ya, yb2 = 0.18, -0.18
    poly = Polygon([(-xh + 0.10, yt), (0, ya), (xh - 0.05, yt),
                    (xh, yb), (0, yb2), (-xh, yb)],
                   closed=True, fc=GRAY, ec='none', zorder=1)
    ax.add_patch(poly)
    # 收缩区上下边界（粗黑折线）
    ax.plot([-xh + 0.10, 0, xh - 0.05], [yt, ya, yt], color='k', lw=1.7,
            zorder=3, solid_capstyle='round')
    ax.plot([-xh, 0, xh], [yb, yb2, yb], color='k', lw=1.7, zorder=3,
            solid_capstyle='round')
    # 边界箭头（画在边界线上，约 45%–58% 处）
    arrow(ax, (-1.66, 1.23), (-1.32, 1.00), lw=1.7, ms=13)   # 左上：向心
    arrow(ax, (1.36, 1.00), (1.70, 1.23), lw=1.7, ms=13)     # 右上：离心
    arrow(ax, (-1.68, -1.23), (-1.34, -1.00), lw=1.7, ms=13)  # 左下：向心
    arrow(ax, (1.36, -1.00), (1.70, -1.23), lw=1.7, ms=13)   # 右下：离心
    # 收缩区中央的背散射箭头（向下）
    arrow(ax, (0, 0.13), (0, -0.13), lw=1.6, ms=15)
    # 电流 I
    arrow(ax, (-3.55, 0.0), (-2.85, 0.0), lw=1.2, ms=13)
    ax.text(-3.20, 0.22, r'$I$', ha='center', va='center', fontsize=11.5)
    # 电压引线与 V（两个圆形电极，箭头指向电极）
    ylineL = ya + (yb - yb2) * 0 + (yb2 - yb) / (-xh - 0) * 0  # 占位
    yl = -0.18 + (0.85 / xh) * (-1.72 + 0.18)
    for sgn in (-1, 1):
        ax.plot([sgn * 0.85, sgn * 0.85], [yl, -1.45], color='k', lw=0.95)
        ax.add_patch(Circle((sgn * 0.85, -1.57), 0.10, fc='white', ec='k',
                            lw=1.0, zorder=3))
    arrow(ax, (-0.22, -1.57), (-0.72, -1.57), lw=1.0, ms=11)
    arrow(ax, (0.22, -1.57), (0.72, -1.57), lw=1.0, ms=11)
    ax.text(0, -1.57, r'$V$', ha='center', va='center', fontsize=11.5,
            bbox=dict(fc='white', ec='none', pad=1.5))
    ax.set_xlim(-3.95, 3.1)
    ax.set_ylim(-2.1, 2.15)
    ax.set_aspect('equal')
    save(fig, '8.5')


# --------------------------------- 8.6 自由费米子的两种量子序及其转变
def _frame86(ax, ox, tag):
    ax.add_patch(Rectangle((ox, 0), 2.2, 2.2, fc='none', ec='k', lw=1.0))
    ax.text(ox - 0.08, 2.42, tag, ha='center', va='center', fontsize=12)


def _ell(ax, cx, cy, rx, ry):
    ax.add_patch(Ellipse((cx, cy), 2 * rx, 2 * ry, fc=GRAY, ec='k',
                         lw=0.8, zorder=2))


def fig_8_6():
    fig, ax = newax(10.2, 2.95)
    ox = [0.0, 2.72, 5.44, 8.16]
    for i, o in enumerate(ox):
        _frame86(ax, o, '(%s)' % 'abcd'[i])
    # (a) 两个有向费米面
    _ell(ax, ox[0] + 0.55, 1.62, 0.30, 0.43)
    _ell(ax, ox[0] + 1.34, 1.13, 0.50, 0.64)
    # (b) 单个费米面
    _ell(ax, ox[1] + 1.10, 1.10, 0.62, 0.66)
    # (c) 两费米面合并（花生形，收腰）：绕腰部点的极坐标双叶曲线
    Mx, My = 0.44, 0.56          # 框内相对坐标
    ph = np.linspace(0, 2 * np.pi, 720)
    rr = (0.2275 + 0.045 * np.cos(ph - np.deg2rad(308))
          - 0.1275 * np.cos(2 * (ph - np.deg2rad(38))))
    pxs = Mx + rr * np.cos(ph)
    pys = My + rr * np.sin(ph)
    P = np.column_stack([ox[2] + 2.2 * pxs, 2.2 * pys])
    ax.fill(P[:, 0], P[:, 1], facecolor=GRAY, edgecolor='k', lw=0.9, zorder=2)
    # (d) 小费米面收缩为一点（黑点）+ 大费米面
    ax.add_patch(Circle((ox[3] + 0.55, 1.62), 0.055, fc='k', ec='k', zorder=3))
    _ell(ax, ox[3] + 1.34, 1.13, 0.50, 0.64)
    ax.set_xlim(-0.45, 10.5)
    ax.set_ylim(-0.15, 2.62)
    ax.set_aspect('equal')
    save(fig, '8.7' if False else '8.6')


# ------------------------------------------- 8.7 序的一种新分类（流程图）
def _rbox(ax, cx, cy, w, h, text='', fs=8.8, shaded=False):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle='round,pad=0.015,rounding_size=0.09',
                                fc='0.85' if shaded else 'white', ec='k',
                                lw=0.9, zorder=3))
    if text:
        ax.text(cx, cy, text, ha='center', va='center', fontsize=fs,
                zorder=4, linespacing=1.25)


def _rell(ax, cx, cy, w, h, text='', fs=8.8):
    ax.add_patch(Ellipse((cx, cy), w, h, fc='white', ec='k', lw=0.9, zorder=3))
    if text:
        ax.text(cx, cy, text, ha='center', va='center', fontsize=fs,
                zorder=4, linespacing=1.25)


def _pline(ax, pts, lw=0.8):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color='k', lw=lw, zorder=1, solid_capstyle='round')


def fig_8_7():
    fig, ax = newax(10.4, 5.5)
    # 顶层
    _rbox(ax, 4.57, 4.88, 0.85, 0.30, 'Orders')
    _pline(ax, [(4.57, 4.73), (4.57, 4.61), (1.59, 4.61), (1.59, 4.38)])
    _pline(ax, [(4.57, 4.61), (7.22, 4.61), (7.22, 4.38)])
    # 左支：对称破缺序（朗道）
    _rbox(ax, 1.80, 4.06, 2.78, 0.62,
          "Symmetry-breaking orders\n'Particle' condensation", shaded=True)
    _rell(ax, 1.80, 3.37, 2.95, 0.62, 'Symmetry group\nNambu–Goldstone mode')
    # 右支：非对称破缺序
    _rbox(ax, 6.93, 4.19, 3.20, 0.36, 'Non-symmetry-breaking orders')
    _pline(ax, [(6.93, 4.01), (6.93, 3.67), (5.97, 3.67), (5.97, 3.12)])
    _pline(ax, [(6.93, 3.67), (8.18, 3.67), (8.18, 3.12)])
    ax.text(6.05, 3.50, 'Quantum system', ha='left', va='center', fontsize=8.8)
    ax.text(8.26, 3.50, 'Classical system', ha='left', va='center', fontsize=8.8)
    _rbox(ax, 6.11, 2.93, 1.76, 0.36, 'Quantum orders')
    _rbox(ax, 8.10, 2.93, 1.50, 0.36)          # 经典系统：空框
    # 量子序的三支
    _pline(ax, [(6.11, 2.75), (6.11, 2.57), (1.59, 2.57), (1.59, 2.06)])
    _pline(ax, [(6.11, 2.57), (4.50, 2.57), (4.50, 2.06)])
    _pline(ax, [(6.11, 2.57), (8.13, 2.57), (8.13, 2.06)])
    _pline(ax, [(8.13, 2.57), (9.86, 2.57)])
    ax.text(1.68, 2.40, 'Gapped', ha='left', va='center', fontsize=8.8)
    _rbox(ax, 1.71, 1.79, 2.57, 0.56,
          'Topological orders\nTopological field theory')
    _rell(ax, 1.73, 1.22, 2.62, 0.44, 'Conformal algebra, $\eta$?')
    _rbox(ax, 4.50, 1.79, 2.38, 0.56,
          'Fermi liquids\nFermi surface topology', shaded=True)
    _rbox(ax, 7.84, 1.91, 2.62, 0.34, 'String-net condensation')
    _rell(ax, 7.94, 1.32, 3.98, 0.70,
          'Projective symmetry group\nGapless gauge bosons/fermions')
    ax.set_xlim(0.0, 10.4)
    ax.set_ylim(0.55, 5.25)
    save(fig, '8.7')


if __name__ == '__main__':
    for f in (fig_8_1, fig_8_2, fig_8_3, fig_8_4, fig_8_5, fig_8_6, fig_8_7):
        f()
