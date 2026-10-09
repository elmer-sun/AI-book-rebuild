# -*- coding: utf-8 -*-
"""
《时空与几何》(Carroll, Spacetime and Geometry) 中文重排工程
第 2 章后 13 幅插图重绘（图 2.15 - 2.27），黑白教材风矢量图。
原图位置：
  2.15/2.16 书页61(p076)  2.17 书页62(p077)  2.18 书页64(p079)
  2.19 书页65(p080)  2.20 书页67(p082)  2.21 书页73(p088)
  2.22 书页78(p093)  2.23 书页79(p094)  2.24 书页80(p095)
  2.25/2.26 书页81(p096)  2.27 书页88(p103)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path as MPath
from matplotlib.patches import (FancyArrowPatch, Ellipse, Circle, Polygon)

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

import os
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)


# ---------------------------------------------------------------- 公共助手
def new_ax(w, h, xlim, ylim):
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis('off')
    return fig, ax


def save(fig, key):
    fig.savefig(os.path.join(FIGDIR, f'fig_{key}.pdf'),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREVDIR, f'fig_{key}.png'),
                bbox_inches='tight', pad_inches=0.03, dpi=170)
    plt.close(fig)


def arrow(ax, p0, p1, lw=1.2, ms=11, color='black', ls='-', zorder=5):
    """带箭头直线（用于轴线、粗向量等）"""
    a = FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=ms,
                        lw=lw, color=color, linestyle=ls,
                        shrinkA=0, shrinkB=0, zorder=zorder)
    ax.add_patch(a)


def swoosh(ax, pts, lw=3.2, ms=22, color='0.72', ls='-', zorder=3):
    """三次贝塞尔粗灰箭头（模仿原书手绘 swoosh 箭头）"""
    codes = [MPath.MOVETO, MPath.CURVE4, MPath.CURVE4, MPath.CURVE4]
    a = FancyArrowPatch(path=MPath(pts, codes), arrowstyle='-|>',
                        mutation_scale=ms, lw=lw, color=color, linestyle=ls,
                        capstyle='round', joinstyle='round',
                        shrinkA=0, shrinkB=0, zorder=zorder)
    ax.add_patch(a)


def leader(ax, p0, p1, rad=0.0, lw=0.7, color='0.15', zorder=6):
    """细指引线（不带箭头）"""
    ax.annotate('', xy=p1, xytext=p0, zorder=zorder,
                arrowprops=dict(arrowstyle='-', lw=lw, color=color,
                                connectionstyle=f'arc3,rad={rad}',
                                shrinkA=0, shrinkB=0))


def shaded_disk(ax, c, R, bright=(0.30, 0.26), vmin=0.05, vmax=0.42,
                res=240, zorder=1):
    """径向灰度渐变圆盘（模拟球面明暗，纯灰度）"""
    xs = np.linspace(c[0] - R, c[0] + R, res)
    ys = np.linspace(c[1] - R, c[1] + R, res)
    X, Y = np.meshgrid(xs, ys)
    d = np.sqrt((X - (c[0] + bright[0] * R)) ** 2 +
                (Y - (c[1] + bright[1] * R)) ** 2) / (1.30 * R)
    V = vmin + (vmax - vmin) * np.clip(d, 0, 1) ** 1.7
    im = ax.imshow(V, cmap='Greys', vmin=0, vmax=1,
                   extent=(xs[0], xs[-1], ys[0], ys[-1]), origin='lower',
                   interpolation='bilinear', zorder=zorder)
    im.set_clip_path(Circle(c, R, transform=ax.transData))


def wavy_pts(p0, p1, amp=0.05, cycles=2.0, phase=0.0, n=60):
    """p0->p1 之间带正波纹的折线点列（端点处波幅归零，保角点）"""
    p0 = np.array(p0, float)
    p1 = np.array(p1, float)
    t = np.linspace(0, 1, n)
    base = p0[None, :] + t[:, None] * (p1 - p0)[None, :]
    d = p1 - p0
    L = np.hypot(*d)
    nvec = np.array([-d[1], d[0]]) / L
    off = amp * np.sin(2 * np.pi * cycles * t + phase) * np.sin(np.pi * t)
    return base + off[:, None] * nvec[None, :]


def quad_bez(p0, c, p1, n=48):
    """二次贝塞尔曲线采样点"""
    p0, c, p1 = [np.array(q, float) for q in (p0, c, p1)]
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * p0[None, :] + 2 * t * (1 - t) * c[None, :] \
        + t ** 2 * p1[None, :]


def warped_patch(ax, corners, nx=4, ny=4, bump=(0.15, 0.30),
                 wig=(0.05, 0.05), fill='0.84', gridcol='0.45',
                 gridlw=0.9, zorder=1):
    """角点 corners=(c00,c10,c01,c11) 的翘曲四边形网格补丁，返回映射函数"""
    c00, c10, c01, c11 = [np.array(c, float) for c in corners]

    def P(s, t):
        p = (c00 + s * (c10 - c00) + t * (c01 - c00)
             + s * t * (c11 - c10 - c01 + c00))
        p = p + bump[0] * np.sin(np.pi * s) * np.sin(np.pi * t) * np.array([1, 0]) \
              + bump[1] * np.sin(np.pi * s) * np.sin(np.pi * t) * np.array([0, 1])
        p = p + np.array([wig[0] * np.sin(2 * np.pi * s + 0.7),
                          wig[1] * np.sin(2 * np.pi * t + 0.4)])
        return p

    n_s = 41
    # 填充边界
    bnd = []
    ss = np.linspace(0, 1, n_s)
    bnd += [P(s, 0) for s in ss]
    bnd += [P(1, t) for t in ss]
    bnd += [P(1 - s, 1) for s in ss]
    bnd += [P(0, 1 - t) for t in ss]
    ax.add_patch(Polygon(bnd, closed=True, facecolor=fill,
                         edgecolor='none', zorder=zorder))
    # 网格线
    for k in range(nx + 1):
        s = k / nx
        line = [P(s, t) for t in np.linspace(0, 1, 41)]
        ax.plot([q[0] for q in line], [q[1] for q in line],
                color=gridcol, lw=gridlw, zorder=zorder + 0.2)
    for k in range(ny + 1):
        t = k / ny
        line = [P(s, t) for s in np.linspace(0, 1, 41)]
        ax.plot([q[0] for q in line], [q[1] for q in line],
                color=gridcol, lw=gridlw, zorder=zorder + 0.2)
    return P


# ---------------------------------------------------------------- 图 2.15
def fig_2_15():
    """S1 上的两坐标卡（双圆环，外圈下开口、内圈上开口）"""
    fig, ax = new_ax(2.3, 2.5, (-1.75, 1.75), (-1.5, 1.65))
    # 外圈 U1：底部开口（缺口 240°–300°）
    th = np.linspace(np.radians(300), np.radians(600), 300)
    ax.plot(np.cos(th), np.sin(th) - 0.02, color='black', lw=1.2, zorder=3)
    for a in (240, 300):
        aa = np.radians(a)
        ax.plot([0.88 * np.cos(aa), 1.08 * np.cos(aa)],
                [0.88 * np.sin(aa) - 0.02, 1.08 * np.sin(aa) - 0.02],
                color='black', lw=1.0)
    # 内圈 U2：顶部开口（缺口 60°–120°）
    th = np.linspace(np.radians(120), np.radians(420), 300)
    ax.plot(0.92 * np.cos(th), 0.92 * np.sin(th) + 0.03, color='black',
            lw=1.2, zorder=3)
    for a in (60, 120):
        aa = np.radians(a)
        ax.plot([0.80 * np.cos(aa), 1.04 * np.cos(aa)],
                [0.80 * np.sin(aa) + 0.03, 1.04 * np.sin(aa) + 0.03],
                color='black', lw=1.0)
    ax.text(-1.55, 1.28, r'$S^1$', fontsize=13)
    ax.text(1.12, 0.70, r'$U_1$', fontsize=13)
    ax.text(-0.52, -0.62, r'$U_2$', fontsize=13)
    save(fig, '2.15')


# ---------------------------------------------------------------- 图 2.16
def fig_2_16():
    """S2 的球极投影坐标卡：北极向切于南极的平面 x3=-1 投影"""
    fig, ax = new_ax(4.7, 2.95, (0, 4.7), (0, 2.95))
    # 参考平面 x^3 = -1
    quad = [(0.55, 0.42), (0.95, 1.15), (4.50, 1.45), (4.10, 0.72)]
    ax.add_patch(Polygon(quad, closed=True, facecolor='0.90',
                         edgecolor='0.55', lw=0.8, zorder=1))
    ax.text(3.85, 1.10, r'$x^3=-1$', fontsize=12, zorder=6)
    # 球（灰度渐变）
    shaded_disk(ax, (2.45, 1.55), 0.78, bright=(0.20, 0.28), vmin=0.08,
                vmax=0.52, zorder=2)
    # 坐标轴 triad
    arrow(ax, (0.65, 1.90), (0.65, 2.72), lw=1.0, ms=10)
    ax.text(0.58, 2.80, r'$x^3$', fontsize=12)
    arrow(ax, (0.65, 1.90), (1.48, 1.93), lw=1.0, ms=10)
    ax.text(1.56, 1.86, r'$x^2$', fontsize=12)
    arrow(ax, (0.65, 1.90), (0.18, 1.50), lw=1.0, ms=10)
    ax.text(0.02, 1.36, r'$x^1$', fontsize=12)
    # 投影线：北极 -> 球面点（球内浅灰细线）-> 平面点（黑色粗线）
    npole = (2.45, 2.33)
    ps = (2.00, 1.13)
    pp = (1.81, 0.62)
    ax.plot([npole[0], ps[0]], [npole[1], ps[1]], color='0.45', lw=1.0,
            zorder=3)
    ax.plot([ps[0], pp[0]], [ps[1], pp[1]], color='black', lw=1.8, zorder=4)
    for q in (npole, ps, pp):
        ax.plot(*q, marker='o', ms=4.5, color='black', zorder=5)
    ax.text(1.58, 1.27, r'$(x^1,x^2,x^3)$', fontsize=12, ha='right',
            zorder=6)
    ax.text(1.60, 0.70, r'$(y^1,y^2)$', fontsize=12, ha='right', zorder=6)
    save(fig, '2.16')


# ---------------------------------------------------------------- 图 2.17
def fig_2_17():
    """链式法则交换图：R^m -> R^n -> R^l"""
    fig, ax = new_ax(4.0, 3.25, (-0.15, 3.55), (-0.80, 2.30))
    boxes = [((0, 1), (1, 2), r'$\mathbf{R}^m$'),
             ((2.2, 1), (3.2, 2), r'$\mathbf{R}^l$'),
             ((1.1, -0.55), (2.1, 0.45), r'$\mathbf{R}^n$')]
    for (x0, y0), (x1, y1), lab in boxes:
        ax.add_patch(Polygon([(x0, y0), (x1, y0), (x1, y1), (x0, y1)],
                             closed=True, facecolor='white',
                             edgecolor='black', lw=1.4, zorder=2))
        ax.text(x1 - 0.10, y1 - 0.16, lab, fontsize=13, ha='right',
                zorder=3)
    # g∘f ：上方水平 swoosh
    swoosh(ax, [(1.02, 1.52), (1.45, 1.28), (1.80, 1.30), (2.18, 1.56)])
    ax.text(1.60, 1.68, r'$g\circ f$', fontsize=13)
    # f ：左上 -> 下方
    swoosh(ax, [(0.50, 0.98), (0.40, 0.62), (0.70, 0.30), (1.04, 0.10)])
    ax.text(0.33, 0.66, r'$f$', fontsize=13)
    # g ：下方 -> 右上
    swoosh(ax, [(2.12, -0.08), (2.50, -0.18), (2.62, 0.28), (2.66, 0.96)])
    ax.text(2.80, 0.42, r'$g$', fontsize=13)
    save(fig, '2.17')


# ---------------------------------------------------------------- 图 2.18
def fig_2_18():
    """流形坐标网格上的偏导数基向量 d1, d2 与点 p"""
    fig, ax = new_ax(3.5, 2.65, (-0.35, 2.95), (-1.05, 1.95))
    P = warped_patch(ax, [(0.0, 0.60), (1.35, 1.60), (1.05, -0.55),
                          (2.55, 0.70)],
                     nx=5, ny=5, bump=(0.16, 0.30), wig=(0.05, 0.04))
    p = P(0.50, 0.45)
    eps = 1e-3
    es = (P(0.5 + eps, 0.45) - p) / eps      # 沿 s：上右（d2）
    et = (P(0.5, 0.45 + eps) - p) / eps      # 沿 t：下右（d1）
    es = np.array(es) / np.hypot(*es)
    et = np.array(et) / np.hypot(*et)
    e2 = 0.62 * es
    e1 = 0.52 * et
    arrow(ax, p, (p[0] + e2[0], p[1] + e2[1]), lw=2.0, ms=15, zorder=6)
    arrow(ax, p, (p[0] + e1[0], p[1] + e1[1]), lw=2.0, ms=15, zorder=6)
    ax.plot(*p, marker='o', ms=4, color='black', zorder=7)
    ax.text(p[0] - 0.12, p[1] - 0.10, r'$p$', fontsize=13, ha='right',
            zorder=7)
    ax.text(p[0] + e2[0] - 0.24, p[1] + e2[1] + 0.06, r'$\partial_2$',
            fontsize=13, zorder=7)
    ax.text(p[0] + e1[0] + 0.02, p[1] + e1[1] + 0.14, r'$\partial_1$',
            fontsize=13, zorder=7)
    l1 = P(0.10, 1.02)
    l2 = P(0.92, 1.02)
    ax.text(l1[0] - 0.22, l1[1] - 0.14, r'$x^1$', fontsize=13)
    ax.text(l2[0] + 0.10, l2[1] - 0.10, r'$x^2$', fontsize=13)
    save(fig, '2.18')


# ---------------------------------------------------------------- 图 2.19
def fig_2_19():
    """切向量分解的映射缠绕图：R -> M -> R 与 R^n 坐标卡"""
    fig, ax = new_ax(3.9, 3.5, (0, 3.55), (0, 3.6))
    # 左右两条斜线（R）
    ax.plot([0.30, 0.78], [1.72, 2.92], color='black', lw=2.4, zorder=3)
    ax.text(0.17, 2.72, r'$\mathbf{R}$', fontsize=13)
    ax.plot([2.62, 3.10], [1.72, 2.92], color='black', lw=2.4, zorder=3)
    ax.text(3.18, 2.72, r'$\mathbf{R}$', fontsize=13)
    # 顶部 f∘γ
    swoosh(ax, [(0.92, 3.12), (1.55, 3.06), (2.25, 3.10), (2.88, 3.18)],
           lw=2.6, ms=20)
    ax.text(1.88, 3.34, r'$f\circ\gamma$', fontsize=13)
    # M 椭圆（灰度渐变）+ 内部曲线
    from matplotlib.patches import Ellipse as Ell
    e = Ell((1.78, 2.32), 1.42, 0.86, facecolor='0.82', edgecolor='black',
            lw=1.2, zorder=3)
    ax.add_patch(e)
    arc = quad_bez((1.42, 1.97), (1.92, 2.04), (2.12, 2.62))
    ax.plot(arc[:, 0], arc[:, 1], color='black', lw=2.2, zorder=4)
    ax.text(2.35, 2.86, r'$M$', fontsize=13)
    # gamma、f 短箭头
    swoosh(ax, [(0.80, 2.31), (0.90, 2.29), (1.02, 2.30), (1.16, 2.33)],
           lw=2.2, ms=16)
    ax.text(0.88, 2.50, r'$\gamma$', fontsize=13)
    swoosh(ax, [(2.44, 2.33), (2.54, 2.31), (2.66, 2.32), (2.80, 2.35)],
           lw=2.2, ms=16)
    ax.text(2.52, 2.52, r'$f$', fontsize=13)
    # phi^{-1}（向上）与 phi（向下）
    swoosh(ax, [(1.20, 1.60), (1.20, 1.75), (1.20, 1.90), (1.20, 2.05)],
           lw=2.2, ms=16)
    ax.text(0.84, 1.74, r'$\phi^{-1}$', fontsize=13)
    swoosh(ax, [(1.98, 2.05), (1.98, 1.90), (1.98, 1.75), (1.98, 1.60)],
           lw=2.2, ms=16)
    ax.text(2.12, 1.78, r'$\phi$', fontsize=13)
    # R^n 方框 + 小坐标轴
    ax.add_patch(Polygon([(1.00, 0.22), (2.36, 0.22), (2.36, 1.56),
                          (1.00, 1.56)], closed=True, facecolor='white',
                         edgecolor='black', lw=1.4, zorder=2))
    ax.text(2.22, 1.34, r'$\mathbf{R}^n$', fontsize=13, ha='right', zorder=3)
    arrow(ax, (1.28, 0.50), (1.28, 0.98), lw=1.0, ms=10, zorder=3)
    arrow(ax, (1.28, 0.50), (1.80, 0.50), lw=1.0, ms=10, zorder=3)
    ax.text(1.66, 0.28, r'$x^\mu$', fontsize=12, zorder=3)
    # phi∘gamma（左下大弧）与 f∘phi^{-1}（右下大弧）
    swoosh(ax, [(0.44, 1.92), (0.30, 1.30), (0.52, 0.86), (0.92, 0.66)],
           lw=3.0, ms=24)
    ax.text(0.16, 1.20, r'$\phi\circ\gamma$', fontsize=13)
    swoosh(ax, [(2.44, 0.62), (2.86, 0.86), (2.94, 1.44), (2.70, 1.90)],
           lw=3.0, ms=24)
    ax.text(2.98, 1.08, r'$f\circ\phi^{-1}$', fontsize=13)
    save(fig, '2.19')


# ---------------------------------------------------------------- 图 2.20
def fig_2_20():
    """坐标变换 x^mu -> x^mu' 诱导切空间基变换（两块网格补丁）"""
    fig, ax = new_ax(4.7, 2.35, (-2.95, 3.25), (-1.25, 1.65))
    # 左补丁
    P = warped_patch(ax, [(-2.50, 0.55), (-1.30, 1.15), (-2.15, -0.65),
                          (-0.95, -0.05)],
                     nx=4, ny=4, bump=(0.08, 0.20), wig=(0.05, 0.05))
    p = P(0.55, 0.45)
    eps = 1e-3
    es = (P(0.55 + eps, 0.45) - p) / eps
    et = (P(0.55, 0.45 + eps) - p) / eps
    es = np.array(es) / np.hypot(*es)
    et = np.array(et) / np.hypot(*et)
    e2 = 0.52 * es          # d2：沿浅方向上右
    e1 = 0.50 * et          # d1：沿陡方向下右
    arrow(ax, p, (p[0] + e2[0], p[1] + e2[1]), lw=2.0, ms=15, zorder=6)
    arrow(ax, p, (p[0] + e1[0], p[1] + e1[1]), lw=2.0, ms=15, zorder=6)
    ax.plot(*p, marker='o', ms=4, color='black', zorder=7)
    ax.text(p[0] + e2[0] - 0.26, p[1] + e2[1] + 0.10, r'$\partial_2$',
            fontsize=13, zorder=7)
    ax.text(p[0] + e1[0] + 0.10, p[1] + e1[1] + 0.02, r'$\partial_1$',
            fontsize=13, zorder=7)
    lt = P(0.40, -0.10)
    ax.text(lt[0] - 0.18, lt[1] + 0.34, r'$x^\mu$', fontsize=13)
    # 右补丁
    P2 = warped_patch(ax, [(0.95, -0.20), (1.10, 1.35), (2.60, -0.38),
                           (2.75, 1.12)],
                      nx=4, ny=4, bump=(-0.10, 0.16), wig=(0.06, 0.05))
    p2 = P2(0.58, 0.55)
    es2 = (P2(0.58 + eps, 0.55) - p2) / eps
    et2 = (P2(0.58, 0.55 + eps) - p2) / eps
    es2 = np.array(es2) / np.hypot(*es2)
    et2 = np.array(et2) / np.hypot(*et2)
    e1b = 0.55 * es2                     # d1'：向上
    e2b = -0.52 * et2                    # d2'：向左
    arrow(ax, p2, (p2[0] + e1b[0], p2[1] + e1b[1]), lw=2.0, ms=15, zorder=6)
    arrow(ax, p2, (p2[0] + e2b[0], p2[1] + e2b[1]), lw=2.0, ms=15, zorder=6)
    ax.plot(*p2, marker='o', ms=4, color='black', zorder=7)
    ax.text(p2[0] + e1b[0] + 0.12, p2[1] + e1b[1] + 0.02, r"$\partial_{1'}$",
            fontsize=13, zorder=7)
    ax.text(p2[0] + e2b[0] + 0.02, p2[1] + e2b[1] - 0.30, r"$\partial_{2'}$",
            fontsize=13, zorder=7)
    ax.text(0.30, 0.28, r"$x^{\mu'}$", fontsize=13)
    save(fig, '2.20')


# ---------------------------------------------------------------- 图 2.21
def fig_2_21():
    """二维球面上的线元：ds, dtheta, sin(theta) dphi"""
    fig, ax = new_ax(3.4, 3.3, (-1.7, 1.7), (-1.5, 1.8))
    shaded_disk(ax, (0, 0), 1.25, bright=(0.32, 0.28), vmin=0.06,
                vmax=0.40, zorder=1)
    # 自转轴
    ax.plot([0.05, 0.05], [1.23, 1.72], color='black', lw=1.0, zorder=3)
    ax.text(-0.55, 0.42, r'$S^2$', fontsize=14, zorder=4)
    A = (0.42, 0.72)     # 上顶点
    C = (0.95, 0.45)     # 右顶点
    B = (0.70, 0.00)     # 下顶点
    # 经线 A->B（细）
    m1 = quad_bez(A, (0.47, 0.33), B)
    ax.plot(m1[:, 0], m1[:, 1], color='black', lw=1.0, zorder=4)
    # 纬线 B->C（细）
    m2 = quad_bez(B, (0.86, -0.07), C)
    ax.plot(m2[:, 0], m2[:, 1], color='black', lw=1.0, zorder=4)
    # ds 弧 A->C（粗）
    m3 = quad_bez(A, (0.84, 0.74), C)
    ax.plot(m3[:, 0], m3[:, 1], color='black', lw=2.4, zorder=5)
    ax.plot(*A, marker='o', ms=4.5, color='black', zorder=6)
    ax.plot(*C, marker='o', ms=4.5, color='black', zorder=6)
    ax.text(1.28, 1.10, r'$ds$', fontsize=13, zorder=6)
    leader(ax, (1.22, 1.02), (0.82, 0.64), rad=0.0, zorder=6)
    ax.text(0.14, 0.26, r'$d\theta$', fontsize=13, zorder=6)
    ax.text(0.62, -0.52, r'$\sin\theta\, d\phi$', fontsize=13, zorder=6)
    leader(ax, (0.84, -0.38), (0.84, -0.03), rad=-0.35, zorder=6)
    save(fig, '2.21')


# ---------------------------------------------------------------- 图 2.22
def fig_2_22():
    """a(t)∝t^q (0<q<1) 平坦 RW 宇宙时空图：与奇点相切的光锥"""
    fig, ax = new_ax(4.5, 2.65, (-0.10, 6.35), (-0.28, 3.42))
    k = 1.15          # r(t) = k |sqrt(t) - 1|, 腰部 t=1
    t_top = 2.85
    # t 轴
    arrow(ax, (0.15, 0.0), (0.15, 3.28), lw=1.2, ms=11)
    ax.text(0.02, 3.26, r'$t$', fontsize=13, ha='right')
    # 奇点线（虚线横轴，右端箭头）
    arrow(ax, (0.15, 0.0), (6.15, 0.0), lw=1.2, ms=11, ls=(0, (5, 4)))
    for c in (2.00, 4.35):
        tt = np.linspace(0.012, t_top, 240)
        hw = k * np.abs(np.sqrt(tt) - 1.0)
        ax.plot(c - hw, tt, color='black', lw=1.3, zorder=3)
        ax.plot(c + hw, tt, color='black', lw=1.3, zorder=3)
        # 顶部开口椭圆
        hwt = k * (np.sqrt(t_top) - 1.0)
        ax.add_patch(Ellipse((c, t_top), 2 * hwt, 2 * hwt * 0.15,
                             fill=False, edgecolor='black', lw=1.0,
                             zorder=4))
        # 底部小截面椭圆
        tb = 0.18
        hwb = k * (1.0 - np.sqrt(tb))
        ax.add_patch(Ellipse((c, tb), 2 * hwb, 2 * hwb * 0.13,
                             fill=False, edgecolor='black', lw=0.9,
                             zorder=4))
    save(fig, '2.22')


# ---------------------------------------------------------------- 图 2.23
def fig_2_23():
    """类空面 Sigma 上的连通子集 S 及 D±(S)、H±(S)"""
    fig, ax = new_ax(4.0, 2.6, (-2.1, 2.3), (-1.45, 1.5))
    L = (-1.85, -0.32)
    T = (0.35, 0.55)
    Rt = (2.00, -0.10)
    B = (-0.30, -1.00)
    S_c = (0.05, -0.12)
    a_ell, b_ell = 0.55, 0.175
    apex_u = (0.10, 0.98)
    apex_d = (0.10, -1.12)
    # 下锥（先画，之后被半透明 Sigma 部分遮盖）
    ml = (S_c[0] - a_ell, S_c[1])
    mr = (S_c[0] + a_ell, S_c[1])
    th = np.linspace(np.pi, 2 * np.pi, 60)   # 下半椭圆
    low = [(S_c[0] + a_ell * np.cos(t), S_c[1] + b_ell * np.sin(t))
           for t in th]
    ax.add_patch(Polygon([ml, apex_d, mr] + low, closed=True,
                         facecolor='0.80', edgecolor='0.35', lw=0.8,
                         zorder=1))
    # Sigma 波纹面（半透明，可透出下锥）
    bnd = []
    bnd += list(wavy_pts(L, T, amp=0.035, cycles=1.2, phase=0.5))
    bnd += list(wavy_pts(T, Rt, amp=0.035, cycles=1.1, phase=2.2))
    bnd += list(wavy_pts(Rt, B, amp=0.035, cycles=1.2, phase=4.0))
    bnd += list(wavy_pts(B, L, amp=0.035, cycles=1.1, phase=5.6))
    ax.add_patch(Polygon(bnd, closed=True, facecolor='0.88', alpha=0.50,
                         edgecolor='0.30', lw=0.9, zorder=2))
    ax.text(-1.40, -0.16, r'$\Sigma$', fontsize=14, zorder=6)
    # S 椭圆盘（前沿黑线）
    ax.add_patch(Ellipse(S_c, 2 * a_ell, 2 * b_ell, facecolor='0.90',
                         edgecolor='none', zorder=3))
    th_f = np.linspace(np.pi, 2 * np.pi, 60)
    ax.plot(S_c[0] + a_ell * np.cos(th_f), S_c[1] + b_ell * np.sin(th_f),
            color='black', lw=1.1, zorder=4)
    ax.text(-0.06, -0.10, r'$S$', fontsize=14, zorder=6)
    # 上锥（不透明，双色调）
    th_b = np.linspace(0, np.pi, 60)         # 上半椭圆（远沿）
    up = [(S_c[0] + a_ell * np.cos(t), S_c[1] + b_ell * np.sin(t))
          for t in th_b]
    ax.add_patch(Polygon([ml, apex_u, mr] + up, closed=True,
                         facecolor='0.87', edgecolor='0.35', lw=0.8,
                         zorder=5))
    ax.add_patch(Polygon([ml, apex_u, (S_c[0], S_c[1] - b_ell)],
                         closed=True, facecolor='0.78', edgecolor='none',
                         zorder=5))
    # 透过上锥可见的 S 远沿（淡灰弧）
    ax.plot(S_c[0] + a_ell * np.cos(th_b),
            S_c[1] + 1.02 * b_ell * np.sin(th_b),
            color='0.62', lw=0.9, zorder=6)
    # 标注与指引线
    ax.text(-1.10, 0.95, r'$H^+(S)$', fontsize=13, zorder=7)
    leader(ax, (-0.78, 0.88), (-0.34, 0.50), rad=0.18, zorder=7)
    ax.text(1.20, 1.02, r'$D^+(S)$', fontsize=13, zorder=7)
    leader(ax, (1.02, 0.94), (0.48, 0.52), rad=-0.15, zorder=7)
    ax.text(-1.32, -1.08, r'$H^-(S)$', fontsize=13, zorder=7)
    leader(ax, (-0.74, -1.02), (-0.32, -0.74), rad=-0.15, zorder=7)
    ax.text(1.32, -1.10, r'$D^-(S)$', fontsize=13, zorder=7)
    leader(ax, (0.98, -1.00), (0.46, -0.74), rad=0.12, zorder=7)
    save(fig, '2.23')


# ---------------------------------------------------------------- 图 2.24
def fig_2_24():
    """闵氏时空中选差的类空超曲面 Sigma：D+(Sigma) 止于光锥"""
    fig, ax = new_ax(3.0, 2.6, (-1.45, 1.85), (-0.22, 1.32))
    apex = (0.0, 0.52)
    a_m, b_m = 0.475, 0.124
    mouth = (0.0, 1.08)
    ml = (-a_m, mouth[1])
    mr = (a_m, mouth[1])
    # 上锥体（双色调）
    th = np.linspace(0, np.pi, 60)
    up = [(a_m * np.cos(t), mouth[1] + b_m * np.sin(t)) for t in th]
    ax.add_patch(Polygon([ml, apex, mr] + up, closed=True,
                         facecolor='0.87', edgecolor='0.35', lw=0.8,
                         zorder=3))
    ax.add_patch(Polygon([ml, apex, (0, mouth[1])], closed=True,
                         facecolor='0.78', edgecolor='none', zorder=3))
    # 下锥（大张角，先画，之后被 Sigma 丘部分遮盖）
    bl = (-1.32, -0.15)
    br = (1.32, -0.15)
    ax.add_patch(Polygon([apex, bl, br], closed=True, facecolor='0.86',
                         edgecolor='0.40', lw=0.8, zorder=1))
    ax.add_patch(Polygon([apex, bl, (0, -0.15)], closed=True,
                         facecolor='0.78', edgecolor='none', zorder=1))
    # Sigma：大土丘（缓波纹边）
    bnd = list(wavy_pts((-1.08, -0.15), (0.0, 0.38), amp=0.025,
                        cycles=0.8, phase=0.8))
    bnd += list(wavy_pts((0.0, 0.38), (1.08, -0.15), amp=0.025,
                         cycles=0.8, phase=2.5))
    bnd += list(wavy_pts((1.08, -0.15), (-1.08, -0.15), amp=0.02,
                         cycles=1.2, phase=4.5))
    ax.add_patch(Polygon(bnd, closed=True, facecolor='0.85',
                         edgecolor='0.25', lw=1.0, zorder=2))
    # 锥轮廓在丘外的下段（重画于丘之上）
    for sgn in (-1, 1):
        ax.plot([apex[0] + sgn * 1.02, sgn * 1.32], [0.0, -0.15],
                color='0.40', lw=0.8, zorder=2.5)
    # 开口（嘴）椭圆：白腔 + 内壁阴影（上弦月牙）
    ax.add_patch(Ellipse(mouth, 2 * a_m, 2 * b_m, facecolor='white',
                         edgecolor='black', lw=1.0, zorder=4))
    ax.add_patch(Ellipse((0, mouth[1] + 0.042), 0.70, 0.10,
                         facecolor='0.84', edgecolor='none', zorder=5))
    ax.add_patch(Ellipse((0, mouth[1] + 0.005), 0.70, 0.10,
                         facecolor='white', edgecolor='none', zorder=5.5))
    # 标注
    ax.text(-0.14, 0.48, r'$p$', fontsize=13, zorder=6)
    ax.text(0.72, 0.80, r'$D^+(\Sigma)$', fontsize=13, zorder=6)
    leader(ax, (0.68, 0.74), (0.05, 0.28), rad=0.0, zorder=6)
    ax.text(1.42, 0.30, r'$\Sigma$', fontsize=14, zorder=6)
    leader(ax, (1.38, 0.27), (0.90, 0.14), rad=0.0, zorder=6)
    save(fig, '2.24')


# ---------------------------------------------------------------- 图 2.25
def fig_2_25():
    """柱状时空与闭合类时线：光锥逐渐倾斜，identify 两竖边"""
    fig, ax = new_ax(3.9, 3.3, (-0.75, 3.35), (-0.15, 3.45))
    xl, xr = 0.05, 2.15
    # 圆柱两竖边
    ax.plot([xl, xl], [0.05, 2.75], color='black', lw=1.8, zorder=3)
    ax.plot([xr, xr], [0.05, 2.75], color='black', lw=1.8, zorder=3)
    # t=0 面（实线）
    ax.plot([xl, xr], [1.42, 1.42], color='black', lw=1.3, zorder=3)
    # Sigma 波纹线
    xs = np.linspace(xl, xr, 120)
    ys = 0.28 + 0.045 * np.sin(3 * np.pi * (xs - xl) / (xr - xl))
    ax.plot(xs, ys, color='black', lw=1.0, zorder=3)
    ax.text(0.24, 0.02, r'$\Sigma$', fontsize=13, zorder=4)

    def lcone(x, y, tilt, a=0.24, h=0.34, z=4):
        t = -np.radians(tilt)          # 正 tilt = 顺时针（口向右倒）
        ca, sa = np.cos(t), np.sin(t)

        def R(px, py):
            return (x + px * ca - py * sa, y + px * sa + py * ca)
        ml, mr = R(-a, h), R(a, h)
        ax.add_patch(Polygon([(x, y), ml, mr], closed=True,
                             facecolor='0.80', edgecolor='0.45', lw=0.6,
                             zorder=z))
        ax.add_patch(Ellipse(R(0, h), 2 * a, 2 * a * 0.30,
                             angle=-tilt, facecolor='0.93',
                             edgecolor='0.40', lw=0.6, zorder=z + 0.1))
    for cx in (0.68, 1.50):
        lcone(cx, 0.62, 0)
        lcone(cx, 1.08, 12)
        lcone(cx, 1.75, 32)
        lcone(cx, 2.35, 58)
    # 闭合类时线（虚线，穿过顶排锥口，随 identify 闭合）
    xs = np.linspace(xl, xr, 140)
    ys = 2.52 + 0.055 * np.sin(3 * np.pi * (xs - xl) / (xr - xl) + 0.6)
    ax.plot(xs, ys, color='black', lw=1.3, ls=(0, (5, 3.5)), zorder=5)
    ax.text(2.26, 2.06, 'closed\ntimelike curve', fontsize=10.5, zorder=5)
    leader(ax, (2.24, 2.40), (1.96, 2.50), rad=0.0, zorder=5)
    # identify 椭圆弧（双箭头）
    th = np.linspace(np.radians(14), np.radians(166), 80)
    pts = [(1.10 + 1.38 * np.cos(t), 2.42 + 0.40 * np.sin(t)) for t in th]
    codes = [MPath.MOVETO] + [MPath.LINETO] * (len(pts) - 1)
    ax.add_patch(FancyArrowPatch(path=MPath(pts, codes),
                                 arrowstyle='<|-|>', mutation_scale=12,
                                 lw=1.0, color='0.15', zorder=4))
    ax.text(1.10, 3.12, 'identify', fontsize=12, ha='center', zorder=5)
    save(fig, '2.25')


# ---------------------------------------------------------------- 图 2.26
def fig_2_26():
    """奇点 p 使其未来从 D+(Sigma) 中剔除（V 形柯西地平线）"""
    fig, ax = new_ax(2.9, 2.45, (-0.05, 2.75), (-0.50, 2.95))
    poly = [(0.10, 2.20), (0.78, 2.20), (1.30, 0.85), (1.82, 2.20),
            (2.50, 2.20), (2.50, 0.0)]
    bnd = poly + list(wavy_pts((2.50, 0.0), (0.10, 0.0), amp=0.04,
                               cycles=2.5, phase=1.0))[1:]
    ax.add_patch(Polygon(bnd, closed=True, facecolor='0.82',
                         edgecolor='0.30', lw=1.0, zorder=2))
    # 柯西地平线（虚线 V），右支带指向 p 的箭头
    ax.plot([0.78, 1.30], [2.20, 0.85], color='black', lw=1.4,
            ls=(0, (6, 4)), zorder=4)
    a = FancyArrowPatch((1.82, 2.20), (1.36, 0.91), arrowstyle='-|>',
                        mutation_scale=13, lw=1.4, color='black',
                        linestyle=(0, (6, 4)), shrinkA=0, shrinkB=0,
                        zorder=4)
    ax.add_patch(a)
    # 标注
    ax.text(0.72, 2.58, r'$H^+(\Sigma)$', fontsize=13, zorder=5)
    leader(ax, (0.92, 2.48), (1.00, 1.76), rad=0.0, zorder=5)
    ax.text(1.38, 0.55, r'$p$', fontsize=13, zorder=5)
    ax.text(0.30, 0.28, r'$D^+(\Sigma)$', fontsize=13, zorder=5)
    ax.text(1.02, -0.32, r'$\Sigma$', fontsize=14, zorder=5)
    save(fig, '2.26')


# ---------------------------------------------------------------- 图 2.27
def fig_2_27():
    """无穷小 n 维区域的平行六面体，由有序向量组 U, V, W 张成"""
    fig, ax = new_ax(2.6, 2.3, (-0.60, 3.00), (-0.85, 1.70))
    O = np.array([0.0, 0.0])
    U = np.array([1.95, -0.30])
    V = np.array([0.85, 0.50])
    W = np.array([0.10, 0.72])

    def face(corner_list, shade, z):
        ax.add_patch(Polygon([tuple(O + c) for c in corner_list],
                             closed=True, facecolor=shade,
                             edgecolor='0.55', lw=0.5, zorder=z))
    face([W, U + W, U + V + W, V + W], '0.90', 1)     # 顶面
    face([U, U + V, U + V + W, U + W], '0.82', 1)     # 右面
    face([O, U, U + W, W], '0.72', 2)                 # 前左面
    # 三条棱向量箭头
    arrow(ax, tuple(O), tuple(0.97 * U), lw=2.6, ms=17, zorder=5)
    arrow(ax, tuple(O), tuple(0.97 * W), lw=2.6, ms=17, zorder=5)
    arrow(ax, tuple(O), tuple(0.96 * V), lw=2.2, ms=15, color='0.50',
          zorder=5)
    ax.text(U[0] - 0.10, U[1] - 0.34, r'$U$', fontsize=14, zorder=5)
    ax.text(W[0] - 0.34, W[1] + 0.06, r'$W$', fontsize=14, zorder=5)
    ax.text(V[0] + 0.20, V[1] - 0.22, r'$V$', fontsize=14, zorder=5)
    save(fig, '2.27')


# ---------------------------------------------------------------- 生成
if __name__ == '__main__':
    for k in range(15, 28):
        globals()[f'fig_2_{k}']()
        print(f'fig 2.{k} done')
