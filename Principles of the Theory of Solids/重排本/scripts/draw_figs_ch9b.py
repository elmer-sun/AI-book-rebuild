# -*- coding: utf-8 -*-
"""Redraw Ziman, Principles of the Theory of Solids, 2nd ed., Chapter 9 (part 2),
Figs. 164-174.  Black-and-white textbook-style vector figures.

Figures and their sources (page PNGs under 齐曼/原书转换/pages):
  164  p324  Fermi surface of copper (4 spheres + necks)
  165  p325  (a) real-space trajectory, (b) orbit on Fermi surface
  166  p326  R.F. size effect, (a)(b)(c) in one slab drawing
  167  p329  Solution of Schroedinger equation in a magnetic field
  168  p330  Quantization scheme, (a) without / (b) with magnetic field
  169  p332  Tubes of quantized magnetic levels (3D)
  170  p335  (a) FS need not coincide with quantized orbit, (b) levels pass zeta
  171  p335  Occupation of magnetic levels, (a)(b)(c)
  172  p338  (a) parabolic band quantization, (b) density of states
  173  p339  Magneto-optical transitions, two hole bands
  174  p341  (a) free-electron orbit, (b) reconnected orbits at zone boundary
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.path import Path
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Ellipse, Arc, Polygon

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

BASE = r'E:\AI整理书籍\齐曼\重排本'
OUT = os.path.join(BASE, 'figures')
PRE = os.path.join(OUT, 'preview')
os.makedirs(PRE, exist_ok=True)


def save(fig, key):
    fig.savefig(os.path.join(OUT, 'fig_%s.pdf' % key), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRE, 'fig_%s.png' % key), bbox_inches='tight', pad_inches=0.03, dpi=150)
    plt.close(fig)
    print('saved', key)


def arrow(ax, p0, p1, lw=1.1, ms=11, ls='-'):
    ax.annotate('', xy=p1, xytext=p0, zorder=9,
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw, linestyle=ls,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def darrow(ax, p0, p1, lw=1.0, ms=9):
    """Double-headed dimension arrow."""
    ax.annotate('', xy=p1, xytext=p0, zorder=9,
                arrowprops=dict(arrowstyle='<|-|>', color='k', lw=lw,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def stipple(ax, inside, bbox, n=400, s=0.35, seed=0, color='k', maxtry=20000):
    """Scatter stipple dots at points where inside(x, y) is True."""
    rng = np.random.default_rng(seed)
    x0, x1, y0, y1 = bbox
    pts = []
    tries = 0
    while len(pts) < n and tries < maxtry:
        m = min(2000, maxtry - tries)
        xs = rng.uniform(x0, x1, m)
        ys = rng.uniform(y0, y1, m)
        for x, y in zip(xs, ys):
            if inside(x, y):
                pts.append((x, y))
                if len(pts) >= n:
                    break
        tries += m
    if pts:
        pts = np.array(pts)
        ax.scatter(pts[:, 0], pts[:, 1], s=s, c=color, linewidths=0, zorder=5)


def circ_pts(c, r, th):
    th = np.deg2rad(th)
    return (c[0] + r * np.cos(th), c[1] + r * np.sin(th))


# ---------------------------------------------------------------- fig 164
def fig_164():
    """Fermi surface of copper: four spheres joined by <111> necks."""
    fig = plt.figure(figsize=(3.6, 4.1))
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_axis_off()
    ax.set_xlim(-1.30, 1.30)
    ax.set_ylim(-1.45, 1.45)
    ax.set_aspect('equal')

    R = 0.52
    spheres = {          # rough repeated-zone view of the copper FS
        'top':    (0.30, 0.78),
        'left':   (-0.60, 0.05),
        'right':  (0.64, -0.03),
        'bottom': (-0.15, -0.77),
    }
    neck_pairs = [('top', 'left'), ('top', 'right'),
                  ('left', 'bottom'), ('right', 'bottom')]
    collar_ang = {'top': 95, 'left': 155, 'right': 25, 'bottom': 250}

    # --- spheres (with shading, collar stubs and dark neck-holes)
    for name, c in spheres.items():
        ax.add_patch(mpatches.Circle(c, R, facecolor='white', edgecolor='k',
                                     lw=1.3, zorder=4))
        # radial stipple, denser near the rim
        rng = np.random.default_rng(abs(hash(name)) % 9999)
        pts = []
        while len(pts) < 800:
            x, y = rng.uniform(c[0] - R, c[0] + R), rng.uniform(c[1] - R, c[1] + R)
            d2 = (x - c[0]) ** 2 + (y - c[1]) ** 2
            if d2 > (0.965 * R) ** 2 or d2 < (0.18 * R) ** 2:
                continue
            f = np.sqrt(d2) / R
            if rng.uniform() < 0.10 + 0.90 * f ** 3.0:
                pts.append((x, y))
        pts = np.array(pts)
        ax.scatter(pts[:, 0], pts[:, 1], s=1.1, c='k', linewidths=0, zorder=5)
        # collar (neck stub pointing outwards)
        ang = collar_ang[name]
        t = np.deg2rad(ang)
        ux, uy = np.cos(t), np.sin(t)
        nx, ny = -uy, ux
        base = (c[0] + R * 0.99 * ux, c[1] + R * 0.99 * uy)
        top = (base[0] + 0.19 * ux, base[1] + 0.19 * uy)
        ax.plot([base[0] - 0.125 * nx, top[0] - 0.095 * nx],
                [base[1] - 0.125 * ny, top[1] - 0.095 * ny], 'k-', lw=1.0, zorder=6)
        ax.plot([base[0] + 0.125 * nx, top[0] + 0.095 * nx],
                [base[1] + 0.125 * ny, top[1] + 0.095 * ny], 'k-', lw=1.0, zorder=6)
        ax.add_patch(Ellipse(top, 0.20, 0.11, angle=np.rad2deg(t) - 90,
                             facecolor='0.90', edgecolor='k', lw=0.9, zorder=6))
        # dark neck-holes facing the viewer
        for da, off in [(46, 0.46), (-40, 0.44)]:
            a2 = t + np.deg2rad(da)
            hx = c[0] + R * off * np.cos(a2)
            hy = c[1] + R * off * np.sin(a2)
            ax.add_patch(Ellipse((hx, hy), 0.21, 0.15, angle=np.rad2deg(a2) + 90,
                                 facecolor='k', edgecolor='k', lw=0.5, zorder=6))

    # --- necks bridging the gaps (drawn on top of the rims)
    for a, b in neck_pairs:
        ca, cb = np.array(spheres[a]), np.array(spheres[b])
        th = np.arctan2((cb - ca)[1], (cb - ca)[0])
        w = 0.17                                   # half width of neck at rims
        d1 = np.arcsin(min(0.9, w / R))            # angular half-width on sphere a
        pa1 = ca + R * np.array([np.cos(th + d1), np.sin(th + d1)])
        pa2 = ca + R * np.array([np.cos(th - d1), np.sin(th - d1)])
        pb1 = cb - R * np.array([np.cos(th - d1), np.sin(th - d1)])
        pb2 = cb - R * np.array([np.cos(th + d1), np.sin(th + d1)])
        mid = 0.5 * (ca + cb)
        nv = np.array([-np.sin(th), np.cos(th)])
        c1 = mid + nv * (w - 0.085)
        c2 = mid - nv * (w - 0.085)
        verts = [tuple(pa1)]
        codes = [Path.MOVETO]
        verts += [tuple(c1), tuple(pb1)]
        codes += [Path.CURVE3, Path.CURVE3]
        verts += [tuple(pb2)]
        codes += [Path.LINETO]
        verts += [tuple(c2), tuple(pa2)]
        codes += [Path.CURVE3, Path.CURVE3]
        verts += [tuple(pa1)]
        codes += [Path.CLOSEPOLY]
        pth = Path(verts, codes)
        ax.add_patch(mpatches.PathPatch(pth, facecolor='white', edgecolor='k',
                                        lw=1.1, zorder=7))
        bx0, bx1 = min(pa1[0], pa2[0], pb1[0], pb2[0]), max(pa1[0], pa2[0], pb1[0], pb2[0])
        by0, by1 = min(pa1[1], pa2[1], pb1[1], pb2[1]), max(pa1[1], pa2[1], pb1[1], pb2[1])
        rng = np.random.default_rng(abs(hash((a, b))) % 9999)
        pts = []
        while len(pts) < 110:
            x, y = rng.uniform(bx0, bx1), rng.uniform(by0, by1)
            if pth.contains_point((x, y)):
                pts.append((x, y))
        pts = np.array(pts)
        ax.scatter(pts[:, 0], pts[:, 1], s=0.9, c='k', linewidths=0, zorder=8)

    save(fig, 164)


# ---------------------------------------------------------------- fig 165
def fig_165():
    """(a) Trajectory of electron in real space. (b) Orbit on Fermi surface."""
    fig = plt.figure(figsize=(4.8, 2.1))
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.96])
    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.set_xlim(-2.0, 5.05)
    ax.set_ylim(-1.45, 1.15)

    # ---------------- (a) plus-shaped trajectory
    cx, cy = 0.0, 0.0
    ahw, ahh = 1.00, 0.28        # horizontal arm half-length/height
    vhw, vhh = 0.27, 0.60        # vertical arm half-width/height
    rs = 0.16                    # rounding

    def rrect(x0, y0, w, h, rs):
        return FancyBboxPatch((x0 + rs, y0 + rs), w - 2 * rs, h - 2 * rs,
                              boxstyle='round,pad=%.3f,rounding_size=%.3f' % (rs, rs),
                              fc='white', ec='k', lw=1.3, mutation_aspect=1)

    # union outline trick: draw both outlines, then both white fills
    r_h = FancyBboxPatch((-ahw + rs, cy - ahh + rs), 2 * ahw - 2 * rs, 2 * ahh - 2 * rs,
                         boxstyle='round,pad=%.3f,rounding_size=%.3f' % (rs, rs),
                         fc='none', ec='k', lw=1.3)
    r_v = FancyBboxPatch((cx - vhw + rs, -vhh + rs), 2 * vhw - 2 * rs, 2 * vhh - 2 * rs,
                         boxstyle='round,pad=%.3f,rounding_size=%.3f' % (rs, rs),
                         fc='none', ec='k', lw=1.3)
    ax.add_patch(r_h); ax.add_patch(r_v)
    f_h = FancyBboxPatch((-ahw + rs, cy - ahh + rs), 2 * ahw - 2 * rs, 2 * ahh - 2 * rs,
                         boxstyle='round,pad=%.3f,rounding_size=%.3f' % (rs, rs),
                         fc='white', ec='none')
    f_v = FancyBboxPatch((cx - vhw + rs, -vhh + rs), 2 * vhw - 2 * rs, 2 * vhh - 2 * rs,
                         boxstyle='round,pad=%.3f,rounding_size=%.3f' % (rs, rs),
                         fc='white', ec='none')
    ax.add_patch(f_h); ax.add_patch(f_v)

    # orbit direction arrows (counter-clockwise)
    ytop, ybot = vhh, -vhh
    arrow(ax, (0.42, ytop), (0.10, ytop), lw=1.2, ms=12)      # top, leftward
    arrow(ax, (-0.42, ybot), (-0.10, ybot), lw=1.2, ms=12)    # bottom, rightward
    arrow(ax, (-ahw + 0.02, 0.16), (-ahw + 0.02, -0.16), lw=1.2, ms=11)  # A, down
    arrow(ax, (ahw - 0.02, -0.16), (ahw - 0.02, 0.16), lw=1.2, ms=11)    # B, up

    # horizontal mid-line + velocity arrows
    ax.plot([-1.48, 1.48], [0, 0], 'k-', lw=0.8)
    xs = np.arange(-1.40, -0.05, 0.072)
    for x in xs:
        L = 0.04 + 0.20 * min(1.0, abs(x) / 1.05)
        arrow(ax, (x, -0.015), (x, -0.015 - L), lw=0.55, ms=4.5)
    xs = np.arange(0.05, 1.40, 0.072)
    for x in xs:
        L = 0.04 + 0.20 * min(1.0, abs(x) / 1.05)
        arrow(ax, (x, 0.015), (x, 0.015 + L), lw=0.55, ms=4.5)
    ax.text(-1.12, 0.05, '$A$', fontsize=12, ha='center', va='bottom')
    ax.text(1.13, -0.05, '$B$', fontsize=12, ha='left', va='top')

    # H symbol (into the page), circle-dot + clockwise arrow
    hc = (-1.62, 0.72)
    ax.add_patch(mpatches.Circle(hc, 0.14, fc='none', ec='k', lw=1.0))
    ax.plot([hc[0]], [hc[1]], 'k.', ms=4)
    ax.add_patch(Arc(hc, 0.28, 0.28, theta1=35, theta2=145, lw=1.0))
    arrow(ax, circ_pts(hc, 0.14, 40), circ_pts(hc, 0.14, 28), lw=1.0, ms=8)
    ax.text(hc[0] + 0.20, hc[1] - 0.02, '$H$', fontsize=12)

    # dimension arrows
    darrow(ax, (-1.48, 0.92), (1.48, 0.92), lw=0.9)
    ax.text(0, 0.97, r'$\frac{1}{2}\lambda$', fontsize=12, ha='center', va='bottom',
            bbox=dict(fc='white', ec='none', pad=0.5))
    darrow(ax, (-1.48, -1.02), (1.48, -1.02), lw=0.9)
    ax.text(0, -1.07, '$2r_x$', fontsize=12, ha='center', va='top',
            bbox=dict(fc='white', ec='none', pad=0.5))

    # small x-y axes
    ax.annotate('', xy=(2.30, -0.30), xytext=(2.30, -0.72),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0, mutation_scale=10))
    ax.annotate('', xy=(2.72, -0.72), xytext=(2.30, -0.72),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.0, mutation_scale=10))
    ax.text(2.22, -0.28, '$y$', fontsize=12, ha='right')
    ax.text(2.72, -0.84, '$x$', fontsize=12, ha='center', va='top')
    ax.text(0, -1.38, '($a$)', fontsize=12, ha='center')

    # ---------------- (b) orbit on Fermi surface (stippled cross)
    cx2, cy2 = 3.62, 0.05
    vhw2, vhh2 = 0.25, 0.72
    ahw2, ahh2 = 0.46, 0.22
    r_h2 = FancyBboxPatch((cx2 - ahw2 + rs, cy2 - ahh2 + rs), 2 * ahw2 - 2 * rs, 2 * ahh2 - 2 * rs,
                          boxstyle='round,pad=%.3f,rounding_size=%.3f' % (rs, rs),
                          fc='none', ec='k', lw=1.3)
    r_v2 = FancyBboxPatch((cx2 - vhw2 + rs, cy2 - vhh2 + rs), 2 * vhw2 - 2 * rs, 2 * vhh2 - 2 * rs,
                          boxstyle='round,pad=%.3f,rounding_size=%.3f' % (rs, rs),
                          fc='none', ec='k', lw=1.3)
    ax.add_patch(r_h2); ax.add_patch(r_v2)
    f_h2 = FancyBboxPatch((cx2 - ahw2 + rs, cy2 - ahh2 + rs), 2 * ahw2 - 2 * rs, 2 * ahh2 - 2 * rs,
                          boxstyle='round,pad=%.3f,rounding_size=%.3f' % (rs, rs),
                          fc='white', ec='none')
    f_v2 = FancyBboxPatch((cx2 - vhw2 + rs, cy2 - vhh2 + rs), 2 * vhw2 - 2 * rs, 2 * vhh2 - 2 * rs,
                          boxstyle='round,pad=%.3f,rounding_size=%.3f' % (rs, rs),
                          fc='white', ec='none')
    ax.add_patch(f_h2); ax.add_patch(f_v2)

    def inside_b(x, y):
        return (abs(x - cx2) <= ahw2 and abs(y - cy2) <= ahh2) or \
               (abs(x - cx2) <= vhw2 and abs(y - cy2) <= vhh2)
    stipple(ax, inside_b, (cx2 - ahw2, cx2 + ahw2, cy2 - vhh2, cy2 + vhh2),
            n=900, s=0.6, seed=7)
    # traversal arrow on right edge of vertical bar
    arrow(ax, (cx2 + vhw2, cy2 - 0.48), (cx2 + vhw2, cy2 - 0.16), lw=1.0, ms=10)
    # velocity arrows at A (bottom) and B (top)
    arrow(ax, (cx2, cy2 + vhh2), (cx2, cy2 + vhh2 + 0.24), lw=1.1, ms=11)
    arrow(ax, (cx2, cy2 - vhh2), (cx2, cy2 - vhh2 - 0.24), lw=1.1, ms=11)
    ax.text(cx2 + 0.08, cy2 + vhh2 + 0.16, '$B$', fontsize=12, ha='left')
    ax.text(cx2 - 0.10, cy2 - vhh2 - 0.26, '$v$', fontsize=12, ha='right', va='top')
    ax.text(cx2 + 0.08, cy2 - vhh2 - 0.22, '$A$', fontsize=12, ha='left', va='top')
    darrow(ax, (cx2 + 0.95, cy2 - vhh2 + 0.02), (cx2 + 0.95, cy2 + vhh2 - 0.02), lw=0.9)
    ax.text(cx2 + 1.03, cy2, '$2k_y$', fontsize=12, ha='left', va='center')
    ax.text(cx2, cy2 - vhh2 - 0.62, '($b$)', fontsize=12, ha='center', va='top')

    save(fig, 165)


# ---------------------------------------------------------------- fig 166
def fig_166():
    """R.F. size effect in a slab: (a) extremal trajectory, (b) scattered
    trajectory, (c) chain of trajectories induced by internal skin layers."""
    fig = plt.figure(figsize=(4.8, 2.35))
    ax = fig.add_axes([0.01, 0.03, 0.97, 0.94])
    ax.set_axis_off()
    ax.set_xlim(-0.25, 10.95)
    ax.set_ylim(-0.75, 3.95)
    ax.set_aspect('equal')

    X0, X1, Y0, Y1 = 0.0, 10.0, 0.0, 3.0

    # slab body with light diagonal hatch
    ax.add_patch(Rectangle((X0, Y0), X1 - X0, Y1 - Y0, facecolor='white',
                           edgecolor='k', lw=1.1, zorder=1))
    ax.add_patch(Rectangle((X0, Y0), X1 - X0, Y1 - Y0, facecolor='none',
                           edgecolor='0.68', lw=0, hatch='//', zorder=1))

    def band(x0, x1, y0, y1):
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor='white',
                               edgecolor='k', lw=0.9, zorder=2))
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor='none',
                               edgecolor='0.30', lw=0, hatch='////', zorder=2))

    band(X0, X1, 2.68, 3.0)          # top skin layer
    band(X0, X1, 0.0, 0.32)          # bottom skin layer
    band(6.55, X1, 2.02, 2.26)       # internal layers
    band(6.55, X1, 1.02, 1.26)

    # delta brackets (right side)
    for (ya, yb) in [(2.68, 3.0), (2.02, 2.26), (1.02, 1.26), (0.0, 0.32)]:
        ax.add_patch(Arc((10.12, 0.5 * (ya + yb)), 0.18, yb - ya,
                         theta1=-62, theta2=62, lw=0.9))
        ax.text(10.30, 0.5 * (ya + yb), r'$\delta$', fontsize=11, ha='left', va='center')

    def orbit(c, r, angs, ccw=True, zorder=6):
        ax.add_patch(mpatches.Circle(c, r, facecolor='white', edgecolor='k',
                                     lw=1.2, zorder=zorder))
        sgn = 1 if ccw else -1
        for a in angs:
            p0 = circ_pts(c, r, a - sgn * 9)
            p1 = circ_pts(c, r, a)
            arrow(ax, p0, p1, lw=1.0, ms=9)

    # (a) extremal trajectory touching both faces
    orbit((2.45, 1.5), 1.18, [112, 185, 268])
    # (b) scattered trajectory
    orbit((5.55, 1.45), 1.15, [100])
    arrow(ax, (5.55, 0.30), (5.02, 0.98), lw=1.0, ms=10, ls='--')
    ax.add_patch(Arc((5.55, 0.30), 0.55, 0.35, theta1=180, theta2=225,
                     lw=0.9, linestyle='--'))
    # (c) chain of small orbits between internal layers
    orbit((8.25, 2.47), 0.22, [100])
    orbit((8.25, 1.64), 0.39, [100])
    orbit((8.25, 0.67), 0.36, [100])

    # driving field and field direction
    ax.text(1.75, 3.42, '$E_x\\ \\sin\\ \\omega t$', fontsize=11, ha='center')
    arrow(ax, (0.55, 3.20), (3.05, 3.20), lw=1.1, ms=11)
    hcp = (6.85, 3.45)
    ax.add_patch(mpatches.Circle(hcp, 0.26, fc='none', ec='k', lw=1.1))
    ax.plot([hcp[0]], [hcp[1]], 'k.', ms=5)
    ax.add_patch(Arc(hcp, 0.52, 0.52, theta1=40, theta2=140, lw=1.0))
    arrow(ax, circ_pts(hcp, 0.26, 46), circ_pts(hcp, 0.26, 36), lw=1.0, ms=8)
    ax.text(hcp[0] + 0.38, hcp[1] + 0.02, '$H$', fontsize=12)

    ax.text(2.45, -0.55, '($a$)', fontsize=12, ha='center')
    ax.text(5.55, -0.55, '($b$)', fontsize=12, ha='center')
    ax.text(8.25, -0.55, '($c$)', fontsize=12, ha='center')

    save(fig, 166)


# ---------------------------------------------------------------- fig 167
def fig_167():
    """Solution of the Schroedinger equation for an electron in a field B."""
    fig = plt.figure(figsize=(3.9, 2.9))
    ax = fig.add_axes([0.10, 0.10, 0.84, 0.84])
    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.set_xlim(-1.15, 6.55)
    ax.set_ylim(-0.85, 4.35)

    # box
    ax.add_patch(Rectangle((0, 0), 5.6, 3.6, facecolor='none', edgecolor='k', lw=1.1))
    # dimensions
    darrow(ax, (-0.45, 0.02), (-0.45, 3.58), lw=0.9)
    ax.text(-0.60, 1.8, '$L_y$', fontsize=12, ha='right', va='center')
    darrow(ax, (0.02, -0.45), (5.58, -0.45), lw=0.9)
    ax.text(2.8, -0.62, '$L_x$', fontsize=12, ha='center', va='top')

    # axes inside the box
    Ox, Oy = 1.15, 1.55
    arrow(ax, (Ox, Oy), (4.95, Oy), lw=1.0, ms=10)
    arrow(ax, (Ox, Oy), (Ox, 3.05), lw=1.0, ms=10)
    ax.text(5.05, Oy - 0.06, '$x$', fontsize=12, ha='left', va='center')
    ax.text(Ox - 0.10, 3.08, '$y$', fontsize=12, ha='right', va='bottom')
    ax.text(Ox - 0.10, Oy - 0.08, '$O$', fontsize=12, ha='right', va='top')

    # wave packet u(x) centred at x0
    x0 = 3.30
    sig, kk, amp = 0.72, 10.5, 0.78
    xs = np.linspace(Ox, 4.95, 900)
    env = amp * np.exp(-((xs - x0) ** 2) / (2 * sig ** 2))
    ax.plot(xs, Oy + env * np.cos(kk * (xs - x0)), 'k-', lw=1.0)
    # small arrow on an early crest
    arrow(ax, (1.58, Oy + 0.22), (1.66, Oy + 0.52), lw=0.8, ms=8)
    ax.text(x0, Oy - 0.13, '$x_0$', fontsize=12, ha='center', va='top')

    # dashed cyclotron circle centred on x0
    c = (x0, Oy)
    r = 1.08
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(c[0] + r * np.cos(th), c[1] + r * np.sin(th), 'k--', lw=0.9)
    p0 = circ_pts(c, r, 82)
    p1 = circ_pts(c, r, 96)
    arrow(ax, p0, p1, lw=0.9, ms=9, ls='--')

    save(fig, 167)


# ---------------------------------------------------------------- fig 168
def fig_168():
    """Quantization scheme for free electrons: (a) without field (filled disc
    of allowed states + energy circles), (b) orbits condense on beaded circles."""
    fig = plt.figure(figsize=(3.5, 6.3))
    axa = fig.add_axes([0.10, 0.535, 0.84, 0.435])
    axb = fig.add_axes([0.10, 0.075, 0.84, 0.435])
    for ax in (axa, axb):
        ax.set_axis_off()
        ax.set_aspect('equal')
        ax.set_xlim(-1.62, 1.75)
        ax.set_ylim(-1.55, 1.62)
    radii = [0.35, 0.62, 0.88, 1.15]

    # ---- (a)
    ax = axa
    arrow(ax, (0, -1.28), (0, 1.50), lw=1.1, ms=11)
    arrow(ax, (-1.42, 0), (1.62, 0), lw=1.1, ms=11)
    ax.text(0.07, 1.46, '$k_y$', fontsize=12, ha='left', va='top')
    ax.text(1.58, -0.10, '$k_x$', fontsize=12, ha='center', va='top')
    for r in radii:
        ax.add_patch(mpatches.Circle((0, 0), r, fc='none', ec='k', lw=1.0, zorder=6))
    # dot lattice filling the disc
    rng = np.random.default_rng(3)
    g = np.arange(-1.12, 1.121, 0.056)
    XX, YY = np.meshgrid(g, g)
    keep = XX ** 2 + YY ** 2 <= 1.12 ** 2
    ax.scatter(XX[keep], YY[keep], s=0.5, c='k', linewidths=0, zorder=4)
    ax.text(0.10, 0.415, '$n=0$', fontsize=10, ha='left', zorder=8,
            bbox=dict(fc='white', ec='none', pad=0.4))
    for r, lab, ang in [(0.62, '1', 47), (0.88, '2', 42), (1.15, '3', 39)]:
        p = circ_pts((0, 0), r + 0.075, ang)
        ax.text(p[0], p[1], lab, fontsize=10, ha='left', va='bottom', zorder=8,
                bbox=dict(fc='white', ec='none', pad=0.2))
    ax.text(0, -1.50, '($a$)', fontsize=12, ha='center', va='top')

    # ---- (b)
    ax = axb
    for i, r in enumerate(radii):
        n = int(2 * np.pi * r / 0.026)
        th = np.linspace(0, 2 * np.pi, n, endpoint=False)
        s = 2.6 if i > 0 else 3.4
        ax.scatter(r * np.cos(th), r * np.sin(th), s=s, c='k', linewidths=0)
    ax.text(0, -1.50, '($b$)', fontsize=12, ha='center', va='top')

    save(fig, 168)


# ---------------------------------------------------------------- fig 169
def fig_169():
    """Tubes of quantized magnetic levels: nested wavy tubes, H vertically up."""
    fig = plt.figure(figsize=(3.3, 2.75))
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.set_xlim(-1.30, 1.30)
    ax.set_ylim(-0.10, 1.62)

    # rim levels (y, half-width)
    rims = [(0.965, 0.075), (0.875, 0.155), (0.770, 0.275), (0.650, 0.435),
            (0.520, 0.600), (0.390, 0.660), (0.265, 0.560), (0.150, 0.375),
            (0.055, 0.185)]

    SQ = 0.26   # perspective squash of the rims

    def rim_curve(i, half):
        """Half curve of rim i: 'front' (lower) or 'back' (upper)."""
        y, w = rims[i]
        ph = 0.9 * i
        t = np.linspace(0, np.pi, 160)
        wob = 1 + 0.055 * np.cos(3 * t + ph) + 0.03 * np.cos(5 * t + 2 * ph)
        x = w * np.cos(t) * wob
        yy = y + SQ * w * np.sin(t)
        if half == 'front':                     # sin(t) < 0 : lower half
            x, yy = x[::-1], yy[::-1]           # left -> right, dipping down
        return x, yy                            # 'back': left -> right over the top

    # bands between successive rims: lower(front) half of upper rim +
    # back(upper) half of lower rim, drawn top -> bottom
    for i in range(len(rims) - 1):
        x1, y1 = rim_curve(i, 'front')
        x2, y2 = rim_curve(i + 1, 'back')
        vx = np.concatenate([x1, x2[::-1]])
        vy = np.concatenate([y1, y2[::-1]])
        ax.add_patch(Polygon(np.column_stack([vx, vy]), closed=True,
                             facecolor='white', edgecolor='none', zorder=3))
        if i % 2 == 1:
            pth = Path(np.column_stack([vx, vy]))
            rng = np.random.default_rng(40 + i)
            pts = []
            while len(pts) < 480:
                x = rng.uniform(vx.min(), vx.max())
                y = rng.uniform(min(vy.min(), rims[i + 1][0] - SQ * rims[i + 1][1]),
                                max(vy.max(), rims[i][0]))
                if pth.contains_point((x, y)):
                    pts.append((x, y))
            pts = np.array(pts)
            ax.scatter(pts[:, 0], pts[:, 1], s=0.45, c='k', linewidths=0, zorder=4)

    # rims on top: front halves solid, back halves dashed
    for i in range(len(rims)):
        x, y = rim_curve(i, 'front')
        ax.plot(x, y, 'k-', lw=1.15, zorder=6)
        x, y = rim_curve(i, 'back')
        ax.plot(x, y, 'k--', lw=0.7, zorder=5)

    # top stub and bottom stub
    ax.plot([-0.055, -0.045], [0.965, 1.065], 'k-', lw=1.0, zorder=6)
    ax.plot([0.055, 0.045], [0.965, 1.065], 'k-', lw=1.0, zorder=6)
    t = np.linspace(0, np.pi, 60)
    ax.plot(0.045 * np.cos(t), 1.065 + 0.035 * np.sin(t), 'k-', lw=0.9, zorder=6)
    ax.plot([-0.185, -0.09], [0.055, -0.03], 'k--', lw=0.8, zorder=6)
    ax.plot([0.185, 0.09], [0.055, -0.03], 'k--', lw=0.8, zorder=6)
    ax.plot(0.095 * np.cos(t), -0.03 + 0.045 * np.sin(t), 'k-', lw=0.9, zorder=6)

    # H arrow
    arrow(ax, (0, 1.10), (0, 1.52), lw=1.4, ms=13)
    ax.text(0.09, 1.44, '$\\mathbf{H}$', fontsize=13, ha='left')

    save(fig, 169)


# ---------------------------------------------------------------- fig 170
def fig_170():
    """(a) Fermi surface section vs quantized orbits (nested rounded-diamond
    contours, solid/dashed).  (b) quantized levels sweep through zeta vs H."""
    fig = plt.figure(figsize=(4.8, 2.35))
    ax = fig.add_axes([0.01, 0.03, 0.98, 0.94])
    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.set_xlim(0, 6.9)
    ax.set_ylim(-0.85, 2.55)

    # ---------- (a)
    cx, cy, R0 = 1.05, 1.02, 0.95
    th = np.linspace(0, 2 * np.pi, 400)

    def prof(rr):
        return rr * (1 - 0.185 * np.cos(4 * th))

    Rs = [1.00, 0.80, 0.61, 0.435, 0.27]
    lsty = ['-', '--', '-', '--', '-']
    lws = [1.5, 1.0, 1.1, 1.0, 1.1]
    for r, ls, lw in zip(Rs, lsty, lws):
        rr = prof(r)
        ax.plot(cx + rr * np.cos(th), cy + rr * np.sin(th), 'k' + ls, lw=lw)

    def band_stip(ri, ro, n, seed):
        def inside(x, y):
            dx, dy = x - cx, y - cy
            r = np.hypot(dx, dy)
            # invert the 4-fold profile approximately along the radius
            c4 = np.cos(4 * np.arctan2(dy, dx))
            f = 1 - 0.185 * c4
            return ri * f <= r <= ro * f
        stipple(ax, inside, (cx - R0, cx + R0, cy - R0, cy + R0), n=n, s=0.4, seed=seed)

    band_stip(Rs[1], Rs[0], 950, 11)
    band_stip(Rs[3], Rs[2], 650, 12)
    ax.text(cx, -0.28, '($a$)', fontsize=12, ha='center')

    # ---------- (b)
    xH0, xH1, yH = 3.35, 6.75, 0.62
    xE = 4.35
    # stippled occupied sea below the H axis
    xb = np.linspace(xH0 - 0.10, xH1, 120)
    yb = yH - 0.55 + 0.07 * np.sin(3 * (xb - xH0)) + 0.04 * np.cos(7 * (xb - xH0))
    verts = list(zip(xb, yb)) + [(xH1, yH), (xH0 - 0.10, yH)]
    ax.add_patch(Polygon(verts, closed=True, facecolor='0.88', edgecolor='none'))
    rng = np.random.default_rng(21)
    n = 2600
    xs = rng.uniform(xH0 - 0.10, xH1, n)
    ys = rng.uniform(yH - 0.62, yH, n)
    pth = Path(verts)
    keep = pth.contains_points(np.column_stack([xs, ys]))
    ax.scatter(xs[keep], ys[keep], s=0.35, c='k', linewidths=0)

    # fan of quantized levels E_n(H)
    m = 0.30
    for i in range(8):
        c0 = yH + 0.16 + 0.235 * i
        ls = '-' if i % 2 == 0 else '--'
        xs2 = np.array([xH0 - 0.28, xH1 - 0.05])
        ys2 = c0 + m * (xs2 - xE)
        ax.plot(xs2, ys2, 'k' + ls, lw=1.0 if ls == '-' else 0.9)

    # axes
    arrow(ax, (xH0 - 0.15, yH), (xH1 + 0.12, yH), lw=1.2, ms=12)
    ax.text(xH1 + 0.18, yH, '$H$', fontsize=13, ha='left', va='center')
    arrow(ax, (xE, yH - 0.52), (xE, yH + 1.42), lw=1.2, ms=12)
    ax.text(xE - 0.10, yH + 1.44, '$\\mathcal{E}$', fontsize=13, ha='right', va='bottom')
    ax.plot([xH0 - 0.15, xH0 + 1.55], [yH + 0.185, yH + 0.185], 'k:', lw=1.1)
    ax.text(xE - 0.08, yH + 0.205, '$\\mathcal{E}_F$', fontsize=12, ha='right')
    ax.text(4.95, -0.55, '($b$)', fontsize=12, ha='center')

    save(fig, 170)


# ---------------------------------------------------------------- fig 171
def fig_171():
    """Occupation of magnetic levels as the magnetic field changes (a)(b)(c)."""
    fig = plt.figure(figsize=(4.8, 1.95))
    ax = fig.add_axes([0.01, 0.04, 0.98, 0.92])
    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.set_xlim(0, 6.35)
    ax.set_ylim(-0.42, 1.85)

    def panel(i, spec, yF=0.72, sparse=None):
        seed = 30 + i
        x0 = 0.25 + 2.05 * i
        w = 1.50
        arrow(ax, (x0, 0.08), (x0, 1.72), lw=1.1, ms=10)
        ax.text(x0 - 0.07, 1.70, '$\\mathcal{E}$', fontsize=12, ha='right', va='top')
        # stippled Fermi sea below zeta
        xb = np.linspace(x0 + 0.02, x0 + w, 90)
        yb = 0.16 + 0.035 * np.sin(3 * (xb - x0) * 4) + 0.025 * np.cos(9 * (xb - x0))
        ytop = yF
        verts = list(zip(xb, yb)) + [(x0 + w, ytop), (x0 + 0.02, ytop)]
        ax.add_patch(Polygon(verts, closed=True, facecolor='0.88', edgecolor='none'))
        rng = np.random.default_rng(seed)
        xs = rng.uniform(x0, x0 + w, 650)
        ys = rng.uniform(0.10, ytop, 650)
        keep = Path(verts).contains_points(np.column_stack([xs, ys]))
        ax.scatter(xs[keep], ys[keep], s=0.3, c='k', linewidths=0)
        ax.plot([x0 + 0.02, x0 + w], [yF, yF], 'k-', lw=1.0)
        ax.text(x0 - 0.06, yF, '$\\mathcal{E}_F$', fontsize=11, ha='right', va='center')

        for y, style in spec:
            if style == 'd':
                ax.plot([x0 + 0.02, x0 + w], [y, y], 'k--', lw=0.95)
            elif style == 's':
                ax.plot([x0 + 0.02, x0 + w], [y, y], 'k-', lw=1.0)
            elif style == 'o':   # occupied: dots row
                ax.plot([x0 + 0.02, x0 + w], [y, y], 'k-', lw=0.9)
                xs = np.arange(x0 + 0.10, x0 + w - 0.03, 0.098)
                ax.scatter(xs, [y] * len(xs), s=4.5, c='k', linewidths=0, zorder=6)
        if sparse:
            y, xs_off = sparse
            ax.plot([x0 + 0.02, x0 + w], [y, y], 'k-', lw=1.0)
            xs = x0 + 0.12 + np.array(xs_off)
            ax.scatter(xs, [y] * len(xs), s=4.5, c='k', linewidths=0, zorder=6)
        ax.text(x0 + 0.75, -0.30, '($%s$)' % 'abc'[i], fontsize=12, ha='center')

    # (a) zeta half-way between two orbits
    panel(0, [(1.50, 'd'), (1.24, 's'), (0.99, 'd'),
              (0.585, 'o'), (0.47, 'd'), (0.345, 'o'), (0.24, 'd')])
    # (b) an orbit coincides with zeta
    panel(1, [(1.50, 'd'), (1.24, 's'), (0.99, 'd'),
              (0.60, 'd'), (0.475, 'o'), (0.36, 'd'), (0.24, 'o')],
          sparse=None)
    # draw the dots row ON the Fermi level of panel (b)
    x0 = 0.25 + 2.05 * 1
    xs = np.arange(x0 + 0.10, x0 + 1.47, 0.098)
    ax.scatter(xs, [0.72] * len(xs), s=4.5, c='k', linewidths=0, zorder=7)
    # (c) an orbit just above zeta begins to fill
    panel(2, [(1.50, 'd'), (1.24, 's'), (0.99, 'd'),
              (0.585, 'd'), (0.46, 'o'), (0.345, 'd')],
          sparse=(0.825, [0.0, 0.32, 0.62, 0.95]))

    save(fig, 171)


# ---------------------------------------------------------------- fig 172
def fig_172():
    """(a) Magnetic quantization of a parabolic band; (b) density of states."""
    fig = plt.figure(figsize=(4.8, 2.55))
    ax = fig.add_axes([0.01, 0.04, 0.98, 0.92])
    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.set_xlim(0, 7.35)
    ax.set_ylim(-0.75, 2.75)

    # ---------------- (a) parabolas E vs kz
    xk = 1.35
    # base line
    ax.plot([0.25, 2.55], [0, 0], 'k-', lw=0.9)
    arrow(ax, (1.55, -0.30), (2.42, -0.30), lw=1.0, ms=10)
    ax.text(1.47, -0.30, '$k_z$', fontsize=12, ha='right', va='center')
    arrow(ax, (xk, 0), (xk, 2.42), lw=1.1, ms=11)
    ax.text(xk - 0.09, 2.42, '$\\mathcal{E}$', fontsize=12, ha='right', va='bottom')

    xs = np.linspace(0.30, 2.42, 300)
    # H = 0 dashed parabola
    y0 = 0.62 * (xs - xk) ** 2
    m = y0 <= 2.15
    ax.plot(xs[m], y0[m], 'k--', lw=1.0)
    ax.text(2.02, 0.10, '$H=0$', fontsize=11, ha='left')
    for n in range(4):
        yn = 0.33 + 0.44 * n
        y = yn + 0.60 * (xs - xk) ** 2
        m = y <= 2.30
        ax.plot(xs[m], y[m], 'k-', lw=1.25)
        ax.text(xk + 0.14, yn + 0.115, '$n=%d$' % n, fontsize=10, ha='left')
    ax.text(1.35, -0.62, '($a$)', fontsize=12, ha='center')

    # ---------------- (b) density of states N_H(E)
    x0 = 3.85
    arrow(ax, (x0, 0), (x0, 2.55), lw=1.1, ms=11)
    ax.text(x0 - 0.10, 2.50, '$\\mathcal{E}$', fontsize=12, ha='right', va='bottom')
    ax.plot([x0, 6.95], [0, 0], 'k-', lw=0.9)
    ax.text(5.15, -0.26, '$N_H(\\mathcal{E})$', fontsize=11, ha='center', va='top')
    arrow(ax, (5.80, -0.26), (6.35, -0.26), lw=1.0, ms=10)

    ylev = [0.30, 0.70, 1.10, 1.50, 1.90]
    xbar = [x0 + 0.02, 4.62, 4.52, 4.44, 4.38]   # left end of each thick bar
    # dashed parabolas (reference: H=0 and subband parabolas N ~ sqrt(E-En))
    yy = np.linspace(0, 2.55, 300)
    for yc, scale in [(0.0, 0.62), (ylev[1], 0.56), (ylev[2], 0.50), (ylev[3], 0.44)]:
        sel = yy >= yc
        xx = x0 + scale * np.sqrt(yy[sel] - yc)
        m = xx <= 7.2
        ax.plot(xx[m], yy[sel][m], 'k--', lw=0.9)
    ax.text(4.52, 0.52, '$H=0$', fontsize=11, ha='left')

    # hooks (singular 1D densities) then bars and labels
    for n in range(5):
        yn = ylev[n]
        if n < 4:
            xs_h, xe_h = xbar[n] + 0.44, xbar[n + 1]
            u = np.linspace(0, 1, 80)
            hx = xs_h + (xe_h - xs_h) * u ** 0.72
            hy = yn + (ylev[n + 1] - yn) * u
            ax.plot(hx, hy, 'k-', lw=1.3)
        else:
            xs_h = xbar[4] + 0.44
            u = np.linspace(0, 1, 60)
            hx = xs_h + (xbar[4] - xs_h) * u ** 0.72
            hy = yn + 0.24 * u
            ax.plot(hx, hy, 'k-', lw=1.3)
    for n in range(5):
        yn = ylev[n]
        if n > 0:
            ax.plot([x0 + 0.02, xbar[n]], [yn, yn], 'k--', lw=0.9)
        ax.plot([xbar[n], 6.90], [yn, yn], 'k-', lw=2.0, solid_capstyle='butt')
        ax.text(6.05, yn + 0.07, '$n=%d$' % n, fontsize=10, ha='left')
    ax.text(5.55, -0.70, '($b$)', fontsize=12, ha='center')

    save(fig, 172)


# ---------------------------------------------------------------- fig 173
def fig_173():
    """Magneto-optical transitions in a semiconductor with two hole bands."""
    fig = plt.figure(figsize=(4.4, 4.5))
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.set_xlim(-3.05, 3.05)
    ax.set_ylim(-3.35, 3.30)

    yC, yV = 1.05, -1.05
    # band-edge horizontal lines
    ax.plot([-2.75, 2.75], [yC, yC], 'k-', lw=0.8)
    ax.plot([-2.75, 2.75], [yV, yV], 'k-', lw=0.8)
    # central vertical axis (electron energy up, hole energy down)
    ax.plot([0, 0], [-2.95, 2.95], 'k-', lw=1.0)
    arrow(ax, (0, 2.55), (0, 3.05), lw=1.0, ms=11)
    arrow(ax, (0, -2.55), (0, -3.05), lw=1.0, ms=11)
    ax.text(0.10, 2.92, '$\\mathcal{E}_e$', fontsize=12, ha='left', va='bottom')
    ax.text(0.12, -2.88, '$\\mathcal{E}_h$', fontsize=12, ha='left', va='top')

    # energy gap arrow
    darrow(ax, (2.45, yV + 0.02), (2.45, yC - 0.02), lw=0.9)
    ax.text(2.52, 0, '$\\mathcal{E}_G$', fontsize=12, ha='left', va='center')

    xs = np.linspace(-1.95, 1.95, 400)
    # conduction band
    yec = yC + 0.62 * xs ** 2
    ax.plot(xs, yec, 'k-', lw=1.2)
    # conduction Landau levels
    wc = 0.36
    for n in range(4):
        yn = yC + (n + 0.5) * wc
        ax.plot([-1.85, 1.85], [yn, yn], 'k-', lw=1.1)
        ax.text(-0.60 - 0.05 * (3 - n), yn + 0.05, '%d' % n, fontsize=10,
                ha='right', va='bottom')
        if n < 2:
            ax.text(0.10, yn + 0.04, '$%d$' % n, fontsize=10, ha='left', va='bottom')
        elif n == 2:
            ax.text(0.28, yn + 0.04, '$2$', fontsize=10, ha='left', va='bottom')
        else:
            ax.text(0.95, yn + 0.04, '$n=3$', fontsize=10, ha='left', va='bottom')
    darrow(ax, (0.75, yC + 2.5 * wc), (0.75, yC + 3.5 * wc), lw=0.9)
    ax.text(0.68, yC + 3.0 * wc, '$\\hbar\\omega_e$', fontsize=10, ha='right', va='center')
    ax.text(1.60, yC + 3.30 * wc + 0.10, 'cyclotron\nresonance', fontsize=10,
            ha='left', va='center')

    # two hole bands: light (steep) and heavy (shallow)
    ylh = yV - 0.95 * xs ** 2
    yhh = yV - 0.48 * xs ** 2
    ax.plot(xs, ylh, 'k-', lw=1.2)
    ax.plot(xs, yhh, 'k-', lw=1.2)
    # light-hole ladder (left), heavy-hole ladder (right)
    whL, whR = 0.30, 0.27
    for n in range(5):
        yn = yV - (n + 0.5) * whL
        ax.plot([-1.80, -0.10], [yn, yn], 'k-', lw=1.1)
        if n < 4:
            ax.text(-0.62 - 0.14 * n, yn + 0.04, '$%d$' % n, fontsize=10,
                    ha='right', va='bottom')
        else:
            ax.text(-1.88, yn - 0.02, '$n=4$', fontsize=10, ha='right', va='center')
    for n in range(5):
        yn = yV - (n + 0.5) * whR
        ax.plot([0.10, 1.80], [yn, yn], 'k-', lw=1.1)
        if n == 0:
            ax.text(0.55, yn - 0.05, '$0$', fontsize=10, ha='left', va='top')
        else:
            ax.text(0.60 + 0.28 * n, yn - 0.05, '$%d$' % n, fontsize=10,
                    ha='left', va='top')
    # long level line labelled n = 1 at the bottom (heavy band, drawn long)
    ax.plot([-1.05, 1.05], [-2.68, -2.68], 'k-', lw=1.1)
    ax.text(0.38, -2.76, '$n=1$', fontsize=10, ha='left', va='top')
    darrow(ax, (-0.45, yV - 2.5 * whL), (-0.45, yV - 3.5 * whL), lw=0.9)
    ax.text(-0.38, yV - 3.0 * whL - 0.02, '$\\hbar\\omega_h$', fontsize=10,
            ha='left', va='center')

    # vertical transition arrows (Delta n = 0)
    arrow(ax, (-1.35, yV - 3.5 * whL + 0.05), (-1.35, yC + 3.5 * wc - 0.03), lw=1.0, ms=10)
    arrow(ax, (-0.82, yV - 0.5 * whL + 0.05), (-0.82, yC + 0.5 * wc - 0.03), lw=1.0, ms=10)
    arrow(ax, (0.35, yV - 0.5 * whR + 0.05), (0.35, yC + 0.5 * wc - 0.03), lw=1.0, ms=10)
    arrow(ax, (0.68, yV - 1.5 * whR + 0.05), (0.68, yC + 1.5 * wc - 0.03), lw=1.0, ms=10)

    save(fig, 173)


# ---------------------------------------------------------------- fig 174
def fig_174():
    """(a) Free-electron orbit crossing a zone boundary; (b) orbits
    reconnected at the zone boundary (lenses + open orbit)."""
    fig = plt.figure(figsize=(4.8, 2.25))
    ax = fig.add_axes([0.01, 0.03, 0.98, 0.94])
    ax.set_axis_off()
    ax.set_aspect('equal')
    ax.set_xlim(0, 6.35)
    ax.set_ylim(-0.55, 2.45)

    # ---------------- (a)
    c1, c2, r = (0.98, 1.05), (1.90, 1.05), 0.72
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(c1[0] + r * np.cos(th), c1[1] + r * np.sin(th), 'k-', lw=1.4)
    ax.plot(c2[0] + r * np.cos(th), c2[1] + r * np.sin(th), 'k--', lw=1.4)
    # zone planes: left tangent, central secant, right tangent
    for x in (c1[0] - r, 0.5 * (c1[0] + c2[0]), c2[0] + r):
        ax.plot([x, x], [0.02, 2.08], 'k-', lw=0.8)
    ax.text(0.5 * (c1[0] + c2[0]), -0.12, 'Z.B.', fontsize=10, ha='center', va='top')
    # direction arrows (clockwise on both circles)
    p0, p1 = circ_pts(c1, r, 84), circ_pts(c1, r, 70)
    arrow(ax, p0, p1, lw=1.1, ms=11)
    p0, p1 = circ_pts(c1, r, -46), circ_pts(c1, r, -64)
    arrow(ax, p0, p1, lw=1.1, ms=11)
    p0, p1 = circ_pts(c2, r, 152), circ_pts(c2, r, 132)
    arrow(ax, p0, p1, lw=1.1, ms=11)
    # labels
    xt = 0.5 * (c1[0] + c2[0])
    ax.text(xt - 0.10, 1.66, '$A$', fontsize=12, ha='right', va='center')
    ax.text(c2[0] + 0.28, 0.92, '$B$', fontsize=12, ha='left')
    ax.text(c2[0] + 0.30, 1.92, '$C$', fontsize=12, ha='left')
    ax.text(1.44, -0.48, '($a$)', fontsize=12, ha='center')

    # ---------------- (b)
    xL = [3.15, 4.30, 5.45]
    cy = 1.05
    for x in xL:
        ax.plot([x, x], [0.02, 2.08], 'k-', lw=0.8)
    ax.text(4.30, -0.12, 'Z.B.', fontsize=10, ha='center', va='top')
    # remnants of the free-electron circles (dashed arcs, top and bottom)
    r2 = 0.82
    for xc in (3.725, 4.875):
        for a0, a1 in [(28, 152), (208, 332)]:
            tt = np.linspace(np.deg2rad(a0), np.deg2rad(a1), 120)
            ax.plot(xc + r2 * np.cos(tt), cy + r2 * np.sin(tt), 'k--', lw=1.2)
    # lenses centred on zone planes
    for x in xL:
        ax.add_patch(Ellipse((x, cy), 0.30, 1.18, facecolor='white',
                             edgecolor='k', lw=1.3, zorder=4))
    # open orbits across the tops and bottoms of the lenses
    xs = np.linspace(2.72, 5.88, 400)
    ytop = 1.775 - 0.135 * np.cos(2 * np.pi * (xs - xL[0]) / 1.15)
    ybot = 0.325 + 0.135 * np.cos(2 * np.pi * (xs - xL[0]) / 1.15)
    ax.plot(xs, ytop, 'k-', lw=1.3, zorder=5)
    ax.plot(xs, ybot, 'k-', lw=1.3, zorder=5)

    def y_top(x):
        return 1.775 - 0.135 * np.cos(2 * np.pi * (x - xL[0]) / 1.15)

    def y_bot(x):
        return 0.325 + 0.135 * np.cos(2 * np.pi * (x - xL[0]) / 1.15)

    # arrows and labels
    arrow(ax, (4.52, y_top(4.52)), (4.80, y_top(4.80)), lw=1.1, ms=11)
    arrow(ax, (4.44, cy + 0.30), (4.44, cy - 0.02), lw=1.0, ms=10)
    arrow(ax, (4.05, y_bot(4.05)), (3.78, y_bot(3.78)), lw=1.1, ms=11)
    ax.text(4.40, 1.80, '$A$', fontsize=12, ha='left', va='bottom')
    ax.text(4.92, 2.02, '$C$', fontsize=12, ha='left')
    ax.text(4.55, 0.98, '$B$', fontsize=12, ha='left')
    ax.text(4.30, -0.48, '($b$)', fontsize=12, ha='center')

    save(fig, 174)


# ---------------------------------------------------------------- driver
ALL = [fig_164, fig_165, fig_166, fig_167, fig_168,
       fig_169, fig_170, fig_171, fig_172, fig_173, fig_174]

if __name__ == '__main__':
    import sys
    want = [int(a) for a in sys.argv[1:]] or [f.__name__.split('_')[1] for f in ALL]
    for f in ALL:
        num = int(f.__name__.split('_')[1])
        if num in want:
            f()
