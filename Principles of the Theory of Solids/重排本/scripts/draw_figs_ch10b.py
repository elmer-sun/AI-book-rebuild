# -*- coding: utf-8 -*-
"""Redraw Ziman, Principles of the Theory of Solids, 2nd ed., Chapter 10 (part 2),
Figs. 187-198 (Magnetism: order-disorder, Ising, spin waves, antiferromagnetism).
Black-and-white textbook-style vector figures.

Figures and their sources (page PNGs under 齐曼/原书转换/pages):
  187  p372  Specific heat, quasi-chemical approximation (lambda singularity)
  188  p374  Bethe-Peierls cluster (hatched atoms, H / H_I axes, J links)
  189  p375  (a) long-range order implies short-range order, (b) converse false
  190  p377  Specific heat of linear chain (Schottky peak)
  191  p378  Long-range order in linear chain (a) destroyed by a single break (b)
  192  p378  A region of reversed spins (square Ising lattice, heavy boundary)
  193  p379  Specific heat of quadratic layer lattice: Onsager formula (log divergence)
  194  p380  Triangular layer lattice (a) and simple cubic lattice (b), p = 6
  195  p381  Operator S†S exchanges spin deviations, (a) -> (b)
  196  p386  Axes of quantization of antiferromagnetic system
  197  p390  AF ordered state (a); exchange operator creates two spin deviations (b)
  198  p391  AF array (a) can rotate bodily without change of energy (b)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import numpy as np
import os

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


def arrow(ax, p0, p1, lw=1.1, ms=10, zorder=9):
    ax.annotate('', xy=p1, xytext=p0, zorder=zorder,
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def stipple_disc(ax, xy, r, n=120, s=0.5, seed=0, zorder=3):
    """Scatter small dots uniformly inside a disc (stippled atom)."""
    rng = np.random.default_rng(seed)
    pts = []
    while len(pts) < n:
        p = rng.uniform(-r, r, (2 * n, 2))
        for px, py in p:
            if px * px + py * py <= r * r * 0.95:
                pts.append((xy[0] + px, xy[1] + py))
                if len(pts) >= n:
                    break
    arr = np.array(pts)
    ax.scatter(arr[:, 0], arr[:, 1], s=s, c='k', linewidths=0, zorder=zorder)


def clipped_disc(ax, xy, r, ang, keep=0.55, lw=1.2, zorder=2):
    """Hatched disc cut by a chord; the side toward direction `ang` is kept.
    Draws the hatched part plus a stroke on the chord."""
    ux, uy = np.cos(ang), np.sin(ang)
    nx, ny = -uy, ux
    c = r * (2.0 * keep - 1.0)
    t = np.sqrt(max(r * r - c * c, 1e-9))
    cx, cy = xy[0] + c * ux, xy[1] + c * uy
    p1 = (cx + t * nx, cy + t * ny)
    p2 = (cx - t * nx, cy - t * ny)
    L = 4.0 * r
    poly = mpatches.Polygon([p1, p2, (p2[0] + L * ux, p2[1] + L * uy),
                             (p1[0] + L * ux, p1[1] + L * uy)],
                            closed=True, facecolor='none', edgecolor='none')
    ax.add_patch(poly)
    circ = mpatches.Circle(xy, r, facecolor='none', edgecolor='k',
                           hatch='///', lw=lw, zorder=zorder)
    ax.add_patch(circ)
    circ.set_clip_path(poly)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='k', lw=lw * 0.8,
            zorder=zorder + 1, solid_capstyle='round')


def dashed_axis(ax, x, ylo, yhi, head='up', dash=(0, (5, 4)), lw=1.0, ms=5, zorder=5):
    """Vertical dashed quantization axis with a small solid arrowhead."""
    ax.plot([x, x], [ylo, yhi], linestyle=dash, color='k', lw=lw, zorder=zorder)
    yh = yhi if head == 'up' else ylo
    m = '^' if head == 'up' else 'v'
    ax.plot([x], [yh], marker=m, ms=ms, color='k', zorder=zorder)


def spin(ax, xy, tilt_deg, half=0.26, dot=0.0, lw=1.3, ms=10, dashed=False,
         zorder=6, tail_frac=1.0):
    """A spin: straight shaft through xy at angle tilt_deg (from vertical,
    +=right), optional centre dot, arrowhead at the + end."""
    th = np.deg2rad(tilt_deg)
    ux, uy = np.sin(th), np.cos(th)
    p0 = (xy[0] - half * ux * (2 - tail_frac), xy[1] - half * uy * (2 - tail_frac))
    p1 = (xy[0] + half * ux, xy[1] + half * uy)
    if dashed:
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], linestyle=(0, (3, 3)), color='k',
                lw=lw, zorder=zorder)
    arrow(ax, p0, p1, lw=lw, ms=ms, zorder=zorder)
    if dot:
        ax.plot([xy[0]], [xy[1]], marker='o', ms=dot, color='k', zorder=zorder + 1)


def brace(ax, x0, x1, y, h, tip='down', lw=1.1, zorder=6):
    """Horizontal curly brace from x0 to x1 at height y; the centre cusp points
    'down' or 'up', the end hooks curl the other way."""
    xm = 0.5 * (x0 + x1)
    s = -1.0 if tip == 'down' else 1.0
    e = -s
    hb = 0.55 * h
    w = x1 - x0
    verts = [(x0, y + e * hb),
             (x0, y), (x0 + 0.08 * w, y),
             (xm, y), (xm, y + s * h),
             (x1 - 0.08 * w, y), (x1, y),
             (x1, y), (x1, y + e * hb)]
    codes = [mpath.Path.MOVETO] + [mpath.Path.CURVE3] * 8
    ax.add_patch(mpatches.PathPatch(mpath.Path(verts, codes), fill=False,
                                    lw=lw, edgecolor='k', capstyle='round',
                                    zorder=zorder))


# ---------------------------------------------------------------- fig 187
def fig_187():
    fig, ax = plt.subplots(figsize=(3.4, 3.05))
    xc, ymax = 0.63, 2.45
    # axes
    ax.plot([0, 1.03], [0, 0], color='k', lw=1.3)
    ax.plot([0, 0], [0, 2.62], color='k', lw=1.3)
    for yv in (1.0, 2.0):
        ax.plot([-0.018, 0.0], [yv, yv], color='k', lw=1.1)
        ax.text(-0.05, yv, '%d' % yv, ha='right', va='center', fontsize=11)
    ax.text(-0.16, 1.32, r'$C/Nk$', ha='center', va='center', fontsize=12, rotation=90)
    # vertical line at Tc
    ax.plot([xc, xc], [0, ymax], color='k', lw=0.7)
    ax.text(xc, -0.16, r'$T_c$', ha='center', va='top', fontsize=12)
    # left branch (convex rise to the lambda point)
    xl = np.linspace(0.10, xc, 300)
    yl = ymax * ((xl - 0.10) / (xc - 0.10)) ** 3.0
    ax.plot(xl, yl, color='k', lw=1.5)
    # right branch: discontinuous drop, slow decay
    xr = np.linspace(xc, 1.0, 300)
    yr = 0.05 + 0.27 * np.exp(-(xr - xc) / 0.13)
    ax.plot(xr, yr, color='k', lw=1.5)
    ax.text(0.685, 0.27, 'Short-range order', fontsize=9.5, ha='left', va='bottom')
    ax.set_xlim(-0.34, 1.10)
    ax.set_ylim(-0.34, 2.75)
    ax.axis('off')
    save(fig, 187)


# ---------------------------------------------------------------- fig 188
def fig_188():
    fig, ax = plt.subplots(figsize=(3.9, 4.15))
    R = 0.375                      # atom radius
    a = 1.0                        # pitch
    dy = 0.87
    C = (0.0, 0.0)
    nb = {'TL': (-0.5, dy), 'TR': (0.5, dy),
          'ML': (-a, 0.0), 'MR': (a, 0.0),
          'BL': (-0.5, -dy), 'BR': (0.5, -dy)}
    # peripheral broken atoms (second shell), chord faces the cluster
    periph = [(-1.3, 1.41), (-0.13, 1.61), (0.85, 1.62),
              (1.3, 0.955), (1.7, 0.043), (1.41, -0.80),
              (-1.5, 0.87), (-1.78, -0.02), (-1.46, -0.87),
              (-0.87, -1.54), (-0.02, -1.61), (0.87, -1.52)]
    keeps = [0.50, 0.55, 0.45, 0.50, 0.38, 0.45,
             0.50, 0.35, 0.45, 0.45, 0.55, 0.45]
    for (px, py), kp in zip(periph, keeps):
        ang = np.arctan2(-py, -px)
        clipped_disc(ax, (px * 1.18, py * 1.18), R, ang, keep=kp)
    # dashed exchange links J from central atom to its neighbours
    for pos in nb.values():
        ax.plot([C[0], pos[0]], [C[1], pos[1]], linestyle=(0, (5, 4)),
                color='k', lw=0.9, zorder=4)
    ax.text(0.54, 0.045, r'$J$', fontsize=12, ha='left', va='bottom', zorder=8)
    ax.text(0.30, -0.50, r'$J$', fontsize=12, ha='left', va='top', zorder=8)
    # small arrowhead on the right-hand J link
    arrow(ax, (0.60, 0.0), (0.76, 0.0), lw=1.0, ms=8, zorder=6)
    # the seven atoms (hatched)
    for pos in list(nb.values()) + [C]:
        ax.add_patch(mpatches.Circle(pos, R, facecolor='none', edgecolor='k',
                                     hatch='//////', lw=1.25, zorder=5))
    # dashed local quantization axes with upward arrowheads
    for pos in [C, nb['TR'], nb['ML'], nb['MR'], nb['BR']]:
        dashed_axis(ax, pos[0], pos[1] - 0.56, pos[1] + 0.74, head='up')
    # plain thin spin arrows on TL and BL
    for pos in [nb['TL'], nb['BL']]:
        arrow(ax, (pos[0], pos[1] - 0.46), (pos[0], pos[1] + 0.60), lw=1.0, ms=9)
    # thick spin "needles"
    spin(ax, nb['TR'], -12, half=0.42, lw=1.6, ms=9)
    spin(ax, nb['ML'], 40, half=0.42, lw=1.6, ms=9)
    spin(ax, nb['MR'], 8, half=0.42, lw=1.6, ms=9)
    spin(ax, nb['BR'], 225, half=0.42, lw=1.6, ms=9)
    # central spin S0: three thick vectors
    spin(ax, C, 45, half=0.40, lw=1.6, ms=9)
    spin(ax, C, 86, half=0.32, lw=1.6, ms=9)
    # SW needle starts away from the centre so the S0 label stays readable
    th = np.deg2rad(225)
    arrow(ax, (0.12 * np.sin(th), 0.12 * np.cos(th)),
          (0.44 * np.sin(th), 0.44 * np.cos(th)), lw=1.6, ms=9)
    # centre dots
    for pos in list(nb.values()) + [C]:
        ax.plot([pos[0]], [pos[1]], marker='o', ms=4.5, color='k', zorder=8)
    # labels
    ax.text(0.07, 0.86, r'$H$', fontsize=12, ha='left', va='bottom', zorder=8)
    ax.text(nb['TR'][0] + 0.08, nb['TR'][1] + 0.82, r'$H_I$', fontsize=12,
            ha='left', va='bottom', zorder=8)
    ax.text(nb['ML'][0] - 0.08, nb['ML'][1] + 0.82, r'$H_I$', fontsize=12,
            ha='right', va='bottom', zorder=8)
    ax.text(nb['MR'][0] + 0.08, nb['MR'][1] + 0.82, r'$H_I$', fontsize=12,
            ha='left', va='bottom', zorder=8)
    ko = dict(facecolor='white', edgecolor='none', pad=0.8)
    ax.text(-0.24, 0.16, r'$S_0$', fontsize=12, ha='right', va='center',
            zorder=8, bbox=ko)
    ax.text(nb['BL'][0] - 0.16, nb['BL'][1] - 0.12, r'$S_j$', fontsize=12,
            ha='right', va='center', zorder=8, bbox=ko)
    ax.set_xlim(-2.35, 2.35)
    ax.set_ylim(-2.25, 2.25)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 188)


# ---------------------------------------------------------------- fig 189
def fig_189():
    fig, ax = plt.subplots(figsize=(4.6, 3.7))

    def group(y0, tilts, brace_spans, panel):
        xs = np.arange(len(tilts)) * 0.55
        for x, t in zip(xs, tilts):
            spin(ax, (x, y0), t, half=0.24, dot=4.5, lw=1.1, ms=8.5)
        (bx0, bx1, by, tip, lab, ly) = brace_spans[0]
        brace(ax, bx0, bx1, y0 + by, 0.13, tip=tip)
        ax.text(0.5 * (bx0 + bx1), y0 + by + (0.24 if tip == 'down' else -0.26),
                lab, fontsize=10.5, ha='center',
                va='bottom' if tip == 'down' else 'top')
        if len(brace_spans) > 1:
            (bx0, bx1, by, tip, lab, ly) = brace_spans[1]
            brace(ax, bx0, bx1, y0 + by, 0.13, tip=tip)
            ax.text(0.5 * (bx0 + bx1), y0 + by + (0.24 if tip == 'down' else -0.26),
                    lab, fontsize=10.5, ha='center',
                    va='bottom' if tip == 'down' else 'top')
        ax.text(0.80 * xs[-1], y0 - 1.00, '(%s)' % panel, fontsize=11.5,
                ha='center', va='top')

    # (a): long-range order -> short-range order
    group(0.0, [0, 28, 0, -28, 0, 28, -30, 0, 30, 35],
          [(-0.18, 5.08, 0.55, 'down', 'Long-range order', 0),
           (-0.18, 1.28, -0.55, 'up', 'Short-range order', 0)], 'a')
    # (b): short-range order does not imply long-range order
    group(-2.55, [0, 28, 2, -50, -90, -55, -122, -165, -115, -172, 172, 150],
          [(-0.18, 5.63, 0.55, 'down', 'Long-range disorder', 0),
           (1.32, 2.62, -0.55, 'up', 'Short-range order', 0)], 'b')
    ax.set_xlim(-0.45, 6.25)
    ax.set_ylim(-4.35, 1.15)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 189)


# ---------------------------------------------------------------- fig 190
def fig_190():
    fig, ax = plt.subplots(figsize=(3.05, 3.35))
    ax.plot([0, 2.06], [0, 0], color='k', lw=1.3)
    ax.plot([0, 0], [0, 0.555], color='k', lw=1.3)
    # ticks
    ax.plot([-0.018, 0], [0.5, 0.5], color='k', lw=1.1)
    ax.text(-0.045, 0.5, r'0$\cdot$5', ha='right', va='center', fontsize=11)
    ax.text(-0.045, -0.012, r'0', ha='right', va='top', fontsize=11)
    ax.plot([1, 1], [0, -0.012], color='k', lw=1.1)
    ax.text(1, -0.045, r'1', ha='center', va='top', fontsize=11)
    ax.text(1.98, -0.10, r'$kT/J$', ha='center', va='top', fontsize=12)
    ax.text(-0.13, 0.28, r'$C/Nk$', ha='center', va='center', fontsize=12, rotation=90)
    x = np.linspace(1e-4, 2.05, 1200)
    y = (1.0 / x ** 2) / (np.cosh(1.0 / x)) ** 2
    y = np.concatenate([[0.0], y])
    x = np.concatenate([[0.0], x])
    ax.plot(x, y, color='k', lw=1.5)
    ax.set_xlim(-0.35, 2.20)
    ax.set_ylim(-0.20, 0.60)
    ax.axis('off')
    save(fig, 190)


# ---------------------------------------------------------------- fig 191
def fig_191():
    fig, ax = plt.subplots(figsize=(3.8, 1.55))

    def plus(ax, x, y, s=0.085, lw=1.6):
        ax.plot([x - s, x + s], [y, y], color='k', lw=lw, solid_capstyle='butt')
        ax.plot([x, x], [y - s, y + s], color='k', lw=lw, solid_capstyle='butt')

    def minus(ax, x, y, s=0.085, lw=1.6):
        ax.plot([x - s, x + s], [y, y], color='k', lw=lw, solid_capstyle='butt')

    ya, yb = 0.0, -0.62
    for i in range(9):
        plus(ax, i * 0.5, ya)
    ax.text(4 * 0.5, ya - 0.22, '($a$)', fontsize=11.5, ha='center', va='top')
    for i in range(4):
        plus(ax, i * 0.5, yb)
    for i in range(5):
        minus(ax, (i + 5) * 0.5, yb)
    # the break: an up arrow just below the row at the 4.5th position
    arrow(ax, (4.5 * 0.5, yb - 0.34), (4.5 * 0.5, yb + 0.02), lw=1.3, ms=10)
    ax.text(4.5 * 0.5, yb - 0.44, '($b$)', fontsize=11.5, ha='center', va='top')
    ax.set_xlim(-0.35, 4.95)
    ax.set_ylim(-1.35, 0.30)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 191)


# ---------------------------------------------------------------- fig 192
def fig_192():
    fig, ax = plt.subplots(figsize=(3.0, 3.0))
    minus_cells = [(2, 3), (2, 4), (2, 5),
                   (3, 3), (3, 4),
                   (4, 3), (4, 4),
                   (5, 2), (5, 3), (5, 4),
                   (6, 3)]
    mset = set(minus_cells)
    # grid lines
    g0, g1 = -0.28, 7.28
    for i in range(8):
        ax.plot([i, i], [g0, g1], color='k', lw=0.8, zorder=1)
        ax.plot([g0, g1], [i, i], color='k', lw=0.8, zorder=1)
    # heavy boundary polygon of the reversed region
    poly = [(2, 1), (5, 1), (5, 2), (4, 2), (4, 5), (3, 5), (3, 6),
            (2, 6), (2, 5), (1, 5), (1, 4), (2, 4), (2, 2), (2, 1)]
    ax.plot([p[0] for p in poly], [p[1] for p in poly], color='k', lw=2.2,
            zorder=3, solid_capstyle='round', solid_joinstyle='miter')
    # signs
    s = 0.13
    for r in range(1, 8):
        for c in range(1, 8):
            x, y = c - 0.5, r - 0.5
            if (r, c) in mset:
                ax.plot([x - s, x + s], [y, y], color='k', lw=1.5, zorder=2)
            else:
                ax.plot([x - s, x + s], [y, y], color='k', lw=1.5, zorder=2)
                ax.plot([x, x], [y - s, y + s], color='k', lw=1.5, zorder=2)
    ax.set_xlim(-0.42, 7.42)
    ax.set_ylim(7.42, -0.42)   # row 1 at top
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 192)


# ---------------------------------------------------------------- fig 193
def fig_193():
    fig, ax = plt.subplots(figsize=(3.45, 3.15))
    xc, top = 0.655, 3.0
    # box frame
    ax.plot([0, 1.0, 1.0, 0, 0], [0, 0, top, top, 0], color='k', lw=1.2)
    # y ticks
    for yv in (1, 2, 3):
        ax.plot([0, 0.028], [yv, yv], color='k', lw=1.1)
        ax.text(-0.035, yv, '%d' % yv, ha='right', va='center', fontsize=11)
    ax.text(-0.13, 1.5, r'$C/Nk$', ha='center', va='center', fontsize=12, rotation=90)
    # Tc tick and label; extended T axis with arrow
    ax.plot([xc, xc], [0, -0.07], color='k', lw=1.1)
    ax.text(xc, -0.13, r'$T_c$', ha='center', va='top', fontsize=12)
    arrow(ax, (1.0, 0.0), (1.10, 0.0), lw=1.2, ms=10)
    ax.text(1.06, -0.13, r'$T$', ha='center', va='top', fontsize=12)

    def logterm(dx, a=1.65, b=0.045):
        return a * np.log(1.0 + b / np.maximum(dx, 1e-6))

    # left branch (T < Tc): rises from the axis and diverges at Tc
    xl = np.linspace(0.227, xc - 1e-4, 500)
    dxl = xc - xl
    yl = logterm(dxl) - logterm(0.428)
    yl = np.minimum(yl, top)
    ax.plot(xl, yl, color='k', lw=1.5)
    # right branch (T > Tc): diverges, then slow decay
    xr = np.linspace(xc + 1e-4, 1.0, 500)
    dxr = xr - xc
    yr = logterm(dxr)
    yr = np.minimum(yr, top)
    yr = yr * (1.0 - 0.5 * np.clip((dxr - 0.12) / 0.22, 0.0, 1.0))
    ax.plot(xr, yr, color='k', lw=1.5)
    ax.set_xlim(-0.22, 1.24)
    ax.set_ylim(-0.34, 3.28)
    ax.axis('off')
    save(fig, 193)


# ---------------------------------------------------------------- fig 194
def fig_194():
    fig, ax = plt.subplots(figsize=(4.75, 2.05))
    # ---- (a) triangular layer lattice
    rows = [(np.arange(5) - 2.0, 1.30),
            (np.arange(4) - 1.5, 0.433),
            (np.arange(5) - 2.0, -0.433),
            (np.arange(4) - 1.5, -1.30)]
    sites = []
    for xs, y in rows:
        for x in xs:
            sites.append((x, y))
    sites = np.array(sites)
    # bonds at unit distance
    for i in range(len(sites)):
        for j in range(i + 1, len(sites)):
            d = np.hypot(*(sites[i] - sites[j]))
            if abs(d - 1.0) < 1e-6:
                ax.plot([sites[i][0], sites[j][0]], [sites[i][1], sites[j][1]],
                        color='k', lw=1.1, zorder=2)
    # thick six-coordination star at the centre site (-0.5, 0.433)
    c0 = np.array([-0.5, 0.433])
    for k, sg in ((0, 1),):
        pass
    neigh = [c0 + np.array(v) for v in
             [(-1, 0), (1, 0), (-0.5, 0.866), (0.5, 0.866),
              (-0.5, -0.866), (0.5, -0.866)]]
    for p in neigh:
        ax.plot([c0[0], p[0]], [c0[1], p[1]], color='k', lw=3.0,
                zorder=3, solid_capstyle='round')
    for (x, y) in sites:
        ax.add_patch(mpatches.Circle((x, y), 0.085, facecolor='white',
                                     edgecolor='k', lw=1.2, zorder=5))
    ax.text(-0.5, -1.95, '($a$)', fontsize=11.5, ha='center', va='top')
    # ---- (b) simple cubic lattice (oblique projection)
    ox, oy = 5.15, 0.0
    dxz, dyz = 0.52, 0.40          # depth offset per unit k
    pts = {}
    for i in range(3):
        for j in range(3):
            for k in range(3):
                pts[(i, j, k)] = (ox + i + k * dxz, oy + j + k * dyz)
    # bonds (drawn back-to-front roughly by k)
    for k in range(3):
        for i in range(3):
            for j in range(3):
                p = pts[(i, j, k)]
                if i < 2:
                    q = pts[(i + 1, j, k)]
                    ax.plot([p[0], q[0]], [p[1], q[1]], color='k', lw=0.9, zorder=2)
                if j < 2:
                    q = pts[(i, j + 1, k)]
                    ax.plot([p[0], q[0]], [p[1], q[1]], color='k', lw=0.9, zorder=2)
                if k < 2:
                    q = pts[(i, j, k + 1)]
                    ax.plot([p[0], q[0]], [p[1], q[1]], color='k', lw=0.9, zorder=2)
    # thick six-coordination star at the body-centre site (1,1,1)
    c1 = np.array(pts[(1, 1, 1)])
    for d in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
        q = np.array(pts[tuple(np.array((1, 1, 1)) + np.array(d))])
        ax.plot([c1[0], q[0]], [c1[1], q[1]], color='k', lw=3.0,
                zorder=3, solid_capstyle='round')
    for p in pts.values():
        ax.add_patch(mpatches.Circle(p, 0.075, facecolor='white',
                                     edgecolor='k', lw=1.2, zorder=5))
    ax.text(ox + 1.52, -1.95 + 0.0, '($b$)', fontsize=11.5, ha='center', va='top')
    ax.set_xlim(-2.75, 8.55)
    ax.set_ylim(-2.45, 3.05)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 194)


# ---------------------------------------------------------------- fig 195
def fig_195():
    fig, ax = plt.subplots(figsize=(4.6, 1.6))
    for grp, dev in ((0.0, 2), (0.0, 3)):
        pass
    x0a, x0b = 0.0, 4.1
    for x0, devsite, panel in ((x0a, 2, 'a'), (x0b, 3, 'b')):
        for i in range(6):
            x = x0 + i * 0.55
            spin(ax, (x, 0.0), 0, half=0.27, dot=4.5, lw=1.15, ms=9)
            if i == devsite:
                spin(ax, (x, 0.0), 55, half=0.46, lw=1.1, ms=10)
        ax.text(x0 + 2 * 0.55, 0.44, r'$l$', fontsize=12, ha='center', va='bottom')
        ax.text(x0 + 3 * 0.55, 0.44, r"$l'$", fontsize=12, ha='center', va='bottom')
        ax.text(x0 + 2 * 0.55, -0.62, '($%s$)' % panel, fontsize=11.5,
                ha='center', va='top')
    ax.set_xlim(-0.5, 7.4)
    ax.set_ylim(-1.05, 0.85)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 195)


# ---------------------------------------------------------------- fig 196
def fig_196():
    fig, ax = plt.subplots(figsize=(3.25, 3.4))
    dx, dy, r = 1.0, 1.35, 0.33
    tilts = [[38, -8, -34, 28],
             [-35, 30, -6, -32],
             [5, -28, 33, -20]]
    for ri in range(3):
        for ci in range(4):
            x, y = ci * dx, -ri * dy
            up = ((ri + ci) % 2 == 0)
            ax.add_patch(mpatches.Circle((x, y), r, facecolor='none',
                                         edgecolor='k', lw=1.2, zorder=4))
            stipple_disc(ax, (x, y), r, n=110, s=0.5, seed=100 + 4 * ri + ci)
            dashed_axis(ax, x, y - 0.55, y + 0.55, head='up' if up else 'down',
                        ms=5.5)
            spin(ax, (x, y), tilts[ri][ci] if up else 180 + tilts[ri][ci],
                 half=0.26, lw=1.7, ms=10)
            ax.plot([x], [y], marker='o', ms=4, color='k', zorder=8)
    ax.text(3 * dx + 0.10, 0.68, r'$H_A$', fontsize=12,
            ha='left', va='bottom')
    ax.set_xlim(-0.75, 4.15)
    ax.set_ylim(-3.55, 1.05)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 196)


# ---------------------------------------------------------------- fig 197
def fig_197():
    fig, ax = plt.subplots(figsize=(4.6, 1.5))
    for x0, panel in ((0.0, 'a'), (4.6, 'b')):
        for i in range(7):
            x = x0 + i * 0.55
            if panel == 'b' and i in (2, 3):
                # dashed remnants of the ordered spin
                ax.plot([x, x], [-0.24, 0.24], linestyle=(0, (3, 3)),
                        color='k', lw=1.0, zorder=5)
            else:
                t = 0 if i % 2 == 0 else 180
                spin(ax, (x, 0.0), t, half=0.26, lw=1.15, ms=9)
        ax.text(x0 + 2 * 0.55, 0.46, r'$l$', fontsize=12, ha='center', va='bottom')
        ax.text(x0 + 3 * 0.55, 0.46, r"$l'$", fontsize=12, ha='center', va='bottom')
        ax.text(x0 + 1.1, -0.72, '($%s$)' % panel, fontsize=11.5,
                ha='center', va='top')
    # the two created deviations in (b)
    spin(ax, (4.6 + 2 * 0.55, 0.0), 40, half=0.33, lw=1.5, ms=11)
    spin(ax, (4.6 + 3 * 0.55, 0.0), 140, half=0.33, lw=1.5, ms=11)
    ax.set_xlim(-0.5, 8.4)
    ax.set_ylim(-1.1, 0.85)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 197)


# ---------------------------------------------------------------- fig 198
def fig_198():
    fig, ax = plt.subplots(figsize=(4.8, 2.5))
    dx, dy, r = 1.0, 1.0, 0.35
    for arr, (ox, oy) in (('a', (0.0, 0.0)), ('b', (5.4, 0.0))):
        for ri in range(4):
            for ci in range(4):
                x, y = ox + ci * dx, oy - ri * dy
                up = ((ri + ci) % 2 == 0)
                ax.add_patch(mpatches.Circle((x, y), r, facecolor='none',
                                             edgecolor='k', lw=1.2, zorder=4))
                stipple_disc(ax, (x, y), r, n=120, s=0.5,
                             seed=7 + 4 * ri + ci + (0 if arr == 'a' else 50))
                if arr == 'a':
                    tilt = 0 if up else 180
                else:
                    tilt = 40 if up else 220   # bodily clockwise rotation
                spin(ax, (x, y), tilt, half=0.24, lw=1.5, ms=9)
                ax.plot([x], [y], marker='o', ms=4, color='k', zorder=8)
        ax.text(ox + 1.5, oy - 3.85, '($%s$)' % arr, fontsize=11.5,
                ha='center', va='top')
    ax.set_xlim(-0.85, 8.0)
    ax.set_ylim(-4.55, 0.85)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, 198)


# ---------------------------------------------------------------- driver
ALL = [fig_187, fig_188, fig_189, fig_190, fig_191, fig_192,
       fig_193, fig_194, fig_195, fig_196, fig_197, fig_198]

if __name__ == '__main__':
    import sys
    want = [int(a) for a in sys.argv[1:]] or [int(f.__name__.split('_')[1]) for f in ALL]
    for f in ALL:
        num = int(f.__name__.split('_')[1])
        if num in want:
            f()
