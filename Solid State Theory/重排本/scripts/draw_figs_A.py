# -*- coding: utf-8 -*-
"""
李正中《固体理论》（第2版）中文重排本 插图重绘 第一批：第一至三章 图1.1-图3.5（共26幅）
黑白教材风矢量图，PDF + PNG 双输出。
基准：原书页面 PNG（原书转换/pages/p-021/022/024/031/032/033/044/046/047/048/066/075/076/078/082/083/088/093/104）。
"""
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Ellipse, Circle, Rectangle, Polygon

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = r"E:\AI整理书籍\李正中\重排本"
FIGD = os.path.join(BASE, 'figures')
PRED = os.path.join(FIGD, 'preview')
os.makedirs(PRED, exist_ok=True)

LW_MAIN, LW_AUX = 1.2, 0.8


def save(fig, name):
    fig.savefig(os.path.join(FIGD, f'fig{name}.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRED, f'fig{name}.png'), bbox_inches='tight',
                pad_inches=0.03, dpi=220)
    plt.close(fig)


def arrow_axis(ax, x0, y0, x1, y1, lw=LW_MAIN, ms=12):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def dline(ax, x0, y0, x1, y1, lw=LW_AUX, dashes=(5, 2.6)):
    ax.plot([x0, x1], [y0, y1], 'k-', lw=lw, dashes=dashes)


def arr(ax, x0, y0, x1, y1, lw=LW_MAIN, ms=11):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def darr(ax, x0, y0, x1, y1, lw=LW_MAIN, ms=11):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms))


def plain_axes(ax):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def ctext(ax, x, y, s, **kw):
    kw.setdefault('ha', 'center'); kw.setdefault('va', 'center')
    kw.setdefault('fontsize', 10)
    ax.text(x, y, s, **kw)


def spring(ax, x0, y0, x1, y1, amp=0.06, n=6, lw=1.0):
    """弹簧（锯齿线）"""
    dx, dy = x1 - x0, y1 - y0
    L = np.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    px, py = -uy, ux
    ts = np.linspace(0, 1, 2 * n + 1)
    xs, ys = [], []
    for i, t in enumerate(ts):
        off = amp * ((i % 2) * 2 - 1) if 0 < i < 2 * n else 0.0
        xs.append(x0 + dx * t + px * off)
        ys.append(y0 + dy * t + py * off)
    ax.plot(xs, ys, 'k-', lw=lw)


# ================================================================ 图 1.1
def fig_1_1():
    """二维点阵的元胞和基矢：斜点阵 6x4，四种基矢取法"""
    s = 0.09                       # e2 的剪切量
    e1 = np.array([1.0, 0.0])
    e2 = np.array([s, 1.0])

    def P(i, j):
        return i * e1 + j * e2

    fig, ax = plt.subplots(figsize=(3.55, 2.55))
    plain_axes(ax)
    ax.set_xlim(-0.55, 7.75)
    ax.set_ylim(-0.85, 4.45)
    ax.set_aspect('equal')

    # 网格（含边界）：7 列 x 4 行
    for j in range(5):
        ax.plot([P(0, j)[0], P(7, j)[0]], [P(0, j)[1], P(7, j)[1]], 'k-', lw=1.3)
    for i in range(8):
        ax.plot([P(i, 0)[0], P(i, 4)[0]], [P(i, 0)[1], P(i, 4)[1]], 'k-', lw=1.3)

    # 左下角斜线区元胞
    cell = Polygon([P(0, 0), P(1, 0), P(1, 1), P(0, 1)],
                   closed=True, facecolor='white', edgecolor='k',
                   lw=1.2, hatch='/////')
    ax.add_patch(cell)

    # a1、a2（沿斜线区元胞下、左边，端点在格点）
    arr(ax, 0.0, 0.0, 1.0, 0.0, lw=1.9, ms=12)
    arr(ax, 0.0, 0.0, 0.0, 1.0, lw=1.9, ms=12)
    ctext(ax, 0.62, -0.38, r'$a_1$', fontsize=11)
    ctext(ax, -0.44, 0.62, r'$a_2$', fontsize=11)

    # 取法2（左上）：(-e1+e2, e1)，虚线补全
    arr(ax, *P(1, 3), *P(0, 4), lw=2.2, ms=15)
    arr(ax, *P(1, 3), *P(2, 3), lw=2.2, ms=15)
    dline(ax, *P(1, 4), *P(2, 3), lw=1.3)

    # 取法3（中右）：(-e1, 2e1+e2)
    arr(ax, *P(4, 2), *P(3, 2), lw=2.2, ms=15)
    arr(ax, *P(4, 2), *P(6, 3), lw=2.2, ms=15)
    dline(ax, *P(3, 2), *P(5, 3), lw=1.3)

    # 取法4（下右）：(-e1, 3e1+e2)
    arr(ax, *P(3, 0), *P(2, 0), lw=2.2, ms=15)
    arr(ax, *P(3, 0), *P(6, 1), lw=2.2, ms=15)
    dline(ax, *P(2, 0), *P(5, 1), lw=1.3)
    save(fig, '1-1')


# ================================================================ 图 1.2
def fig_1_2():
    """二维六角点阵的 W-S 元胞（正六边形蜂窝）"""
    R = 0.5
    a = np.sqrt(3) * R                     # 最近邻距离
    u = np.array([a, 0.0])
    v = np.array([a / 2, a * np.sqrt(3) / 2])

    def hexedge(c):
        pts = [c + R * np.array([np.cos(np.deg2rad(30 + 60 * k)),
                                 np.sin(np.deg2rad(30 + 60 * k))]) for k in range(6)]
        return pts

    fig, ax = plt.subplots(figsize=(3.1, 2.75))
    plain_axes(ax)
    ax.set_xlim(-1.62, 1.72)
    ax.set_ylim(-1.55, 1.75)
    ax.set_aspect('equal')

    for i in range(-3, 4):
        for j in range(-3, 4):
            c = i * u + j * v
            if not (-2.4 < c[0] < 2.4 and -2.2 < c[1] < 2.2):
                continue
            pts = hexedge(c)
            xs = [p[0] for p in pts] + [pts[0][0]]
            ys = [p[1] for p in pts] + [pts[0][1]]
            ax.plot(xs, ys, 'k-', lw=1.1)
            ax.plot([c[0]], [c[1]], 'k.', ms=4.5)

    # 中心格点：6 条虚线到近邻 + a1、a2
    nb = [u, v, v - u, -u, -v, u - v]
    for d in nb:
        dline(ax, 0, 0, d[0], d[1], lw=1.0, dashes=(4, 2.4))
    arr(ax, 0, 0, u[0] * 0.96, 0, lw=1.5, ms=13)
    arr(ax, 0, 0, v[0] * 0.96, v[1] * 0.96, lw=1.5, ms=13)
    ctext(ax, 0.60 * a, 0.14, r'$a_1$', fontsize=11)
    ctext(ax, 0.10, 0.82, r'$a_2$', fontsize=11)
    save(fig, '1-2')


# ================================================================ 图 1.3
def _face_verts(V, n):
    """法向 n 的面：取 v·n 最大的顶点，按面内方位角排序"""
    d = V @ n
    m = d.max() - 1e-9
    idx = np.where(d > m)[0]
    pts = V[idx]
    c = pts.mean(axis=0)
    # 面内两组正交基
    a1 = pts[0] - c
    a1 = a1 / np.linalg.norm(a1)
    a2 = np.cross(n, a1)
    ang = np.arctan2((pts - c) @ a2, (pts - c) @ a1)
    order = np.argsort(ang)
    return pts[order]


def _draw_polyhedron(ax, V, normals, view, hatch_map, lw=1.2):
    v = np.array(view, float)
    v = v / np.linalg.norm(v)
    f = -v
    r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r)
    up = np.cross(r, f)

    def prj(p):
        return np.array([p @ r, p @ up])

    faces = []
    for n in normals:
        n = np.array(n, float)
        if n @ v <= 1e-9:          # 背面剔除（保留正面）
            continue
        fv = _face_verts(V, n)
        depth = fv.mean(axis=0) @ v
        faces.append((depth, n, fv))
    faces.sort(key=lambda t: t[0])          # 由远及近
    for depth, n, fv in faces:
        key = tuple(np.round(n).astype(int))
        h = hatch_map.get(key, None)
        poly = Polygon([prj(p) for p in fv], closed=True,
                       facecolor='white', edgecolor='k', lw=lw,
                       hatch=h)
        ax.add_patch(poly)
    return r, up


def fig_1_3():
    """sc、bcc、fcc 点阵的 W-S 元胞，三面板"""
    fig, axs = plt.subplots(1, 3, figsize=(7.0, 2.45))
    for ax in axs:
        plain_axes(ax)
        ax.set_aspect('equal')

    # ---- (a) sc：立方框（透视线框，12 条棱全画）
    ax = axs[0]
    s, dx, dy = 1.0, 0.30, 0.24
    F = [(0, 0), (1, 0), (1, 1), (0, 1)]
    B = [(x + dx, y + dy) for x, y in F]
    for i in range(4):
        j = (i + 1) % 4
        ax.plot([F[i][0], F[j][0]], [F[i][1], F[j][1]], 'k-', lw=1.3)
        ax.plot([B[i][0], B[j][0]], [B[i][1], B[j][1]], 'k-', lw=1.3)
        ax.plot([F[i][0], B[i][0]], [F[i][1], B[i][1]], 'k-', lw=1.3)
    ax.set_xlim(-0.12, 1.5)
    ax.set_ylim(-0.12, 1.42)
    ctext(ax, 0.62, -0.42, '(a) sc', fontsize=10.5)

    # ---- (b) bcc：截角八面体
    ax = axs[1]
    # ---- (b) bcc：截角八面体，顶点 = (0,±1,±2) 的所有排列
    from itertools import permutations
    V = set()
    for pm in permutations(range(3)):
        for a_ in (1, -1):
            for b_ in (1, -1):
                vert = [0, 0, 0]
                vert[pm[0]] = 0
                vert[pm[1]] = a_
                vert[pm[2]] = 2 * b_
                V.add(tuple(vert))
    V = np.array(sorted(V), float)
    normals = []
    for sx in (1, -1):
        normals.append((sx, 0, 0))
        normals.append((0, sx, 0))
        normals.append((0, 0, sx))
    for sx in (1, -1):
        for sy in (1, -1):
            for sz in (1, -1):
                normals.append((sx, sy, sz))
    view_b = (0.55, 0.62, 0.72)
    # 三个可见正方形面打斜线：上(+z)、左下(+x)、右(+y)
    hb = {(0, 0, 1): '/////', (1, 0, 0): '/////', (0, 1, 0): '/////'}
    _draw_polyhedron(ax, V, normals, view_b, hb)
    ax.set_xlim(-2.6, 2.6)
    ax.set_ylim(-2.6, 2.6)
    ctext(ax, 0, -3.15, '(b) bcc', fontsize=10.5)

    # ---- (c) fcc：菱形十二面体
    ax = axs[2]
    Vc = []
    for k in range(3):
        for sg in (1, -1):
            p = [0, 0, 0]; p[k] = 2 * sg
            Vc.append(tuple(p))
    for a_ in (1, -1):
        for b_ in (1, -1):
            for c_ in (1, -1):
                Vc.append((a_, b_, c_))
    Vc = np.array(sorted(set(Vc)), float)
    nc = []
    for sx in (1, -1):
        for sy in (1, -1):
            nc.append((sx, sy, 0))
            nc.append((sx, 0, sy))
            nc.append((0, sx, sy))
    view_c = (1.15, 0.35, 1.0)
    hc = {(1, 0, 1): None,                       # 前面大白菱形（白）
          (1, 1, 0): '/////', (1, -1, 0): '/////',
          (0, 1, 1): '/////', (0, -1, 1): '/////',
          (1, 0, -1): '/////'}
    _draw_polyhedron(ax, Vc, nc, view_c, hc)
    ax.set_xlim(-2.7, 2.7)
    ax.set_ylim(-2.7, 2.7)
    ctext(ax, 0, -3.25, '(c) fcc', fontsize=10.5)
    save(fig, '1-3')


# ================================================================ 图 1.4
def fig_1_4():
    """玻恩-卡门循环"""
    fig, ax = plt.subplots(figsize=(2.55, 2.55))
    plain_axes(ax)
    ax.set_xlim(-1.62, 1.62)
    ax.set_ylim(-1.52, 1.52)
    ax.set_aspect('equal')
    R = 1.0
    ax.add_patch(Circle((0, 0), R, facecolor='none', edgecolor='k', lw=1.3))

    dots = {r'$N$': 97, '1': 73, '2': 50, '3': 27,
            r'$N{-}1$': 120, r'$N{-}2$': 143, r'$N{-}3$': 166, '': 189}
    for lab, deg in dots.items():
        p = R * np.array([np.cos(np.deg2rad(deg)), np.sin(np.deg2rad(deg))])
        ax.plot([p[0]], [p[1]], 'k.', ms=5.5)
        if lab == '':
            continue
        if lab == r'$N{-}3$':
            ctext(ax, p[0] - 0.30, p[1] + 0.12, lab, fontsize=9.5)
        else:
            q = 1.17 * p
            ctext(ax, q[0], q[1], lab, fontsize=9.5)

    # 循环方向箭头（圆右侧 3 点钟附近，顺时针向下）
    a0, a1_ = np.deg2rad(7), np.deg2rad(-3)
    p0 = R * np.array([np.cos(a0), np.sin(a0)])
    p1 = R * np.array([np.cos(a1_), np.sin(a1_)])
    arr(ax, p0[0], p0[1], p1[0], p1[1], lw=1.2, ms=12)

    # 原点小圆圈（N 点内侧）
    q = 0.84 * R * np.array([np.cos(np.deg2rad(83)), np.sin(np.deg2rad(83))])
    ax.add_patch(Circle(q, 0.05, facecolor='none', edgecolor='k', lw=1.0))
    save(fig, '1-4')


# ================================================================ 图 1.5
def _bz_frame(ax, ticklabels=True):
    """正方 BZ 框 + kx/ky 坐标轴 + pi/a 刻度标注（照原书：无刻度短线）"""
    ax.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], 'k-', lw=1.3)
    arrow_axis(ax, -1.38, 0, 1.52, 0, lw=1.1)
    arrow_axis(ax, 0, -1.38, 0, 1.52, lw=1.1)
    ctext(ax, 1.44, -0.16, r'$k_x$', fontsize=10.5)
    ctext(ax, 0.16, 1.46, r'$k_y$', fontsize=10.5)
    if ticklabels:
        ctext(ax, -0.19, 1.13, r'$\pi/a$', fontsize=9.5)
        ctext(ax, -0.21, -1.16, r'$-\pi/a$', fontsize=9.5)
        ctext(ax, -1.38, 0.17, r'$-\pi/a$', fontsize=9.5)
        ctext(ax, 1.32, 0.17, r'$\pi/a$', fontsize=9.5)


def fig_1_5():
    """图1.5 BZ 与 k1..k8 星（无图注文字）"""
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    plain_axes(ax)
    ax.set_xlim(-1.72, 1.78)
    ax.set_ylim(-1.68, 1.72)
    ax.set_aspect('equal')
    _bz_frame(ax)
    angs = [22, 55, 80, 150, 207, 252, 287, -22]
    offs = {0: (-0.02, 0.15), 1: (-0.16, 0.06), 2: (-0.15, 0.02),
            3: (-0.15, 0.03), 4: (-0.10, -0.13), 5: (0.0, -0.15),
            6: (0.09, -0.13), 7: (0.13, -0.10)}
    L = 0.80
    for i, a_ in enumerate(angs):
        d = np.array([np.cos(np.deg2rad(a_)), np.sin(np.deg2rad(a_))])
        arr(ax, 0, 0, L * d[0], L * d[1], lw=1.3, ms=12)
        ctext(ax, L * d[0] + offs[i][0], L * d[1] + offs[i][1],
              rf'$k_{i+1}$', fontsize=10)
    save(fig, '1-5')


# ================================================================ 图 1.6
def fig_1_6():
    """图1.6 BZ 中高对称点与线"""
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    plain_axes(ax)
    ax.set_xlim(-1.72, 1.78)
    ax.set_ylim(-1.68, 1.72)
    ax.set_aspect('equal')
    _bz_frame(ax)
    ax.plot([0, 1], [0, 1], 'k-', lw=1.4)                    # Sigma
    ax.plot([0, 1], [0, 0], 'k-', lw=1.4)                    # Delta
    for p in [(0, 0), (1, 1), (1, 0.5), (0.5, 0)]:
        ax.plot([p[0]], [p[1]], 'k.', ms=5.5)
    ctext(ax, -0.13, -0.14, r'$\Gamma$', fontsize=11)
    ctext(ax, 1.10, 1.06, r'$M$', fontsize=11)
    ctext(ax, 0.88, -0.17, r'$X$', fontsize=11)
    ctext(ax, 1.12, 0.50, r'$Z$', fontsize=11)
    ctext(ax, 0.58, 0.68, r'$\Sigma$', fontsize=11)
    ctext(ax, 0.42, -0.16, r'$\Delta$', fontsize=11)
    save(fig, '1-6')


# ================================================================ 图 1.7
def fig_1_7():
    """图1.7（无图注文字）：M 点波矢群，对角双箭头"""
    fig, ax = plt.subplots(figsize=(2.45, 2.45))
    plain_axes(ax)
    ax.set_xlim(-1.35, 1.55)
    ax.set_ylim(-1.32, 1.42)
    ax.set_aspect('equal')
    ax.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], 'k-', lw=1.3)
    darr(ax, -1, -1, 1, 1, lw=1.2, ms=12)
    darr(ax, -1, 1, 1, -1, lw=1.2, ms=12)
    ax.plot([0], [0], 'k.', ms=5.5)
    ctext(ax, 1.10, 1.06, r'$M$', fontsize=11)
    save(fig, '1-7')


# ================================================================ 图 1.8
def fig_1_8():
    """图1.8（无图注文字）：X 点与 Z 等效点"""
    fig, ax = plt.subplots(figsize=(2.45, 2.45))
    plain_axes(ax)
    ax.set_xlim(-1.42, 1.62)
    ax.set_ylim(-1.32, 1.42)
    ax.set_aspect('equal')
    ax.plot([-1, 1, 1, -1, -1], [-1, -1, 1, 1, -1], 'k-', lw=1.3)
    darr(ax, -1, 0, 1, 0, lw=1.2, ms=12)
    ax.plot([0], [0], 'k.', ms=5.5)
    for x in (-1, 1):
        ax.plot([x], [0.55], 'k.', ms=5.5)
    ctext(ax, -1.15, 0.55, r"$z'$", fontsize=10.5)
    ctext(ax, 1.15, 0.55, r'$z$', fontsize=10.5)
    ctext(ax, 1.12, 0.0, r'$X$', fontsize=11)
    save(fig, '1-8')


# ================================================================ 图 2.1
def fig_2_1():
    """二维正方晶格：5x5 原子圆，近邻 1-4、次近邻 5-8（斜线），弹簧 f1"""
    fig, ax = plt.subplots(figsize=(3.35, 3.55))
    plain_axes(ax)
    ax.set_xlim(-0.62, 5.15)
    ax.set_ylim(-1.05, 4.62)
    ax.set_aspect('equal')
    rad = 0.15
    hatch = {(3, 2), (1, 2), (2, 3), (2, 1), (3, 3), (1, 1), (1, 3), (3, 1)}
    for i in range(5):
        for j in range(5):
            h = (i, j) in hatch
            ax.add_patch(Circle((i, j), rad, facecolor='white',
                                edgecolor='k', lw=1.1, hatch='////' if h else None))
    # 弹簧 0-1（f1）与 0-5（f2）
    spring(ax, 2 + rad + 0.03, 2, 3 - rad - 0.03, 2, amp=0.07, n=6, lw=1.0)
    spring(ax, 2 + 0.105, 2 + 0.105, 3 - 0.105, 3 - 0.105, amp=0.06, n=6, lw=1.0)
    ctext(ax, 2.5, 1.66, r'$f_1$', fontsize=10)
    ctext(ax, 2.72, 2.42, r'$f_2$', fontsize=10)
    # 编号（照原书：除 0 在左下外，均在对应原子正下方）
    ctext(ax, 1.78, 1.62, '0', fontsize=9.5)
    ctext(ax, 3.0, 1.62, '1', fontsize=9.5)
    ctext(ax, 1.0, 1.62, '2', fontsize=9.5)
    ctext(ax, 2.0, 2.62, '3', fontsize=9.5)
    ctext(ax, 2.0, 0.62, '4', fontsize=9.5)
    ctext(ax, 3.0, 2.62, '5', fontsize=9.5)
    ctext(ax, 1.0, 0.62, '6', fontsize=9.5)
    ctext(ax, 1.0, 2.62, '7', fontsize=9.5)
    ctext(ax, 3.0, 0.62, '8', fontsize=9.5)
    # 晶格常数标注 a（下、右）
    darr(ax, 2, -0.62, 3, -0.62, lw=1.0, ms=10)
    ax.plot([2, 2], [-0.55, -0.69], 'k-', lw=1.0)
    ax.plot([3, 3], [-0.55, -0.69], 'k-', lw=1.0)
    ctext(ax, 2.5, -0.90, r'$a$', fontsize=10.5)
    darr(ax, 4.62, 0, 4.62, 1, lw=1.0, ms=10)
    ax.plot([4.55, 4.69], [0, 0], 'k-', lw=1.0)
    ax.plot([4.55, 4.69], [1, 1], 'k-', lw=1.0)
    ctext(ax, 4.92, 0.5, r'$a$', fontsize=10.5)
    save(fig, '2-1')


# ================================================================ 图 2.2
def fig_2_2():
    """二维正方晶格的极化矢量"""
    fig, ax = plt.subplots(figsize=(3.1, 3.35))
    plain_axes(ax)
    ax.set_xlim(-0.42, 2.62)
    ax.set_ylim(-0.62, 2.42)
    ax.set_aspect('equal')
    ax.plot([0, 2, 2, 0, 0], [0, 0, 2, 2, 0], 'k-', lw=1.4)
    G, M, X = (1, 1), (2, 2), (2, 1)
    Zp = (2, 1.3)
    ax.plot([G[0], M[0]], [G[1], M[1]], 'k-', lw=1.2)          # Sigma
    ax.plot([G[0], X[0]], [G[1], X[1]], 'k-', lw=1.2)          # Delta
    dline(ax, G[0], G[1], Zp[0], Zp[1], lw=1.0)                # Gamma-Z 虚线
    for p in [G, M, X, Zp, (2, 1.6), (1.45, 1), (1.55, 1.55)]:
        ax.plot([p[0]], [p[1]], 'k.', ms=5)
    # Sigma 点极化：L 沿 Sigma，T 垂直
    arr(ax, 1.60, 1.60, 1.78, 1.78, lw=1.3, ms=11)
    arr(ax, 1.51, 1.64, 1.40, 1.75, lw=1.3, ms=11)
    ctext(ax, 1.87, 1.68, r'$L$', fontsize=10,
          bbox=dict(fc='white', ec='none', pad=1.0))
    ctext(ax, 1.35, 1.83, r'$T$', fontsize=10)
    ctext(ax, 1.60, 1.44, r'$\Sigma$', fontsize=10,
          bbox=dict(fc='white', ec='none', pad=1.0))
    # Delta 点极化：L 沿 x，T 垂直
    arr(ax, 1.50, 1.0, 1.68, 1.0, lw=1.3, ms=11)
    arr(ax, 1.45, 1.05, 1.45, 1.23, lw=1.3, ms=11)
    ctext(ax, 1.58, 1.31, r'$T$', fontsize=10,
          bbox=dict(fc='white', ec='none', pad=1.0))
    ctext(ax, 1.72, 0.90, r'$L$', fontsize=10)
    ctext(ax, 1.36, 0.88, r'$\Delta$', fontsize=10.5)
    # Z 点：kz 箭头 + (2) 横箭头
    arr(ax, 1.78, 1.08, 1.95, 1.265, lw=1.2, ms=10)
    ctext(ax, 1.80, 1.40, r'$k_z$', fontsize=9.5,
          bbox=dict(fc='white', ec='none', pad=1.0))
    arr(ax, 2.0, 1.3, 2.24, 1.3, lw=1.3, ms=11)
    ctext(ax, 2.40, 1.3, r'(2)', fontsize=10)
    arr(ax, 2.0, 1.62, 2.0, 1.84, lw=1.3, ms=11)
    ctext(ax, 2.14, 1.72, r'(1)', fontsize=10)
    ctext(ax, 1.82, 1.09, r'$Z$', fontsize=10.5,
          bbox=dict(fc='white', ec='none', pad=1.0))
    ctext(ax, 0.87, 0.87, r'$\Gamma$', fontsize=11)
    ctext(ax, 2.10, 2.08, r'$M$', fontsize=11)
    ctext(ax, 2.15, 0.92, r'$X$', fontsize=11)
    # 2pi/a 尺寸线
    yd = -0.30
    ax.plot([0, 0], [yd - 0.07, yd + 0.07], 'k-', lw=1.0)
    ax.plot([2, 2], [yd - 0.07, yd + 0.07], 'k-', lw=1.0)
    arr(ax, 0.62, yd, 0.03, yd, lw=1.0, ms=10)
    arr(ax, 1.38, yd, 1.97, yd, lw=1.0, ms=10)
    ctext(ax, 1.0, yd, r'$2\pi/a$', fontsize=10, ha='center',
          va='center', bbox=dict(fc='white', ec='none', pad=1.2))
    save(fig, '2-2')


# ================================================================ 图 2.3
def fig_2_3():
    """图2.3 沿 Sigma 的格波色散曲线（示意）"""
    fig, ax = plt.subplots(figsize=(2.75, 3.15))
    plain_axes(ax)
    ax.set_xlim(-0.42, 1.38)
    ax.set_ylim(-0.40, 1.10)
    ax.set_aspect('auto')
    arrow_axis(ax, 0, 0, 0, 1.02, lw=1.2)
    arrow_axis(ax, 0, 0, 1.30, 0, lw=1.2)
    ax.plot([1.0, 1.0], [0, 1.0], 'k-', lw=1.2)
    ctext(ax, -0.10, 1.02, r'$\omega^2$', fontsize=11, ha='center')
    ctext(ax, 1.36, -0.02, r'$k$', fontsize=11)
    ctext(ax, -0.09, -0.05, r'$O$', fontsize=10)
    from scipy.interpolate import PchipInterpolator
    Lx = [0, .15, .30, .45, .58, .68, .76, .82, .88, 1.0]
    Ly = [0, .09, .21, .33, .44, .515, .555, .565, .562, .535]
    Lf = PchipInterpolator(Lx, Ly)
    Tx = [0, .2, .4, .6, .8, 1.0]
    Ty = [0, .115, .245, .365, .455, .525]
    Tf = PchipInterpolator(Tx, Ty)
    xx = np.linspace(0, 1, 200)
    ax.plot(xx, Lf(xx), 'k-', lw=1.5)
    ax.plot(xx, Tf(xx), 'k-', lw=1.5)
    ctext(ax, 0.60, 0.60, 'L', fontsize=10.5, style='italic')
    ctext(ax, 0.66, 0.31, 'T', fontsize=10.5, style='italic')
    ctext(ax, -0.26, 0.735, r'$\dfrac{4f_1}{M}$', fontsize=11)
    ctext(ax, 0.50, -0.095, r'$\Sigma$', fontsize=10.5)
    ctext(ax, 1.0, -0.145, r'$\dfrac{\sqrt{2}\,\pi}{a}$', fontsize=10)
    ctext(ax, -0.20, -0.235, r'$(\Gamma)$', fontsize=10)
    ctext(ax, 1.0, -0.30, r'$(M)$', fontsize=10)
    save(fig, '2-3')


# ================================================================ 图 2.4
def fig_2_4():
    """图2.4 沿 Delta 的色散"""
    fig, ax = plt.subplots(figsize=(2.6, 2.95))
    plain_axes(ax)
    ax.set_xlim(-0.42, 1.38)
    ax.set_ylim(-0.40, 1.05)
    arrow_axis(ax, 0, 0, 0, 0.97, lw=1.2)
    arrow_axis(ax, 0, 0, 1.30, 0, lw=1.2)
    ax.plot([1.0, 1.0], [0, 0.97], 'k-', lw=1.2)
    ctext(ax, -0.10, 0.97, r'$\omega^2$', fontsize=11, ha='center')
    ctext(ax, 1.36, -0.02, r'$k$', fontsize=11)
    ctext(ax, -0.09, -0.05, r'$O$', fontsize=10)
    from scipy.interpolate import PchipInterpolator
    Lf = PchipInterpolator([0, .2, .4, .6, .8, 1.0],
                           [0, .08, .25, .47, .65, .72])
    Tf = PchipInterpolator([0, .3, .5, .7, .85, 1.0],
                           [0, .055, .125, .205, .26, .30])
    xx = np.linspace(0, 1, 200)
    ax.plot(xx, Lf(xx), 'k-', lw=1.5)
    ax.plot(xx, Tf(xx), 'k-', lw=1.5)
    ctext(ax, 0.60, 0.60, 'L', fontsize=10.5, style='italic')
    ctext(ax, 0.80, 0.34, 'T', fontsize=10.5, style='italic')
    ctext(ax, -0.27, 0.72, r'$\dfrac{4(f_1+f_2)}{M}$', fontsize=10)
    ctext(ax, -0.25, 0.30, r'$\dfrac{4f_2}{M}$', fontsize=10)
    ctext(ax, 0.50, -0.095, r'$\Delta$', fontsize=10.5)
    ctext(ax, 1.0, -0.155, r'$\dfrac{\pi}{a}$', fontsize=10.5)
    ctext(ax, -0.20, -0.245, r'$(\Gamma)$', fontsize=10)
    ctext(ax, 1.0, -0.31, r'$(X)$', fontsize=10)
    save(fig, '2-4')


# ================================================================ 图 2.5
def fig_2_5():
    """图2.5 沿 Z 的色散"""
    fig, ax = plt.subplots(figsize=(2.6, 2.95))
    plain_axes(ax)
    ax.set_xlim(-0.42, 1.52)
    ax.set_ylim(-0.40, 1.05)
    arrow_axis(ax, 0, 0, 0, 0.97, lw=1.2)
    arrow_axis(ax, 0, 0, 1.44, 0, lw=1.2)
    ax.plot([1.0, 1.0], [0, 0.97], 'k-', lw=1.2)
    ctext(ax, -0.10, 0.97, r'$\omega^2$', fontsize=11, ha='center')
    ctext(ax, 1.36, 0.06, r"$k'$", fontsize=11)
    ctext(ax, 1.36, -0.07, r"$k_z$", fontsize=9)
    ctext(ax, -0.09, -0.05, r'$O$', fontsize=10)
    from scipy.interpolate import PchipInterpolator
    W1 = PchipInterpolator([0, .2, .4, .6, .8, 1.0],
                           [.72, .675, .625, .578, .538, .505])
    W2 = PchipInterpolator([0, .2, .4, .6, .8, 1.0],
                           [.30, .352, .405, .450, .483, .503])
    xx = np.linspace(0, 1, 200)
    ax.plot(xx, W1(xx), 'k-', lw=1.5)
    ax.plot(xx, W2(xx), 'k-', lw=1.5)
    ctext(ax, 0.33, 0.625, r'$\omega_1^2(z)$', fontsize=10)
    ctext(ax, 0.47, 0.345, r'$\omega_2^2(z)$', fontsize=10)
    ctext(ax, -0.27, 0.72, r'$\dfrac{4(f_1+f_2)}{M}$', fontsize=10)
    ctext(ax, -0.25, 0.505, r'$\dfrac{4f_1}{M}$', fontsize=10)
    ctext(ax, -0.25, 0.30, r'$\dfrac{4f_2}{M}$', fontsize=10)
    ctext(ax, 0.50, -0.095, r'$z$', fontsize=10.5)
    ctext(ax, 1.0, -0.155, r'$\dfrac{\pi}{a}$', fontsize=10.5)
    ctext(ax, -0.20, -0.245, r'$(X)$', fontsize=10)
    ctext(ax, 1.0, -0.31, r'$(M)$', fontsize=10)
    save(fig, '2-5')


# ================================================================ 图 2.6
def fig_2_6():
    """一维复式晶格模型"""
    fig, ax = plt.subplots(figsize=(5.0, 1.55))
    plain_axes(ax)
    ax.set_xlim(-0.95, 4.95)
    ax.set_ylim(-0.72, 0.95)
    ax.set_aspect('equal')
    rad = 0.085
    a = 1.7                      # 元胞长（图面）
    cells = [-1, 0, 1]
    x0 = 1.7                     # cell l 的起点（虚线处）
    off = {'-1': x0 - a, '0': x0, '1': x0 + a}
    # 弹簧与原子：cell l: M1 at l+0.2a, M2 at l+0.8a；f2 跨 (l-0.2a, l+0.2a)
    y = 0.0
    for c in [-1, 0, 1]:
        b = x0 + c * a
        # 两端的 f2 弹簧（每 cell 画左端 f2）
        spring(ax, b - 0.2 * a, y, b + 0.2 * a, y, amp=0.055, n=5, lw=1.0)
        ctext(ax, b, 0.20, r'$f_2$', fontsize=9.5)
        spring(ax, b + 0.25 * a, y, b + 0.75 * a, y, amp=0.055, n=6, lw=1.0)
        ctext(ax, b + 0.5 * a, 0.20, r'$f_1$', fontsize=9.5)
        for dx, lab, hat in [(0.25 * a, r'$M_1$', False), (0.75 * a, r'$M_2$', True)]:
            ax.add_patch(Circle((b + dx, y), rad, facecolor='white',
                                edgecolor='k', lw=1.1,
                                hatch='////' if hat else None))
            ctext(ax, b + dx, -0.24, lab, fontsize=9.5)
    # 最右端再补一个 M1 与半个 f2
    b = x0 + a
    spring(ax, b + 0.25 * a, y, b + 0.75 * a, y, amp=0.055, n=6, lw=1.0)
    ctext(ax, b + 0.5 * a, 0.20, r'$f_1$', fontsize=9.5)
    ax.add_patch(Circle((b + 0.25 * a, y), rad, facecolor='white',
                        edgecolor='k', lw=1.1))
    ctext(ax, b + 0.25 * a, -0.24, r'$M_1$', fontsize=9.5)
    spring(ax, b + 0.8 * a, y, b + 1.18 * a, y, amp=0.055, n=4, lw=1.0)
    ctext(ax, b + 1.0 * a, 0.20, r'$f_2$', fontsize=9.5)
    # 元胞虚线
    for c in [0, 1]:
        b = x0 + c * a
        dline(ax, b, 0.42, b, -0.60, lw=1.0, dashes=(5, 3))
    # 元胞标注
    ctext(ax, x0 - a + 0.5 * a, 0.72, r'$l{-}1$', fontsize=10)
    ctext(ax, x0 + 0.5 * a - 0.10, 0.72, r'$l$', fontsize=10)
    ctext(ax, x0 + 0.5 * a + 0.34, 0.72, '（元胞）', fontsize=9, fontfamily='SimSun')
    ctext(ax, x0 + a + 0.5 * a, 0.72, r'$l{+}1$', fontsize=10)
    # a 尺寸线
    yd = -0.47
    arr(ax, x0 + 0.28 * a, yd, x0 + 0.02, yd, lw=1.0, ms=10)
    arr(ax, x0 + 0.72 * a, yd, x0 + 0.98 * a, yd, lw=1.0, ms=10)
    ctext(ax, x0 + 0.5 * a, yd, r'$a$', fontsize=10,
          bbox=dict(fc='white', ec='none', pad=1.0))
    save(fig, '2-6')


# ================================================================ 图 2.7
def fig_2_7():
    """图2.7 一维双原子链色散"""
    fig, ax = plt.subplots(figsize=(2.85, 2.85))
    plain_axes(ax)
    ax.set_xlim(-1.62, 1.78)
    ax.set_ylim(-0.24, 1.28)
    arrow_axis(ax, 0, 0, 0, 1.20, lw=1.2)
    arrow_axis(ax, -1.42, 0, 1.60, 0, lw=1.2)
    ctext(ax, 0.11, 1.18, r'$\omega$', fontsize=11)
    ctext(ax, 1.52, -0.04, r'$k$', fontsize=11)
    ax.plot([-1, -1], [0, 0.92], 'k-', lw=1.2)
    ax.plot([1, 1], [0, 0.92], 'k-', lw=1.2)
    from scipy.interpolate import PchipInterpolator
    # ω+ 支：k=0 处最大，±π/a 处有限值；ω- 支：k=0 为 0（声学支）
    xk = np.array([1, .7, .45, .25, .1, 0])
    wk = np.array([.585, .635, .675, .700, .715, .72])
    xs = np.concatenate([-xk[:-1], xk[1:][::-1]])   # [-1,-.7,-.45,-.25,-.1, 0,.1,.25,.45,.7]
    ws = np.concatenate([wk[:-1], wk[1:][::-1]])
    Pp = PchipInterpolator(xs, ws)
    xx = np.linspace(-1, 1, 200)
    ax.plot(xx, Pp(xx), 'k-', lw=1.5)
    xm = [0, .2, .4, .6, .8, 1.0]
    wm = [0, .10, .225, .34, .415, .45]
    Pm = PchipInterpolator(xm, wm)
    xs2 = np.concatenate([np.array(xm), np.array(xm[1:]) * -1])
    ws2 = np.concatenate([np.array(wm), np.array(wm[1:])])
    o2 = np.argsort(xs2)
    Pm2 = PchipInterpolator(xs2[o2], ws2[o2])
    ax.plot(xx, Pm2(xx), 'k-', lw=1.5)
    ctext(ax, 0.10, 0.765, r'$\omega_+$', fontsize=10.5)
    ctext(ax, 0.17, 0.44, r'$\omega_-$', fontsize=10.5)
    ctext(ax, -1, -0.115, r'$-\dfrac{\pi}{a}$', fontsize=9.5)
    ctext(ax, 0, -0.10, r'$O$', fontsize=10)
    ctext(ax, 1, -0.115, r'$\dfrac{\pi}{a}$', fontsize=9.5)
    save(fig, '2-7')


# ================================================================ 图 2.8
def fig_2_8():
    """图2.8 极化激元的色散曲线"""
    fig, ax = plt.subplots(figsize=(2.6, 2.9))
    plain_axes(ax)
    ax.set_xlim(-0.30, 1.18)
    ax.set_ylim(-0.09, 1.14)
    arrow_axis(ax, 0, 0, 0, 1.06, lw=1.2)
    arrow_axis(ax, 0, 0, 1.10, 0, lw=1.2)
    ctext(ax, -0.13, 1.04, r'$\omega$', fontsize=11)
    ctext(ax, 1.06, -0.05, r'$k$', fontsize=11)
    ctext(ax, -0.08, -0.05, r'$O$', fontsize=10)
    wL, wT = 0.516, 0.43
    dline(ax, 0, wL, 1.05, wL, lw=0.9)
    dline(ax, 0, wT, 1.05, wT, lw=0.9)
    ctext(ax, -0.16, wL + 0.02, r'$\omega_{\rm L}$', fontsize=10)
    ctext(ax, -0.16, wT - 0.03, r'$\omega_{\rm T}$', fontsize=10)
    # 两条光线
    ax.plot([0, 0.345], [0, 1.0], 'k-', lw=0.9)
    ax.plot([0, 0.575], [0, 1.62 * 0.575], 'k-', lw=0.9)
    ctext(ax, 0.375, 1.035, r'$c/\sqrt{\varepsilon_\infty}$', fontsize=10, ha='left')
    ctext(ax, 0.615, 0.885, r'$c/\sqrt{\varepsilon_0}$', fontsize=10, ha='left')
    # 下支：沿 c/√e0 起步，较长一段贴光线，后趋于 wT
    from scipy.interpolate import PchipInterpolator
    lo = PchipInterpolator([0, .05, .10, .15, .20, .24, .28, .34, .44, .58, .75, .95],
                           [0, .081, .162, .243, .324, .385, .408, .420,
                            .4255, .4280, .4290, .4294])
    xx = np.linspace(0, 0.95, 200)
    ax.plot(xx, lo(xx), 'k-', lw=1.9)
    # 上支：从 (0, wL) 出发并入 c/√e∞
    hi = PchipInterpolator([0, .04, .09, .15, .21, .26, .30, .325, .345],
                           [wL, wL + .002, wL + .012, wL + .045, .60, .68, .80, .93, 1.0])
    xx = np.linspace(0, 0.345, 200)
    ax.plot(xx, hi(xx), 'k-', lw=1.9)
    save(fig, '2-8')


# ================================================================ 图 2.9
def fig_2_9():
    """图2.9 极化激元的介电函数"""
    e_inf, e0 = 2.25, 3.24
    wL = 0.50
    wT = wL / 1.2
    wmax = 0.85

    def eps(w):
        return e_inf * (wL ** 2 - w ** 2) / (wT ** 2 - w ** 2)

    fig, ax = plt.subplots(figsize=(3.05, 2.85))
    plain_axes(ax)
    ax.set_xlim(-1.15, 4.75)
    ax.set_ylim(-0.13, 1.02)
    arrow_axis(ax, 0, 0, 0, 0.93, lw=1.2)
    arrow_axis(ax, 0, 0, 4.55, 0, lw=1.2)
    ctext(ax, -0.17, 0.90, r'$\omega$', fontsize=11)
    ctext(ax, 4.42, 0.07, r'$\varepsilon(\omega)$', fontsize=10.5)
    ctext(ax, -0.12, -0.05, r'$O$', fontsize=10)
    # 水平虚线（横贯全图）
    dline(ax, -1.1, wL, 4.5, wL, lw=0.9)
    dline(ax, -1.1, wT, 4.5, wT, lw=0.9)
    ctext(ax, -0.20, wL + 0.045, r'$\omega_{\rm L}$', fontsize=10)
    ctext(ax, -0.20, wT - 0.05, r'$\omega_{\rm T}$', fontsize=10)
    # 竖直虚线：1（到 wL）、eps_inf（到上部）、eps_0（到中部）
    dline(ax, 1.0, 0, 1.0, wL, lw=0.9)
    dline(ax, e_inf, 0, e_inf, 0.82, lw=0.9)
    dline(ax, e0, 0, e0, 0.58, lw=0.9)
    for x, lab in [(1.0, '1'), (e_inf, r'$\varepsilon_\infty$'),
                   (e0, r'$\varepsilon_0$')]:
        ctext(ax, x, -0.085, lab, fontsize=9.5)
    # 曲线（照原书形态示意）
    from scipy.interpolate import PchipInterpolator
    # A: wT<w<wL 负支：左缘贴 wT，升到 (0,wL)
    fA = PchipInterpolator([-1.15, -0.75, -0.45, -0.22, -0.08, 0.0],
                           [0.4240, 0.4290, 0.4400, 0.4560, 0.4720, 0.5000])
    xs = np.linspace(-1.15, 0.0, 120)
    ax.plot(xs, fA(xs), 'k-', lw=1.8)
    # B: w>wL 正支：从 (0,wL) 上升，趋于 eps_inf 渐近线
    wB = np.linspace(wL + 0.0005, 0.93, 240)
    ax.plot(eps(wB), wB, 'k-', lw=1.8)
    # D: 0<w<wT：自 (eps0,0) 弯向 (≈1, wT 下方)
    fD = PchipInterpolator([1.04, 1.15, 1.50, 1.90, 2.35, 2.75, 3.05, 3.24],
                           [0.4155, 0.412, 0.402, 0.375, 0.300, 0.200, 0.090, 0.0])
    xs = np.linspace(1.04, 3.24, 160)
    ax.plot(xs, fD(xs), 'k-', lw=1.8)
    save(fig, '2-9')


# ================================================================ 图 2.10
def fig_2_10():
    """图2.10 反射比曲线（照原书形态示意：w* 处深谷，wT 以下回升）"""
    from scipy.interpolate import PchipInterpolator
    wL, wT, wstar, wmax = 0.43, 0.35, 0.56, 0.94

    fig, ax = plt.subplots(figsize=(2.6, 2.9))
    plain_axes(ax)
    ax.set_xlim(-0.28, 1.34)
    ax.set_ylim(-0.16, 1.02)
    arrow_axis(ax, 0, 0, 0, 0.94, lw=1.2)
    arrow_axis(ax, 0, 0, 1.26, 0, lw=1.2)
    ctext(ax, -0.14, 0.92, r'$\omega$', fontsize=11)
    arr(ax, 0.13, 0, 0.27, 0, lw=1.0, ms=9)
    ctext(ax, 0.47, -0.065, r'$R(\omega)$', fontsize=10.5)
    ctext(ax, -0.09, -0.06, r'$O$', fontsize=10)
    ctext(ax, 1.0, -0.10, '1', fontsize=10)
    # 水平虚线：w*（上，无标注）、wL（标注在上）、wT（标注在下）
    dline(ax, -0.24, wstar, 1.0, wstar, lw=0.9)
    dline(ax, -0.24, wL, 1.02, wL, lw=0.9)
    dline(ax, -0.24, wT, 1.02, wT, lw=0.9)
    ctext(ax, -0.17, wL + 0.045, r'$\omega_{\rm L}$', fontsize=10)
    ctext(ax, -0.17, wT - 0.05, r'$\omega_{\rm T}$', fontsize=10)
    # 上段（w>w*）：自谷底回升，趋于高值
    f1 = PchipInterpolator([wstar, wstar + 0.04, wstar + 0.09, wstar + 0.16,
                            wstar + 0.26, wmax],
                           [0.05, 0.16, 0.25, 0.31, 0.345, 0.37])
    xs = np.linspace(wstar, wmax, 160)
    ax.plot(f1(xs), xs, 'k-', lw=1.8)
    # 中段（wL..w*）：自 R~1 俯冲入谷
    f2 = PchipInterpolator([wL, wL + 0.015, wL + 0.035, wL + 0.06, wstar - 0.015, wstar],
                           [0.97, 0.92, 0.74, 0.44, 0.13, 0.06])
    xs = np.linspace(wL, wstar, 160)
    ax.plot(f2(xs), xs, 'k-', lw=1.8)
    # 下段（0..wT）：R 自 ~0.5 升至 1
    f3 = PchipInterpolator([0, 0.05, 0.12, 0.20, 0.27, wT - 0.004],
                           [0.48, 0.51, 0.575, 0.67, 0.80, 0.96])
    xs = np.linspace(0.0, wT - 0.004, 160)
    ax.plot(f3(xs), xs, 'k-', lw=1.8)
    save(fig, '2-10')


# ================================================================ 图 2.11
def _vhs_panel(ax, kind, w0):
    """范霍夫奇点单面板：kind in a,b,c,d"""
    H = 0.80
    ax.plot([0, 1.06, 1.06, 0, 0], [0, 0, H, H, 0], 'k-', lw=1.0)
    arrow_axis(ax, 0, 0, 0, H + 0.06, lw=1.1, ms=9)
    arrow_axis(ax, 0, 0, 1.12, 0, lw=1.1, ms=9)
    ctext(ax, -0.075, H + 0.02, r'$g(\omega)$', fontsize=9.5, ha='right')
    ctext(ax, 1.15, -0.015, r'$\omega$', fontsize=9.5)
    ctext(ax, -0.05, -0.05, r'$O$', fontsize=9)
    xx = np.linspace(0.001, 1.0, 10)
    from scipy.interpolate import PchipInterpolator
    if kind == 'a':
        t = np.linspace(0.004, 1.0, 150)
        g = 0.60 * np.sqrt(t / 1.0)
        ax.plot(w0 + t * 0.53, g, 'k-', lw=1.5)
        ctext(ax, w0, -0.09, r'$\omega(k_0)$', fontsize=9)
    elif kind == 'b':
        t = np.linspace(0.004, 1.0, 150)
        g = 0.60 * np.sqrt(t)
        ax.plot(w0 - t * 0.52, g, 'k-', lw=1.5)
        ctext(ax, w0, -0.09, r'$\omega(k_0)$', fontsize=9)
    elif kind == 'c':
        dline(ax, w0, 0, w0, 0.45, lw=0.9)
        t = np.linspace(0.004, 1.0, 150)
        g = 0.44 * np.sqrt(t)
        ax.plot(w0 - 0.23 + t * 0.23, g, 'k-', lw=1.5)
        f = PchipInterpolator([w0, w0 + .15, w0 + .30, w0 + .50],
                              [.44, .515, .565, .615])
        xs = np.linspace(w0, w0 + 0.50, 80)
        ax.plot(xs, f(xs), 'k-', lw=1.5)
        ctext(ax, w0, -0.09, r'$\omega(k_0)$', fontsize=9)
    else:
        dline(ax, w0, 0, w0, 0.47, lw=0.9)
        f = PchipInterpolator([w0 - 0.47, w0 - .30, w0 - .15, w0],
                              [.66, .585, .525, .47])
        xs = np.linspace(w0 - 0.47, w0, 80)
        ax.plot(xs, f(xs), 'k-', lw=1.5)
        t = np.linspace(0.004, 1.0, 150)
        g = 0.47 * np.sqrt(1 - t)
        ax.plot(w0 + t * 0.33, g, 'k-', lw=1.5)
        ctext(ax, w0, -0.09, r'$\omega(k_0)$', fontsize=9)


def fig_2_11():
    """图2.11 范·霍夫奇点附近的态密度"""
    fig, axs = plt.subplots(2, 2, figsize=(5.0, 4.35))
    mathcap = [['(a)$M_0$', '(b)$M_3$'], ['(c)$M_1$', '(d)$M_2$']]
    zhcap = [['型（极小点）', '型（极大点）'],
             ['型（I类鞍点）', '型（II类鞍点）']]
    kinds = [['a', 'b'], ['c', 'd']]
    for i in range(2):
        for j in range(2):
            ax = axs[i][j]
            plain_axes(ax)
            ax.set_xlim(-0.22, 1.30)
            ax.set_ylim(-0.24, 0.98)
            k = kinds[i][j]
            _vhs_panel(ax, k, {'a': 0.42, 'b': 0.74, 'c': 0.45, 'd': 0.55}[k])
            ax.text(0.435, -0.20, mathcap[i][j], fontsize=9.5,
                    ha='right', va='center')
            ax.text(0.465, -0.20, zhcap[i][j], fontsize=9,
                    ha='left', va='center', fontfamily='SimSun')
    fig.subplots_adjust(wspace=0.25, hspace=0.42)
    save(fig, '2-11')


# ================================================================ 图 2.12
def fig_2_12():
    """含单个缺陷的一维链模型"""
    fig, ax = plt.subplots(figsize=(4.7, 1.45))
    plain_axes(ax)
    ax.set_xlim(-2.85, 2.85)
    ax.set_ylim(-0.55, 1.05)
    ax.set_aspect('equal')
    rad = 0.135
    ls_ = [-2, -1, 0, 1, 2]
    for l in ls_:
        x = 1.0 * l
        # 两边的弹簧 f
        spring(ax, x - 0.5, 0, x - 0.17, 0, amp=0.05, n=3, lw=1.0)
        spring(ax, x + 0.17, 0, x + 0.5, 0, amp=0.05, n=3, lw=1.0)
        hat = (l != 0)
        ax.add_patch(Circle((x, 0), rad, facecolor='white', edgecolor='k',
                            lw=1.1, hatch='////' if hat else None))
    # 每个弹簧一个 f 标注（含两端半弹簧）
    for xg in [-2.33, -1.5, -0.5, 0.5, 1.5, 2.33]:
        ctext(ax, xg, 0.18, r'$f$', fontsize=9)
    # 原子标注
    for l in [-2, -1, 1, 2]:
        ctext(ax, l, -0.30, r'$M$', fontsize=9.5)
    ctext(ax, 0, -0.30, r"$M'$", fontsize=9.5)
    for l in ls_:
        ctext(ax, l, -0.52, rf'$l{{=}}{l}$', fontsize=8.5)
    # a 尺寸（l=1 与 l=2 之间，上方）
    for x in (1.0, 2.0):
        dline(ax, x, 0.17, x, 0.88, lw=0.9)
    yd = 0.75
    arr(ax, 1.28, yd, 1.02, yd, lw=1.0, ms=9)
    arr(ax, 1.72, yd, 1.98, yd, lw=1.0, ms=9)
    ctext(ax, 1.5, yd, r'$a$', fontsize=9.5,
          bbox=dict(fc='white', ec='none', pad=0.8))
    save(fig, '2-12')


# ================================================================ 图 2.13
def _f_panel(ax, heavy=True):
    """式(2.10.14)作图解单面板：6 条竖直渐近线（最后一条为 wM）"""
    xM = 2.52
    xs = [0.42 * (j + 1) for j in range(6)]        # w1..w5, wM
    A = 0.64
    FCLIP = 1.52
    # 首支（0..w1）：重杂质自 O 上升，轻杂质自 O 下降
    u = np.linspace(0.0, 0.955, 120)
    F0 = (A if heavy else -A) * np.tan(np.pi * u / 2)
    ax.plot(xs[0] * u, F0, 'k-', lw=1.5)
    # 中间各支（w_l..w_{l+1}）：S 形上升
    for j in range(5):
        u = np.linspace(0.02, 0.98, 120)
        F = A * np.tan(np.pi * (u - 0.5))
        m = np.abs(F) < FCLIP
        ax.plot(xs[j] + u[m] * 0.42, F[m], 'k-', lw=1.5)
    # wM 之外的支：重杂质在 F<0 趋于 0；轻杂质自 +∞ 降并穿过 F=1
    s = np.linspace(0.10, 1.5, 140)
    Fb = (-0.42 if heavy else 0.63) / s
    m = np.abs(Fb) < 1.55
    ax.plot(xM + s[m], Fb[m], 'k-', lw=1.5)
    # 竖直渐近线
    for x in xs:
        ax.plot([x, x], [-0.92, 0.80], 'k-', lw=1.0)
    # 坐标轴
    arrow_axis(ax, 0, -1.0, 0, 1.28, lw=1.2)
    arrow_axis(ax, 0, 0, 3.55, 0, lw=1.2)
    ctext(ax, -0.14, 1.30, r'$F$', fontsize=11)
    ctext(ax, 3.48, -0.10, r'$\omega$', fontsize=11)
    ctext(ax, -0.10, -0.09, r'$O$', fontsize=10)
    ax.plot([0], [0], 'k.', ms=5)
    ctext(ax, -0.10, 1.0, '1', fontsize=9.5)
    # F=1 水平线与交点
    ax.plot([0, 3.44], [1, 1], 'k-', lw=1.1)
    if heavy:
        for x in xs:                               # 带内根：紧邻右渐近线
            ax.plot([x - 0.055], [1.0], 'k.', ms=5)
    else:
        for x in xs[:-1]:                          # 带内根：紧邻左渐近线
            ax.plot([x + 0.055], [1.0], 'k.', ms=5)
        ax.plot([xM + 0.63], [1.0], 'k.', ms=5)    # 局域模根
    for x in xs:
        ax.plot([x], [0.0], 'k.', ms=5)
    ctext(ax, xM + 0.13, -0.13, r'$\omega_{\rm M}$', fontsize=9.5)


def fig_2_13():
    """图2.13 式(2.10.14)的作图解"""
    fig, axs = plt.subplots(2, 1, figsize=(5.6, 5.9))
    for ax, heavy, cap in [(axs[0], True, '(a) 重杂质情况'),
                           (axs[1], False, '(b) 轻杂质情况')]:
        plain_axes(ax)
        ax.set_xlim(-0.35, 4.05)
        ax.set_ylim(-1.35, 1.35)
        ax.set_aspect('auto')
        _f_panel(ax, heavy)
        ax.text(3.66, 1.16, (r'$\varepsilon<0$' if heavy else r'$\varepsilon>0$'),
                fontsize=10, ha='center', va='center')
        ax.text(3.66, 0.90, (r"$(M'>M)$" if heavy else r"$(M'<M)$"),
                fontsize=10, ha='center', va='center')
        ax.text(1.85, -1.24, cap, fontsize=10.5,
                ha='center', va='center', fontfamily='SimSun',
                bbox=dict(fc='white', ec='none', pad=1.8), zorder=5)
    fig.subplots_adjust(hspace=0.14)
    save(fig, '2-13')


# ================================================================ 图 3.1
def _spin_arrow(ax, x, y0, ln, lw=2.3, ms=13):
    arr(ax, x, y0, x, y0 + ln, lw=lw, ms=ms)


def fig_3_1():
    """自旋-自旋互作用系统的基态"""
    fig, ax = plt.subplots(figsize=(4.9, 3.15))
    plain_axes(ax)
    ax.set_xlim(-0.5, 7.6)
    ax.set_ylim(-4.9, 1.6)
    ax.set_aspect('equal')
    sp = 0.55
    # (a) 铁磁
    for i in range(6):
        _spin_arrow(ax, i * sp, 0, 0.95)
    ctext(ax, 1.55, -0.55, '(a)简单铁磁序', fontsize=10)
    # (b) 反铁磁：长↑与短↓自同一顶线垂下（照原书比例）
    x0 = 4.1
    for i in range(6):
        if i % 2 == 1:
            _spin_arrow(ax, x0 + i * sp, 0, 0.95)             # 长自旋（自底线向上）
        else:
            arr(ax, x0 + i * sp, 0.95, x0 + i * sp, 0.36, lw=2.3, ms=13)
    ctext(ax, x0 + 1.4, -0.55, '(b) 简单反铁磁序', fontsize=10)
    # (c) 铁淦氧磁序：长↑与短↓自同一顶线垂下
    y0 = -2.9
    for i in range(8):
        x = 0.9 + i * sp
        if i % 2 == 0:
            _spin_arrow(ax, x, y0, 1.05)          # 长自旋（尾在下）
        else:
            arr(ax, x, y0 + 1.05, x, y0 + 0.50, lw=2.3, ms=13)  # 短自旋（尾在顶线）
    ctext(ax, 2.9, y0 - 0.30, '(c) 铁淦氧磁序', fontsize=10)
    save(fig, '3-1')


# ================================================================ 图 3.2
def fig_3_2():
    """自旋波的经典图像"""
    fig, axs = plt.subplots(2, 1, figsize=(4.9, 3.7))
    dx = 0.62
    # ---- (a) 立体图：顶线处"眼形"进动圆，自旋箭头自底部转出
    ax = axs[0]
    plain_axes(ax)
    ax.set_xlim(-0.45, 4.45)
    ax.set_ylim(-0.85, 0.65)
    ax.set_aspect('equal')
    yb = 0.0                       # 自旋尾部（底）高度
    ye = 0.50                      # 眼形中心高度
    w, hl, hu = 0.185, 0.085, 0.10
    for j in range(7):
        x = 0.25 + j * dx
        # 眼形（上下两弧，两端尖）
        tu = np.linspace(np.pi, 0, 60)
        ax.plot(x + w * np.cos(tu), ye + hu * np.sin(tu), 'k-', lw=1.1)
        tl = np.linspace(np.pi, 2 * np.pi, 60)
        ax.plot(x + w * np.cos(tl), ye + hl * np.sin(tl), 'k-', lw=1.1)
        # 进动方向小箭头（上弧左段，指向左端尖点）
        ta = np.linspace(np.deg2rad(150), np.deg2rad(172), 20)
        xs_ = x + w * np.cos(ta)
        ys_ = ye + hu * np.sin(ta)
        ax.plot(xs_, ys_, 'k-', lw=1.0)
        arr(ax, xs_[-3], ys_[-3], xs_[-1], ys_[-1], lw=1.0, ms=7)
        # 竖直虚线轴（尾 -> 眼中心）
        dline(ax, x, yb, x, ye, lw=1.0)
        # 自旋箭头：方位角 phi = 90 - 45(j)
        ph = np.deg2rad(90 - 45 * j)
        tip = (x + 1.02 * w * np.sin(ph), ye - 1.05 * hl * np.cos(ph))
        arr(ax, x, yb, tip[0], tip[1], lw=1.6, ms=10)
    ctext(ax, 2.11, -0.62, '(a) 立体图', fontsize=10)
    # ---- (b) 顶观图
    ax = axs[1]
    plain_axes(ax)
    ax.set_xlim(-0.45, 4.45)
    ax.set_ylim(-0.52, 0.52)
    ax.set_aspect('equal')
    rr = 0.26
    tips = []
    for j in range(7):
        x = 0.25 + j * dx
        ax.add_patch(Circle((x, 0), rr, facecolor='none', edgecolor='k', lw=1.4))
        th = np.deg2rad(0 - 45 * j)
        tip = (x + rr * 0.97 * np.cos(th), rr * 0.97 * np.sin(th))
        arr(ax, x, 0, tip[0], tip[1], lw=1.4, ms=10)
        tips.append(tip)
    from scipy.interpolate import PchipInterpolator
    txx = [t[0] for t in tips]
    tyy = [t[1] for t in tips]
    f = PchipInterpolator(txx, tyy)
    xs = np.linspace(txx[0], txx[-1] + 0.28, 220)
    ax.plot(xs, f(xs), 'k-', lw=1.2)
    ctext(ax, 2.11, -0.44, '(b) 顶观图', fontsize=10)
    fig.subplots_adjust(hspace=0.42)
    save(fig, '3-2')


# ================================================================ 图 3.3
def fig_3_3():
    """图3.3（无图注文字）：偏转在 l 与 l+1 格点间传递"""
    fig, axs = plt.subplots(1, 2, figsize=(4.9, 1.85))
    for ax, dev in [(axs[0], 2), (axs[1], 3)]:
        plain_axes(ax)
        ax.set_xlim(-0.55, 3.05)
        ax.set_ylim(-1.55, 0.85)
        ax.set_aspect('equal')
        for i in range(6):
            x = 0.5 * i
            if i == dev:
                # 偏转格点：dot 下方虚线 + dot 上方短箭头 + 斜箭头
                dline(ax, x, -0.55, x, -0.03, lw=1.2)
                arr(ax, x, 0.05, x, 0.32, lw=1.6, ms=9)
                arr(ax, x - 0.30, -0.42, x + 0.33, 0.55, lw=2.0, ms=12)
                ax.plot([x], [0.0], 'k.', ms=7)
            else:
                arr(ax, x, -0.55, x, 0.55, lw=2.0, ms=12)
                ax.plot([x], [0.0], 'k.', ms=7)
        ctext(ax, 1.0, -0.82, r'$l$', fontsize=10.5)
        ctext(ax, 1.5, -0.82, r'$l{+}1$', fontsize=10.5)
        ctext(ax, 1.25, -1.32, f'({chr(97 + (dev == 3))})', fontsize=10.5)
    save(fig, '3-3')


# ================================================================ 图 3.4
def fig_3_4():
    """EuO 的 hbar omega_k(T) 曲线，Tc=69.1 K"""
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(3.7, 3.5))
    plain_axes(ax)
    # 框
    ax.plot([0, 72, 72, 0, 0], [0, 0, 6.55, 6.55, 0], 'k-', lw=1.1)
    # y 轴刻度：主刻度 3、6 带标注，其余每 1 meV 短刻度
    for v in range(1, 7):
        ax.plot([-0.9 if v in (3, 6) else -0.6, 0], [v, v], 'k-',
                lw=1.0 if v in (3, 6) else 0.9)
    for v in (3, 6):
        ctext(ax, -2.0, v, str(v), fontsize=9.5, ha='right')
    # x 轴刻度：10/30/50/70 主，20/40/60 次
    for v in (10, 20, 30, 40, 50, 60, 70):
        ax.plot([v, v], [0, 0.16 if v in (10, 30, 50, 70) else 0.10],
                'k-', lw=1.0)
    for v in (10, 30, 50, 70):
        ctext(ax, v, -0.42, str(v), fontsize=9.5)
    ctext(ax, -2.4, -0.35, r'$O$', fontsize=10, ha='right')
    ctext(ax, 0.5, 6.92, r'$\hbar\omega_k(T)$/meV', fontsize=10, ha='left')
    arrow_axis(ax, 0, 0, 71.3, 0, lw=1.1)          # 底轴箭头（框内）
    Tc = 69.1
    ax.plot([Tc, Tc], [0, 0.45], 'k-', lw=1.0)     # Tc 短竖线
    ctext(ax, Tc - 1.6, 0.62, r'$T_{\rm c}$', fontsize=10)

    def curve(pts, trange):
        f = PchipInterpolator([p[0] for p in pts], [p[1] for p in pts])
        t = np.linspace(trange[0], trange[1], 160)
        return t, f(t)
    # k=10 (square)
    t, y = curve([(0, 5.70), (10, 5.62), (20, 5.55), (30, 5.38), (41, 5.02),
                  (51, 4.52), (57, 4.12), (60, 3.75)], (0, 60))
    ax.plot(t, y, 'k-', lw=1.4)
    for tt, yy in [(10, 5.60), (30, 5.36), (45, 4.90), (55, 4.32)]:
        ax.plot([tt], [yy], 's', mfc='white', mec='k', ms=5, mew=1.0)
    # k=8 (triangle)
    t, y = curve([(0, 4.72), (10, 4.66), (20, 4.58), (30, 4.48), (41, 4.20),
                  (51, 3.80), (56, 3.42), (58.5, 3.10)], (0, 58.5))
    ax.plot(t, y, 'k-', lw=1.4)
    for tt, yy in [(10, 4.64), (30, 4.46), (45, 4.12), (53, 3.70)]:
        ax.plot([tt], [yy], '^', mfc='white', mec='k', ms=5.5, mew=1.0)
    # k=6 (circle)
    t, y = curve([(0, 3.30), (10, 3.26), (20, 3.19), (30, 3.10), (41, 2.94),
                  (51, 2.68), (56, 2.45)], (0, 56))
    ax.plot(t, y, 'k-', lw=1.4)
    for tt, yy in [(10, 3.25), (30, 3.14), (45, 2.90), (53, 2.62)]:
        ax.plot([tt], [yy], 'o', mfc='white', mec='k', ms=5, mew=1.0)
    ax.plot([57.5], [2.10], 'o', mfc='white', mec='k', ms=5, mew=1.0)  # 脱离点
    # k=2 (filled circle)
    t, y = curve([(0, 0.50), (10, 0.49), (20, 0.483), (30, 0.475), (40, 0.465),
                  (50, 0.455), (55, 0.448), (60, 0.428), (63, 0.375),
                  (66, 0.25), (68, 0.12), (69.1, 0.02), (69.4, 0.0)], (0, 69.4))
    ax.plot(t, y, 'k-', lw=1.4)
    for tt, yy in [(10, .49), (20, .483), (30, .475), (40, .465), (50, .455),
                   (56.5, .447), (58, .444), (59.5, .44), (61, .43),
                   (63.5, .36), (65.5, .24), (67.5, .10), (69.0, .015)]:
        ax.plot([tt], [yy], 'o', mfc='k', mec='k', ms=4)
    ax.set_xlim(-5, 76)
    ax.set_ylim(-0.75, 7.3)
    save(fig, '3-4')


# ================================================================ 图 3.5
def fig_3_5():
    """Fe3O4 中的自旋波（24℃，[001]）"""
    from scipy.interpolate import PchipInterpolator
    fig, ax = plt.subplots(figsize=(3.35, 3.2))
    plain_axes(ax)                             # 去默认刻度/边框，仅保留自绘标度
    for s in ax.spines.values():
        s.set_visible(False)
    ax.plot([0, 1.05, 1.05, 0, 0], [0, 0, 0.95, 0.95, 0], 'k-', lw=1.2)
    for v in (0.2, 0.4, 0.6, 0.8, 1.0):
        ax.plot([v, v], [0, 0.025], 'k-', lw=1.0)
        ctext(ax, v, -0.06, f'{v:.1f}' if v != 1.0 else '1.0', fontsize=9.5)
    for v in (0.2, 0.4, 0.6, 0.8):
        ax.plot([0, 0.022], [v, v], 'k-', lw=1.0)
        ctext(ax, -0.035, v, f'{v:.1f}', fontsize=9.5, ha='right')
    ctext(ax, -0.03, -0.06, r'$O$', fontsize=10)
    ctext(ax, 0.02, 1.005, r'$\hbar\omega$/eV', fontsize=10.5, ha='left')
    ctext(ax, 0.86, 0.885, '24℃', fontsize=10, fontfamily='SimSun')
    ctext(ax, 0.87, 0.815, '[001]', fontsize=10)
    fo = PchipInterpolator([0, .10, .20, .30, .38, .45],
                           [.57, .60, .645, .705, .775, .862])
    xs = np.linspace(0, 0.45, 160)
    ax.plot(xs, fo(xs), 'k-', lw=1.6)
    ctext(ax, 0.345, 0.725, '光频自旋波', fontsize=10, fontfamily='SimSun')
    fa = PchipInterpolator([0, .05, .10, .20, .30, .40, .50, .60, .70,
                            .80, .90, 1.0],
                           [.004, .018, .05, .155, .295, .415, .515, .595,
                            .652, .692, .718, .74])
    xs = np.linspace(0, 1.0, 240)
    ax.plot(xs, fa(xs), 'k-', lw=1.6)
    ctext(ax, 0.60, 0.42, '声频自旋波', fontsize=10, fontfamily='SimSun')
    ax.set_xlim(-0.09, 1.13)
    ax.set_ylim(-0.13, 1.04)
    save(fig, '3-5')


if __name__ == '__main__':
    todo = ['1-1', '1-2', '1-3', '1-4', '1-5', '1-6', '1-7', '1-8',
            '2-1', '2-2', '2-3', '2-4', '2-5', '2-6', '2-7', '2-8',
            '2-9', '2-10', '2-11', '2-12', '2-13',
            '3-1', '3-2', '3-3', '3-4', '3-5']
    import sys
    if len(sys.argv) > 1:
        todo = sys.argv[1:]
    for t in todo:
        fn = 'fig_' + t.replace('-', '_')
        globals()[fn]()
        print(f'fig{t} done', flush=True)
