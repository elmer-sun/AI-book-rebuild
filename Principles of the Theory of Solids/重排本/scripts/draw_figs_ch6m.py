# -*- coding: utf-8 -*-
"""Redraw Ziman, Principles of the Theory of Solids, 2nd ed., Figs. 102-108
(Sec. 6.6, The mass tensor: electrons and holes).  Black-and-white textbook
style vector figures.  Fig. 108 actually sits on book page 187 (p201)."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Circle, Wedge, FancyBboxPatch, Polygon, PathPatch, Rectangle
from matplotlib.path import Path
from matplotlib.collections import LineCollection

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
    'hatch.linewidth': 0.7,
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, 'figures')
PREVDIR = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVDIR, exist_ok=True)

ARROW = dict(arrowstyle='-|>', color='k', lw=1.1, mutation_scale=11,
             shrinkA=0, shrinkB=0)


def _save(fig, key):
    fig.savefig(os.path.join(FIGDIR, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREVDIR, 'fig_%s.png' % key),
                bbox_inches='tight', pad_inches=0.03, dpi=170)
    plt.close(fig)
    print('saved fig_%s' % key)


def _arrow(ax, p0, p1, lw=1.1, scale=11):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                mutation_scale=scale, shrinkA=0, shrinkB=0))


# ---------------------------------------------------------------- fig. 102
def fig_102():
    """Mass is large 'along the valley': nested elliptical energy contours."""
    fig, ax = plt.subplots(figsize=(4.0, 2.0))
    for w, h in [(5.8, 2.06), (4.0, 1.42), (1.9, 0.68)]:
        ax.add_patch(Ellipse((0, 0), w, h, fill=False, lw=1.4))
    ax.plot([0], [0], 'k.', ms=4.5)
    # horizontal axis k1
    ax.plot([-3.3, 3.30], [0, 0], 'k-', lw=1.0)
    _arrow(ax, (3.30, 0), (3.62, 0), lw=1.0)
    ax.text(3.28, -0.30, r'$k_1$', ha='center', va='center')
    # vertical axis k2, k3
    ax.plot([0, 0], [-1.30, 1.28], 'k-', lw=1.0)
    _arrow(ax, (0, 1.28), (0, 1.56), lw=1.0)
    ax.text(0.14, 1.48, r'$k_2, k_3$', ha='left', va='center')
    ax.text(0.08, -0.32, r'$k_0$', ha='left', va='center')
    ax.set_xlim(-3.75, 3.95)
    ax.set_ylim(-1.62, 1.80)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, 102)


# ---------------------------------------------------------------- fig. 103
def fig_103():
    """Hyperboloidal energy surface ('neck')."""
    fig, ax = plt.subplots(figsize=(4.5, 2.7))
    L, b, a, e = 3.30, 1.00, 0.33, 0.19
    x = np.linspace(-L, L, 300)
    r = np.sqrt(a**2 + (b**2 - a**2) * (x / L)**2)
    # cross-section rings
    for f in (0.16, 0.38, 0.62):
        for s in (-1, 1):
            xr = s * f * L
            rr = np.sqrt(a**2 + (b**2 - a**2) * f**2)
            ax.add_patch(Ellipse((xr, 0), 2 * e, 2 * rr, fill=False,
                                 lw=0.8))
    # silhouette (top and bottom)
    ax.plot(x, r, 'k-', lw=1.5)
    ax.plot(x, -r, 'k-', lw=1.5)
    # shading strokes on the flared left end
    seg = []
    for phi in np.arange(8, 353, 14):
        p0 = (-L + e * np.cos(np.radians(phi)), b * np.sin(np.radians(phi)))
        seg.append([p0, (p0[0] + 0.30, p0[1] * 0.965)])
    ax.add_collection(LineCollection(seg, colors='0.25', linewidths=0.6))
    # end ellipses
    ax.add_patch(Ellipse((-L, 0), 2 * e, 2 * b, fill=False, lw=1.6))
    ax.add_patch(Ellipse((L, 0), 2 * e, 2 * b, fill=False, lw=1.6))
    # axes through the waist
    ax.plot([0, 0], [0, 1.42], 'k-', lw=1.0)          # k1
    _arrow(ax, (0, 1.42), (0, 1.68), lw=1.0)
    ax.text(0.10, 1.58, r'$k_1$', ha='left', va='center')
    ax.plot([0, L - 0.10], [0, 0], 'k--', lw=1.0, dashes=(4, 3))   # k3
    ax.plot([L + e * 0.7, L + 0.55], [0, 0], 'k-', lw=1.0)
    _arrow(ax, (L + 0.55, 0), (L + 0.88, 0), lw=1.0)
    ax.text(L + 0.30, 0.13, r'$k_3$', ha='left', va='center')
    _arrow(ax, (0, 0), (-0.85, -0.76), lw=1.0)         # k2
    ax.text(-1.08, -0.66, r'$k_2$', ha='center', va='center')
    ax.set_xlim(-4.05, 4.55)
    ax.set_ylim(-1.55, 1.90)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, 103)


# ---------------------------------------------------------------- fig. 104
def fig_104():
    """A 'pocket of holes' at the top of a nearly-filled band."""
    fig, ax = plt.subplots(figsize=(3.2, 2.7))
    A, B, H = 1.00, 0.24, 0.62
    # stippled skirt below the base plane
    t = np.linspace(0, 1, 60)
    ob_x = (1 - t)**2 * (-1) + 2 * (1 - t) * t * 0 + t**2 * 1
    ob_y = (1 - t)**2 * 0 + 2 * (1 - t) * t * (-1.40) + t**2 * 0
    th = np.linspace(0, np.pi, 80)
    in_x, in_y = np.cos(th), -B * np.sin(th)
    verts = np.vstack([np.column_stack([ob_x, ob_y]),
                       np.column_stack([in_x[::-1], in_y[::-1]])])
    ax.add_patch(Polygon(verts, closed=True, facecolor='0.88',
                         edgecolor='none'))
    # dome silhouette
    td = np.linspace(0, np.pi, 120)
    ax.plot(np.cos(td) * A, np.sin(td) * H, 'k-', lw=1.5)
    # meridians on the dome
    for s in (-1, 1):
        tm = np.linspace(0, 1, 60)
        mx = (1 - tm)**2 * (s * 0.55) + 2 * (1 - tm) * tm * (s * 0.66) + tm**2 * 0
        my = (1 - tm)**2 * (-0.185) + 2 * (1 - tm) * tm * 0.33 + tm**2 * H
        ax.plot(mx, my, 'k-', lw=0.9)
    # hatched base disk
    ax.add_patch(Ellipse((0, 0), 2 * A, 2 * B, facecolor='white',
                         edgecolor='k', lw=1.4, hatch='///'))
    # vertical energy axis
    ax.plot([0, 0], [-0.62, 0.92], 'k-', lw=1.0)
    _arrow(ax, (0, 0.92), (0, 1.14), lw=1.0)
    ax.text(0.07, 1.08, r'$\mathcal{E}(\mathbf{k})$', ha='left', va='center')
    ax.text(0.08, 0.72, r'$k_0$', ha='left', va='center')
    # velocity vector tangent to the dome, upper-left flank
    ax.plot([-0.74], [0.42], 'k.', ms=4)
    _arrow(ax, (-0.74, 0.42), (-0.30, 0.74), lw=1.1)
    ax.text(-1.02, 0.52, r'$\mathbf{v}_k$', ha='center', va='center')
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-0.95, 1.42)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, 104)


# ---------------------------------------------------------------- fig. 105
def fig_105():
    """(a) gap in the electron distribution; (b) the 'hole', inverted scale."""
    fig, axes = plt.subplots(1, 2, figsize=(4.6, 2.7))
    plt.subplots_adjust(wspace=0.30, left=0.02, right=0.98,
                        bottom=0.04, top=0.98)
    # ---- (a)
    ax = axes[0]
    th = np.linspace(np.radians(172), np.radians(8), 150)
    ax.plot(np.cos(th), np.sin(th), 'k-', lw=1.6)
    ax.plot([0, 0], [-1.02, 1.14], 'k-', lw=1.0)
    _arrow(ax, (0, 0.18), (0, 0.50), lw=1.0)
    ax.text(0.07, 0.47, r'$\mathcal{E}(\mathbf{k})$', ha='left', va='center')
    _arrow(ax, (-0.71, 0.71), (-0.31, 1.06), lw=1.2)
    ax.text(-0.93, 0.93, r'$\mathbf{v}$', ha='center', va='center')
    ax.text(0, -1.38, r'$(a)$', ha='center', va='center')
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-1.55, 1.65)
    ax.set_aspect('equal')
    ax.axis('off')
    # ---- (b)
    ax = axes[1]
    th = np.linspace(np.radians(188), np.radians(352), 150)
    ax.plot(np.cos(th), np.sin(th), 'k-', lw=1.6)
    ax.plot([0, 0], [-1.05, 1.30], 'k-', lw=1.0)
    _arrow(ax, (0, 1.30), (0, 1.48), lw=1.0)
    ax.text(0.08, 1.52, r'$\mathcal{E}_h=\mathcal{E}_v-\mathcal{E}(\mathbf{k})$',
            ha='left', va='center')
    ax.text(-1.52, 0.34, r'$\mathcal{E}_v$', ha='center', va='center')
    # the hole: small square on the left branch
    sq = Rectangle((-0.70, -0.76), 0.17, 0.17, angle=-30,
                   rotation_point='xy', facecolor='white', edgecolor='k',
                   lw=1.1)
    ax.add_patch(sq)
    _arrow(ax, (-0.60, -0.64), (-0.99, -0.23), lw=1.1)
    ax.text(-0.35, -0.50, r'$-e\,\mathbf{v}$', ha='left', va='center')
    ax.text(0, -1.38, r'$(b)$', ha='center', va='center')
    ax.set_xlim(-1.85, 1.95)
    ax.set_ylim(-1.55, 1.75)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, 105)


# ---------------------------------------------------------------- fig. 106
def fig_106():
    """Band with small overlap: (a) extended; (b) repeated zone scheme."""
    fig, axes = plt.subplots(1, 2, figsize=(4.8, 2.6))
    plt.subplots_adjust(wspace=0.10, left=0.01, right=0.99,
                        bottom=0.03, top=0.99)
    # ---- (a) extended zone scheme
    ax = axes[0]
    ax.add_patch(FancyBboxPatch((-1.0, -0.85), 2.0, 1.70,
                                boxstyle='round,pad=0,rounding_size=0.30',
                                facecolor='0.84', edgecolor='k', lw=1.6))
    ax.add_patch(Wedge((0, 0.85), 0.26, 0, 180, facecolor='white',
                       edgecolor='k', lw=1.3, hatch='///'))
    ax.add_patch(Wedge((0, -0.85), 0.26, 180, 360, facecolor='white',
                       edgecolor='k', lw=1.3, hatch='///'))
    ax.add_patch(Wedge((-1.0, 0), 0.26, 90, 270, facecolor='white',
                       edgecolor='k', lw=1.3, hatch='///'))
    ax.add_patch(Wedge((1.0, 0), 0.26, -90, 90, facecolor='white',
                       edgecolor='k', lw=1.3, hatch='///'))
    ax.text(0, -1.42, r'$(a)$', ha='center', va='center')
    ax.set_xlim(-1.62, 1.62)
    ax.set_ylim(-1.62, 1.34)
    ax.set_aspect('equal')
    ax.axis('off')
    # ---- (b) repeated zone scheme
    ax = axes[1]
    t = np.linspace(0, 2 * np.pi, 400)
    rr = 1 + 0.055 * np.sin(3 * t + 0.8) + 0.04 * np.sin(5 * t + 2.0) \
        + 0.028 * np.sin(7 * t + 4.0)
    ax.fill(1.24 * rr * np.cos(t), 1.13 * rr * np.sin(t), '0.86',
            zorder=1)
    g = 0.62
    for y in (-g, 0, g):
        ax.plot([-1.12, 1.12], [y, y], 'k-', lw=0.9, zorder=2)
    for x in (-g, 0, g):
        ax.plot([x, x], [-1.02, 1.02], 'k-', lw=0.9, zorder=2)
    for (cx, cy) in [(-g, g), (g, g), (-g, -g), (g, -g)]:
        ax.add_patch(Circle((cx, cy), 0.165, facecolor='none',
                            edgecolor='k', lw=1.5, zorder=3))
    for (cx, cy) in [(0, g), (0, -g), (-g, 0), (g, 0)]:
        ax.add_patch(Circle((cx, cy), 0.165, facecolor='white',
                            edgecolor='k', lw=1.5, hatch='///', zorder=3))
    ax.text(0, -1.42, r'$(b)$', ha='center', va='center')
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.62, 1.34)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, 106)


# ---------------------------------------------------------------- fig. 107
def fig_107():
    """(a) empty sphere in the electron distribution; (b) sphere of holes."""
    fig, axes = plt.subplots(1, 2, figsize=(4.6, 2.5))
    plt.subplots_adjust(wspace=0.25, left=0.02, right=0.98,
                        bottom=0.03, top=0.99)
    R = 0.62
    # ---- (a)
    ax = axes[0]
    ax.add_patch(Circle((0, 0), R, facecolor='white', edgecolor='k',
                        lw=1.7, zorder=3))
    rng = np.random.default_rng(7)
    seg = []
    for phi in np.arange(0, 360, 6.0):
        r1 = R * (1.12 + 0.05 * rng.random())
        r2 = r1 + R * (0.36 + 0.10 * rng.random())
        c, s = np.cos(np.radians(phi)), np.sin(np.radians(phi))
        seg.append([(r1 * c, r1 * s), (r2 * c, r2 * s)])
    ax.add_collection(LineCollection(seg, colors='k', linewidths=1.0,
                                     zorder=1))
    a1 = np.radians(204)
    _arrow(ax, (0.62 * R * np.cos(a1), 0.62 * R * np.sin(a1)),
           (0.11 * R * np.cos(a1), 0.11 * R * np.sin(a1)), lw=1.2)
    ax.text(-0.31 * R, 0.26 * R, r'$e\mathbf{v}$', ha='center', va='center')
    a2 = np.radians(-50)
    _arrow(ax, (0.77 * R * np.cos(a2), 0.77 * R * np.sin(a2)),
           (0.26 * R * np.cos(a2), 0.26 * R * np.sin(a2)), lw=1.2)
    ax.text(0.46 * R, -0.35 * R, r'$e\mathbf{v}$', ha='left', va='center')
    ax.text(0, -1.32, r'$(a)$', ha='center', va='center')
    ax.set_xlim(-1.38, 1.38)
    ax.set_ylim(-1.50, 1.22)
    ax.set_aspect('equal')
    ax.axis('off')
    # ---- (b)
    ax = axes[1]
    ax.add_patch(Circle((0, 0), R, facecolor='white', edgecolor='k',
                        lw=1.7, hatch='////', zorder=2))
    ax.text(0, 0.10, 'Holes', ha='center', va='center', zorder=4,
            bbox=dict(facecolor='white', edgecolor='none', pad=0.5))
    b1 = np.radians(200)
    _arrow(ax, (R * np.cos(b1), R * np.sin(b1)),
           (1.58 * R * np.cos(b1), 1.58 * R * np.sin(b1)), lw=1.2)
    ax.text(1.60 * R * np.cos(b1) - 0.02, 1.60 * R * np.sin(b1) + 0.12,
            r'$-e\mathbf{v}$', ha='center', va='center')
    b2 = np.radians(-62)
    _arrow(ax, (R * np.cos(b2), R * np.sin(b2)),
           (1.52 * R * np.cos(b2), 1.52 * R * np.sin(b2)), lw=1.2)
    ax.text(1.54 * R * np.cos(b2) + 0.18, 1.54 * R * np.sin(b2),
            r'$-e\mathbf{v}$', ha='left', va='center')
    ax.text(0, -1.32, r'$(b)$', ha='center', va='center')
    ax.set_xlim(-1.38, 1.38)
    ax.set_ylim(-1.50, 1.22)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, 107)


# ---------------------------------------------------------------- fig. 108
def fig_108():
    """Impurity levels in a semiconductor."""
    fig, ax = plt.subplots(figsize=(3.4, 3.0))
    x0, x1 = 2.8, 7.2
    # conduction band (stippled), lower edge = band edge (solid)
    ax.add_patch(Rectangle((x0, 7.40), x1 - x0, 0.95, facecolor='0.82',
                           edgecolor='none'))
    ax.plot([x0, x1], [7.40, 7.40], 'k-', lw=1.8)
    ax.plot([x0, x1], [8.35, 8.35], color='0.45', lw=0.7,
            linestyle=(0, (1, 2)))
    # donor levels: filled dots + dashed line, just below conduction band
    ax.plot([4.10, 5.35], [7.18, 7.18], 'k--', lw=1.2, dashes=(5, 4))
    ax.plot([4.10, 5.35], [7.18, 7.18], 'ko', ms=5)
    ax.text(5.60, 7.18, 'Donor levels', ha='left', va='center')
    # acceptor levels: open circles + dashed line, just above valence band
    ax.plot([3.50, 4.60], [6.13, 6.13], 'k--', lw=1.2, dashes=(5, 4))
    ax.plot([3.50, 4.60], [6.13, 6.13], 'o', ms=5, mfc='white', mec='k')
    ax.text(4.85, 6.13, 'Acceptor levels', ha='left', va='center')
    # valence band (hatched), upper edge = band edge (solid)
    ax.add_patch(Rectangle((x0, 4.75), x1 - x0, 1.08, facecolor='white',
                           edgecolor='0.55', lw=0.7, hatch='////'))
    ax.plot([x0, x1], [5.83, 5.83], 'k-', lw=1.8)
    ax.set_xlim(2.3, 9.7)
    ax.set_ylim(4.3, 8.85)
    ax.set_aspect('equal')
    ax.axis('off')
    _save(fig, 108)


if __name__ == '__main__':
    for f in (fig_102, fig_103, fig_104, fig_105, fig_106, fig_107,
              fig_108):
        f()
