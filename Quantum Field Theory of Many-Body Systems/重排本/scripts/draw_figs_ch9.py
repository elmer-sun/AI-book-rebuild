# -*- coding: utf-8 -*-
"""
B7 批次：文小刚《多体量子场论》第9章 9.1–9.16 共 16 幅插图重绘（黑白矢量）。
输出: figures/fig_9.x.pdf + figures/preview/fig_9.x.png

说明
----
* 9.1–9.7, 9.15, 9.16 为示意图，按原书页面逐要素重绘。
* 9.8–9.14 为自旋子色散/双自旋子谱等值线图：按书中拟设公式
  (9.6.1)–(9.6.10), (9.2.33)/(9.2.34)/(9.2.39)/(9.2.41), (9.8.9)
  数值计算能带（Wen 的 tau^l 约定：tau1,tau3 实对称、tau2 实反对称），
  E2s(k) = min_q [E(q)+E(k-q)]（min-plus 卷积）。
  书未给出作图参数值，这里取能复现原书图案（节点位置/周期性/等值线密度）
  的代表性参数；节点与周期性与原书一致，个别等值线形状为近似。
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse, Rectangle, FancyArrowPatch, Polygon

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

GRAY = '0.80'
DGRAY = '0.45'


def save(fig, key):
    fig.savefig(os.path.join(FIGDIR, f'fig_{key}.pdf'),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREVDIR, f'fig_{key}.png'),
                dpi=150, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)
    print('saved', key)


def arrow_head(ax, x, y, dx, dy, size, lw=1.1):
    """实心箭头头部（画在线段中点等处）。"""
    n = np.hypot(dx, dy)
    dx, dy = dx / n, dy / n
    px, py = -dy, dx
    w, h = size * 0.42, size
    tri = np.array([[x + dx * h, y + dy * h],
                    [x - dx * h * 0.5 + px * w, y - dy * h * 0.5 + py * w],
                    [x - dx * h * 0.5 - px * w, y - dy * h * 0.5 - py * w]])
    ax.add_patch(Polygon(tri, closed=True, fc='k', ec='k', lw=lw * 0.3))


def link_arrow(ax, x0, y0, x1, y1, lw=1.0, head=0.11, at=0.5):
    """在键线中点处加箭头（原书格点键样式：细线+中部小箭头）。"""
    ax.plot([x0, x1], [y0, y1], '-', color='k', lw=lw,
            solid_capstyle='butt', zorder=3)
    xm, ym = x0 + (x1 - x0) * at, y0 + (y1 - y0) * at
    dx, dy = x1 - x0, y1 - y0
    n = np.hypot(dx, dy)
    d = head * 1.15
    ax.add_patch(FancyArrowPatch(
        (xm - dx / n * d, ym - dy / n * d), (xm + dx / n * d, ym + dy / n * d),
        arrowstyle='-|>', mutation_scale=9, lw=0, color='k', zorder=4))


def spin(ax, x, y, up=True, gray=False, r=0.155):
    """格点自旋：圆圈+竖箭头。"""
    ax.add_patch(Circle((x, y), r, fc=(GRAY if gray else 'white'),
                        ec='k', lw=0.9, zorder=5))
    s = 1.0 if up else -1.0
    a0, a1 = y - s * r * 0.62, y + s * r * 0.62
    ax.plot([x, x], [a0, a1 * 1.0], '-', color='k', lw=0.9, zorder=6)
    ax.add_patch(FancyArrowPatch((x, a1 - s * r * 0.42), (x, a1),
                                 arrowstyle='-|>', mutation_scale=7,
                                 lw=0, color='k', zorder=7))


# ======================================================================
#  数值引擎：SU(2) 拟设 → 自旋子色散（Wen 的 tau 约定）
# ======================================================================
_T0 = np.eye(2, dtype=complex)
_T1 = np.array([[0, 1], [1, 0]], dtype=complex)
_T2 = np.array([[0, -1], [1, 0]], dtype=complex)   # 实反对称 (tau^2)
_T3 = np.array([[1, 0], [0, -1]], dtype=complex)


def h_single(bonds, kx, ky):
    """单格胞：H(k)=sum u e^{ik.d} + u^dag e^{-ik.d}；bonds=[(dx,dy,u)]。"""
    h = np.zeros((2, 2), dtype=complex)
    for d, u in bonds:
        dx, dy = d
        ph = np.exp(1j * (kx * dx + ky * dy))
        h += u * ph + u.conj().T / ph
    return h


def h_double(bonds, kx, ky):
    """x 方向加倍胞（子格 A(x 偶)/B(x 奇)）。
    bonds=[((dx,dy),uA,uB)]：uA/uB 为起点在 A/B 上的 hopping 矩阵。
    相位取全位移 e^{ik.d}（全布里渊区取样，谱自动具有加倍胞周期性）。"""
    h = np.zeros((4, 4), dtype=complex)
    for d, uA, uB in bonds:
        dx, dy = d
        ph = np.exp(1j * (kx * dx + ky * dy))
        for sa in (0, 1):
            u = uA if sa == 0 else uB
            sb = (sa + dx) % 2
            h[2 * sb:2 * sb + 2, 2 * sa:2 * sa + 2] += u * ph
            h[2 * sa:2 * sa + 2, 2 * sb:2 * sb + 2] += u.conj().T / ph
    return h


def band_single(bonds, kxs, kys, onsite=None):
    """2x2 拟设的正能带 E+(k)（kxs,kys 为弧度网格）。"""
    nx, ny = len(kxs), len(kys)
    e = np.empty((ny, nx))
    for iy, ky in enumerate(kys):
        for ix, kx in enumerate(kxs):
            h = h_single(bonds, kx, ky)
            if onsite is not None:
                h = h + onsite
            ev = np.linalg.eigvalsh(h)
            e[iy, ix] = ev[-1]
    return e


def band_double(bonds, kxs, kys):
    """加倍胞拟设的最低正能带 min(E1,E2)。"""
    nx, ny = len(kxs), len(kys)
    e = np.empty((ny, nx))
    for iy, ky in enumerate(kys):
        for ix, kx in enumerate(kxs):
            ev = np.linalg.eigvalsh(h_double(bonds, kx, ky))
            ev = ev[ev > 1e-9]
            e[iy, ix] = ev[0] if len(ev) else 0.0
    return e


def two_spinon(egrid):
    """E2s(k)=min_q [E(q)+E(k-q)]，网格循环 min-plus 卷积。"""
    n = egrid.shape[0]
    out = np.full_like(egrid, np.inf)
    for dy in range(n):
        for dx in range(n):
            cand = egrid + np.roll(np.roll(egrid, dy, axis=0), dx, axis=1)
            np.minimum(out, cand, out=out)
    return out


def refine(Z, n=260):
    """样条细化等值线网格。"""
    from scipy.interpolate import RectBivariateSpline
    m = Z.shape[0]
    x = np.linspace(0, 1, m)
    sp = RectBivariateSpline(x, x, Z, kx=3, ky=3, s=0)
    xn = np.linspace(0, 1, n)
    return sp(xn, xn)


def _cpanel(fig, rect, Z, extent, levels, *, xt, yt, grid=(), diamond=False,
            blackfill=None):
    """单个等值线面板（方框、内侧刻度、y 轴标在右侧）。"""
    ax = fig.add_axes(rect)
    nx, ny = Z.shape[1], Z.shape[0]
    X = np.linspace(extent[0], extent[1], nx)
    Y = np.linspace(extent[2], extent[3], ny)
    if blackfill is not None:
        ax.contourf(X, Y, Z, levels=[blackfill, max(Z.max(), blackfill * 2)],
                    colors='k')
    ax.contour(X, Y, Z, levels=levels, colors='k', linewidths=0.55)
    for gx in grid:
        ax.axvline(gx, color='k', lw=0.45)
    for gy in grid:
        ax.axhline(gy, color='k', lw=0.45)
    if diamond:
        e = extent[1]
        for sgn in (1, -1):
            ax.plot([0, sgn * e], [e, 0], '-', color='k', lw=0.6)
            ax.plot([0, sgn * e], [-e, 0], '-', color='k', lw=0.6)
    ax.set_xlim(extent[:2]); ax.set_ylim(extent[2:])
    ax.set_aspect('equal')
    ax.set_xticks(xt); ax.set_yticks(yt)
    ax.tick_params(direction='in', length=3.2, width=0.7,
                   labelsize=8.5, top=True, right=True,
                   labelright=True, labelleft=False, pad=2)
    for s in ax.spines.values():
        s.set_linewidth(0.8)
    return ax


def _legend_box(fig, rect, labels, lw=0.85):
    ax = fig.add_axes(rect)
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_linewidth(0.7)
    n = len(labels)
    for i, t in enumerate(labels):
        y = 1 - (i + 0.5) / n
        ax.plot([0.10, 0.48], [y, y], '-', color='k', lw=lw)
        ax.text(0.60, y, t, ha='left', va='center', fontsize=8.5)
    return ax


def _clabel(fig, rect, tag):
    fig.text(rect[0] - 0.035, rect[1] + rect[3] + 0.008, tag,
             fontsize=11, ha='left', va='bottom')


#  ————— 各拟设 bond 列表 —————
def bonds_92141(chi, eta, gam, a3=0.0, a1=0.0, flip_diag=False):
    """(9.6.1)/(9.2.41) 型（厄米键形式，含 onsite a3*T3+a1*T1）。"""
    dg = -gam if flip_diag else gam
    bonds = [((1, 0), chi * _T3 + eta * _T1),
             ((0, 1), chi * _T3 - eta * _T1),
             ((1, 1), dg * _T3),
             ((-1, 1), gam * _T3)]
    return bonds, a3 * _T3 + a1 * _T1


def bonds_96_1(chi, eta, gam):
    """(9.6.1) Z2A0013 原始形式。"""
    return [((1, 0), chi * _T1 - eta * _T2),
            ((0, 1), chi * _T1 + eta * _T2),
            ((1, 1), gam * _T1),
            ((-1, 1), gam * _T1)], None


def bonds_96_3(chi, eta, c1, e1, l1):
    """(9.6.3) Z2A001n。"""
    u0 = chi * _T1 + eta * _T2
    d1 = c1 * _T1 + e1 * _T2 + l1 * _T3
    d2 = c1 * _T1 - e1 * _T2 - l1 * _T3
    return [((1, 0), u0), ((0, 1), chi * _T1 - eta * _T2),
            ((2, 1), d1), ((-1, 2), d2), ((2, -1), d1), ((1, 2), d2)], None


def bonds_96_4(chi, eta, c1, e1, lam):
    """(9.6.4) Z2Azz1n。"""
    d1 = c1 * _T1 + e1 * _T2 + lam * _T3
    d2 = c1 * _T1 - e1 * _T2 + lam * _T3
    d3 = c1 * _T1 + e1 * _T2 - lam * _T3
    d4 = c1 * _T1 - e1 * _T2 - lam * _T3
    return [((1, 0), chi * _T1 + eta * _T2),
            ((0, 1), chi * _T1 - eta * _T2),
            ((2, 1), d1), ((-1, 2), d2), ((2, -1), d3), ((1, 2), d4)], None


def bonds_96_5(chi, eta, g2, l2, a1=0.0):
    """(9.6.5) Z2B0013（加倍胞）。"""
    ux = chi * _T1 - eta * _T2
    uy = chi * _T1 + eta * _T2
    u2x = -g2 * _T1 + l2 * _T2
    u2y = -g2 * _T1 - l2 * _T2
    b = [((1, 0), ux, ux), ((0, 1), uy, -uy),
         ((2, 0), u2x, u2x), ((0, 2), u2y, u2y)]
    return b, a1 * _T1


def bonds_96_6(chi, eta, g1):
    """(9.6.6) Z2Bzz13。"""
    ux = chi * _T1 - eta * _T2
    uy = chi * _T1 + eta * _T2
    b = [((1, 0), ux, ux), ((0, 1), uy, -uy),
         ((2, 2), -g1 * _T1, -g1 * _T1), ((-2, 2), g1 * _T1, g1 * _T1)]
    return b, None


def bonds_96_7(chi, eta, lam):
    """(9.6.7) Z2B001n。"""
    ux = chi * _T1 + eta * _T2
    uy = chi * _T1 - eta * _T2
    d = lam * _T3
    b = [((1, 0), ux, ux), ((0, 1), uy, -uy),
         ((2, 1), d, d), ((-1, 2), -d, -d),
         ((2, -1), d, d), ((1, 2), -d, -d)]
    return b, None


def bonds_96_8(chi, eta, c1, e1, lam):
    """(9.6.8) Z2Bzz1n。"""
    ux = chi * _T1 + eta * _T2
    uy = chi * _T1 - eta * _T2
    b = [((1, 0), ux, ux), ((0, 1), uy, -uy),
         ((2, 1), c1 * _T1 + e1 * _T2 + lam * _T3,
                 c1 * _T1 + e1 * _T2 + lam * _T3),
         ((-1, 2), c1 * _T1 - e1 * _T2 + lam * _T3,
                  c1 * _T1 - e1 * _T2 + lam * _T3),
         ((2, -1), c1 * _T1 + e1 * _T2 - lam * _T3,
                  c1 * _T1 + e1 * _T2 - lam * _T3),
         ((1, 2), c1 * _T1 - e1 * _T2 - lam * _T3,
                 c1 * _T1 - e1 * _T2 - lam * _T3)]
    return b, None


def bonds_9234(chi, eta):
    """(9.2.34) U1Cn01n 交错通量（加倍胞）。"""
    z = 1j
    uxA = z * chi * _T0 - z * eta * _T3
    uxB = z * chi * _T0 + z * eta * _T3
    uyA = z * chi * _T0 + z * eta * _T3
    uyB = z * chi * _T0 - z * eta * _T3
    return [((1, 0), uxA, uxB), ((0, 1), uyA, uyB)], None


def bonds_989(eta, chi):
    """(9.8.9) U1Cn00x（lam=0 无能隙相）。"""
    return [((1, 0), eta * _T1), ((0, 1), eta * _T1),
            ((1, 1), chi * _T3), ((-1, 1), chi * _T3)], None


# ======================================================================
#  FIG 9.1  二聚体态 / 三重态 / 位移二聚体弦
# ======================================================================
def fig_9_1():
    fig = plt.figure(figsize=(7.0, 2.6))
    ax = fig.add_axes([0.03, 0.05, 0.94, 0.90])
    ax.set_xlim(-0.9, 12.9); ax.set_ylim(-0.75, 3.75)
    ax.axis('off'); ax.set_aspect('equal')

    # 位移二聚体行(第2行, y=2)与三重态(第3行, y=1)标记（0 基列号）
    displaced = {(5, 6), (7, 8), (9, 10)}         # 行 y=2
    singles = {(4, 1), (11, 1)}                   # (列, 行)
    triplet = (2, 3)                              # 行 y=1 的 dimer(2,3)

    for row in range(4):
        y = 3 - row
        # 点线（横向连接线穿过每行，纵向穿过每列）
        ax.plot([0.2, 11.8], [y, y], ':', color=DGRAY, lw=0.7, zorder=1)
    for col in range(12):
        ax.plot([col, col], [-0.25, 3.25], ':', color=DGRAY, lw=0.7, zorder=1)

    def dimmer(y, c0, c1, style='-', shaded=False, updown=(False, True),
               grayspin=False):
        if shaded:      # 位移二聚体：灰底、稍大
            ax.add_patch(Ellipse(((c0 + c1) / 2, y), 1.62, 0.94,
                                 fc=GRAY, ec='k', lw=1.0, zorder=3))
        else:
            ax.add_patch(Ellipse(((c0 + c1) / 2, y), 1.52, 0.86,
                                 fill=False, ec='k', lw=1.0, ls=style,
                                 zorder=4))
        g = shaded or grayspin
        spin(ax, c0, y, up=updown[0], gray=g)
        spin(ax, c1, y, up=updown[1], gray=g)

    normal = [(2 * j, 2 * j + 1) for j in range(6)]
    for row in range(4):
        y = 3 - row
        if row == 1:                       # 位移二聚体串所在行
            dimmer(y, 0, 1)
            dimmer(y, 2, 3)
            spin(ax, 4, y, up=True, gray=True)          # 弦端点自旋 1/2
            for c0, c1 in [(5, 6), (7, 8), (9, 10)]:    # 位移二聚体
                dimmer(y, c0, c1, shaded=True, updown=(True, False))
            spin(ax, 11, y, up=True, gray=True)         # 弦端点自旋 1/2
        elif row == 2:                     # 三重态所在行
            for c0, c1 in normal:
                if (c0, c1) == triplet:     # 三重态：虚线椭圆、两个灰 ↑
                    dimmer(y, c0, c1, style=(0, (3, 1.8)),
                           updown=(True, True), grayspin=True)
                else:
                    dimmer(y, c0, c1)
        else:
            for c0, c1 in normal:
                dimmer(y, c0, c1)

    save(fig, '9.1')


# ======================================================================
#  FIG 9.2  pi 通量态拟设 (a) + 费米子色散面 (b)
# ======================================================================
def fig_9_2():
    fig = plt.figure(figsize=(7.0, 2.7))

    # ---- (a) 格子 ----
    ax = fig.add_axes([0.03, 0.06, 0.36, 0.88])
    ax.set_xlim(-1.15, 4.15); ax.set_ylim(-0.65, 4.15)
    ax.axis('off'); ax.set_aspect('equal')
    n = 3
    for j in range(4):                       # 竖线，箭头方向交替
        up = (j % 2 == 0)
        ax.plot([j, j], [-0.45, 3.45], '-', color='k', lw=1.0, zorder=2)
        for i in range(n):
            if up:
                link_arrow(ax, j, i, j, i + 1)
            else:
                link_arrow(ax, j, i + 1, j, i)
    for i in range(4):                       # 横线，箭头向右
        ax.plot([-0.45, 3.45], [i, i], '-', color='k', lw=1.0, zorder=2)
        for j in range(n):
            link_arrow(ax, j, i, j + 1, i)
    fig.text(0.045, 0.90, '(a)', fontsize=11)

    # ---- (b) 3D 色散面 ----
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    ax = fig.add_axes([0.42, 0.02, 0.56, 0.96], projection='3d')
    kk = np.linspace(-np.pi, np.pi, 61)
    KX, KY = np.meshgrid(kk, kk)
    E = 2 * np.sqrt(2.0) * np.sqrt(np.cos(KX) ** 2 + np.cos(KY) ** 2)
    ax.plot_wireframe(KX, KY, E, rstride=2, cstride=2, lw=0.22,
                      color='k')
    ax.plot_wireframe(KX, KY, -E, rstride=2, cstride=2, lw=0.22,
                      color='k')
    ax.set_axis_off()
    ax.view_init(elev=26, azim=-56)
    ax.set_box_aspect((1, 1, 0.62))
    ax.set_xlim(-np.pi * 1.02, np.pi * 1.02)
    ax.set_ylim(-np.pi * 1.02, np.pi * 1.02)
    fig.text(0.44, 0.90, '(b)', fontsize=11)

    save(fig, '9.2')


# ======================================================================
#  FIG 9.3  手征自旋态拟设
# ======================================================================
def fig_9_3():
    fig = plt.figure(figsize=(3.6, 2.9))
    ax = fig.add_axes([0.05, 0.05, 0.90, 0.90])
    ax.set_xlim(-1.5, 4.0); ax.set_ylim(-1.35, 3.0)
    ax.axis('off'); ax.set_aspect('equal')
    nx, ny = 4, 3

    # 细对角线（每个方格两条，向四周延伸约 0.8 格距）
    for i in range(nx - 1):
        for j in range(ny - 1):
            ax.plot([i - 0.5 - 0.8, i + 1.5 + 0.8],
                    [j - 0.5 - 0.8, j + 1.5 + 0.8],
                    '-', color='k', lw=0.55, zorder=1)
            ax.plot([i + 1.5 + 0.8, i - 0.5 - 0.8],
                    [j - 0.5 - 0.8, j + 1.5 + 0.8],
                    '-', color='k', lw=0.55, zorder=1)
    # 粗方格线（向外延伸）
    for i in range(nx):
        ax.plot([i, i], [-0.55, ny - 1 + 0.55], '-', color='k',
                lw=1.6, zorder=3)
    for j in range(ny):
        ax.plot([-0.55, nx - 1 + 0.55], [j, j], '-', color='k',
                lw=1.6, zorder=3)
    # 键上箭头
    for i in range(nx - 1):
        for j in range(ny):
            link_arrow(ax, i, j, i + 1, j, lw=1.6)          # 横向 -> 右
    for j in range(ny - 1):
        for i in range(nx):
            link_arrow(ax, i, j + 1, i, j, lw=1.6)          # 纵向 -> 下
    # 对角线箭头：每格中心附近两个 NE 向箭头（分居中心西北/东南）
    for i in range(nx - 1):
        for j in range(ny - 1):
            cx, cy = i + 0.5, j + 0.5
            d = 0.16
            arrow_head(ax, cx - d, cy + d, 1, 1, 0.24)      # "\" 线西北段
            arrow_head(ax, cx + d, cy - d, 1, 1, 0.24)      # "\" 线东南段

    save(fig, '9.3')


# ======================================================================
#  FIG 9.4  Z2 涡旋
# ======================================================================
def fig_9_4():
    fig = plt.figure(figsize=(3.7, 3.1))
    ax = fig.add_axes([0.05, 0.05, 0.90, 0.90])
    ax.set_xlim(-0.9, 5.3); ax.set_ylim(-1.0, 4.4)
    ax.axis('off'); ax.set_aspect('equal')
    nx, ny = 5, 4
    for i in range(nx):
        ax.plot([i, i], [-0.55, ny - 1 + 0.35], '-', color='k', lw=0.7)
    for j in range(ny):
        ax.plot([-0.35, nx - 1 + 0.35], [j, j], '-', color='k', lw=0.7)
    # 符号翻转的粗键（三条竖键）
    for i in (2, 3, 4):
        ax.plot([i, i], [1, 2], '-', color='k', lw=2.6, solid_capstyle='butt')
    # 虚线（弦）
    ax.plot([0.75, 4.95], [1.5, 1.5], '--', color='k', lw=0.95, dashes=(4, 2.2))
    # 涡旋 X 记号
    s = 0.17
    ax.plot([1.18 - s, 1.18 + s], [1.5 - s, 1.5 + s], '-', color='k', lw=2.4)
    ax.plot([1.18 - s, 1.18 + s], [1.5 + s, 1.5 - s], '-', color='k', lw=2.4)
    ax.text(1.30, 0.98, r'$Z_2$ vortex', fontsize=10, ha='left')
    # 坐标轴箭头
    ax.plot([1, 1], [2.55, 3.72], '-', color='k', lw=1.3)
    arrow_head(ax, 1, 3.85, 0, 1, 0.30)
    ax.plot([3.5, 4.7], [0, 0], '-', color='k', lw=1.3)
    arrow_head(ax, 4.85, 0, 1, 0, 0.30)

    save(fig, '9.4')


# ======================================================================
#  FIG 9.5  穿过 x 线 / y 线的键变号
# ======================================================================
def fig_9_5():
    fig = plt.figure(figsize=(3.9, 3.5))
    ax = fig.add_axes([0.05, 0.05, 0.90, 0.90])
    ax.set_xlim(-1.35, 5.85); ax.set_ylim(-1.05, 5.4)
    ax.axis('off'); ax.set_aspect('equal')
    n = 5
    for i in range(n):
        ax.plot([i, i], [-0.5, n - 1 + 0.35], '-', color='k', lw=0.7, zorder=1)
    for j in range(n):
        ax.plot([-0.5, n - 1 + 0.35], [j, j], '-', color='k', lw=0.7, zorder=1)
    # 粗键：横过 y 线(x=1.5)的横键；纵过 x 线(y=0.5)的竖键
    for j in range(4):
        ax.plot([1, 2], [j, j], '-', color='k', lw=2.6,
                solid_capstyle='butt', zorder=3)
    for i in range(4):
        ax.plot([i, i], [0, 1], '-', color='k', lw=2.6,
                solid_capstyle='butt', zorder=3)
    # 虚线 x/y line
    ax.plot([1.5, 1.5], [-0.85, 4.75], '--', color='k', lw=0.95,
            dashes=(4, 2.2), zorder=2)
    ax.plot([-0.95, 4.95], [0.5, 0.5], '--', color='k', lw=0.95,
            dashes=(4, 2.2), zorder=2)
    # 轴箭头
    ax.plot([1, 1], [3.3, 4.35], '-', color='k', lw=1.3, zorder=4)
    arrow_head(ax, 1, 4.5, 0, 1, 0.30)
    ax.plot([3.5, 4.65], [0, 0], '-', color='k', lw=1.3, zorder=4)
    arrow_head(ax, 4.8, 0, 1, 0, 0.30)
    # 标签
    ax.text(1.52, 4.92, r'$y$ line', fontsize=10, ha='left')
    ax.text(0.82, 4.35, r'$y$ axis', fontsize=10, ha='right')
    ax.text(5.05, 0.62, r'$x$ line', fontsize=10, ha='left')
    ax.text(4.62, -0.52, r'$x$ axis', fontsize=10, ha='left')

    save(fig, '9.5')


# ======================================================================
#  FIG 9.6  (a) g=1 与 (b) g=2 黎曼面（2g 个孔）
# ======================================================================
def _torus_eye(ax, cx, cy, a, b, lw=1.0):
    """孔的前缘（实线眼形）+ 后缘（虚线椭圆）。"""
    ax.add_patch(Ellipse((cx, cy), 2 * a, 2 * b, fill=False, ec='k',
                         lw=lw, ls=(0, (4, 2.4)), zorder=3))
    t = np.linspace(0, np.pi, 60)
    # 上缘：两段浅弧在中部略降
    xu = np.array([-a, -0.45 * a, 0.02 * a, 0.5 * a, a])
    yu = np.array([0.0, 0.30 * b, 0.10 * b, 0.30 * b, 0.0])
    # 下缘：浅弧
    xl = np.array([-a, 0.0, a])
    yl = np.array([0.0, -0.42 * b, 0.0])
    ax.plot(cx + xu, cy + yu, '-', color='k', lw=lw, zorder=4)
    ax.plot(cx + xl, cy + yl, '-', color='k', lw=lw, zorder=4)


def fig_9_6():
    fig = plt.figure(figsize=(7.0, 2.5))
    # ---- (a) 环面 ----
    ax = fig.add_axes([0.03, 0.06, 0.42, 0.88])
    ax.set_xlim(-2.2, 2.2); ax.set_ylim(-1.55, 1.85)
    ax.axis('off'); ax.set_aspect('equal')
    ax.add_patch(Ellipse((0, 0), 3.3, 2.1, fill=False, ec='k', lw=1.1))
    _torus_eye(ax, 0, 0, 1.0, 0.62)
    ax.plot([0, 0], [-1.45, 1.45], '--', color='k', lw=0.95, dashes=(4, 2.4))
    fig.text(0.05, 0.88, '(a)', fontsize=11)

    # ---- (b) g=2 ----
    ax = fig.add_axes([0.47, 0.06, 0.52, 0.88])
    ax.set_xlim(-3.35, 3.35); ax.set_ylim(-1.55, 1.85)
    ax.axis('off'); ax.set_aspect('equal')
    t = np.linspace(0, 2 * np.pi, 500)
    # 双孔外轮廓（花生形）：双峰包络
    u = np.cos(t)
    xo = 2.62 * u
    yo = 1.02 * np.sin(t) * (1 - 0.44 * np.exp(-xo ** 2 / 0.75))
    ax.plot(xo, yo, '-', color='k', lw=1.1, zorder=2)
    _torus_eye(ax, -1.28, 0, 0.95, 0.60)
    _torus_eye(ax, 1.28, 0, 0.95, 0.60)
    ax.plot([-1.28, -1.28], [-1.32, 1.32], '--', color='k', lw=0.95,
            dashes=(4, 2.4), zorder=1)
    ax.plot([1.28, 1.28], [-1.32, 1.32], '--', color='k', lw=0.95,
            dashes=(4, 2.4), zorder=1)
    fig.text(0.49, 0.88, '(b)', fontsize=11)

    save(fig, '9.6')


# ======================================================================
#  FIG 9.7  平均场相图 (a) 与物理相图 (b)
# ======================================================================
def _psg_axes(ax):
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.plot([0.04, 0.04], [0.04, 0.98], '-', color='k', lw=1.0)
    ax.plot([0.04, 0.98], [0.04, 0.04], '-', color='k', lw=1.0)
    ax.text(0.005, 0.99, r'$g_2$', fontsize=11, ha='left', va='top')
    ax.text(0.985, 0.0, r'$g_1$', fontsize=11, ha='right', va='top')


def fig_9_7():
    fig = plt.figure(figsize=(7.0, 2.9))
    # ---- (a) ----
    ax = fig.add_axes([0.05, 0.08, 0.40, 0.86])
    _psg_axes(ax)
    y = np.linspace(0.98, 0.03, 80)
    x1 = 0.28 + 0.15 * ((0.98 - y) / 0.95) ** 1.7
    ax.plot(x1, y, '-', color='k', lw=1.2)
    x2 = 0.63 + 0.075 * np.sin(np.pi * (0.98 - y) / 0.95) \
        - 0.155 * ((0.98 - y) / 0.95) ** 2.2
    ax.plot(x2, y, '-', color='k', lw=1.2)
    ax.text(0.44, 0.74, r'PSG$_3$', fontsize=11, ha='center')
    ax.text(0.15, 0.42, r'PSG$_1$', fontsize=11, ha='center')
    ax.text(0.75, 0.42, r'PSG$_2$', fontsize=11, ha='center')
    fig.text(0.05, 0.93, '(a)', fontsize=11)

    # ---- (b) ----
    ax = fig.add_axes([0.55, 0.08, 0.40, 0.86])
    _psg_axes(ax)
    x3 = 0.26 + 0.04 * np.sin(np.pi * (0.98 - y) / 0.95) \
        + 0.13 * ((0.98 - y) / 0.95) ** 2.4
    ax.plot(x3, y, '-', color='k', lw=1.2)
    ax.text(0.60, 0.74, r'PSG$_{\rm cr}$ = PSG$_3$', fontsize=10.5,
            ha='left')
    ax.annotate('', xy=(0.315, 0.42), xytext=(0.58, 0.665),
                arrowprops=dict(arrowstyle='-|>', lw=1.0,
                                connectionstyle='arc3,rad=-0.3'))
    ax.text(0.13, 0.42, r'PSG$_1$', fontsize=11, ha='center')
    ax.text(0.62, 0.42, r'PSG$_2$', fontsize=11, ha='center')
    fig.text(0.55, 0.93, '(b)', fontsize=11)

    save(fig, '9.7')


# ======================================================================
#  FIG 9.8  Z2A 四态自旋子色散等值线 (kx/2pi, ky/2pi in [-1,1])
# ======================================================================
_KW = np.linspace(-2 * np.pi, 2 * np.pi, 301)
_KXG, _KYG = np.meshgrid(_KW, _KW)
_LEV5 = [0.3, 1, 2, 3, 4]


def _norm(Z, ref=4.35, pct=97):
    return Z * (ref / np.percentile(Z, pct))


def _grid45():
    xt = [-1, -0.5, 0, 0.5, 1]
    return xt, xt


def fig_9_8():
    fig = plt.figure(figsize=(7.6, 7.2))
    xt, yt = _grid45()
    ext = (-1, 1, -1, 1)

    # (a) Z2A0013 —— (9.2.41) 型公式，有能隙（a3 较大）。
    #     参数使 eps=0 根位于 cos kx = -1 与 -0.12（对应原书
    #     (±0.5,±0.5) 深极小 + 对角小岛），η,a1 取大以抑制
    #     反对角假极小；按峰值归一化使中心仅剩 4 级等值线。
    bonds, ons = bonds_92141(1.123, 0.9, 1.0, a3=0.49, a1=0.27)
    E = band_single(bonds, _KW, _KW, onsite=ons)
    E = E * (4.08 / E.max())
    rects = [(0.09, 0.55, 0.335, 0.37), (0.545, 0.55, 0.335, 0.37),
             (0.09, 0.09, 0.335, 0.37), (0.545, 0.09, 0.335, 0.37)]
    _cpanel(fig, rects[0], E, ext, _LEV5, xt=xt, yt=yt,
            grid=(0, -0.5, 0.5))
    _clabel(fig, rects[0], '(a)')
    _legend_box(fig, (0.465, 0.66, 0.055, 0.16),
                ['4', '3', '2', '1', '0.3'])

    # (b) Z2Azz13 —— (9.6.2) 的规范等价色散（对角线翻转）
    bonds, ons = bonds_92141(1.0, 0.35, 0.5, flip_diag=True)
    E = band_single(bonds, _KW, _KW)
    _cpanel(fig, rects[1], _norm(E), ext, _LEV5, xt=xt, yt=yt,
            grid=(0, -0.5, 0.5))
    _clabel(fig, rects[1], '(b)')

    # (c) Z2A001n —— (9.6.3)
    bonds, ons = bonds_96_3(1.0, 0.4, 0.45, 0.20, 0.25)
    E = band_single(bonds, _KW, _KW)
    _cpanel(fig, rects[2], _norm(E), ext, _LEV5, xt=xt, yt=yt,
            grid=(0, -0.5, 0.5))
    _clabel(fig, rects[2], '(c)')

    # (d) Z2Azz1n —— (9.6.4)
    bonds, ons = bonds_96_4(1.0, 0.4, 0.45, 0.20, 0.30)
    E = band_single(bonds, _KW, _KW)
    _cpanel(fig, rects[3], _norm(E), ext, _LEV5, xt=xt, yt=yt,
            grid=(0, -0.5, 0.5))
    _clabel(fig, rects[3], '(d)')

    save(fig, '9.8')


# ======================================================================
#  FIG 9.9  Z2B 四态自旋子色散等值线
# ======================================================================
def fig_9_9():
    fig = plt.figure(figsize=(7.6, 7.2))
    xt, yt = _grid45()
    ext = (-1, 1, -1, 1)
    kw = np.linspace(-2 * np.pi, 2 * np.pi, 201)
    rects = [(0.09, 0.55, 0.335, 0.37), (0.545, 0.55, 0.335, 0.37),
             (0.09, 0.09, 0.335, 0.37), (0.545, 0.09, 0.335, 0.37)]

    cases = [
        ('(a)', bonds_96_5(1.0, 0.4, 0.35, 0.20)),
        ('(b)', bonds_96_6(1.0, 0.4, 0.30)),
        ('(c)', bonds_96_7(1.0, 0.4, 0.35)),
        ('(d)', bonds_96_8(1.0, 0.4, 0.50, 0.20, 0.30)),
    ]
    for (tag, (bonds, ons)), rc in zip(cases, rects):
        E = band_double(bonds, kw, kw)
        _cpanel(fig, rc, _norm(E), ext, _LEV5, xt=xt, yt=yt,
                grid=(0, -0.5, 0.5))
        _clabel(fig, rc, tag)
    _legend_box(fig, (0.465, 0.66, 0.055, 0.16),
                ['4', '3', '2', '1', '0.3'])

    save(fig, '9.9')


# ======================================================================
#  FIG 9.10  (a) Z2Ax2(12)n 无能隙态 (b) Z2Bx2(12)n 二次型态
# ======================================================================
def fig_9_10():
    fig = plt.figure(figsize=(8.2, 4.1))
    xt, yt = _grid45()
    ext = (-1, 1, -1, 1)

    # (a) 精确公式 (9.2.39)：E+ = 2 eta(sx+sy) + 2 chi sqrt(2cx^2+2cy^2)
    chi, eta = 1.0, 0.35
    E = 2 * eta * (np.sin(_KXG) + np.sin(_KYG)) \
        + 2 * chi * np.sqrt(2 * np.cos(_KXG) ** 2 + 2 * np.cos(_KYG) ** 2)
    E = E * (3.6 / np.percentile(E, 99.5))
    lev = [-1, -0.3, 0, 0.3, 1, 2, 3]
    rc1 = (0.07, 0.13, 0.345, 0.56)
    _cpanel(fig, rc1, E, ext, lev, xt=xt, yt=yt, grid=(0, -0.5, 0.5))
    _clabel(fig, rc1, '(a)')
    _legend_box(fig, (0.435, 0.55, 0.05, 0.22),
                ['3', '2', '1', '0.3', '0', r'$-0.3$', r'$-1$'])

    # (b) (9.6.10) Z2Bx2(12)n（加倍胞数值能带）
    chi, eta = 1.0, 0.4
    z = 1j
    ux = z * chi * _T0 + eta * _T1
    uy = z * chi * _T0 + eta * _T2
    bonds = [((1, 0), ux, ux), ((0, 1), uy, -uy)]
    kw = np.linspace(-2 * np.pi, 2 * np.pi, 201)
    E = band_double(bonds, kw, kw)
    E = _norm(E, ref=4.1)
    rc2 = (0.56, 0.13, 0.345, 0.56)
    _cpanel(fig, rc2, E, ext, _LEV5, xt=xt, yt=yt, grid=(0, -0.5, 0.5))
    _clabel(fig, rc2, '(b)')
    _legend_box(fig, (0.925, 0.55, 0.05, 0.16),
                ['4', '3', '2', '1', '0.3'])

    save(fig, '9.10')


# ======================================================================
#  FIG 9.11  Z2A 四态双自旋子谱 E2s（范围 [-0.5,0.5]，(c)(d) 带简约 BZ）
# ======================================================================
def _e2s_panels(fig, cases, diamonds, blackfill_idx=None):
    xt = yt = [-0.4, -0.2, 0, 0.2, 0.4]
    ext = (-0.5, 0.5, -0.5, 0.5)
    rects = [(0.09, 0.55, 0.335, 0.37), (0.545, 0.55, 0.335, 0.37),
             (0.09, 0.09, 0.335, 0.37), (0.545, 0.09, 0.335, 0.37)]
    kw = np.linspace(-np.pi, np.pi, 96)
    KX, KY = np.meshgrid(kw, kw)
    for i, (tag, E1) in enumerate(cases):
        E2 = two_spinon(E1)
        E2 = _norm(E2, ref=4.3)
        Z = refine(E2)
        bf = 4.0 if (blackfill_idx is not None and i == blackfill_idx) \
            else None
        _cpanel(fig, rects[i], Z, ext, _LEV5, xt=xt, yt=yt,
                grid=(0, -0.25, 0.25), diamond=diamonds[i], blackfill=bf)
        _clabel(fig, rects[i], tag)
    _legend_box(fig, (0.465, 0.66, 0.055, 0.16),
                ['4', '3', '2', '1', '0.3'])


def _E_single_positive(bonds, kw, onsite=None, double=False):
    if double:
        return band_double(bonds, kw, kw)
    return band_single(bonds, kw, kw, onsite=onsite)


def fig_9_11():
    fig = plt.figure(figsize=(7.6, 7.2))
    kw = np.linspace(-np.pi, np.pi, 96)
    b, ons = bonds_92141(1.123, 0.9, 1.0, a3=0.49, a1=0.27)
    Ea = _E_single_positive(b, kw, onsite=ons)
    b, _ = bonds_92141(1.0, 0.35, 0.5, flip_diag=True)
    Eb = _E_single_positive(b, kw)
    b, _ = bonds_96_3(1.0, 0.4, 0.45, 0.20, 0.25)
    Ec = _E_single_positive(b, kw)
    b, _ = bonds_96_4(1.0, 0.4, 0.45, 0.20, 0.30)
    Ed = _E_single_positive(b, kw)
    _e2s_panels(fig, [('(a)', Ea), ('(b)', Eb), ('(c)', Ec), ('(d)', Ed)],
                diamonds=[False, False, True, True])
    save(fig, '9.11')


# ======================================================================
#  FIG 9.12  Z2B 四态双自旋子谱 E2s
# ======================================================================
def fig_9_12():
    fig = plt.figure(figsize=(7.6, 7.2))
    kw = np.linspace(-np.pi, np.pi, 96)
    b, _ = bonds_96_5(1.0, 0.4, 0.35, 0.20)
    Ea = _E_single_positive(b, kw, double=True)
    b, _ = bonds_96_6(1.0, 0.4, 0.30)
    Eb = _E_single_positive(b, kw, double=True)
    b, _ = bonds_96_7(1.0, 0.4, 0.35)
    Ec = _E_single_positive(b, kw, double=True)
    b, _ = bonds_96_8(1.0, 0.4, 0.50, 0.20, 0.30)
    Ed = _E_single_positive(b, kw, double=True)
    _e2s_panels(fig, [('(a)', Ea), ('(b)', Eb), ('(c)', Ec), ('(d)', Ed)],
                diamonds=[False, False, False, False])
    save(fig, '9.12')


# ======================================================================
#  FIG 9.13  (a) Z2Ax2(12)n (b) Z2Bx2(12)n 双自旋子谱
# ======================================================================
def fig_9_13():
    fig = plt.figure(figsize=(7.6, 3.8))
    xt = yt = [-0.4, -0.2, 0, 0.2, 0.4]
    ext = (-0.5, 0.5, -0.5, 0.5)
    kw = np.linspace(-np.pi, np.pi, 96)
    KX, KY = np.meshgrid(kw, kw)

    # (a) (9.2.39) 精确单自旋子谱 E+（取正支）
    chi, eta = 1.0, 0.35
    E1 = 2 * eta * (np.sin(KX) + np.sin(KY)) \
        + 2 * chi * np.sqrt(2 * np.cos(KX) ** 2 + 2 * np.cos(KY) ** 2)
    E2 = two_spinon(E1)
    rc1 = (0.075, 0.12, 0.35, 0.56)
    _cpanel(fig, rc1, refine(_norm(E2, ref=4.3)), ext, _LEV5, xt=xt, yt=yt,
            grid=(0, -0.25, 0.25), blackfill=4.0)
    _clabel(fig, rc1, '(a)')
    _legend_box(fig, (0.45, 0.52, 0.05, 0.20), ['4', '3', '2', '1', '0.3'])

    # (b) (9.6.10)
    z = 1j
    chi, eta = 1.0, 0.4
    ux = z * chi * _T0 + eta * _T1
    uy = z * chi * _T0 + eta * _T2
    bonds = [((1, 0), ux, ux), ((0, 1), uy, -uy)]
    E1 = band_double(bonds, kw, kw)
    E2 = two_spinon(E1)
    rc2 = (0.565, 0.12, 0.35, 0.56)
    _cpanel(fig, rc2, refine(_norm(E2, ref=4.1)), ext, _LEV5, xt=xt, yt=yt,
            grid=(0, -0.25, 0.25))
    _clabel(fig, rc2, '(b)')
    _legend_box(fig, (0.935, 0.52, 0.05, 0.20), ['4', '3', '2', '1', '0.3'])

    save(fig, '9.13')


# ======================================================================
#  FIG 9.14  (a) U1Cn01n (b) U1Cn00x 双自旋子谱（带简约 BZ 菱形）
# ======================================================================
def fig_9_14():
    fig = plt.figure(figsize=(7.6, 3.8))
    xt = yt = [-0.4, -0.2, 0, 0.2, 0.4]
    ext = (-0.5, 0.5, -0.5, 0.5)
    kw = np.linspace(-np.pi, np.pi, 96)
    KX, KY = np.meshgrid(kw, kw)

    # (a) 交错通量 (9.2.34) 的精确色散
    chi, eta = 1.0, 0.4
    E1 = 2 * np.sqrt(chi ** 2 * (np.cos(KX) + np.cos(KY)) ** 2
                     + eta ** 2 * (np.cos(KX) - np.cos(KY)) ** 2)
    E2 = two_spinon(E1)
    rc1 = (0.075, 0.12, 0.35, 0.56)
    _cpanel(fig, rc1, refine(_norm(E2, ref=4.3)), ext, _LEV5, xt=xt, yt=yt,
            grid=(0, -0.25, 0.25), diamond=True)
    _clabel(fig, rc1, '(a)')
    _legend_box(fig, (0.45, 0.52, 0.05, 0.20), ['4', '3', '2', '1', '0.3'])

    # (b) U1Cn00x (9.8.9), lam=0
    b, ons = bonds_989(0.5, 1.0)
    E1 = _E_single_positive(b, kw, onsite=ons)
    E2 = two_spinon(E1)
    rc2 = (0.565, 0.12, 0.35, 0.56)
    _cpanel(fig, rc2, refine(_norm(E2, ref=4.1)), ext, _LEV5, xt=xt, yt=yt,
            grid=(0, -0.25, 0.25), diamond=True)
    _clabel(fig, rc2, '(b)')
    _legend_box(fig, (0.935, 0.52, 0.05, 0.20), ['4', '3', '2', '1', '0.3'])

    save(fig, '9.14')


# ======================================================================
#  FIG 9.15  J1-J2 大 N 相图中各相平均场能量曲线
# ======================================================================
def fig_9_15():
    fig = plt.figure(figsize=(4.9, 4.4))
    ax = fig.add_axes([0.19, 0.11, 0.76, 0.84])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_xticks([0, 1]); ax.set_yticks([])
    ax.tick_params(direction='in', length=4, width=0.9, labelsize=12,
                   top=True, right=True)
    for j in range(1, 9):                      # 内向小刻度
        x = j / 9
        ax.plot([x, x], [0, 0.02], '-', color='k', lw=0.8,
                transform=ax.transData, clip_on=False)
        ax.plot([x, x], [1, 0.98], '-', color='k', lw=0.8, clip_on=False)
        y = j / 9
        ax.plot([0, 0.015], [y, y], '-', color='k', lw=0.8, clip_on=False)
        ax.plot([1, 0.985], [y, y], '-', color='k', lw=0.8, clip_on=False)
    for s in ax.spines.values():
        s.set_linewidth(1.0)
    ax.set_xlabel(r'$J_2$', fontsize=13, va='top', labelpad=6)
    ax.set_ylabel('Energy', fontsize=13, labelpad=8)

    def seg(p, lw=1.2):
        X = np.linspace(p[0], p[1], 100)
        Y = p[2] + p[3] * X
        ax.plot(X, Y, '-', color='k', lw=lw)

    def arc(p0, p1, p2, lw=1.3, n=90):
        t = np.linspace(0, 1, n)[:, None]
        P = (1 - t) ** 2 * np.array(p0) + 2 * (1 - t) * t * np.array(p1) \
            + t ** 2 * np.array(p2)
        ax.plot(P[:, 0], P[:, 1], '-', color='k', lw=lw)

    seg((0.00, 0.775, 0.05, 1.233), lw=1.2)            # A (出顶)
    seg((0.00, 0.60, 0.36, 0.80), lw=1.2)              # I
    seg((0.36, 1.00, 0.75, -1.06), lw=1.2)             # C
    seg((0.55, 1.00, 0.60, -0.39), lw=1.1)             # B（细）
    arc((0.35, 0.29), (0.50, 0.56), (0.60, 0.49))      # D
    arc((0.44, 0.47), (0.55, 0.58), (0.615, 0.535))    # E
    arc((0.44, 0.585), (0.535, 0.648), (0.645, 0.575))  # F
    arc((0.455, 0.628), (0.535, 0.655), (0.64, 0.612))  # H
    # G：加粗曲线段
    tg = np.linspace(0, 1, 60)
    Pg = ((1 - tg) ** 2)[:, None] * np.array((0.545, 0.652)) \
        + 2 * ((1 - tg) * tg)[:, None] * np.array((0.66, 0.60)) \
        + (tg ** 2)[:, None] * np.array((0.79, 0.49))
    ax.plot(Pg[:, 0], Pg[:, 1], '-', color='k', lw=2.6,
            solid_capstyle='round')

    ax.text(0.115, 0.255, 'A', fontsize=13, ha='center')
    ax.text(0.135, 0.53, 'I', fontsize=13, ha='center')
    ax.text(0.83, 0.27, 'C', fontsize=13, ha='center')
    ax.text(0.845, 0.50, 'B', fontsize=13, ha='center')
    ax.text(0.435, 0.415, 'D', fontsize=13, ha='center')
    ax.text(0.405, 0.55, 'E', fontsize=13, ha='center')
    ax.annotate('', xy=(0.452, 0.545), xytext=(0.425, 0.552),
                arrowprops=dict(arrowstyle='-|>', lw=0.9, color='k'))
    ax.text(0.487, 0.625, 'F', fontsize=13, ha='center')
    ax.text(0.535, 0.70, 'H', fontsize=13, ha='center')
    ax.text(0.635, 0.515, 'G', fontsize=13, ha='center')

    save(fig, '9.15')


# ======================================================================
#  FIG 9.16  H(k) 零点的两种分布
# ======================================================================
def _quad_deco(ax, xin, yin, sx, sy, filled, trio=False, pi=np.pi):
    """一个象限的装饰：以象限内侧角 (xin,yin)、指向 (sx,sy) 定位。
    含虚线对角射线+外向箭头、虚线涡旋圆+切向箭头、零点(实/虚)。"""
    X = lambda f: xin + sx * f * pi
    Y = lambda f: yin + sy * f * pi
    # 对角射线（中心到角落，虚线）
    ax.plot([X(0.06), X(1.0)], [Y(0.06), Y(1.0)], '--', color='k', lw=0.95,
            dashes=(4, 2.6), zorder=3)
    # 射线中段大箭头（指向外侧）
    arrow_head(ax, X(0.34), Y(0.34), sx, sy, 0.30, lw=1.0)
    # 涡旋虚线圆 + 两个切向箭头（逆时针）
    cx, cy = X(0.62), Y(0.62)
    r = 0.30 * pi
    th = np.linspace(0, 2 * np.pi, 100)
    ax.plot(cx + r * np.cos(th), cy + r * np.sin(th), '--', color='k',
            lw=0.95, dashes=(4, 2.6), zorder=3)
    for a0 in (0.5, 3.7):
        px, py = cx + r * np.cos(a0), cy + r * np.sin(a0)
        arrow_head(ax, px, py, -np.sin(a0), np.cos(a0), 0.24, lw=0.9)
    # 零点
    if trio:
        bx, by = X(0.55), Y(0.55)
        tdir = np.array([sy, -sx]) / np.sqrt(2)
        ddir = np.array([sx, sy]) / np.sqrt(2)
        pts = [(bx, by) - 0.17 * pi * tdir,
               (bx, by) + 0.05 * pi * ddir,
               (bx, by) + 0.17 * pi * tdir]
        for i, (px, py) in enumerate(pts):
            ax.add_patch(Circle((px, py), 0.085 * pi,
                                fc=('k' if i != 1 else 'white'),
                                ec='k', lw=1.0, zorder=6))
    else:
        px, py = X(0.47), Y(0.47)
        ax.add_patch(Circle((px, py), 0.10 * pi,
                            fc=('k' if filled else 'white'),
                            ec='k', lw=1.1, zorder=6))


def _wavy(ax, pts, lw=1.0):
    """穿过给定点的实线波浪零线（Catmull-Rom）。"""
    P = np.array(pts, dtype=float)
    n = len(P)
    t = np.linspace(0, n - 1, 140)
    out = []
    for i in range(n - 1):
        p0 = P[max(i - 1, 0)]
        p1 = P[i]
        p2 = P[i + 1]
        p3 = P[min(i + 2, n - 1)]
        tt = np.linspace(0, 1, 40)[:, None]
        seg = 0.5 * ((2 * p1) + (-p0 + p2) * tt
                     + (2 * p0 - 5 * p1 + 4 * p2 - p3) * tt ** 2
                     + (-p0 + 3 * p1 - 3 * p2 + p3) * tt ** 3)
        out.append(seg)
    Q = np.vstack(out)
    ax.plot(Q[:, 0], Q[:, 1], '-', color='k', lw=lw, zorder=4)


def fig_9_16():
    fig = plt.figure(figsize=(8.6, 2.7))
    pi = np.pi

    # ---- (a) ----
    ax = fig.add_axes([0.045, 0.10, 0.245, 0.84])
    ax.set_xlim(-pi * 1.18, pi * 1.18)
    ax.set_ylim(-pi * 1.14, pi * 1.24)
    ax.axis('off'); ax.set_aspect('equal')
    ax.add_patch(Rectangle((0, 0), pi, pi, fc='0.85', ec='none', zorder=0))
    ax.plot([-pi, pi], [0, 0], '-', color='k', lw=0.9, zorder=2)
    ax.plot([0, 0], [-pi, pi], '-', color='k', lw=0.9, zorder=2)
    ax.add_patch(Rectangle((-pi, -pi), 2 * pi, 2 * pi, fill=False,
                           ec='k', lw=1.0, zorder=5))
    quad = [(-1, 1, True), (1, 1, False), (-1, -1, False), (1, -1, True)]
    for sx, sy, fl in quad:
        _quad_deco(ax, 0, 0, sx, sy, fl)
        # 实线零线（穿过零点的波浪线）
        X = lambda f: sx * f * pi
        Y = lambda f: sy * f * pi
        _wavy(ax, [(X(0.04), Y(0.98)), (X(0.24), Y(0.72)),
                   (X(0.47), Y(0.47)), (X(0.73), Y(0.27)),
                   (X(0.97), Y(0.04))])
    for lab, y in [(r'$\pi$', pi), (r'$0$', 0), (r'$-\pi$', -pi)]:
        ax.text(-pi - 0.13 * pi, y + 0.06 * pi, lab, fontsize=11,
                ha='right', va='center')
    for lab, x in [(r'$-\pi$', -pi), (r'$0$', 0), (r'$\pi$', pi)]:
        ax.text(x, -pi - 0.16 * pi, lab, fontsize=11, ha='center')
    fig.text(0.045, 0.95, '(a)', fontsize=11)

    # ---- 空心块箭头 ----
    axb = fig.add_axes([0.315, 0.42, 0.065, 0.16])
    axb.set_xlim(0, 1); axb.set_ylim(0, 1); axb.axis('off')
    axb.add_patch(Polygon([(0.02, 0.62), (0.62, 0.62), (0.62, 0.82),
                           (0.98, 0.5), (0.62, 0.18), (0.62, 0.38),
                           (0.02, 0.38)],
                          closed=True, fc='white', ec='k', lw=1.1))

    # ---- (b) ----
    ax = fig.add_axes([0.40, 0.10, 0.575, 0.84])
    ax.set_xlim(-pi * 1.14, 3 * pi + pi * 0.18)
    ax.set_ylim(-pi * 1.14, pi * 1.24)
    ax.axis('off'); ax.set_aspect('equal')
    for x0 in (0, 2 * pi):
        ax.add_patch(Rectangle((x0, 0), pi, pi, fc='0.85', ec='none',
                               zorder=0))
    for x0 in (-pi, 0, pi, 2 * pi):
        ax.plot([x0, x0], [-pi, pi], '-', color='k', lw=0.9, zorder=2)
    ax.plot([-pi, 3 * pi], [0, 0], '-', color='k', lw=0.9, zorder=2)
    ax.add_patch(Rectangle((-pi, -pi), 4 * pi, 2 * pi, fill=False,
                           ec='k', lw=1.0, zorder=5))
    for ox in (-pi, pi):          # 两个周期：象限内侧角在 (ox+pi, 0)
        for sx, sy, fl in quad:
            _quad_deco(ax, ox + pi, 0, sx, sy, fl, trio=True)
            X = lambda f: ox + pi + sx * f * pi
            Y = lambda f: sy * f * pi
            _wavy(ax, [(X(0.04), Y(0.98)), (X(0.26), Y(0.78)),
                       (X(0.52), Y(0.56)), (X(0.76), Y(0.27)),
                       (X(0.97), Y(0.04))])
    for lab, y in [(r'$\pi$', pi), (r'$0$', 0), (r'$-\pi$', -pi)]:
        ax.text(-pi - 0.10 * pi, y + 0.08 * pi, lab, fontsize=11,
                ha='right', va='center')
    for lab, x in [(r'$-\pi$', -pi), (r'$0$', 0), (r'$\pi$', pi),
                   (r'$2\pi$', 2 * pi), (r'$3\pi$', 3 * pi)]:
        ax.text(x, -pi - 0.16 * pi, lab, fontsize=11, ha='center')
    fig.text(0.40, 0.95, '(b)', fontsize=11)

    save(fig, '9.16')


if __name__ == '__main__':
    import sys
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    all_figs = {
        '9.1': fig_9_1, '9.2': fig_9_2, '9.3': fig_9_3, '9.4': fig_9_4,
        '9.5': fig_9_5, '9.6': fig_9_6, '9.7': fig_9_7, '9.8': fig_9_8,
        '9.9': fig_9_9, '9.10': fig_9_10, '9.11': fig_9_11,
        '9.12': fig_9_12, '9.13': fig_9_13, '9.14': fig_9_14,
        '9.15': fig_9_15, '9.16': fig_9_16,
    }
    if only:
        for k in only:
            all_figs[k]()
    else:
        for k, f in all_figs.items():
            f()
