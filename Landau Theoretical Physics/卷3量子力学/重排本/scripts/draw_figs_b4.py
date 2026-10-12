# -*- coding: utf-8 -*-
"""
朗道《量子力学》（卷3）中文重排本插图重绘 —— 第四批：图32–图40
图32 §91 旋转-反射轴（平面 + 轴 + P→P'）        (原书 p328 / PDF p341)
图33 §91 两 π 转轴相乘得垂直轴 PP'               (原书 p329 / PDF p342)
图34 §93 C3v, C4v, D3, D4 对称面/对称轴          (原书 p334 / PDF p347)
图35 §93 D3h, D2d, D3d 对称面/对称轴             (原书 p335 / PDF p348)
图36 §93 T 群：四面体 + 立方体中的 C3, C2        (原书 p337 / PDF p350)
图37 §93 Td 群：立方体 + 四面体中的 S4, C3, σ    (原书 p337 / PDF p350)
图38 §93 Th 群：立方体中的 C2, S6, σ             (原书 p338 / PDF p351)
图39 §93 O 群：立方体中的 C4, C3, C2             (原书 p338 / PDF p351)
图40 §93 Oh 群：立方体中的 C4, S6, C2, σ, σh     (原书 p338 / PDF p351)
统一黑白教材风；输出 figures/figN.pdf + figures/preview/figN.png
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle
import numpy as np
import os

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm', 'axes.unicode_minus': False,
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

LW_MAIN = 1.2      # 主体线
LW_AUX = 0.8       # 辅助线
LW_THICK = 2.0     # 对称轴粗线
DASH = (0, (5, 3)) # 虚线样式


def save(fig, n):
    for ext, path in (('pdf', os.path.join(FIGDIR, 'fig%d.pdf' % n)),
                      ('png', os.path.join(PREVDIR, 'fig%d.png' % n))):
        fig.savefig(path, bbox_inches='tight', pad_inches=0.03, dpi=300)
    plt.close(fig)
    print('fig%d done' % n)


def bare_axis(ax, xlim, ylim):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect('equal'); ax.axis('off')


def open_circle(ax, x, y, r=2.6):
    ax.add_patch(Circle((x, y), r, facecolor='white', edgecolor='k',
                        lw=1.1, zorder=6))


def arc(ax, c, r, a1, a2, lw=LW_MAIN):
    t = np.radians(np.linspace(a1, a2, 40))
    ax.plot(c[0] + r * np.cos(t), c[1] + r * np.sin(t), color='k',
            lw=lw, zorder=5)


def hatch_polygon(ax, pts, angle_deg, spacing=4.0, lw_edge=1.1,
                  lw_hatch=0.55):
    """多边形轮廓 + 内部平行阴影线族（angle_deg 为线方向）。"""
    poly = Polygon(pts, closed=True, facecolor='none', edgecolor='k',
                   lw=lw_edge, zorder=3)
    ax.add_patch(poly)
    pts = np.asarray(pts, float)
    th = np.radians(angle_deg)
    d = np.array([np.cos(th), np.sin(th)])
    nrm = np.array([-np.sin(th), np.cos(th)])
    t = (pts - pts.mean(0)) @ nrm
    c = pts.mean(0) + (t.min() - spacing) * nrm
    L = np.linalg.norm(pts.max(0) - pts.min(0)) + 4 * spacing
    for tt in np.arange(t.min() - spacing, t.max() + spacing, spacing):
        p0 = c + tt * nrm - L / 2 * d
        ax.plot([p0[0], p0[0] + L * d[0]], [p0[1], p0[1] + L * d[1]],
                color='k', lw=lw_hatch, zorder=2,
                clip_path=poly)


# ----------------------------------------------------------------------
# 图34/35 通用元件：竖直对称面（"书页"六边形）、轴端标记、水平二阶轴
# ----------------------------------------------------------------------
def page_plane(ax, alpha_deg, zt, zb, W=76.0, K=50.0, lw=1.15):
    """过竖直轴的对称面示意（书页形）：方位角 alpha（右半方向）。
    A=(0,zt) 与 D=(0,zb) 为全体页面共用的轴上、下端点。"""
    a = np.radians(alpha_deg)
    dx, dz = W * np.cos(a), K * np.sin(a)
    pts = [(0, zt), (dx, zt + dz), (dx, zb + dz), (0, zb),
           (-dx, zb - dz), (-dx, zt - dz)]
    ax.add_patch(Polygon(pts, closed=True, facecolor='none',
                         edgecolor='k', lw=lw, zorder=2))


def tri_marker(ax, x, y, s=9.0, h=13.0):
    """实心向下三角形（3阶轴标记）。(x,y) 为上边中点。"""
    ax.add_patch(Polygon([(x - s, y), (x + s, y), (x, y - h)],
                         closed=True, facecolor='k', edgecolor='k',
                         zorder=6))


def sq_marker(ax, x, y, s=5.2, ang=28.0):
    """实心斜置方块（4阶/旋转反射轴标记）。(x,y) 为中心。"""
    a = np.radians(ang)
    R = np.array([[np.cos(a), -np.sin(a)], [np.sin(a), np.cos(a)]])
    base = np.array([(-s, -s), (s, -s), (s, s), (-s, s)]) @ R.T
    ax.add_patch(Polygon(base + [x, y], closed=True, facecolor='k',
                         edgecolor='k', zorder=6))


def c2_axes(ax, angles_len, y0=0.0, dot=2.6):
    """过中心的水平二阶轴（两端画端点圆点）。angles_len: [(角度,长度)...]"""
    for ang, L in angles_len:
        t = np.radians(ang)
        dx, dy = L * np.cos(t), L * np.sin(t)
        ax.plot([-dx, dx], [y0 - dy, y0 + dy], color='k', lw=LW_MAIN,
                zorder=4)
        ax.plot([-dx, dx], [y0 - dy, y0 + dy], 'o', ms=4.6, mfc='k',
                mec='k', zorder=5)


# =====================================================================
# 图 32  旋转-反射轴
# =====================================================================
def fig_32():
    fig, ax = plt.subplots(figsize=(3.4, 3.15))
    bare_axis(ax, (-190, 195), (-192, 162))
    # 水平反射面（平行四边形，透视）
    plane = [(-166, -46), (-49, 41.4), (170, 41.4), (50, -46)]
    ax.add_patch(Polygon(plane, closed=True, facecolor='none',
                         edgecolor='k', lw=LW_MAIN, zorder=2))
    # 竖直转轴（被平面遮住中段：分两段画）
    ax.plot([0, 0], [148.6, 41.4], color='k', lw=LW_MAIN, zorder=1)
    ax.plot([0, 0], [-45.7, -157.7], color='k', lw=LW_MAIN, zorder=1)
    # 顶部：轴上 J1 点，水平实线到 P；虚线转过 2π/n 到 Q
    J1 = (0, 114.3)
    ax.plot([J1[0], 108.6], [J1[1], 114.3], color='k', lw=LW_MAIN,
            zorder=4)
    ax.plot([J1[0], 77.1], [J1[1], 67.1], color='k', lw=LW_AUX,
            ls=DASH, zorder=3)
    arc(ax, J1, 26, -31.5, 0)
    ax.text(60, 96, r'$2\pi/n$', fontsize=10)
    # P 点（小圆圈）
    open_circle(ax, 108.6, 114.3)
    ax.text(117, 111, r'$P$', fontsize=11)
    # Q 竖直虚线下行，穿过平面上的 O 直到 P'
    ax.plot([77.1, 77.1], [67.1, -168.6], color='k', lw=LW_AUX,
            ls=DASH, zorder=3)
    open_circle(ax, 77.1, -4.3)
    ax.text(58, -7, r'$O$', fontsize=11)
    # 底部：轴上点到 P' 的实线（反射后的像）
    ax.plot([0.9, 77.9], [-114.3, -168.6], color='k', lw=LW_MAIN,
            zorder=4)
    open_circle(ax, 77.9, -168.6)
    ax.text(88, -172, r"$P'$", fontsize=11)
    save(fig, 32)


# =====================================================================
# 图 33  两个 π 转轴 Oa、Ob 相乘给出垂直轴 PP'
# =====================================================================
def fig_33():
    fig, ax = plt.subplots(figsize=(3.2, 2.6))
    bare_axis(ax, (-140, 148), (-108, 114))
    # 水平面
    plane = [(-128, -36), (-35, 41), (128, 41), (33, -36)]
    ax.add_patch(Polygon(plane, closed=True, facecolor='none',
                         edgecolor='k', lw=LW_MAIN, zorder=2))
    # 竖直轴 PP'：面外实线、面内虚线
    ax.plot([0, 0], [101.7, 41], color='k', lw=LW_MAIN, zorder=1)
    ax.plot([0, 0], [41, -36], color='k', lw=LW_AUX, ls=DASH, zorder=1)
    ax.plot([0, 0], [-36, -96.7], color='k', lw=LW_MAIN, zorder=1)
    open_circle(ax, 0, 101.7); ax.text(8, 104, r'$P$', fontsize=11)
    open_circle(ax, 0, -96.7); ax.text(8, -102, r"$P'$", fontsize=11)
    open_circle(ax, 0, 1);     ax.text(-19, -2, r'$O$', fontsize=11)
    # 面内三线：Oa（实）、Ob（实）、Oa'（虚，转过 2φ 后的位置）
    for ang, L, dashed in ((30, 47, True), (0, 50, False),
                           (-30, 38, False)):
        t = np.radians(ang)
        ax.plot([0, L * np.cos(t)], [1, 1 + L * np.sin(t)], color='k',
                lw=LW_MAIN, ls=DASH if dashed else '-', zorder=4)
    # 两个 phi 角弧
    arc(ax, (0, 1), 17, 0, 30)
    arc(ax, (0, 1), 17, -30, 0)
    ax.text(23, 9, r'$\varphi$', fontsize=10)
    ax.text(22, -11, r'$\varphi$', fontsize=10)
    ax.text(51, 31, r"$a'$", fontsize=11)
    ax.text(56, -1, r'$b$', fontsize=11)
    ax.text(40, -28, r'$a$', fontsize=11)
    save(fig, 33)


# =====================================================================
# 图 34  C3v, C4v, D3, D4
# =====================================================================
ZT, ZB = 66.0, -66.0    # 书页（竖直对称面）上下端点（轴上交点）
PW = 40.0               # 页面半宽


def _panel_label(ax, txt, y=-124):
    ax.text(0, y, txt, fontsize=11, ha='center')


def fig_34():
    fig, axs = plt.subplots(1, 4, figsize=(7.6, 2.7))
    for ax in axs:
        bare_axis(ax, (-88, 88), (-136, 106))

    # --- C3v：3 阶轴（三角标记）+ 3 张竖直对称面（2 张可见 + 1 张侧视）---
    ax = axs[0]
    page_plane(ax, 210, ZT, ZB, PW, 56)
    page_plane(ax, 330, ZT, ZB, PW, 56)
    ax.plot([0, 0], [ZT + 3, ZB - 3], color='k', lw=LW_MAIN, zorder=3)
    tri_marker(ax, 0, ZT + 16); tri_marker(ax, 0, ZB - 3)
    _panel_label(ax, r'$C_{3v}$')

    # --- C4v：4 阶轴（斜方块）+ 4 张竖直对称面（含正面矩形）---
    ax = axs[1]
    for al in (0, 45, 135):
        page_plane(ax, al, ZT, ZB, PW, 26)
    ax.plot([0, 0], [ZT + 4, ZB - 4], color='k', lw=LW_MAIN, zorder=3)
    sq_marker(ax, 0, ZT + 13); sq_marker(ax, 0, ZB - 13)
    _panel_label(ax, r'$C_{4v}$')

    # --- D3：3 阶轴 + 3 条水平二阶轴 ---
    ax = axs[2]
    ax.plot([0, 0], [ZT + 3, ZB - 3], color='k', lw=LW_MAIN, zorder=3)
    tri_marker(ax, 0, ZT + 16); tri_marker(ax, 0, ZB - 3)
    c2_axes(ax, [(0, 55), (31, 55), (-31, 55)])
    _panel_label(ax, r'$D_3$')

    # --- D4：4 阶轴 + 4 条水平二阶轴 ---
    ax = axs[3]
    ax.plot([0, 0], [ZT + 4, ZB - 4], color='k', lw=LW_MAIN, zorder=3)
    sq_marker(ax, 0, ZT + 13); sq_marker(ax, 0, ZB - 13)
    c2_axes(ax, [(0, 60), (19, 60), (-19, 60), (82, 64)])
    _panel_label(ax, r'$D_4$')
    save(fig, 34)


# =====================================================================
# 图 35  D3h, D2d, D3d
# =====================================================================
def fig_35():
    fig, axs = plt.subplots(1, 3, figsize=(5.7, 2.7))
    for ax in axs:
        bare_axis(ax, (-88, 88), (-136, 106))

    # --- D3h：3 阶轴 + 3 竖直面 + 水平对称面 + 3 条水平二阶轴 ---
    ax = axs[0]
    page_plane(ax, 210, ZT, ZB, PW, 56)
    page_plane(ax, 330, ZT, ZB, PW, 56)
    ax.add_patch(Polygon([(42, 0), (0, 13), (-42, 0), (0, -13)],
                         closed=True, facecolor='none', edgecolor='k',
                         lw=LW_MAIN, zorder=3))
    ax.plot([0, 0], [ZT + 3, ZB - 3], color='k', lw=LW_MAIN, zorder=4)
    tri_marker(ax, 0, ZT + 16); tri_marker(ax, 0, ZB - 3)
    c2_axes(ax, [(0, 55), (31, 55), (-31, 55)])
    _panel_label(ax, r'$D_{3h}$')

    # --- D2d：4阶旋转反射轴（斜方块）+ 2 竖直面 + 2 条水平二阶轴 ---
    ax = axs[1]
    page_plane(ax, 45, ZT, ZB, PW, 40)
    page_plane(ax, 135, ZT, ZB, PW, 40)
    ax.plot([0, 0], [ZT + 4, ZB - 4], color='k', lw=LW_MAIN, zorder=3)
    sq_marker(ax, 0, ZT + 13); sq_marker(ax, 0, ZB - 13)
    c2_axes(ax, [(-24, 50), (46, 50)])
    _panel_label(ax, r'$D_{2d}$')

    # --- D3d：6阶旋转反射轴（斜方块）+ 3 竖直面 + 3 条水平二阶轴 ---
    ax = axs[2]
    page_plane(ax, 210, ZT, ZB, PW, 56)
    page_plane(ax, 330, ZT, ZB, PW, 56)
    ax.plot([0, 0], [ZT + 4, ZB - 4], color='k', lw=LW_MAIN, zorder=3)
    sq_marker(ax, 0, ZT + 13); sq_marker(ax, 0, ZB - 13)
    c2_axes(ax, [(30, 58), (17, 52), (78, 88)])
    _panel_label(ax, r'$D_{3d}$')
    save(fig, 35)


# =====================================================================
# 图 36–40 公用：立方体投影（斜二测：深度方向右上）
# ----------------------------------------------------------------------
def cube_project(p, dx=0.45, dy=0.38):
    x, y, z = p
    return (x + dx * y, z + dy * y)


def draw_cube(ax, lw=0.9):
    """12 条棱全部虚线。"""
    C = {}
    for x in (0, 1):
        for y in (0, 1):
            for z in (0, 1):
                C[(x, y, z)] = cube_project((x, y, z))
    edges = []
    for x in (0, 1):
        for y in (0, 1):
            edges.append(((x, y, 0), (x, y, 1)))   # 竖棱
    for x in (0, 1):
        for z in (0, 1):
            edges.append(((x, 0, z), (x, 1, z)))
    for y in (0, 1):
        for z in (0, 1):
            edges.append(((0, y, z), (1, y, z)))
    for a, b in edges:
        pa, pb = C[a], C[b]
        ax.plot([pa[0], pb[0]], [pa[1], pb[1]], color='k', lw=lw,
                ls=DASH, zorder=1)
    return C


# =====================================================================
# 图 36  T 群：四面体（C3, C2）+ 立方体（C3, C2）
# =====================================================================
def fig_36():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(4.0, 2.25))
    bare_axis(ax1, (-1.55, 1.25), (-1.32, 1.42))
    bare_axis(ax2, (-0.25, 1.85), (-0.28, 1.62))

    # --- (a) 四面体：C3 过顶点垂直对面，C2 过对边中点 ---
    T = (0.0, 1.02); Bt = (-0.08, -0.98)
    L = (-1.22, -0.12); R = (1.02, 0.08)
    verts = [T, Bt, L, R]
    for i in range(4):
        for j in range(i + 1, 4):
            pa, pb = verts[i], verts[j]
            ax1.plot([pa[0], pb[0]], [pa[1], pb[1]], color='k',
                     lw=0.9, ls=DASH, zorder=1)
    # C3：顶点到对面重心
    cen = ((Bt[0] + L[0] + R[0]) / 3, (Bt[1] + L[1] + R[1]) / 3)
    ax1.plot([T[0], cen[0]], [T[1], cen[1]], color='k', lw=LW_THICK,
             zorder=3)
    # C2：对边中点连线
    m1 = ((L[0] + Bt[0]) / 2, (L[1] + Bt[1]) / 2)
    m2 = ((T[0] + R[0]) / 2, (T[1] + R[1]) / 2)
    ax1.plot([m1[0], m2[0]], [m1[1], m2[1]], color='k', lw=LW_THICK,
             zorder=3)
    ax1.text(-1.08, 0.98, r'$\mathbf{T}$', fontsize=12)
    ax1.text(-0.09, 1.16, r'$C_3$', fontsize=11)
    ax1.text(0.56, 0.63, r'$C_2$', fontsize=11)

    # --- (b) 立方体：体对角线 C3 + 过面心竖直轴 C2 ---
    draw_cube(ax2)
    p0 = cube_project((0, 0, 1)); p1 = cube_project((1, 1, 0))
    ax2.plot([p0[0], p1[0]], [p0[1], p1[1]], color='k', lw=LW_THICK,
             zorder=3)
    q0 = cube_project((0.5, 0.5, 0)); q1 = cube_project((0.5, 0.5, 1))
    ax2.plot([q0[0], q1[0]], [q0[1], q1[1]], color='k', lw=LW_THICK,
             zorder=3)
    ax2.text(-0.18, 1.08, r'$C_3$', fontsize=11)
    ax2.text(0.80, 1.26, r'$C_2$', fontsize=11)
    save(fig, 36)


# =====================================================================
# 图 37  Td 群：立方体（C3, S4, σ）+ 四面体（C3, S4, σ）
# =====================================================================
def fig_37():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(4.0, 2.5))
    bare_axis(ax1, (-0.30, 2.05), (-0.22, 1.62))
    bare_axis(ax2, (-1.42, 1.68), (-1.80, 1.60))

    # --- (a) 立方体：斜对称面 σ（过一对竖直棱）+ S4（面心竖直轴，在面内）
    #         + 体对角线 C3（面的对角线）---
    draw_cube(ax1)
    sq = [cube_project((0, 0, 0)), cube_project((0, 0, 1)),
          cube_project((1, 1, 1)), cube_project((1, 1, 0))]
    hatch_polygon(ax1, sq, 90, spacing=0.055, lw_edge=1.5)
    q0 = cube_project((0.5, 0.5, 0)); q1 = cube_project((0.5, 0.5, 1))
    ax1.plot([q0[0], q1[0]], [q0[1], q1[1]], color='k', lw=LW_THICK,
             zorder=4)
    d0 = cube_project((0, 0, 1)); d1 = cube_project((1, 1, 0))
    ax1.plot([d0[0], d1[0]], [d0[1], d1[1]], color='k', lw=LW_THICK,
             zorder=4)
    ax1.text(-0.26, 1.10, r'$C_3$', fontsize=11)
    ax1.text(0.62, 1.30, r'$S_4$', fontsize=11)
    ax1.text(1.58, 0.62, r'$\sigma$', fontsize=12)

    # --- (b) 四面体：正面阴影 σ，C3 顶点到对面重心，S4 竖直虚线 ---
    A = (0.0, 1.25); BLF = (-0.55, -1.15); R = (1.0, -0.55)
    Bk = (-1.02, -0.88)
    for P, Q in ((A, Bk), (Bk, BLF), (Bk, R)):
        ax2.plot([P[0], Q[0]], [P[1], Q[1]], color='k', lw=0.9,
                 ls=DASH, zorder=1)
    for P, Q in ((A, BLF), (A, R), (BLF, R)):
        ax2.plot([P[0], Q[0]], [P[1], Q[1]], color='k', lw=LW_MAIN,
                 zorder=2)
    hatch_polygon(ax2, [A, BLF, R], 55, spacing=0.075, lw_edge=0.0,
                  lw_hatch=0.6)
    cen = ((BLF[0] + R[0] + Bk[0]) / 3, (BLF[1] + R[1] + Bk[1]) / 3)
    ax2.plot([A[0], cen[0]], [A[1], cen[1]], color='k', lw=LW_THICK,
             zorder=4)
    ax2.plot([0.25, 0.25], [0.80, -1.48], color='k', lw=LW_AUX,
             ls=DASH, zorder=3)
    ax2.text(-0.06, 1.40, r'$C_3$', fontsize=11)
    ax2.text(1.16, 1.10, r'$\mathbf{T}_d$', fontsize=12)
    ax2.text(1.10, -0.38, r'$\sigma$', fontsize=12)
    ax2.text(-0.06, -1.66, r'$S_4$', fontsize=11)
    save(fig, 37)


# =====================================================================
# 图 38  Th 群：C2（面心竖直轴）+ S6（体对角线）+ σ（过一对 C2 的面）
# =====================================================================
def fig_38():
    fig, ax = plt.subplots(figsize=(2.75, 2.6))
    bare_axis(ax, (-0.42, 2.05), (-0.42, 1.80))
    draw_cube(ax)
    # σ：面平行中截面（x=0.5），含竖直 C2 与深度方向 C2
    sq = [cube_project((0.5, 0, 0)), cube_project((0.5, 1, 0)),
          cube_project((0.5, 1, 1)), cube_project((0.5, 0, 1))]
    hatch_polygon(ax, sq, 65, spacing=0.055, lw_edge=1.1)
    q0 = cube_project((0.5, 0.5, 0)); q1 = cube_project((0.5, 0.5, 1))
    ax.plot([q0[0], q1[0]], [q0[1], q1[1]], color='k', lw=LW_THICK,
            zorder=4)
    d0 = cube_project((0, 0, 0)); d1 = cube_project((1, 1, 1))
    ax.plot([d0[0], d1[0]], [d0[1], d1[1]], color='k', lw=LW_THICK,
            zorder=4)
    ax.text(0.22, 1.46, r'$C_2$', fontsize=11)
    ax.text(1.10, 1.16, r'$\sigma$', fontsize=12)
    ax.text(1.56, 1.24, r'$S_6$', fontsize=11)
    ax.text(0.52, -0.34, r'$\mathbf{T}_h$', fontsize=12)
    save(fig, 38)


# =====================================================================
# 图 39  O 群：C4（面心）+ C3（体对角线）+ C2（对棱中点）
# =====================================================================
def fig_39():
    fig, ax = plt.subplots(figsize=(2.65, 2.7))
    bare_axis(ax, (-0.30, 1.90), (-0.40, 1.72))
    draw_cube(ax)
    d0 = cube_project((0, 0, 1)); d1 = cube_project((1, 1, 0))
    ax.plot([d0[0], d1[0]], [d0[1], d1[1]], color='k', lw=LW_THICK,
            zorder=3)
    q0 = cube_project((0.5, 0.5, 0)); q1 = cube_project((0.5, 0.5, 1))
    ax.plot([q0[0], q1[0]], [q0[1], q1[1]], color='k', lw=LW_THICK,
            zorder=3)
    e0 = cube_project((0, 1, 0.5)); e1 = cube_project((1, 0, 0.5))
    ax.plot([e0[0], e1[0]], [e0[1], e1[1]], color='k', lw=LW_THICK,
            zorder=3)
    ax.text(-0.22, 1.08, r'$C_3$', fontsize=11)
    ax.text(0.80, 1.30, r'$C_4$', fontsize=11)
    ax.text(1.12, 0.40, r'$C_2$', fontsize=11)
    ax.text(0.32, -0.30, r'$\mathbf{O}$', fontsize=12)
    save(fig, 39)


# =====================================================================
# 图 40  Oh 群：C4 + S6 + C2 + 水平面 σ + 竖直斜面 σ
# =====================================================================
def fig_40():
    fig, ax = plt.subplots(figsize=(2.65, 2.55))
    bare_axis(ax, (-0.42, 2.0), (-0.42, 1.72))
    draw_cube(ax)
    # σh：水平中截面（横线阴影）
    sh = [cube_project((0, 0, 0.5)), cube_project((1, 0, 0.5)),
          cube_project((1, 1, 0.5)), cube_project((0, 1, 0.5))]
    hatch_polygon(ax, sh, 0, spacing=0.05, lw_edge=1.0)
    # σv：过一对竖直棱的斜面（竖线阴影），含 C4、C2、S6
    sv = [cube_project((0, 0, 0)), cube_project((0, 0, 1)),
          cube_project((1, 1, 1)), cube_project((1, 1, 0))]
    hatch_polygon(ax, sv, 90, spacing=0.05, lw_edge=1.0)
    # C4：面心竖直轴（即 σv 的竖直中线）
    q0 = cube_project((0.5, 0.5, 0)); q1 = cube_project((0.5, 0.5, 1))
    ax.plot([q0[0], q1[0]], [q0[1], q1[1]], color='k', lw=LW_THICK,
            zorder=4)
    # S6：体对角线（σv 的对角线）
    d0 = cube_project((0, 0, 0)); d1 = cube_project((1, 1, 1))
    ax.plot([d0[0], d1[0]], [d0[1], d1[1]], color='k', lw=LW_THICK,
            zorder=4)
    # C2：水平二阶轴（垂直于 σv 面的那条，原书图画法）
    e0 = cube_project((0, 1, 0.5)); e1 = cube_project((1, 0, 0.5))
    ax.plot([e0[0], e1[0]], [e0[1], e1[1]], color='k', lw=LW_THICK,
            zorder=4)
    ax.text(-0.22, 1.13, r'$\sigma$', fontsize=12)
    ax.text(-0.34, 0.58, r'$\sigma$', fontsize=12)
    ax.text(0.82, 1.28, r'$C_4$', fontsize=11)
    ax.text(1.56, 1.22, r'$S_6$', fontsize=11)
    ax.text(0.98, 0.33, r'$C_2$', fontsize=11)
    ax.text(0.36, -0.32, r'$\mathbf{O}_h$', fontsize=12)
    save(fig, 40)


if __name__ == '__main__':
    for f in (fig_32, fig_33, fig_34, fig_35, fig_36, fig_37,
              fig_38, fig_39, fig_40):
        f()
