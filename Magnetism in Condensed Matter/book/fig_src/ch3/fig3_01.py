# -*- coding: utf-8 -*-
# 图 3.1 s/p/d 轨道的角分布（球谐函数模长着色的 3D 曲面，正负瓣深浅区分）
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from mplstyle import save_fig

plt.rcParams.update({'font.size': 11, 'mathtext.fontset': 'stix'})

C_POS = '#c9c9c9'   # 正瓣浅灰
C_NEG = '#5f5f5f'   # 负瓣深灰
C_S   = '#bfbfbf'

th = np.linspace(0, np.pi, 61)
ph = np.linspace(0, 2*np.pi, 81)
TH, PH = np.meshgrid(th, ph)
ST, CT = np.sin(TH), np.cos(TH)
CP, SP = np.cos(PH), np.sin(PH)


def orb_axes(ax):
    """小坐标轴：z 上、y 右、x 左下（默认视角自带）"""
    L = 1.38
    for (dx, dy, dz) in [(0, 0, L), (0, L, 0), (L, 0, 0)]:
        q = ax.quiver(0, 0, 0, dx, dy, dz, arrow_length_ratio=0.07,
                  linewidth=0.9, color='k')
    q.set_zorder(1e3)
    ax.text(0, 0, L + 0.18, '$z$', fontsize=9, ha='center', va='bottom', zorder=1e3)
    ax.text(0, L + 0.16, 0, '$y$', fontsize=9, ha='left', va='center', zorder=1e3)
    ax.text(L + 0.22, 0, 0, '$x$', fontsize=9, ha='left', va='top', zorder=1e3)


def draw_orb(ax, Y, name):
    R = np.abs(Y)
    R /= R.max()
    X, Yc, Z = R * ST * CP, R * ST * SP, R * CT
    pos = np.where(Y >= 0, Z, np.nan)
    neg = np.where(Y < 0, Z, np.nan)
    for ZZ, cc in [(pos, C_POS), (neg, C_NEG)]:
        if np.isfinite(ZZ).any():
            ax.plot_surface(X, Yc, ZZ, rcount=60, ccount=60, color=cc,
                            shade=True, linewidth=0, antialiased=True)
    ax.plot_wireframe(X, Yc, Z, rstride=6, cstride=6,
                      color='0.93', linewidth=0.15)
    orb_axes(ax)
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5); ax.set_zlim(-1.5, 1.5)
    ax.set_box_aspect((1, 1, 1))
    ax.set_axis_off()
    ax.patch.set_alpha(0.0)
    ax.view_init(elev=18, azim=30)
    ax.text2D(0.5, -0.04, name, transform=ax.transAxes,
              ha='center', va='top', fontsize=14)


fig = plt.figure(figsize=(6.6, 7.4))
gs = GridSpec(4, 6, figure=fig,
              left=-0.06, right=0.84, top=0.99, bottom=0.055,
              wspace=0.0, hspace=0.30)

# 第一行：s（球面）
ax = fig.add_subplot(gs[0, 2:4], projection='3d')
try:
    ax.computed_zorder = False
except AttributeError:
    pass
X, Yc, Z = ST * CP, ST * SP, CT
ax.plot_surface(X, Yc, Z, rcount=50, ccount=50, color=C_S,
                shade=True, linewidth=0, antialiased=True)
ax.plot_wireframe(X, Yc, Z, rstride=6, cstride=6, color='0.93', linewidth=0.15)
orb_axes(ax)
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5); ax.set_zlim(-1.5, 1.5)
ax.set_box_aspect((1, 1, 1)); ax.set_axis_off(); ax.view_init(18, 30)
ax.patch.set_alpha(0.0)
ax.text2D(0.5, -0.04, '$s$', transform=ax.transAxes, ha='center', va='top', fontsize=14)

# 第二行：p 轨道
prow = [(lambda: np.sin(TH) * CP, '$p_x$', 0), (lambda: np.sin(TH) * SP, '$p_y$', 2),
        (lambda: CT, '$p_z$', 4)]
for fn, name, c0 in prow:
    ax = fig.add_subplot(gs[1, c0:c0 + 2], projection='3d')
    try:
        ax.computed_zorder = False
    except AttributeError:
        pass
    draw_orb(ax, fn(), name)

# 第三行：d_z2, d_x2-y2（e_g）
eg_row = []
for fn, name, c0 in [(lambda: 3 * CT**2 - 1, '$d_{z^2}$', 0),
                     (lambda: ST**2 * np.cos(2 * PH), '$d_{x^2-y^2}$', 2)]:
    ax = fig.add_subplot(gs[2, c0:c0 + 2], projection='3d')
    try:
        ax.computed_zorder = False
    except AttributeError:
        pass
    draw_orb(ax, fn(), name)
    eg_row.append(ax)

# 第四行：d_xy, d_xz, d_yz（t_2g）
t2g_row = []
for fn, name, c0 in [(lambda: ST**2 * np.sin(2 * PH), '$d_{xy}$', 0),
                     (lambda: ST * CT * CP, '$d_{xz}$', 2),
                     (lambda: ST * CT * SP, '$d_{yz}$', 4)]:
    ax = fig.add_subplot(gs[3, c0:c0 + 2], projection='3d')
    try:
        ax.computed_zorder = False
    except AttributeError:
        pass
    draw_orb(ax, fn(), name)
    t2g_row.append(ax)

# 右侧花括号与简并标记
fig.canvas.draw()
def brace(axs, ylab):
    p0, p1 = axs[0].get_position(), axs[-1].get_position()
    yc = 0.5 * (min(p0.y0, p1.y0) + max(p0.y1, p1.y1))
    fig.text(0.845, yc, '}', fontsize=80, ha='center', va='center')
    fig.text(0.888, yc, ylab, fontsize=16, ha='left', va='center')

brace(eg_row, '$e_g$')
brace(t2g_row, '$t_{2g}$')

save_fig(fig, 'ch3', 'fig3_01')
