# -*- coding: utf-8 -*-
"""
B1 批次：文小刚《多体量子场论》第1章+第2章 12 幅插图重绘（黑白矢量）。
输出: figures/fig_{key}.pdf + figures/preview/fig_{key}.png
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Ellipse, Arc, Rectangle, Circle, Polygon

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

LW = 1.1          # 主体曲线
LW_AX = 0.8       # 坐标轴细线
DASH = (4, 2.4)


def save(fig, key):
    fig.savefig(os.path.join(FIGDIR, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREVDIR, 'fig_%s.png' % key),
                bbox_inches='tight', pad_inches=0.03, dpi=170)
    plt.close(fig)
    print('fig_%s done' % key)


def arrow(ax, p0, p1, lw=1.0, ms=10, style='-|>', color='k'):
    """自绘箭头（合同要求 annotate + -|>）。"""
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, lw=lw, color=color,
                                shrinkA=0, shrinkB=0,
                                mutation_scale=ms))


def catmull_rom(pts, n=24):
    """Catmull-Rom 平滑样条，pts: list of (x,y)。"""
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


# ---------------------------------------------------------------- 1.1 分类树
def _box(ax, cx, cy, w, h, text, fs=9.2):
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle='round,pad=0.02,rounding_size=0.07',
                                fc='white', ec='k', lw=0.9, zorder=3))
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs, zorder=4)


def _ell(ax, cx, cy, w, h, text, fs=9.2):
    ax.add_patch(Ellipse((cx, cy), w, h, fc='white', ec='k', lw=0.9, zorder=2))
    ax.text(cx, cy, text, ha='center', va='center', fontsize=fs, zorder=3)


def _line(ax, pts, lw=0.8):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color='k', lw=lw, zorder=1, solid_capstyle='round')


def fig_1_1():
    fig, ax = plt.subplots(figsize=(7.4, 4.0))
    ax.set_xlim(-0.55, 11.0); ax.set_ylim(2.2, 7.6)
    ax.set_aspect('auto'); ax.axis('off')

    # 顶层
    _box(ax, 4.65, 7.30, 1.15, 0.44, 'Orders')
    _line(ax, [(4.65, 7.08), (4.65, 6.86)])
    _line(ax, [(1.55, 6.86), (6.50, 6.86)])
    _line(ax, [(1.55, 6.86), (1.55, 6.66)])
    _line(ax, [(6.50, 6.86), (6.50, 6.66)])
    _box(ax, 1.55, 6.24, 3.15, 0.82,
         "Symmetry-breaking orders\n'Particle' condensation")
    _box(ax, 6.50, 6.32, 3.55, 0.44, 'Non-symmetry-breaking orders', fs=8.8)
    _ell(ax, 1.55, 5.36, 3.45, 0.98, 'Symmetry group\nNambu–Goldstone mode')

    # 右支：量子/经典系统
    _line(ax, [(6.50, 6.10), (6.50, 5.78)])
    _line(ax, [(5.50, 5.78), (7.90, 5.78)])
    _line(ax, [(5.50, 5.78), (5.50, 5.44)])
    _line(ax, [(7.90, 5.78), (7.90, 5.44)])
    ax.text(5.62, 5.56, 'Quantum system', fontsize=9.2, ha='left', va='center')
    ax.text(8.02, 5.56, 'Classical system', fontsize=9.2, ha='left', va='center')
    _box(ax, 5.50, 5.22, 2.05, 0.44, 'Quantum orders')
    _box(ax, 7.90, 5.22, 2.05, 0.44, '')

    # Quantum orders 下三支
    _line(ax, [(5.50, 5.00), (5.50, 4.64)])
    _line(ax, [(1.55, 4.64), (9.60, 4.64)])
    _line(ax, [(1.55, 4.64), (1.55, 4.38)])
    _line(ax, [(4.75, 4.64), (4.75, 4.38)])
    _line(ax, [(7.90, 4.64), (7.90, 4.38)])
    ax.text(1.68, 4.49, 'Gapped', fontsize=9.2, ha='left', va='center')
    _box(ax, 1.70, 3.94, 2.95, 0.88, 'Topological orders\nTopological field theory',
         fs=8.8)
    _box(ax, 4.75, 3.94, 2.72, 0.88, 'Fermi liquids\nFermi surface topology',
         fs=8.6)
    _box(ax, 7.90, 4.12, 3.15, 0.52, 'String-net condensation')
    _ell(ax, 1.60, 3.06, 3.05, 0.80, r'Conformal algebra, $\eta$?')
    _ell(ax, 7.90, 3.22, 5.15, 1.06,
         'Projective symmetry group\nGapless gauge bosons/fermions')
    save(fig, '1.1')


# ---------------------------------------------------------------- 1.2 弦网
def _rounded_path(pts, r=0.16, closed=True):
    """折线转圆角路径（顶点处二次 Bezier）。"""
    P = list(pts)
    if closed:
        P = [P[-1]] + P + [P[0], P[1]]
    out = [np.asarray(P[1], float)]
    tv = np.linspace(0, 1, 8)
    for i in range(1, len(P) - 2):
        A, B, C = (np.asarray(P[j], float) for j in (i - 1, i, i + 1))
        d1, d2 = np.linalg.norm(A - B), np.linalg.norm(C - B)
        if d1 < 1e-9 or d2 < 1e-9:
            continue
        rr = min(r, 0.45 * d1, 0.45 * d2)
        p1 = B + (A - B) / d1 * rr
        p2 = B + (C - B) / d2 * rr
        out.append(p1)
        bez = ((1 - tv) ** 2)[:, None] * p1 \
            + (2 * (1 - tv) * tv)[:, None] * B \
            + (tv ** 2)[:, None] * p2
        out.extend(list(bez))
    out.append(np.asarray(P[-2], float))
    return np.vstack(out)


def _trochoid_coil(ax, x0, y0, n_loop, a, b, lw=1.1):
    """ prolate trochoid 线圈：x = x0 + a t - b sin t, y = y0 + b(1-cos t)/1 上凸环。
        t: 0 -> 2 pi n_loop """
    t = np.linspace(0, 2 * np.pi * n_loop, 60 * n_loop)
    x = x0 + a * t - b * np.sin(t)
    y = y0 + b - b * np.cos(t)
    ax.plot(x, y, color='k', lw=lw, solid_capstyle='round')


def _loop_coil(ax, xa, xb, y0, n_loop=4, r=0.40, lift=0.28, step=0.55,
               lw=1.15):
    """交叠圆环线圈：n_loop 个相互交叠的圆（圆心在导线上方 lift），
    导线在圆环群两侧引入；相邻线匝相交，模拟原书绕线。"""
    m = r * r - lift * lift
    dx = np.sqrt(m) if m > 0 else 0.0
    total = step * (n_loop - 1) + 2 * r
    c0 = 0.5 * (xa + xb) - 0.5 * total + r
    cis = c0 + step * np.arange(n_loop)
    # 引入导线（到第一匝左交点 / 末匝右交点起）
    for xa_, xb_ in ((xa, cis[0] - dx), (cis[-1] + dx, xb)):
        if xb_ - xa_ > 0.02:
            ax.plot([xa_, xb_], [y0, y0], color='k', lw=lw,
                    solid_capstyle='butt')
    for ci in cis:
        ax.add_patch(Circle((ci, y0 + lift), r, fc='none', ec='k', lw=lw))


def fig_1_2():
    rng = np.random.default_rng(20251008)
    W, H, L = 9.2, 4.8, 0.52
    DIRS = np.arange(8) * 45.0
    LO, HI = -0.30, W + 0.30

    def step(p, d):
        return p + L * np.array([np.cos(np.deg2rad(d)), np.sin(np.deg2rad(d))])

    def turn(d):
        """持续直行为主的转向。"""
        r = rng.random()
        if r < 0.50:
            return d
        if r < 0.68:
            return d + 45
        if r < 0.86:
            return d - 45
        if r < 0.93:
            return d + 90
        return d - 90

    def walk_closed(p0, d0, maxstep=42):
        """随机游走；走到起点附近即闭合。"""
        p, d = np.asarray(p0, float), d0
        pts = [p.copy()]
        for i in range(maxstep):
            q = None
            for _ in range(14):
                dd = turn(d)
                cand = step(p, dd)
                if LO <= cand[0] <= W + 0.30 and -0.30 <= cand[1] <= H + 0.30:
                    q, d = cand, dd % 360
                    break
            if q is None:
                dd = (d + 180) % 360
                q = step(p, dd)
                d = dd
            pts.append(q.copy())
            p = q
            if i > 8 and np.linalg.norm(p - pts[0]) < 0.85 * L:
                pts.append(pts[0].copy())
                return pts
        return None

    def walk_open(p0, d0, nstep):
        p, d = np.asarray(p0, float), d0
        pts = [p.copy()]
        for _ in range(nstep):
            q = None
            for _ in range(14):
                dd = turn(d)
                cand = step(p, dd)
                if LO - 1.2 <= cand[0] <= W + 1.5 and -1.2 <= cand[1] <= H + 1.2:
                    q, d = cand, dd % 360
                    break
            if q is None:
                break
            pts.append(q.copy())
            p = q
        return pts

    fig, ax = plt.subplots(figsize=(7.4, 3.9))
    ax.set_xlim(-0.2, W + 0.2); ax.set_ylim(-0.2, H + 0.2)
    ax.set_aspect('equal'); ax.axis('off')

    # 闭合环：抖动网格起点，避免局部堆积
    cells = [(i, j) for i in range(5) for j in range(4)]
    rng.shuffle(cells)
    n_made = 0
    for (ci, cj) in cells:
        if n_made >= 19:
            break
        cw, ch = W / 5.0, H / 4.0
        p0 = np.array([cw * (ci + 0.5) + rng.uniform(-0.9, 0.9) * cw / 2,
                       ch * (cj + 0.5) + rng.uniform(-0.9, 0.9) * ch / 2])
        for _ in range(25):
            pts = walk_closed(p0, rng.choice(DIRS))
            if pts is not None:
                break
        if pts is None:
            continue
        rp = _rounded_path(pts, r=0.15, closed=True)
        ax.plot(rp[:, 0], rp[:, 1], color='k', lw=2.5,
                solid_capstyle='round', solid_joinstyle='round')
        n_made += 1

    # 开弦（起止于边界外，被裁剪）
    for _ in range(8):
        edge = rng.integers(4)
        if edge == 0:
            p0, d0 = np.array([rng.uniform(0, W), -0.6]), 90
        elif edge == 1:
            p0, d0 = np.array([rng.uniform(0, W), H + 0.6]), 270
        elif edge == 2:
            p0, d0 = np.array([-0.6, rng.uniform(0, H)]), 0
        else:
            p0, d0 = np.array([W + 0.6, rng.uniform(0, H)]), 180
        pts = walk_open(p0, d0 + rng.choice([-45, 0, 45]),
                        int(rng.integers(7, 17)))
        rp = _rounded_path(pts, r=0.15, closed=False)
        ax.plot(rp[:, 0], rp[:, 1], color='k', lw=2.5,
                solid_capstyle='round', solid_joinstyle='round')
    save(fig, '1.2')


# ---------------------------------------------------------------- 2.1 路径积分
def fig_2_1():
    fig, ax = plt.subplots(figsize=(5.0, 4.4))
    ax.set_xlim(0, 9.8); ax.set_ylim(0, 9.0); ax.axis('off')

    xb = [1.3, 3.7, 6.1, 8.5]
    y0, y1 = 1.0, 8.2
    for x in xb:                                   # 四根竖直粗线
        ax.plot([x, x], [y0, y1], color='k', lw=2.8, solid_capstyle='butt')

    xa = (1.3, 4.9)
    t1 = [(3.7, 6.35), (3.7, 5.0), (3.7, 3.05)]
    t2 = [(6.1, 6.85), (6.1, 5.65), (6.1, 3.05)]
    xbp = (8.5, 6.2)

    seg = []
    for p in t1:                                   # xa -> t1 各点
        seg += [(xa, p)]
    for p1 in t1:                                  # t1 -> t2 全连接
        for p2 in t2:
            seg += [(p1, p2)]
    for p in t2:                                   # t2 -> xb
        seg += [(p, xbp)]
    for a, b in seg:
        ax.plot([a[0], b[0]], [a[1], b[1]], color='k', lw=0.7)

    ax.text(1.02, 4.9, r'$x_a$', fontsize=11, ha='right', va='center')
    ax.text(8.76, 6.25, r'$x_b$', fontsize=11, ha='left', va='center')
    for x, lab in zip(xb, ['t_0', 't_1', 't_2', 't_3']):
        ax.text(x, 0.35, r'$%s$' % lab, fontsize=11, ha='center', va='center')
    save(fig, '2.1')


# ---------------------------------------------------------------- 2.2 CL 电路
def fig_2_2():
    fig, ax = plt.subplots(figsize=(4.4, 3.9))
    ax.set_xlim(0, 8.0); ax.set_ylim(0, 7.0); ax.set_aspect('equal'); ax.axis('off')
    xL, xR, yB, yT = 0.9, 6.7, 1.0, 6.3

    # 导线框（右侧留出电容位置）
    ax.plot([xL, xL], [yB, yT], 'k-', lw=1.2)
    ax.plot([xL, 2.1], [yT, yT], 'k-', lw=1.2)
    _loop_coil(ax, 2.1, 5.55, yT, n_loop=4, r=0.40, lift=0.28, lw=1.15)
    ax.plot([5.55, xR], [yT, yT], 'k-', lw=1.2)
    ax.plot([xL, xR], [yB, yB], 'k-', lw=1.2)
    ax.plot([xR, xR], [yB, 4.66], 'k-', lw=1.2)
    ax.plot([xR, xR], [3.32, yB], 'k-', lw=1.2)

    # 电容（水平极板）+ 偶极子
    for yc in (4.60, 3.38):
        ax.add_patch(Rectangle((xR - 0.52, yc), 1.04, 0.11, fc='k', ec='k'))
    ax.add_patch(Circle((xR, 3.97), 0.05, fc='k', ec='k'))
    arrow(ax, (xR, 4.02), (xR, 4.38), lw=0.9, ms=8)

    ax.text(2.15, 5.72, r'$L$', fontsize=12, ha='center', va='center')
    ax.text(xR - 0.66, 3.97, 'Dipole', fontsize=10.5, ha='right', va='center')
    ax.text(7.35, 3.93, r'$C$', fontsize=12, ha='left', va='center')
    save(fig, '2.2')


# ---------------------------------------------------------------- 2.3 围道
def fig_2_3():
    fig, ax = plt.subplots(figsize=(6.2, 3.2))
    ax.set_xlim(0, 12.6); ax.set_ylim(0, 5.4)
    ax.set_aspect('equal'); ax.axis('off')

    # C1：包围虚轴的细长围道
    cx, cy = 2.7, 2.7
    ax.plot([0.4, 5.0], [cy, cy], color='0.55', lw=0.6)          # 实轴
    ax.plot([cx, cx], [0.35, 5.05], color='0.55', lw=0.6)        # 虚轴
    ax.add_patch(FancyBboxPatch((cx - 0.155, 1.05), 0.31, 3.3,
                                boxstyle='round,pad=0.0,rounding_size=0.155',
                                fc='none', ec='k', lw=1.3))
    arrow(ax, (cx + 0.155, 3.30), (cx + 0.155, 3.95), lw=1.3, ms=11)

    # C2：绕原点的圆
    cx2 = 9.6
    ax.plot([7.3, 11.9], [cy, cy], color='0.55', lw=0.6)
    ax.plot([cx2, cx2], [0.35, 5.05], color='0.55', lw=0.6)
    R = 1.95
    ax.add_patch(Circle((cx2, cy), R, fc='none', ec='k', lw=1.3))
    a0 = np.deg2rad(-10)
    p0 = (cx2 + R * np.cos(a0 - 0.14), cy + R * np.sin(a0 - 0.14))
    p1 = (cx2 + R * np.cos(a0 + 0.02), cy + R * np.sin(a0 + 0.02))
    arrow(ax, p0, p1, lw=1.3, ms=11)
    save(fig, '2.3')


# ---------------------------------------------------------------- 2.4 平行移动
def fig_2_4():
    fig, ax = plt.subplots(figsize=(8.2, 3.7))
    ax.set_xlim(0, 12.6); ax.set_ylim(-0.7, 5.5)
    ax.set_aspect('equal'); ax.axis('off')

    C = np.array([2.45, 2.45]); R = 2.05

    # 球面外轮廓
    ax.add_patch(Circle(C, R, fc='none', ec='k', lw=0.8))

    def ell_arc(center, a, b, rot, th1, th2, lw=0.65, dash=None, color='k'):
        t = np.linspace(np.deg2rad(th1), np.deg2rad(th2), 200)
        xs = a * np.cos(t); ys = b * np.sin(t)
        cr, sr = np.cos(np.deg2rad(rot)), np.sin(np.deg2rad(rot))
        xr = center[0] + xs * cr - ys * sr
        yr = center[1] + xs * sr + ys * cr
        if dash:
            ax.plot(xr, yr, color=color, lw=lw, ls=(0, dash))
        else:
            ax.plot(xr, yr, color=color, lw=lw)

    # 赤道：前(下)实线, 后(上)虚线
    ell_arc(C, R, 0.72, -9, 180, 360, lw=0.65)
    ell_arc(C, R, 0.72, -9, 0, 180, lw=0.6, dash=DASH)
    # 经线：左(前)实线, 右(后)虚线
    ell_arc(C, 0.78, R, 14, 90, 270, lw=0.65)
    ell_arc(C, 0.78, R, 14, -90, 90, lw=0.6, dash=DASH)
    # 另一条经线（偏斜, 大部分虚线）
    ell_arc(C, 0.38, R, -10, 100, 260, lw=0.6, dash=DASH)

    # 粗闭环路（顶部留缺口）
    a_lp, b_lp, rot = 2.0, 1.68, -7
    gap1, gap2 = 82.0, 100.0        # 缺口区间(度)
    t = np.linspace(np.deg2rad(gap2), np.deg2rad(gap1 + 360), 500)
    xs = a_lp * np.cos(t); ys = b_lp * np.sin(t)
    cr, sr = np.cos(np.deg2rad(rot)), np.sin(np.deg2rad(rot))
    lx = C[0] + xs * cr - ys * sr
    ly = C[1] + xs * sr + ys * cr
    ax.plot(lx, ly, color='k', lw=1.9, solid_capstyle='round')

    def loop_pt(theta_deg):
        t = np.deg2rad(theta_deg)
        xs = a_lp * np.cos(t); ys = b_lp * np.sin(t)
        p = np.array([C[0] + xs * cr - ys * sr, C[1] + xs * sr + ys * cr])
        dx = -a_lp * np.sin(t); dy = b_lp * np.cos(t)
        dv = np.array([dx * cr - dy * sr, dx * sr + dy * cr])
        return p, dv / np.linalg.norm(dv)

    # 沿路切矢箭头（行进方向：自顶点逆参数下行）
    for th in (128, 163, 213, 252):
        p, dv = loop_pt(th)
        arrow(ax, p - 0.40 * dv, p + 0.48 * dv, lw=2.2, ms=17)

    # 顶部：初/末切矢量 + theta_B 弧
    p_s, dv_s = loop_pt(gap2)       # 起点（左），指向左下
    p_e, dv_e = loop_pt(gap1)       # 终点（右）
    arrow(ax, p_s - 0.05 * dv_s, p_s + 0.62 * dv_s, lw=2.4, ms=19)
    dv_f = np.array([np.cos(np.deg2rad(8)), np.sin(np.deg2rad(8))])   # 末矢量：向右
    arrow(ax, p_e - 0.55 * dv_f, p_e + 0.55 * dv_f, lw=2.4, ms=19)
    th = np.linspace(np.deg2rad(150), np.deg2rad(255), 60)
    arcR = 0.42
    axp = C[0] + a_lp * np.cos(np.deg2rad(91)) * cr - b_lp * np.sin(np.deg2rad(91)) * sr
    ayp = C[1] + a_lp * np.cos(np.deg2rad(91)) * sr + b_lp * np.sin(np.deg2rad(91)) * cr
    ax.plot(axp + arcR * np.cos(th), ayp + arcR * np.sin(th), color='k', lw=0.7)
    arrow(ax, (axp + arcR * np.cos(th[-2]), ayp + arcR * np.sin(th[-2])),
          (axp + arcR * np.cos(th[-1]), ayp + arcR * np.sin(th[-1])),
          lw=0.7, ms=8)
    ax.text(axp + 0.02, ayp - 0.82, r'$\theta_B$', fontsize=12, ha='center')

    # n(t) 矢量
    arrow(ax, (3.05, 1.75), (1.62, 3.42), lw=0.9, ms=10)
    ax.text(2.66, 2.92, r'$\boldsymbol{n}(t)$', fontsize=11.5,
            ha='left', va='center')

    # ------- 右侧：平行移动 = 平移 + 投影 -------
    # 上平面
    up = [(6.75, 4.85), (10.75, 4.85), (9.75, 3.55), (5.75, 3.55)]
    ax.add_patch(Polygon(up, closed=True, fc='none', ec='k', lw=0.7))
    # 上平面上的矢量
    v0, v1 = (8.35, 4.20), (10.0, 4.20)
    arrow(ax, v0, v1, lw=2.2, ms=17)
    # 垂直虚线（平移）
    f0, f1 = (8.35, 1.62), (10.08, 1.28)
    ax.plot([v0[0], f0[0]], [v0[1], f0[1]], color='k', lw=0.6, ls=(0, (3, 2)))
    ax.plot([v1[0], f1[0]], [v1[1], f1[1]], color='k', lw=0.6, ls=(0, (3, 2)))
    # 下平面
    lo = [(6.10, 2.20), (10.65, 1.25), (9.75, 0.42), (5.20, 1.37)]
    ax.add_patch(Polygon(lo, closed=True, fc='none', ec='k', lw=0.7))
    # 投影矢量 + 端点小圆
    arrow(ax, f0, f1, lw=2.2, ms=17)
    ax.add_patch(Circle(f0, 0.05, fc='white', ec='k', lw=0.8))
    ax.add_patch(Circle(f1, 0.05, fc='white', ec='k', lw=0.8))
    ax.text(6.85, 2.72, 'Parallel\nshift', fontsize=10.5, ha='center', va='center')
    ax.text(10.2, 0.72, 'Projection', fontsize=10.5, ha='left', va='center')
    ax.text(7.9, -0.32, 'Parallel transportation', fontsize=10.5,
            ha='center', va='center')
    save(fig, '2.4')


# ---------------------------------------------------------------- 2.5 双势阱
def fig_2_5():
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    ax.set_xlim(0, 7.0); ax.set_ylim(0.6, 5.3); ax.axis('off')
    yA = 2.15
    ax.plot([0.6, 6.4], [yA, yA], color='k', lw=LW_AX)            # 水平轴
    ax.plot([3.5, 3.5], [1.25, 5.0], color='k', lw=LW_AX)         # V 轴
    ax.text(3.66, 4.92, r'$V$', fontsize=12, ha='left', va='center')

    x = np.linspace(-1.78, 1.78, 500)
    V = (x * x - 1) ** 2
    ax.plot(3.5 + 1.05 * x, yA + 0.60 * V, color='k', lw=LW)
    ax.text(3.5 - 1.05, yA - 0.30, r'$-x_0$', fontsize=11.5, ha='center', va='center')
    ax.text(3.5 + 1.05, yA - 0.30, r'$x_0$', fontsize=11.5, ha='center', va='center')
    save(fig, '2.5')


# ------------------------------------------------- 2.6 单瞬子（a 势 / b x(t)）
def fig_2_6():
    fig, ax = plt.subplots(figsize=(7.0, 2.9))
    ax.set_xlim(0, 10.0); ax.set_ylim(-3.3, 1.15); ax.axis('off')

    # (a) 翻转势 + 轨迹
    ax.plot([0.35, 4.45], [0, 0], color='k', lw=LW_AX)
    ax.plot([2.35, 2.35], [-2.95, 0.62], color='k', lw=LW_AX)
    ax.text(2.49, 0.52, r'$V$', fontsize=12, ha='left', va='center')
    x = np.linspace(-1.73, 1.73, 500)
    ax.plot(2.35 + 1.15 * x, -0.80 * (x * x - 1) ** 2, color='k', lw=LW)
    xt = np.linspace(-1.0, 1.0, 300)
    yt = -0.80 * (xt * xt - 1) ** 2 + 0.14 * (1 - xt * xt)
    ax.plot(2.35 + 1.15 * xt, yt, color='k', lw=0.75)
    i0 = np.searchsorted(xt, 0.80)
    i1 = np.searchsorted(xt, 0.965)
    arrow(ax, (2.35 + 1.15 * xt[i0], yt[i0]),
          (2.35 + 1.15 * xt[i1], yt[i1]), lw=0.7, ms=6)
    ax.text(2.35 - 1.15, 0.17, r'$-x_0$', fontsize=11.5, ha='center', va='center')
    ax.text(2.35 + 1.15, 0.17, r'$x_0$', fontsize=11.5, ha='center', va='center')
    ax.text(0.55, 0.62, '(a)', fontsize=11, ha='center', va='center')

    # (b) x(t)：x0 -> -x0 的台阶
    xL, xR = 5.6, 9.5
    ax.plot([xL, 8.05], [0.92, 0.92], color='k', lw=0.8, ls=(0, (1.2, 2.2)))
    ax.plot([6.7, xR], [0.0, 0.0], color='k', lw=0.8, ls=(0, (1.2, 2.2)))
    ax.text(xL - 0.12, 0.92, r'$-x_0$', fontsize=11.5, ha='right', va='center')
    ax.text(xL - 0.12, 0.0, r'$x_0$', fontsize=11.5, ha='right', va='center')
    ax.plot([xL, 6.7], [0, 0], color='k', lw=LW)
    ts = np.linspace(6.7, 7.75, 200)
    xs = 0.46 * (np.tanh(5.2 * (ts - 7.22)) + 1)
    ax.plot(ts, xs, color='k', lw=LW)
    ax.plot([7.75, xR], [0.92, 0.92], color='k', lw=LW)
    # t 轴
    ax.plot([6.15, 9.42], [0.46, 0.46], color='k', lw=0.7)
    arrow(ax, (9.30, 0.46), (9.48, 0.46), lw=0.7, ms=9)
    ax.text(9.44, 0.22, r'$t$', fontsize=11.5, ha='center', va='center')
    ax.text(5.75, 1.22, '(b)', fontsize=11, ha='center', va='center')
    save(fig, '2.6')


# ---------------------------------------------------------------- 2.7 瞬子气体
def fig_2_7():
    fig, ax = plt.subplots(figsize=(6.6, 2.6))
    ax.set_xlim(0, 10.2); ax.set_ylim(-0.55, 3.05); ax.axis('off')

    xL, xR = 0.5, 9.7
    ax.plot([xL, xR], [2.0, 2.0], color='k', lw=0.8, ls=(0, (1.2, 2.2)))
    ax.plot([xL, xR], [0.0, 0.0], color='k', lw=0.8, ls=(0, (1.2, 2.2)))
    ax.text(xL - 0.12, 2.0, r'$-x_0$', fontsize=11.5, ha='right', va='center')
    ax.text(xL - 0.12, 0.0, r'$x_0$', fontsize=11.5, ha='right', va='center')
    # t 轴
    ax.plot([0.75, 9.6], [1.0, 1.0], color='k', lw=0.7)
    arrow(ax, (9.48, 1.0), (9.66, 1.0), lw=0.7, ms=9)
    ax.text(9.62, 0.74, r'$t$', fontsize=11.5, ha='center', va='center')

    def seg(xa, xb, ya, yb, xc, sgn=1):
        ts = np.linspace(xa, xb, 160)
        ys = ya + (yb - ya) * (np.tanh(sgn * 4.6 * (ts - xc)) + 1) / 2
        ax.plot(ts, ys, color='k', lw=LW)

    ax.plot([xL, 2.45], [0, 0], color='k', lw=LW)
    seg(2.45, 3.75, 0, 2.0, 3.1)
    ax.plot([3.75, 4.9], [2.0, 2.0], color='k', lw=LW)
    seg(4.9, 6.15, 2.0, 0.0, 5.5, sgn=-1)
    ax.plot([6.15, 7.35], [0, 0], color='k', lw=LW)
    seg(7.35, 8.6, 0, 2.0, 8.0)
    ax.plot([8.6, xR], [2.0, 2.0], color='k', lw=LW)

    # 穿越时刻
    for xc, lab in [(3.1, 't_1'), (5.5, 't_2'), (8.0, 't_3')]:
        ax.text(xc + 0.22, 0.72, r'$%s$' % lab, fontsize=11.5,
                ha='left', va='center')

    # t_tun 标注（第一条跃迁）
    for xt in (2.68, 3.52):
        ax.plot([xt, xt], [2.06, 2.50], color='k', lw=0.7)
    arrow(ax, (2.72, 2.36), (3.48, 2.36), lw=0.7, ms=9, style='<|-|>')
    ax.text(3.1, 2.72, r'$t_{\rm tun}$', fontsize=11.5, ha='center', va='center')
    save(fig, '2.7')


# ---------------------------------------------------------------- 2.8 亚稳态势
def fig_2_8():
    fig, ax = plt.subplots(figsize=(4.7, 3.1))
    ax.set_xlim(0, 6.8); ax.set_ylim(0.4, 5.3); ax.axis('off')
    yA = 1.95
    ax.plot([0.55, 6.25], [yA, yA], color='k', lw=LW_AX)
    ax.plot([3.05, 3.05], [0.75, 4.95], color='k', lw=LW_AX)
    ax.text(3.21, 4.85, r'$V$', fontsize=12, ha='left', va='center')

    def sig(u):
        return 1.0 / (1.0 + np.exp(-np.clip(u, -50, 50)))

    x = np.linspace(0.55, 5.55, 800)
    base = -0.13 + 0.14 * sig(4.5 * (x - 2.25))          # 左支缓升，越过 x1
    dome = 3.30 * np.exp(-((x - 3.05) ** 2) / (2 * 0.34 ** 2))   # 圆滑势垒
    dip = 0.013 * np.exp(-((x - 4.32) ** 2) / (2 * 0.30 ** 2))   # 势阱触零
    rise = 5.5 * sig(6.0 * (x - 4.55)) * np.maximum(x - 4.60, 0) ** 2
    ax.plot(x, yA + (base + dome - dip + rise) / 1.15, color='k', lw=LW)
    ax.text(2.10, yA - 0.32, r'$x_1$', fontsize=11.5, ha='center', va='center')
    ax.text(4.32, yA - 0.32, r'$x_0$', fontsize=11.5, ha='center', va='center')
    save(fig, '2.8')


# ------------------------------------------- 2.9 单反弹（a 势 / b x(t)）
def fig_2_9():
    fig, ax = plt.subplots(figsize=(7.0, 2.9))
    ax.set_xlim(0, 10.0); ax.set_ylim(-3.3, 1.15); ax.axis('off')

    # (a) 翻转势（亚稳极大在 x0，势垒倒置为极小在 x1 附近）
    ax.plot([0.35, 4.45], [0, 0], color='k', lw=LW_AX)
    ax.plot([1.98, 1.98], [-2.75, 0.62], color='k', lw=LW_AX)
    ax.text(2.12, 0.52, r'$V$', fontsize=12, ha='left', va='center')
    pts = [(0.38, 0.17), (0.95, 0.15), (1.42, -0.02), (1.72, -0.48),
           (1.98, -0.86), (2.28, -0.74), (2.62, -0.30), (2.98, 0.0),
           (3.28, -0.72), (3.48, -1.62), (3.55, -2.55)]
    cur = catmull_rom(pts, n=30)
    ax.plot(cur[:, 0], cur[:, 1], color='k', lw=LW)
    ax.text(1.56, 0.19, r'$x_1$', fontsize=11.5, ha='center', va='center')
    ax.text(2.98, 0.19, r'$x_0$', fontsize=11.5, ha='center', va='center')
    # 反弹运动环形箭头（双线发夹回路）
    ax.plot([2.85, 1.66], [-0.26, -0.26], color='k', lw=1.3,
            solid_capstyle='round')
    u = np.linspace(np.pi / 2, 3 * np.pi / 2, 40)
    ax.plot(1.66 + 0.09 * np.cos(u), -0.36 + 0.10 * np.sin(u),
            color='k', lw=1.3)
    ax.plot([1.66, 2.66], [-0.46, -0.46], color='k', lw=1.3,
            solid_capstyle='round')
    arrow(ax, (2.62, -0.46), (2.84, -0.46), lw=1.3, ms=13)
    ax.text(0.55, 0.62, '(a)', fontsize=11, ha='center', va='center')

    # (b) x(t)：x0 出发的脉冲（到 x1 并返回）
    xL, xR = 5.6, 9.5
    ax.plot([xL, xR], [0.92, 0.92], color='k', lw=0.8, ls=(0, (1.2, 2.2)))
    ax.plot([6.9, xR], [0.0, 0.0], color='k', lw=0.8, ls=(0, (1.2, 2.2)))
    ax.text(xL - 0.12, 0.92, r'$x_1$', fontsize=11.5, ha='right', va='center')
    ax.text(xL - 0.12, 0.0, r'$x_0$', fontsize=11.5, ha='right', va='center')
    ax.plot([xL, 6.28], [0, 0], color='k', lw=LW)
    ts = np.linspace(6.28, 8.62, 300)
    xs = 0.46 * (np.tanh(5.2 * (ts - 6.82)) - np.tanh(5.2 * (ts - 8.08)))
    ax.plot(ts, xs, color='k', lw=LW)
    ax.plot([8.62, xR], [0, 0], color='k', lw=LW)
    ax.plot([6.05, 9.42], [0.46, 0.46], color='k', lw=0.7)
    arrow(ax, (9.30, 0.46), (9.48, 0.46), lw=0.7, ms=9)
    ax.text(9.44, 0.22, r'$t$', fontsize=11.5, ha='center', va='center')
    ax.text(5.75, 1.22, '(b)', fontsize=11, ha='center', va='center')
    save(fig, '2.9')


# ---------------------------------------------------------------- 2.10 RCL 电路
def fig_2_10():
    fig, ax = plt.subplots(figsize=(4.2, 4.1))
    ax.set_xlim(0, 8.0); ax.set_ylim(0, 7.8); ax.set_aspect('equal'); ax.axis('off')
    xL, xR = 0.9, 6.7
    yT, yM, yB = 6.5, 4.1, 1.0

    # 三条并联支路 + 左右母线
    ax.plot([xL, xL], [yB, yT], 'k-', lw=1.2)
    ax.plot([xR, xR], [yB, yT], 'k-', lw=1.2)
    # 顶：电感
    ax.plot([xL, 2.1], [yT, yT], 'k-', lw=1.2)
    _loop_coil(ax, 2.1, 5.55, yT, n_loop=4, r=0.40, lift=0.28, lw=1.15)
    ax.plot([5.55, xR], [yT, yT], 'k-', lw=1.2)
    ax.text(5.80, 5.95, r'$L$', fontsize=12, ha='left', va='center')
    # 中：电阻
    ax.plot([xL, 2.3], [yM, yM], 'k-', lw=1.2)
    ax.add_patch(Rectangle((2.3, yM - 0.26), 2.7, 0.52, fc='white', ec='k', lw=1.2))
    ax.plot([5.0, xR], [yM, yM], 'k-', lw=1.2)
    ax.text(5.25, 3.55, r'$R$', fontsize=12, ha='left', va='center')
    # 底：电容（竖直极板）
    ax.plot([xL, 2.85], [yB, yB], 'k-', lw=1.2)
    ax.add_patch(Rectangle((2.85, yB - 0.44), 0.12, 0.88, fc='k', ec='k'))
    ax.add_patch(Rectangle((3.20, yB - 0.44), 0.12, 0.88, fc='k', ec='k'))
    ax.plot([3.32, xR], [yB, yB], 'k-', lw=1.2)
    ax.text(3.55, 0.42, r'$C$', fontsize=12, ha='left', va='center')
    # 电流 I
    ax.text(2.25, 7.25, r'$I$', fontsize=12, ha='center', va='center')
    arrow(ax, (2.6, 7.2), (4.75, 7.2), lw=0.7, ms=9)
    save(fig, '2.10')


if __name__ == '__main__':
    for f in (fig_1_1, fig_1_2, fig_2_1, fig_2_2, fig_2_3, fig_2_4,
              fig_2_5, fig_2_6, fig_2_7, fig_2_8, fig_2_9, fig_2_10):
        f()
