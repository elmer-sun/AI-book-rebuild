# -*- coding: utf-8 -*-
"""
《时空与几何》(Carroll, Spacetime and Geometry) 第 5 章后段插图重绘
图 5.10 - 5.17：Schwarzschild 黑洞、Kruskal 最大延拓、共形图
黑白教材风矢量图。
产物: figures/fig_5.10.pdf ... fig_5.17.pdf  (+ figures/preview/fig_5.*.png 自检)
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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

BASE = r'E:/AI整理书籍/卡罗尔/重排本'
OUT = os.path.join(BASE, 'figures')
PREV = os.path.join(OUT, 'preview')
os.makedirs(PREV, exist_ok=True)

# --- 检测 mathtext 是否支持花体 I (\mathscr)，不支持则退化为 \mathcal ---
SCRIPT_I = r'\mathscr{I}'
try:
    _f = plt.figure()
    _f.text(0.5, 0.5, r'$\mathscr{I}^{+}$')
    _f.canvas.draw()
    plt.close(_f)
except Exception:
    plt.close('all')
    SCRIPT_I = r'\mathcal{I}'


# ---------------------------------------------------------------- 通用工具
def save(fig, key):
    fig.savefig(os.path.join(OUT, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV, 'fig_%s.png' % key),
                dpi=200, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


def blank_ax(fig, xlim, ylim):
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    return ax


def arrow(ax, p0, p1, lw=1.1, ms=11):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def wavy(ax, p0, p1, amp, periods, lw=1.0, base=True):
    """直线 + 其上的正弦波（奇点 r=0 的锯齿线样式）"""
    p0 = np.array(p0, float)
    p1 = np.array(p1, float)
    t = np.linspace(0, 1, 700)
    pts = p0[None, :] + t[:, None] * (p1 - p0)[None, :]
    d = p1 - p0
    L = np.hypot(*d)
    n = np.array([-d[1], d[0]]) / L
    if base:
        ax.plot(pts[:, 0], pts[:, 1], 'k-', lw=lw)
    off = amp * np.sin(2 * np.pi * periods * t)
    ax.plot(pts[:, 0] + n[0] * off, pts[:, 1] + n[1] * off, 'k-', lw=lw * 0.9)


def hourglass(ax, cx, cy, h, fill='0.72'):
    """小光锥符号：沙漏形（上下两个三角，45° 类光边）"""
    for s in (1, -1):
        ax.add_patch(mpatches.Polygon(
            [(cx - h, cy + s * h), (cx + h, cy + s * h), (cx, cy)],
            closed=True, facecolor=fill, edgecolor='k', lw=0.7))


def brace(ax, p0, p1, depth, lw=0.9):
    """花括号：p0->p1 为主线方向，depth 为尖端凸出量（带符号，垂直主线）"""
    p0 = np.array(p0, float)
    p1 = np.array(p1, float)
    d = p1 - p0
    L = np.hypot(*d)
    u = d / L
    n = np.array([-u[1], u[0]])

    def P(s, t):
        return tuple(p0 + u * s + n * t)

    verts = [P(0, 0), P(0.16 * L, 0.55 * depth), P(0.36 * L, depth),
             P(0.5 * L, depth), P(0.64 * L, depth),
             P(0.84 * L, 0.55 * depth), P(L, 0)]
    codes = [Path.MOVETO, Path.LINETO, Path.CURVE3, Path.CURVE3,
             Path.CURVE3, Path.CURVE3, Path.LINETO]
    ax.add_patch(mpatches.PathPatch(Path(verts, codes), fill=False,
                                    edgecolor='k', lw=lw, capstyle='round',
                                    joinstyle='round'))


def quadbez(p0, p1, p2, n=80):
    t = np.linspace(0, 1, n)[:, None]
    return ((1 - t) ** 2 * np.array(p0)[None, :]
            + 2 * t * (1 - t) * np.array(p1)[None, :]
            + t ** 2 * np.array(p2)[None, :])


def ellipse_pts(cx, cy, a, b, a0, a1, n=80):
    t = np.linspace(a0, a1, n)
    return np.c_[cx + a * np.cos(t), cy + b * np.sin(t)]


def ptr(ax, p0, p1):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], '-', color='0.45', lw=0.7)


# ---------------------------------------------------------- 图 5.10 / 5.11
def ef_cone(ax, cx, cy, m, a, flip):
    """EF 坐标光锥：水平类光边 + 斜边；flip=False 为 (v,r)，True 为 (u,r)"""
    Lp = (cx - a, cy)
    Rt = (cx + a, cy)
    if np.isinf(m):
        U = (cx, cy + a)
    else:
        c = 1.0 / np.hypot(1.0, m)
        if m > 0:
            U = (cx + a * c, cy + a * m * c)
        else:
            U = (cx - a * c, cy - a * m * c)
    D = (2 * cx - U[0], 2 * cy - U[1])
    side = Rt if flip else Lp
    other = Lp if flip else Rt
    # 未来 /过去楔形（灰色填充）
    ax.add_patch(mpatches.Polygon([(cx, cy), side, U], closed=True,
                                  facecolor='0.82', edgecolor='none'))
    ax.add_patch(mpatches.Polygon([(cx, cy), other, D], closed=True,
                                  facecolor='0.82', edgecolor='none'))
    # 类光边（黑实线）
    ax.plot([cx, side[0]], [cy, side[1]], 'k-', lw=1.0)
    ax.plot([D[0], U[0]], [D[1], U[1]], 'k-', lw=1.0)


def _ef_common(ax, lab, flip):
    # r = 0 竖线
    ax.plot([0, 0], [-0.36, 1.50], 'k-', lw=1.1)
    # u/v 轴（位于 r = 2GM）
    arrow(ax, (1, -0.46), (1, 1.58))
    ax.text(1.10, 1.46, '$%s$' % lab, fontsize=12)
    # r 轴
    arrow(ax, (0, 0), (2.92, 0))
    ax.text(2.86, -0.17, '$r$', fontsize=12)
    # v(或 u) = constant 水平线
    ax.plot([0, 1.82], [0.68, 0.68], 'k-', lw=1.0)
    ax.text(1.92, 0.68, '$%s$ = constant' % lab, fontsize=11, va='center')
    ax.text(0.0, -0.58, '$r=0$', ha='center', fontsize=11)
    ax.text(1.0, -0.58, '$r=2GM$', ha='center', fontsize=11)
    if not flip:                       # 图 5.10：(v, r)，未来指向左偏
        ef_cone(ax, 0.50, 0.68, -0.84, 0.27, False)
        ef_cone(ax, 1.00, 0.68, np.inf, 0.30, False)
        ef_cone(ax, 1.48, 0.68, 2.0, 0.27, False)
    else:                              # 图 5.11：(u, r)，镜像
        ef_cone(ax, 0.50, 0.68, 0.84, 0.27, True)
        ef_cone(ax, 1.00, 0.68, np.inf, 0.30, True)
        ef_cone(ax, 1.48, 0.68, -2.0, 0.27, True)


def fig_5_10():
    """Schwarzschild 光锥，(v, r) EF 坐标（书页 221 / p236.png）"""
    fig = plt.figure(figsize=(3.7, 2.75))
    ax = blank_ax(fig, (-0.40, 3.15), (-0.80, 1.78))
    _ef_common(ax, 'v', flip=False)
    save(fig, '5.10')


def fig_5_11():
    """Schwarzschild 光锥，(u, r) EF 坐标（书页 223 / p238.png）"""
    fig = plt.figure(figsize=(3.7, 2.75))
    ax = blank_ax(fig, (-0.40, 3.15), (-0.80, 1.78))
    _ef_common(ax, 'u', flip=True)
    save(fig, '5.11')


# ------------------------------------------------------------------ 图 5.12
def fig_5_12():
    """Kruskal 图（书页 226 / p241.png 上图）"""
    fig = plt.figure(figsize=(4.8, 3.55))
    ax = blank_ax(fig, (-5.85, 6.55), (-4.55, 4.65))
    Ttop = 3.55
    Rc = np.sqrt(Ttop ** 2 - 1)
    Rg = np.linspace(-Rc, Rc, 500)
    Th = np.sqrt(1 + Rg ** 2)
    # 灰色罩区（r < 0，非时空）
    ax.fill(np.r_[Rg, Rg[::-1]], np.r_[Th, np.full(Rg.size, Ttop)],
            color='0.87', lw=0)
    ax.fill(np.r_[Rg, Rg[::-1]], np.r_[-Th, np.full(Rg.size, -Ttop)],
            color='0.87', lw=0)
    # r = 0 双曲线
    ax.plot(Rg, Th, 'k-', lw=1.0)
    ax.plot(Rg, -Th, 'k-', lw=1.0)
    # r = constant 曲线：上/下（开口向上、向下，r < 2GM）
    for c in (0.30, 0.70):
        Rr = np.linspace(-3.30, 3.30, 500)
        Tr = np.sqrt(Rr ** 2 + c)
        mk = Tr < 3.45
        ax.plot(Rr[mk], Tr[mk], 'k-', lw=0.85)
        ax.plot(Rr[mk], -Tr[mk], 'k-', lw=0.85)
    # r = constant 曲线：左/右（开口向左、向右，r > 2GM）
    for c in (3.1, 6.8):
        Tt2 = np.linspace(-3.40, 3.40, 500)
        Rr2 = np.sqrt(Tt2 ** 2 + c)
        ax.plot(Rr2, Tt2, 'k-', lw=0.85)
        ax.plot(-Rr2, Tt2, 'k-', lw=0.85)
    # t = constant 直线（过原点，斜率绝对值 < 1）
    for ml in (0.35, 0.70, -0.35, -0.70):
        ax.plot([-3.35, 3.35], [-3.35 * ml, 3.35 * ml], 'k-', lw=0.85)
    # 重类光视界线 r = 2GM（四条 45° 半线）
    for sx in (1, -1):
        for sy in (1, -1):
            ax.plot([0, 3.55 * sx], [0, 3.55 * sy], 'k-', lw=2.2)
    # 坐标轴
    arrow(ax, (0, -4.15), (0, 4.15), lw=1.1)
    ax.text(0.20, 4.02, '$T$', fontsize=12)
    arrow(ax, (-5.35, 0), (5.95, 0), lw=1.1)
    ax.text(5.88, -0.38, '$R$', fontsize=12)
    # 光锥符号
    for cx, cy in [(3.0, 1.2), (-3.55, 0.55), (-0.55, 0.95), (-0.92, -1.10)]:
        hourglass(ax, cx, cy, 0.17)
    # 四角花括号标注
    for x0, sy, tline, side in [(-3.77, 1, r'$t=-\infty$', 'L'),
                                (3.77, 1, r'$t=+\infty$', 'R'),
                                (-3.77, -1, r'$t=+\infty$', 'L'),
                                (3.77, -1, r'$t=-\infty$', 'R')]:
        ya, yb = 2.10 * sy, 3.00 * sy
        sgn = 1.0 if side == 'L' else -1.0
        brace(ax, (x0, ya), (x0, yb), 0.22 * sgn * sy, lw=1.0)
        xa = x0 - 0.40 if side == 'L' else x0 + 0.40
        ha = 'right' if side == 'L' else 'left'
        yr = 2.72 * sy if sy > 0 else -2.28
        yt = 2.28 * sy if sy > 0 else -2.72
        ax.text(xa, yr, '$r=2GM$', ha=ha, va='center', fontsize=11)
        ax.text(xa, yt, tline, ha=ha, va='center', fontsize=11)
        sxn = 1 if side == 'R' else -1
        ptr(ax, (x0 + 0.12 * sxn, 2.45 * sy), (2.62 * sxn, 2.55 * sy))
    # r = 0 标注（上、下）
    ax.text(-1.20, 2.62, '$r=0$', ha='center', fontsize=11)
    ptr(ax, (-1.50, 2.46), (-1.88, 2.14))
    ax.text(-1.25, -2.80, '$r=0$', ha='center', fontsize=11)
    ptr(ax, (-1.55, -2.62), (-1.85, -2.07))
    # r = constant（左）
    ax.text(-3.35, -1.10, '$r=$ constant', ha='right', va='center', fontsize=11)
    ptr(ax, (-3.25, -1.02), (-2.05, -1.00))
    ptr(ax, (-3.25, -1.18), (-2.98, -1.52))
    # t = constant（右）
    ax.text(3.20, 1.38, '$t=$ constant', ha='left', va='center', fontsize=11)
    ptr(ax, (3.15, 1.30), (2.62, 0.93))
    ptr(ax, (3.15, 1.40), (2.25, 1.58))
    save(fig, '5.12')


# ------------------------------------------------------------------ 图 5.13
def fig_5_13():
    """Kruskal 图的四个区域（书页 226 / p241.png 下图）"""
    fig = plt.figure(figsize=(3.3, 3.1))
    ax = blank_ax(fig, (-2.55, 2.55), (-2.45, 2.45))
    Ttop = 1.90
    Rc = np.sqrt(Ttop ** 2 - 1)
    Rg = np.linspace(-Rc, Rc, 400)
    Th = np.sqrt(1 + Rg ** 2)
    ax.fill(np.r_[Rg, Rg[::-1]], np.r_[Th, np.full(Rg.size, Ttop)],
            color='0.87', lw=0)
    ax.fill(np.r_[Rg, Rg[::-1]], np.r_[-Th, np.full(Rg.size, -Ttop)],
            color='0.87', lw=0)
    ax.plot([-Ttop, Ttop], [-Ttop, Ttop], 'k-', lw=1.4)
    ax.plot([-Ttop, Ttop], [Ttop, -Ttop], 'k-', lw=1.4)
    ax.plot(Rg, Th, 'k-', lw=1.6)
    ax.plot(Rg, -Th, 'k-', lw=1.6)
    for (x, y), num in [((0, 0.55), 'II'), ((1.05, 0), 'I'),
                        ((-1.05, 0), 'IV'), ((0, -0.55), 'III')]:
        ax.add_patch(mpatches.Circle((x, y), 0.30, fill=False, lw=1.0))
        ax.text(x, y, num, ha='center', va='center', fontsize=12)
    save(fig, '5.13')


# ------------------------------------------------------------------ 图 5.14
def fig_5_14():
    """Kruskal 坐标中的类空切片 A-E（书页 228 / p243.png 上图）"""
    fig = plt.figure(figsize=(3.4, 3.7))
    ax = blank_ax(fig, (-2.50, 2.50), (-2.55, 2.55))
    Tt = 2.15
    Rg = np.linspace(-1.9, 1.9, 500)
    Th = np.sqrt(1 + Rg ** 2)
    ax.fill(np.r_[Rg, Rg[::-1]], np.r_[Th, np.full(Rg.size, Tt)],
            color='0.85', lw=0)
    ax.fill(np.r_[Rg, Rg[::-1]], np.r_[-Th, np.full(Rg.size, -Tt)],
            color='0.85', lw=0)
    # 45° 虚线（r = 2GM）
    ax.plot([-1.9, 1.9], [-1.9, 1.9], 'k--', lw=1.1, dashes=(5, 4))
    ax.plot([-1.9, 1.9], [1.9, -1.9], 'k--', lw=1.1, dashes=(5, 4))
    # 中央竖线
    ax.plot([0, 0], [-Tt, Tt], 'k-', lw=1.0)
    # 切片线 A - E
    for T, lab in [(1.43, 'E'), (0.70, 'D'), (0.0, 'C'),
                   (-0.70, 'B'), (-1.43, 'A')]:
        ax.plot([-1.9, 1.9], [T, T], 'k-', lw=1.0)
        ax.text(-2.04, T, lab, ha='right', va='center', fontsize=12)
    # r = 0 加粗双曲线
    ax.plot(Rg, Th, 'k-', lw=2.4)
    ax.plot(Rg, -Th, 'k-', lw=2.4)
    save(fig, '5.14')


# ------------------------------------------------------------------ 图 5.15
def _plate(ax, cx, cy):
    pts = [(cx - 1.02, cy - 0.12), (cx + 0.78, cy - 0.12),
           (cx + 1.02, cy + 0.20), (cx - 0.78, cy + 0.20)]
    ax.add_patch(mpatches.Polygon(pts, closed=True, facecolor='0.82',
                                  edgecolor='k', lw=0.9))


def _panel_connected(ax, cx, a, w2):
    """B/C/D：两片平台由喉管相连的虫洞几何"""
    _plate(ax, cx, 0.85)
    _plate(ax, cx, -0.85)
    mx, my = cx - 0.02, 0.87
    b = 0.16 * a
    wb = 0.05 + 0.10 * w2
    for sy in (1, -1):
        m_y = my * sy
        mouth = ellipse_pts(mx, m_y, a, b, np.pi, 2 * np.pi)      # 下弧 L->R
        if sy < 0:
            mouth = ellipse_pts(mx, m_y, a, b, 0, np.pi)          # 上弧 L->R
        prof_r = quadbez((mx + a, m_y), (cx + 0.62 * a, 0.32 * sy), (cx + w2, 0))
        prof_l = quadbez((mx - a, m_y), (cx - 0.62 * a, 0.32 * sy), (cx - w2, 0))
        waist = ellipse_pts(cx, 0, w2, wb, np.pi, 2 * np.pi)
        if sy < 0:
            waist = ellipse_pts(cx, 0, w2, wb, 0, np.pi)
        poly = np.vstack([mouth, prof_r[1:], waist[::-1][1:], prof_l[::-1][1:]])
        ax.add_patch(mpatches.Polygon(poly, closed=True, facecolor='0.93',
                                      edgecolor='none'))
        ax.plot(prof_r[:, 0], prof_r[:, 1], 'k-', lw=1.0)
        ax.plot(prof_l[:, 0], prof_l[:, 1], 'k-', lw=1.0)
        ax.add_patch(mpatches.Ellipse((mx, m_y), 2 * a, 2 * b, fill=False,
                                      edgecolor='k', lw=0.9))
        ax.add_patch(mpatches.Ellipse((cx, 0), 2 * w2, 2 * wb, fill=False,
                                      edgecolor='k', lw=0.8))


def _panel_pinched(ax, cx):
    """A/E：两片断开，上片为漏斗、下片为尖峰"""
    _plate(ax, cx, 0.85)
    _plate(ax, cx, -0.85)
    mx, a, b = cx - 0.02, 0.34, 0.055
    # 上：漏斗收拢为一点
    mouth = ellipse_pts(mx, 0.87, a, b, np.pi, 2 * np.pi)
    pr = quadbez((mx + a, 0.87), (cx + 0.50 * a, 0.55), (cx + 0.015, 0.28))
    pl = quadbez((mx - a, 0.87), (cx - 0.50 * a, 0.55), (cx - 0.015, 0.28))
    poly = np.vstack([mouth, pr[1:], pl[::-1][1:]])
    ax.add_patch(mpatches.Polygon(poly, closed=True, facecolor='0.93',
                                  edgecolor='none'))
    ax.plot(pr[:, 0], pr[:, 1], 'k-', lw=1.0)
    ax.plot(pl[:, 0], pl[:, 1], 'k-', lw=1.0)
    ax.add_patch(mpatches.Ellipse((mx, 0.87), 2 * a, 2 * b, fill=False,
                                  edgecolor='k', lw=0.9))
    ax.add_patch(mpatches.Circle((cx, 0.23), 0.022, color='k'))
    # 下：尖峰
    mouth = ellipse_pts(mx, -0.87, a, b, 0, np.pi)
    pr = quadbez((mx + a, -0.87), (cx + 0.45 * a, -0.58), (cx, -0.28))
    pl = quadbez((mx - a, -0.87), (cx - 0.45 * a, -0.58), (cx, -0.28))
    poly = np.vstack([mouth, pr[1:], pl[::-1][1:]])
    ax.add_patch(mpatches.Polygon(poly, closed=True, facecolor='0.93',
                                  edgecolor='none'))
    ax.plot(pr[:, 0], pr[:, 1], 'k-', lw=1.0)
    ax.plot(pl[:, 0], pl[:, 1], 'k-', lw=1.0)
    ax.add_patch(mpatches.Ellipse((mx, -0.87), 2 * a, 2 * b, fill=False,
                                  edgecolor='k', lw=0.9))


def fig_5_15():
    """图 5.14 各类空切片的嵌入几何（书页 228 / p243.png 下图）"""
    fig = plt.figure(figsize=(4.8, 1.55))
    ax = blank_ax(fig, (-1.60, 11.55), (-1.85, 1.85))
    xs = [0.0, 2.5, 5.0, 7.5, 10.0]
    _panel_pinched(ax, xs[0])
    _panel_connected(ax, xs[1], 0.40, 0.09)
    _panel_connected(ax, xs[2], 0.52, 0.26)
    _panel_connected(ax, xs[3], 0.40, 0.09)
    _panel_pinched(ax, xs[4])
    for x, lab in zip(xs, 'ABCDE'):
        ax.text(x, 1.42, lab, ha='center', fontsize=12)
    ax.text(xs[2] + 0.62, 0.0, '$r=2GM$', fontsize=11, va='center')
    arrow(ax, (2.55, -1.50), (10.05, -1.50), lw=1.6, ms=24)
    ax.text(10.5, -1.50, '$v$', fontsize=12, va='center')
    save(fig, '5.15')


# ------------------------------------------------------------------ 图 5.16
def fig_5_16():
    """Schwarzschild 时空的共形图（书页 229 / p244.png）"""
    fig = plt.figure(figsize=(4.8, 2.5))
    ax = blank_ax(fig, (-3.20, 3.95), (-1.80, 1.90))
    V = {'i0L': (-2, 0), 'ipL': (-1, 1), 'C': (0, 0), 'imL': (-1, -1),
         'ipR': (1, 1), 'i0R': (2, 0), 'imR': (1, -1)}
    edges = [('i0L', 'ipL'), ('ipL', 'C'), ('C', 'imL'), ('imL', 'i0L'),
             ('C', 'ipR'), ('ipR', 'i0R'), ('i0R', 'imR'), ('imR', 'C')]
    for a, b in edges:
        ax.plot(*zip(V[a], V[b]), 'k-', lw=1.3)
    # 奇点 r = 0（波浪线）
    wavy(ax, (-1, 1), (1, 1), 0.07, 9)
    wavy(ax, (-1, -1), (1, -1), 0.07, 9)
    # 右菱形内：r = constant 竖直透镜（端点在 i+/i-）
    t = np.linspace(-1, 1, 300)
    ax.plot(1 + 0.23 * np.cos(np.pi * t / 2), t, 'k-', lw=0.8)
    ax.plot(1 - 0.23 * np.cos(np.pi * t / 2), t, 'k-', lw=0.8)
    # 右菱形内：t = constant 弧（中心顶点 -> i0）
    s = np.linspace(0, 1, 200)[:, None]
    for sg in (1, -1):
        pts = ((1 - s) ** 2 * np.array([0., 0.])
               + 2 * s * (1 - s) * np.array([1.1, sg * 0.44])
               + s ** 2 * np.array([2., 0.]))
        ax.plot(pts[:, 0], pts[:, 1], 'k-', lw=0.8)
    # 顶点圆点
    for x, y in V.values():
        ax.add_patch(mpatches.Circle((x, y), 0.05, color='k'))
    # 标注
    ax.text(-0.02, 1.26, '$r=0$', ha='center', fontsize=11)
    ax.text(-0.02, -1.33, '$r=0$', ha='center', fontsize=11)
    ax.text(-0.40, 0.62, '$r=2GM$', rotation=-45, ha='center', va='center',
            fontsize=10)
    ax.text(-0.40, -0.62, '$r=2GM$', rotation=45, ha='center', va='center',
            fontsize=10)
    ax.text(-1.72, 0.60, '$%s^+$' % SCRIPT_I, ha='center', fontsize=11)
    ax.text(-1.72, -0.60, '$%s^-$' % SCRIPT_I, ha='center', fontsize=11)
    ax.text(1.68, 0.60, '$%s^+$' % SCRIPT_I, ha='center', fontsize=11)
    ax.text(1.64, -0.60, '$%s^-$' % SCRIPT_I, ha='center', fontsize=11)
    ax.text(-2.12, 0, '$i^0$', ha='right', va='center', fontsize=11.5)
    ax.text(2.10, 0, '$i^0$', ha='left', va='center', fontsize=11.5)
    ax.text(-1.10, 1.24, '$i^+$', ha='center', fontsize=11.5)
    ax.text(1.13, 1.24, '$i^+$', ha='center', fontsize=11.5)
    ax.text(-1.10, -1.27, '$i^-$', ha='center', fontsize=11.5)
    ax.text(1.13, -1.27, '$i^-$', ha='center', fontsize=11.5)
    ptr(ax, (1.86, 0.44), (1.50, 0.17))
    ax.text(1.90, 0.47, '$t=$ constant', ha='left', va='center', fontsize=11)
    ptr(ax, (1.62, -0.88), (1.18, -0.55))
    ax.text(1.66, -0.93, '$r=$ constant', ha='left', va='center', fontsize=11)
    save(fig, '5.16')


# ------------------------------------------------------------------ 图 5.17
def fig_5_17():
    """坍缩恒星形成黑洞的共形图（书页 230 / p245.png）"""
    fig = plt.figure(figsize=(3.4, 3.5))
    ax = blank_ax(fig, (-1.25, 3.55), (-0.60, 4.45))
    # 奇点在上方：A=r=0 顶点(左上), B=i+, C=i0, D=i-
    A, B, C, D = (0, 3.9), (1.3, 3.9), (2.6, 2.6), (0, 0)
    # 恒星表面世界线（单一三次贝塞尔，向右鼓出，避免拼接折痕）
    ts = np.linspace(0, 1, 300)[:, None]
    surf = ((1 - ts) ** 3 * np.array([0.5, 3.9])
            + 3 * ts * (1 - ts) ** 2 * np.array([0.78, 3.30])
            + 3 * ts ** 2 * (1 - ts) * np.array([0.70, 1.20])
            + ts ** 3 * np.array([0.0, 0.0]))
    poly = np.vstack([np.array([A]), np.array([[0.5, 3.9]]), surf])
    ax.add_patch(mpatches.Polygon(poly, closed=True, facecolor='0.82',
                                  edgecolor='none'))
    # 边界
    ax.plot([0, 0], [0, 3.9], 'k-', lw=1.2)                 # r = 0 中轴
    wavy(ax, A, B, 0.085, 5.5)                              # 奇点
    ax.plot(*zip(B, C), 'k-', lw=1.3)                       # I+
    ax.plot(*zip(C, D), 'k-', lw=1.3)                       # I-
    ax.plot(surf[:, 0], surf[:, 1], 'k-', lw=1.2)           # 恒星表面
    ax.plot([1.3, 0], [3.9, 2.6], '--', color='k', lw=1.2,
            dashes=(5, 4))                                  # 事件视界 r=2GM
    for P in (A, B, C, D):
        ax.add_patch(mpatches.Circle(P, 0.05, color='k'))
    ax.text(0.65, 4.10, '$r=0$', ha='center', fontsize=11)
    ax.text(1.42, 3.98, '$i^+$', ha='left', fontsize=11.5)
    ax.text(2.02, 2.96, '$%s^+$' % SCRIPT_I, fontsize=11)
    ax.text(2.74, 2.60, '$i^0$', ha='left', va='center', fontsize=11.5)
    ax.text(2.20, 1.75, '$%s^-$' % SCRIPT_I, fontsize=11)
    ax.text(0.0, -0.32, '$i^-$', ha='center', fontsize=11.5)
    ax.text(-0.16, 1.95, '$r=0$', ha='right', va='center', fontsize=11)
    save(fig, '5.17')


# ----------------------------------------------------------------------
if __name__ == '__main__':
    for fn in (fig_5_10, fig_5_11, fig_5_12, fig_5_13,
               fig_5_14, fig_5_15, fig_5_16, fig_5_17):
        fn()
        print('done:', fn.__name__)
