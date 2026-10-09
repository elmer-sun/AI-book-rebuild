# -*- coding: utf-8 -*-
"""Redraw chapter-1 figures (Chinese edition) in black-white textbook style.
Fallback (original scan) is used only for Fig 1.4 (32-stereogram grid)."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mp
import numpy as np
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures')
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({'font.family': ['Times New Roman', 'SimSun'],
                     'mathtext.fontset': 'cm', 'axes.unicode_minus': False})
K = 'k'

def lens(ax, x, y, w=0.09, h=0.035, ang=0):
    ax.add_patch(mp.Ellipse((x, y), w, h, angle=ang, fc=K, ec=K, zorder=5))

def dot(ax, x, y, s=22):
    ax.plot([x], [y], 'o', ms=3.4, mfc=K, mec=K, zorder=5)

def arrow(ax, x0, y0, x1, y1, label=None, lx=0, ly=0):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color=K, lw=0.9, mutation_scale=11))
    if label:
        ax.text(x1 + lx, y1 + ly, label, fontsize=11, style='italic', ha='center', va='center')

def circle_frame(ax, R=1.0):
    ax.add_patch(mp.Circle((0, 0), R, fc='none', ec=K, lw=1.0, zorder=2))

def new_ax(w=4.6, h=4.6):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_aspect('equal'); ax.axis('off')
    return fig, ax

# ---------- Fig 1.1 : triclinic/monoclinic/orthorhombic/tetragonal stereogram ----------
fig, ax = new_ax()
R = 1.0
circle_frame(ax)
# axes
arrow(ax, 0, 0, 0, R + 0.28, 'x', 0.10, 0.02)
arrow(ax, 0, 0, R + 0.28, 0, 'y', 0.06, -0.11)
# centre 4-fold axis (square)
ax.add_patch(mp.Rectangle((-0.045, -0.045), 0.09, 0.09, fc=K, ec=K, zorder=6))
# rim lenses + spokes (labels placed where E is taken by the operation)
pos = [(0, R, 'E', '$C_{2x}\\;E$', 0.13, 0.0, '$C_{4x}^{+}$', '$C_{2a}$', 0, 0),
       ]
# top lens
lens(ax, 0, R, w=0.11, h=0.05)
ax.text(-0.30, R + 0.02, '$C_{2x}$', fontsize=11)
ax.text(0.14, R + 0.02, '$E$', fontsize=11)
# bottom lens
lens(ax, 0, -R, w=0.11, h=0.05)
ax.text(-0.34, -R - 0.04, '$C_{2z}$', fontsize=11)
ax.text(0.16, -R - 0.04, '$C_{21}$', fontsize=11)
# left lens (on y axis)
lens(ax, -R, 0, w=0.05, h=0.11)
ax.text(-R - 0.36, 0.09, '$C_{4y}^{+}$', fontsize=11)
ax.text(-R - 0.33, -0.10, '$C_{2a}$', fontsize=11)
# right lens
lens(ax, R, 0, w=0.05, h=0.11)
ax.text(R + 0.10, 0.09, '$C_{2b}$', fontsize=11)
ax.text(R + 0.08, -0.10, '$C_{4y}^{-}$', fontsize=11)
# diagonal lenses a/b/b/a
d = R / np.sqrt(2)
for (sx, sy, lab) in [(1, 1, 'b'), (-1, 1, 'a'), (-1, -1, 'b'), (1, -1, 'a')]:
    lens(ax, sx * d, sy * d, w=0.10, h=0.045, ang=np.degrees(np.arctan2(sy, sx)))
    ax.plot([0, sx * d * 0.94], [0, sy * d * 0.94], color=K, lw=0.7, zorder=1)
    ax.text(sx * (d + 0.13), sy * (d + 0.13), lab, fontsize=11, style='italic')
ax.plot([0, 0], [0, d * 0.94], color=K, lw=0.0)
ax.set_xlim(-1.55, 1.55); ax.set_ylim(-1.45, 1.45)
fig.savefig(os.path.join(OUT, 'fig1_1.png'), dpi=300, bbox_inches='tight')
plt.close(fig)

# ---------- Fig 1.2 : trigonal/hexagonal stereogram ----------
fig, ax = new_ax(5.0, 5.0)
R = 1.0
circle_frame(ax)
# centre hexagon (6-fold axis)
th = np.linspace(0, 2 * np.pi, 7)
ax.add_patch(mp.Polygon(0.085 * np.c_[np.cos(th), np.sin(th)], fc=K, ec=K, zorder=6))
# vertical axis up (z out of page not drawn), x to the left, y to lower-right
arrow(ax, 0, 0, -R - 0.30, 0, 'x', -0.10, 0.10)
arrow(ax, 0, 0, R * 0.62, -R * 0.80, 'y', 0.10, -0.06)
# 12 rim marks: lenses (2-fold) and dots (3-fold/6-fold poles)
marks = [
    (90,  'lens', "$C_{21}\\;E$", 0.18, 0.05, "1'", 0.0, 0.19),
    (60,  'dot',  "3''", 0.0, 0.0, None, 0, 0),
    (30,  'lens', "$C_{23}''$", -0.02, 0.17, "2'", 0.17, -0.02),
    (0,   'dot',  "1''", 0.14, 0.0, None, 0, 0),
    (-30, 'lens', "$C_{21}''$", 0.20, 0.02, "2''", 0.14, -0.10),
    (-60, 'dot',  "3'", 0.14, -0.06, None, 0, 0),
    (-90, 'lens', "$C_{2z}\\;C_{21}''$", -0.28, -0.05, "1'", 0.0, -0.21),
    (-120,'dot',  "3''", -0.16, -0.05, None, 0, 0),
    (-150,'lens', "$C_{23}'''$", 0.0, 0.17, "2'", -0.18, -0.03),
    (180, 'dot',  "1''", 0.0, 0.0, None, 0, 0),
    (150, 'lens', "$C_{6}^{+}$", 0.16, 0.05, "3'", -0.20, 0.03),
    (120, 'dot',  "3''", 0.0, 0.0, None, 0, 0),
]
for angd, kind, lab, lx, ly, pol, px, py in marks:
    a = np.radians(angd)
    x, y = R * np.cos(a), R * np.sin(a)
    if kind == 'lens':
        lens(ax, x, y, w=0.10, h=0.045, ang=angd + 90)
        ax.plot([0, x * 0.93], [0, y * 0.93], color=K, lw=0.7, zorder=1)
        ax.text(x + lx - 0.0, y + ly, lab, fontsize=10.5, ha='center')
    else:
        dot(ax, x, y)
        ax.text(x + (0.10 if x >= 0 else -0.10), y + 0.05, pol if pol else lab,
                fontsize=10.5, ha='center')
# C6+/C6- and C3+/C3- labels near upper-left rim (per original)
ax.text(-0.86, 0.42, '$C_{6}^{+}$', fontsize=10.5)
ax.text(-0.88, 0.28, '$C_{6}^{-}$', fontsize=10.5)
ax.text(-0.62, -0.62, '$C_{3}^{+}$', fontsize=10.5)
ax.text(-0.44, -0.74, "$C_{3}^{-}$", fontsize=10.5)
ax.text(0.60, -0.66, "$C_{22}''$", fontsize=10.5)
ax.set_xlim(-1.55, 1.55); ax.set_ylim(-1.45, 1.45)
fig.savefig(os.path.join(OUT, 'fig1_2.png'), dpi=300, bbox_inches='tight')
plt.close(fig)

# ---------- Fig 1.5 : stereogram showing C4z+ then C2x acting on point A ----------
fig, ax = new_ax(4.8, 5.4)
R = 1.0
circle_frame(ax)
ax.plot([0, 0], [R, -R - 0.25], color=K, lw=0.9)
arrow(ax, 0, -R - 0.05, 0, -R - 0.30, 'x', 0.0, -0.13)
arrow(ax, 0, 0, R + 0.30, 0, 'y', 0.05, -0.12)
dot(ax, 0.13, 0.72); ax.text(0.20, 0.66, '$A$', fontsize=12)
dot(ax, -0.52, 0.06); ax.text(-0.47, 0.13, '$B$', fontsize=12)
ax.plot([0.62], [0.0], 'o', ms=5.5, mfc='none', mec=K)
ax.text(0.58, 0.09, '$C$', fontsize=12)
ax.text(-0.10, -R - 0.52, '', fontsize=10)
fig.savefig(os.path.join(OUT, 'fig1_5.png'), dpi=300, bbox_inches='tight')
plt.close(fig)

# ---------- Fig 1.6 : square 2-d Bravais lattice ----------
fig, ax = plt.subplots(figsize=(5.6, 4.4))
ax.set_aspect('equal'); ax.axis('off')
for iy in range(5):
    for ix in range(7):
        ax.plot([ix], [iy], 'o', ms=3.2, mfc=K, mec=K)
ax.set_xlim(-0.5, 6.5); ax.set_ylim(-0.5, 4.5)
fig.savefig(os.path.join(OUT, 'fig1_6.png'), dpi=300, bbox_inches='tight')
plt.close(fig)

# ---------- Fig 1.8 : (a) rectangular p  (b) centred rectangular c ----------
fig, axes = plt.subplots(2, 1, figsize=(5.6, 6.8))
ax = axes[0]; ax.set_aspect('equal'); ax.axis('off')
xs, ys = range(4), range(5)
for iy in ys:
    for ix in xs:
        ax.plot([ix * 1.4], [iy], 'o', ms=3.4, mfc=K, mec=K)
ax.add_patch(mp.Rectangle((0, 1), 1.4, 1, fc='none', ec=K, lw=1.0, ls='--'))
ax.text(2.1 + 0.25, -0.75, '(a)', fontsize=12)
ax = axes[1]; ax.set_aspect('equal'); ax.axis('off')
for iy in range(6):
    off = 0.7 if iy % 2 else 0.0
    for ix in range(4):
        ax.plot([ix * 1.4 + off], [iy * 0.5], 'o', ms=3.4, mfc=K, mec=K)
ax.add_patch(mp.Rectangle((0, 0.5), 1.4, 1.0, fc='none', ec=K, lw=1.0, ls='--'))
ax.plot([0, 1.4, 1.4, 0, 0], [0.5, 1.5, 0.5, 1.5, 0.5], color=K, lw=1.0)
ax.text(2.1 + 0.25, -0.45, '(b)', fontsize=12)
for ax in axes:
    ax.set_xlim(-0.6, 4.8); ax.set_ylim(-0.9, 4.4)
fig.savefig(os.path.join(OUT, 'fig1_8.png'), dpi=300, bbox_inches='tight')
plt.close(fig)

print('done:', sorted(os.listdir(OUT)))
