# -*- coding: utf-8 -*-
"""Ziman, Principles of the Theory of Solids (2nd ed.), Chapter 2, Figs. 26-35.
Black-and-white textbook-style vector redraws. One function per figure."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
    'hatch.linewidth': 0.5,
})

BASE = r'E:\AI整理书籍\齐曼\重排本'
FIGD = os.path.join(BASE, 'figures')
PREV = os.path.join(FIGD, 'preview')
os.makedirs(PREV, exist_ok=True)


def save(fig, key):
    fig.savefig(os.path.join(FIGD, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV, 'fig_%s.png' % key),
                dpi=200, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)
    print('fig_%s done' % key)


def ax_on(fig, rect, xlim, ylim, aspect='equal'):
    ax = fig.add_axes(rect)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.axis('off')
    if aspect == 'equal':
        ax.set_aspect('equal', adjustable='box')
    return ax


def arr(ax, p0, p1, ms=11, lw=0.0, style='-|>', z=6):
    """arrowhead-carrying arrow (optionally a short visible shaft if lw>0)."""
    ax.annotate('', xy=tuple(p1), xytext=tuple(p0),
                arrowprops=dict(arrowstyle=style, color='k', lw=lw,
                                shrinkA=0, shrinkB=0, mutation_scale=ms),
                zorder=z)


def seg(ax, p0, p1, lw=1.2, ls='-', z=3):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color='k', lw=lw, ls=ls,
            solid_capstyle='butt', zorder=z)


def polyline(ax, pts, lw=1.2, ls='-', z=3):
    pts = np.asarray(pts)
    ax.plot(pts[:, 0], pts[:, 1], color='k', lw=lw, ls=ls, zorder=z)


def cr(pts, n=30):
    """Catmull-Rom smooth spline through control points."""
    pts = np.asarray(pts, float)
    P = np.vstack([pts[0], pts, pts[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        t = np.linspace(0, 1, n)[:, None]
        out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                          + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t ** 2
                          + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    return np.vstack(out)


def spring(ax, p0, p1, amp=0.10, waves=6.5, arrow_at=None, lw=1.1, ms=10):
    """phonon wavy line; arrow_at in {'start','end',None}"""
    p0 = np.array(p0, float); p1 = np.array(p1, float)
    d = p1 - p0
    L = np.hypot(*d)
    u = d / L
    v = np.array([-u[1], u[0]])
    t = np.linspace(0, L, 400)
    window = np.sqrt(np.clip(np.sin(np.pi * t / L), 0, 1))
    s = amp * window * np.sin(t / L * waves * 2 * np.pi)
    pts = p0[None, :] + t[:, None] * u[None, :] + s[:, None] * v[None, :]
    polyline(ax, pts, lw=lw)
    if arrow_at == 'end':
        arr(ax, p1 - 0.30 * u * L ** 0 + 0.0 * v, p1, ms=ms)
    elif arrow_at == 'start':
        arr(ax, p0 + 0.30 * u, p0, ms=ms)


def right_angle(ax, F, d1, d2, a=0.14):
    d1 = np.array(d1, float); d1 /= np.hypot(*d1)
    d2 = np.array(d2, float); d2 /= np.hypot(*d2)
    F = np.array(F, float)
    pts = [F, F + a * d1, F + a * (d1 + d2), F + a * d2]
    polyline(ax, pts, lw=0.9)


def superellipse(r, n, c=(0.0, 0.0), N=240):
    t = np.linspace(0, 2 * np.pi, N)
    ct, st = np.cos(t), np.sin(t)
    x = c[0] + r * np.sign(ct) * np.abs(ct) ** (2.0 / n)
    y = c[1] + r * np.sign(st) * np.abs(st) ** (2.0 / n)
    return x, y


# ---------------------------------------------------------------- Fig. 26
def fig_26():
    fig = plt.figure(figsize=(4.6, 5.85))
    ax = ax_on(fig, [0.01, 0.01, 0.98, 0.98], (0, 10), (0, 12.6))
    Ca = np.array([5.0, 8.7])
    h, D, R = 1.55, 3.05, 2.72

    # ---- (a) extended zone scheme --------------------------------------
    # hatched Debye sphere (clipped by nothing; dashed outline on top)
    circ = plt.Circle(Ca, R, facecolor='white', edgecolor='black',
                      lw=0.0, hatch='///', zorder=1)
    ax.add_patch(circ)
    # diamond (second-zone boundary in extended scheme)
    dia = plt.Polygon([Ca + [0, D], Ca + [D, 0], Ca + [0, -D], Ca + [-D, 0]],
                      closed=True, fill=False, lw=1.25, zorder=4)
    ax.add_patch(dia)
    # first Brillouin zone (square)
    sq = plt.Rectangle(Ca - [h, h], 2 * h, 2 * h, fill=False, lw=1.25,
                       zorder=4)
    ax.add_patch(sq)
    # dashed Debye-sphere outline
    ax.add_patch(plt.Circle(Ca, R, fill=False, ls=(0, (5, 4)), lw=1.05,
                            zorder=5))
    # acoustic contour family (continuous across the zone boundary)
    for r, n in zip([0.13, 0.30, 0.52, 0.76, 1.02], [2.1, 2.3, 2.8, 3.6, 5.0]):
        x, y = superellipse(r * h, n, Ca)
        ax.plot(x, y, 'k-', lw=1.1, zorder=6)
    # small oval loops straddling the zone-edge midpoints
    for cx, cy, w, hh in [(h, 0, 0.14, 0.68), (-h, 0, 0.14, 0.68),
                          (0, h, 0.68, 0.14), (0, -h, 0.68, 0.14)]:
        ax.add_patch(matplotlib.patches.Ellipse(
            Ca + [cx, cy], w, hh, fill=False, lw=1.1, zorder=6))
    # arcs centred on the reciprocal-lattice points (diamond corners)
    for corner, ang in [((0, -1), (60, 120)), ((0, 1), (240, 300)),
                        ((-1, 0), (-30, 30)), ((1, 0), (150, 210))]:
        cc = Ca + D * np.array(corner, float)
        for r in (0.18, 0.32):
            t = np.linspace(np.deg2rad(ang[0]), np.deg2rad(ang[1]), 60)
            ax.plot(cc[0] + r * np.cos(t), cc[1] + r * np.sin(t), 'k-',
                    lw=1.1, zorder=6)
    for ln in ax.lines[-8:]:
        ln.set_clip_path(dia)
    ax.text(7.25, 11.2, 'Debye sphere', ha='left', va='center', fontsize=10)
    arr(ax, (7.2, 11.05), (6.62, 10.78), ms=9, z=7)
    ax.text(Ca[0], 4.95, '($a$)', ha='center', va='top', fontsize=11)

    # ---- (b) two separate zones ----------------------------------------
    centers = [np.array([2.55, 2.75]), np.array([7.45, 2.75])]
    # Acoustic
    C = centers[0]
    sq1 = plt.Rectangle(C - [h, h], 2 * h, 2 * h, fill=False, lw=1.25,
                        zorder=4)
    ax.add_patch(sq1)
    for r, n in zip([0.13, 0.30, 0.52, 0.76, 0.88], [2.1, 2.3, 2.8, 3.6, 5.0]):
        x, y = superellipse(r * h, n, C)
        ax.plot(x, y, 'k-', lw=1.1, zorder=6)
    for cx, cy, w, hh in [(h, 0, 0.22, 0.85), (-h, 0, 0.22, 0.85),
                          (0, h, 0.85, 0.22), (0, -h, 0.85, 0.22)]:
        e = matplotlib.patches.Ellipse(C + [cx, cy], w, hh, fill=False,
                                       lw=1.1, zorder=6)
        ax.add_patch(e)
        e.set_clip_path(sq1)
    corners = [(-1, -1), (1, -1), (-1, 1), (1, 1)]
    for cx, cy in corners:
        cc = C + h * np.array([cx, cy], float)
        a0 = np.deg2rad(np.arctan2(-cy, -cx))
        for r in (0.20, 0.36):
            t = np.linspace(a0, a0 + np.pi / 2, 40)
            ax.plot(cc[0] + r * np.cos(t), cc[1] + r * np.sin(t), 'k-',
                    lw=1.1, zorder=6)
    for ln in ax.lines[-8:]:
        ln.set_clip_path(sq1)
    ax.text(C[0], 0.78, 'Acoustic', ha='center', va='center', fontsize=10.5)

    # Optical
    C = centers[1]
    sq2 = plt.Rectangle(C - [h, h], 2 * h, 2 * h, fill=False, lw=1.25,
                        zorder=4)
    ax.add_patch(sq2)
    seg(ax, C - [h, h], C + [h, h], ls=(0, (5, 4)))
    seg(ax, C + [-h, h], C + [h, -h], ls=(0, (5, 4)))
    ax.add_patch(plt.Circle(C, 0.20, fill=False, lw=1.1, zorder=6))
    ax.add_patch(plt.Circle(C, 0.10, fill=False, lw=1.1, zorder=6))
    for cx, cy, ang in [(1, 1, 45), (-1, 1, 135), (-1, -1, 45), (1, -1, 135)]:
        ax.add_patch(matplotlib.patches.Ellipse(
            C + [0.41 * h * cx, 0.41 * h * cy], 0.53, 0.26, angle=ang,
            fill=False, lw=1.1, zorder=6))
    # large arcs bulging inward from each edge
    dd, rr = 1.92 * h, 1.36 * h
    arcs = [((0, dd), 222.6, 317.4), ((0, -dd), 42.6, 137.4),
            ((-dd, 0), -42.6, 42.6), ((dd, 0), 137.4, 222.6)]
    for cen, a0, a1 in arcs:
        t = np.linspace(np.deg2rad(a0), np.deg2rad(a1), 100)
        ax.plot(C[0] + cen[0] + rr * np.cos(t), C[1] + cen[1] + rr * np.sin(t),
                'k-', lw=1.1, zorder=6)
    for cx, cy in corners:
        cc = C + h * np.array([cx, cy], float)
        a0 = np.deg2rad(np.arctan2(-cy, -cx))
        for r in (0.20, 0.36):
            t = np.linspace(a0, a0 + np.pi / 2, 40)
            ax.plot(cc[0] + r * np.cos(t), cc[1] + r * np.sin(t), 'k-',
                    lw=1.1, zorder=6)
    for ln in ax.lines[-14:]:
        ln.set_clip_path(sq2)
    ax.text(C[0], 0.78, 'Optical', ha='center', va='center', fontsize=10.5)
    ax.text(5.0, 0.12, '($b$)', ha='center', va='center', fontsize=11)
    save(fig, '26')


# ---------------------------------------------------------------- Fig. 27
def fig_27():
    fig = plt.figure(figsize=(3.9, 2.65))
    ax = ax_on(fig, [0.02, 0.02, 0.96, 0.96], (0, 10.6), (0, 6.9))
    x0, y0 = 1.15, 0.75
    # axes
    seg(ax, (x0, y0), (x0, 6.35), lw=1.1)
    seg(ax, (x0, y0), (9.9, y0), lw=1.1)
    arr(ax, (9.75, y0), (10.05, y0), ms=11)
    ax.text(10.0, y0 - 0.34, r'$\nu$', ha='center', va='top', fontsize=12)
    ax.text(0.85, 3.6, r'$\mathcal{D}(\nu)$', ha='right', va='center',
            fontsize=12)
    # curve
    c1 = cr([(2.45, y0), (2.62, 1.62), (2.95, 2.02), (3.5, 2.22),
             (4.15, 2.32)], 24)
    riser1 = cr([(4.15, 2.32), (4.20, 2.52), (4.18, 2.72)], 12)
    c2 = cr([(4.18, 2.72), (4.55, 2.83), (5.05, 2.83), (5.55, 2.72),
             (6.0, 2.62)], 24)
    riser2 = cr([(6.0, 2.62), (6.07, 2.38), (6.05, 2.02)], 12)
    c3 = cr([(6.05, 2.02), (6.3, 1.86), (6.55, 1.86), (6.8, 1.96),
             (7.0, 2.16), (7.14, 2.38), (7.2, 2.52)], 30)
    for c in (c1, riser1, c2, riser2, c3):
        polyline(ax, c, lw=1.25)
    # final peak and vertical plunge to zero
    polyline(ax, cr([(7.2, 2.52), (7.26, 2.59), (7.3, 2.59), (7.34, 2.50)],
                    12), lw=1.25)
    polyline(ax, cr([(7.34, 2.50), (7.37, 2.1), (7.37, 1.4), (7.37, y0)],
                    20), lw=1.25)
    # labels with pointing arrows
    ax.text(2.55, 3.25, 'Minimum', ha='center', va='center', fontsize=10)
    arr(ax, (2.5, 3.05), (2.47, 1.15), ms=8)
    ax.text(4.35, 3.45, r'$S_1$', ha='center', va='center', fontsize=12)
    arr(ax, (4.3, 3.25), (4.2, 2.85), ms=8)
    ax.text(6.35, 3.75, r'$S_2$', ha='center', va='center', fontsize=12)
    arr(ax, (6.25, 3.55), (6.12, 2.85), ms=8)
    ax.text(8.45, 2.85, 'Maximum', ha='center', va='center', fontsize=10)
    arr(ax, (8.15, 2.7), (7.42, 2.45), ms=8)
    save(fig, '27')


# ---------------------------------------------------------------- Fig. 28
def fig_28():
    fig = plt.figure(figsize=(4.3, 3.55))
    ax = ax_on(fig, [0.02, 0.02, 0.96, 0.96], (0, 10.4), (-1.1, 8.0))
    M = [np.array([1.55, 6.65]), np.array([7.05, 6.7]),
         np.array([1.55, 1.7]), np.array([6.95, 1.65])]
    mL = np.array([4.05, 4.2]); mR = np.array([9.3, 4.25])
    rM, rm = 0.42, 0.33
    # solid MM paths (rectangle edges)
    seg(ax, M[0] + [0, -rM], M[2] + [0, rM])
    seg(ax, M[1] + [0, -rM], M[3] + [0, rM])
    seg(ax, M[0] + [rM, 0], M[1] + [-rM, 0])
    seg(ax, M[2] + [rM, 0], M[3] + [-rM, 0])
    # mm path
    seg(ax, mL + [rm, 0], mR + [-rm, 0])
    # dashed alternative paths (quadratic Bezier)
    def bez(p0, p1, p2, n=60):
        t = np.linspace(0, 1, n)[:, None]
        return ((1 - t) ** 2 * p0 + 2 * (1 - t) * t * p1 + t ** 2 * p2)
    for P in [bez(M[1] + [-0.3, -0.3], [5.3, 5.9], mL + [0.1, 0.3]),
              bez(M[1] + [0.3, -0.3], [8.7, 5.6], mR + [-0.1, 0.3]),
              bez(M[3] + [-0.3, 0.3], [5.2, 2.5], mL + [0.1, -0.3]),
              bez(M[3] + [0.3, 0.3], [8.6, 2.8], mR + [-0.1, -0.3])]:
        polyline(ax, P, lw=1.0, ls=(0, (4, 3)))
    # alternative zone (dashed rectangle)
    zx0, zy0, zx1, zy1 = 4.55, 0.05, 8.85, 5.35
    poly = plt.Rectangle((zx0, zy0), zx1 - zx0, zy1 - zy0, fill=False,
                         ls=(0, (4, 3)), lw=1.0)
    ax.add_patch(poly)
    ax.text(6.05, -0.72, 'Alternative zone', ha='center', va='center',
            fontsize=9.5)
    arr(ax, (7.35, -0.55), (8.15, 0.02), ms=9)
    # saddle S and minima markers on the mm path
    ymm = 0.5 * (mL[1] + mR[1])
    for xx in (5.05, 5.8, 7.85, 8.6):
        ax.plot([xx], [ymm], marker='x', ms=5.5, mew=1.4, color='k',
                ls='none', zorder=6)
    ax.text(6.72, ymm + 0.28, r'$S$', ha='center', va='center', fontsize=12)
    # circles
    for i, p in enumerate(M):
        ax.add_patch(plt.Circle(p, rM, facecolor='0.82', edgecolor='k',
                                lw=1.1, zorder=5))
        ax.text(p[0], p[1], r'$M$', ha='center', va='center', fontsize=12,
                zorder=7)
    for p in (mL, mR):
        ax.add_patch(plt.Circle(p, rm, facecolor='white', edgecolor='k',
                                lw=1.1, zorder=5))
        ax.text(p[0], p[1], r'$m$', ha='center', va='center', fontsize=12,
                zorder=7)
    save(fig, '28')


# ---------------------------------------------------------------- Fig. 29
def fig_29():
    fig = plt.figure(figsize=(4.85, 2.15))
    ax = ax_on(fig, [0.01, 0.02, 0.98, 0.96], (0, 16.4), (0, 7.2))

    # ---------------- (a) X-ray diffraction -----------------------------
    ax.text(0.25, 3.95, 'Incident', ha='left', va='center', fontsize=9.5)
    ax.text(0.25, 3.35, 'beam', ha='left', va='center', fontsize=9.5)
    seg(ax, (1.45, 3.65), (3.15, 3.65))
    arr(ax, (1.55, 3.65), (2.45, 3.65), ms=11)
    # crystal (tilted hatched slab)
    cx, cy, ang = 3.55, 3.62, -20
    ca, sa = np.cos(np.deg2rad(ang)), np.sin(np.deg2rad(ang))
    w, hh = 0.46, 0.32
    corners = []
    for dx, dy in [(-w, -hh), (w, -hh), (w, hh), (-w, hh)]:
        corners.append([cx + dx * ca - dy * sa, cy + dx * sa + dy * ca])
    crys = plt.Polygon(corners, closed=True, facecolor='white',
                       edgecolor='k', lw=1.0, hatch='////')
    ax.add_patch(crys)
    # dashed continuation of the incident direction
    seg(ax, (4.05, 3.6), (6.6, 3.6), ls=(0, (4, 3)))
    # diffracted beam
    a2 = np.deg2rad(36)
    d0 = np.array([cx + 0.12, cy + 0.12])
    d1 = d0 + 2.1 * np.array([np.cos(a2), np.sin(a2)])
    seg(ax, d0, d1)
    arr(ax, d0 + 1.35 * np.array([np.cos(a2), np.sin(a2)]), d1, ms=11)
    ax.text(4.28, 4.78, 'Diffracted beam', ha='center', va='center',
            fontsize=9.5, rotation=36)
    # 2theta arc
    t = np.linspace(0, a2, 30)
    ax.plot(4.35 + 0.62 * np.cos(t), 3.6 + 0.62 * np.sin(t), 'k-', lw=0.9)
    ax.text(5.15, 3.86, r'$2\theta$', ha='left', va='center', fontsize=11)
    # crystal axis
    seg(ax, (3.45, 3.3), (5.9, 2.05), ls=(0, (4, 3)))
    ax.text(6.55, 2.45, 'Crystal axis', ha='left', va='center', fontsize=9.5)
    arr(ax, (6.48, 2.42), (5.85, 2.28), ms=9)
    ax.text(3.4, 1.35, '($a$)', ha='center', va='center', fontsize=11)

    # ---------------- (b) Ewald construction ----------------------------
    O = np.array([10.6, 3.6]); R = 2.85
    P = O + [R, 0]
    th = np.deg2rad(33)
    Q = O + R * np.array([np.cos(th), np.sin(th)])
    # incident beam line
    seg(ax, (7.4, 3.6), O)
    arr(ax, (8.35, 3.6), (9.45, 3.6), ms=11)
    ax.text(8.8, 3.15, r'$\mathbf{k}$', ha='center', va='top', fontsize=11)
    seg(ax, O, P)
    arr(ax, (12.6, 3.6), (13.35, 3.6), ms=9)
    ax.text(12.35, 3.15, r'$\mathbf{k}$', ha='center', va='top', fontsize=11)
    # Ewald circle (arc through Q and P), dashed continuation below
    t = np.linspace(np.deg2rad(96), np.deg2rad(-28), 200)
    ax.plot(O[0] + R * np.cos(t), O[1] + R * np.sin(t), 'k-', lw=1.1)
    t = np.linspace(np.deg2rad(-28), np.deg2rad(-64), 60)
    ax.plot(O[0] + R * np.cos(t), O[1] + R * np.sin(t), 'k-',
            ls=(0, (4, 3)), lw=1.0)
    # k' and g
    arr(ax, O + 0.06 * (Q - O), Q - 0.05 * (Q - O), ms=12, lw=1.3)
    ax.text(11.25, 4.75, r"$\mathbf{k}'$", ha='center', va='bottom',
            fontsize=11)
    arr(ax, P + 0.08 * (Q - P), Q - 0.06 * (Q - P), ms=10, lw=1.0)
    ax.text(13.45, 4.35, r'$\mathbf{g}$', ha='left', va='center',
            fontsize=11)
    # theta arc at O
    t = np.linspace(0, th, 30)
    ax.plot(O[0] + 1.0 * np.cos(t), O[1] + 1.0 * np.sin(t), 'k-', lw=0.9)
    ax.text(11.9, 3.78, r'$\theta$', ha='left', va='bottom', fontsize=11)
    # reciprocal lattice dots (rotated), P and Q are lattice points
    e1 = Q - P
    e2 = 1.25 * np.array([np.cos(np.deg2rad(-24)), np.sin(np.deg2rad(-24))])
    for i in range(-1, 3):
        for j in range(-3, 3):
            p = P + i * e1 + j * e2
            if not (8.6 < p[0] < 16.2 and 0.7 < p[1] < 6.6):
                continue
            if np.hypot(*(p - O)) < 0.35:
                continue
            ax.add_patch(plt.Circle(p, 0.055, facecolor='k', zorder=5))
    # dashed reciprocal-lattice row through the dots below P
    p0 = P + 0.6 * e2
    polyline(ax, np.array([p0 + k * e2 for k in np.linspace(-0.4, 2.4, 2)]),
             lw=0.9, ls=(0, (4, 3)))
    for p, lab, dxy in [(O, '$O$', (-0.05, -0.32)), (P, '$P$', (0.3, 0.0)),
                        (Q, '$Q$', (0.3, 0.22))]:
        ax.add_patch(plt.Circle(p, 0.07, facecolor='k', zorder=6))
        ax.text(p[0] + dxy[0], p[1] + dxy[1], lab, ha='center',
                va='center', fontsize=12, zorder=7)
    ax.text(11.3, 1.35, '($b$)', ha='center', va='center', fontsize=11)
    save(fig, '29')


# ---------------------------------------------------------------- Fig. 30
def fig_30():
    fig = plt.figure(figsize=(4.35, 3.0))
    ax = ax_on(fig, [0.02, 0.02, 0.96, 0.96], (-5.4, 5.9), (-2.5, 3.6))
    th = np.deg2rad(35)
    u = np.array([np.cos(-th), np.sin(-th)])   # incident direction
    v = np.array([np.cos(th), np.sin(th)])     # diffracted direction
    M0 = np.array([0.0, 0.0])                  # upper scattering atom
    B = np.array([0.0, -1.15])                 # lower scattering atom
    d = 1.15
    # lattice dots
    for r, y in [(9, d), (9, 0.0), (9, -d)]:
        for i in range(-4, 5):
            ax.add_patch(plt.Circle([i, y], 0.075, facecolor='k',
                                    zorder=4))
    # rays
    for base, t0 in [(M0, 4.7), (B, 4.7)]:
        p_start = base - t0 * u
        seg(ax, p_start, base)
        arr(ax, base - (t0 - 1.15) * u, base - (t0 - 1.85) * u, ms=12)
        p_end = base + 4.35 * v
        seg(ax, base, p_end)
        arr(ax, base + 3.3 * v, p_end, ms=12)
    ax.text(-3.35, 1.55, r'$\mathbf{k}$', ha='center', va='center',
            fontsize=12)
    ax.text(3.35, 1.9, r"$\mathbf{k}'$", ha='center', va='center',
            fontsize=12)
    # theta marks at M0 with horizontal dashed stubs
    seg(ax, (-0.85, 0), (-0.16, 0), ls=(0, (4, 3)), lw=0.9)
    seg(ax, (0.16, 0), (0.85, 0), ls=(0, (4, 3)), lw=0.9)
    t = np.linspace(np.pi - th, np.pi, 30)
    ax.plot(0.55 * np.cos(t), 0.55 * np.sin(t), 'k-', lw=0.9)
    t = np.linspace(0, th, 30)
    ax.plot(0.55 * np.cos(t), 0.55 * np.sin(t), 'k-', lw=0.9)
    ax.text(-0.82, 0.30, r'$\theta$', ha='center', va='center', fontsize=11)
    ax.text(0.82, 0.30, r'$\theta$', ha='center', va='center', fontsize=11)
    # dash-dot normal between the rows through M0 and B
    seg(ax, M0, B, ls=(0, (6, 3, 1, 3)), lw=1.0)
    # perpendiculars from B onto the upper rays
    sA = np.dot(B - M0, u)
    Af = M0 + sA * u
    sC = np.dot(B - M0, v)
    Cf = M0 + sC * v
    seg(ax, B, Af, lw=1.0)
    seg(ax, B, Cf, lw=1.0)
    right_angle(ax, Af, u, (B - Af), 0.16)
    right_angle(ax, Cf, v, (B - Cf), 0.16)
    # d sin theta arcs at B
    dirL = (Af - B) / np.linalg.norm(Af - B)
    dirR = (Cf - B) / np.linalg.norm(Cf - B)
    aL0, aL1 = np.arctan2(dirL[1], dirL[0]), np.pi / 2
    aR0 = np.pi / 2
    aR1 = np.arctan2(dirR[1], dirR[0])
    t = np.linspace(aL0, aL1, 30)
    ax.plot(B[0] + 0.42 * np.cos(t), B[1] + 0.42 * np.sin(t), 'k-', lw=0.9)
    t = np.linspace(aR0, aR1, 30)
    ax.plot(B[0] + 0.42 * np.cos(t), B[1] + 0.42 * np.sin(t), 'k-', lw=0.9)
    ax.text(-0.85, -1.85, r'$d\sin\theta$', ha='center', va='center',
            fontsize=10.5)
    ax.text(0.9, -1.85, r'$d\sin\theta$', ha='center', va='center',
            fontsize=10.5)
    ax.text(-1.05, -0.72, r'$A$', ha='center', va='center', fontsize=12)
    ax.text(1.05, -0.72, r'$C$', ha='center', va='center', fontsize=12)
    ax.text(0.0, -1.62, r'$B$', ha='center', va='center', fontsize=12)
    # interplanar spacing d at the right
    seg(ax, (4.15, 0), (4.6, 0), ls=(0, (4, 3)), lw=0.9)
    seg(ax, (4.15, -d), (4.6, -d), ls=(0, (4, 3)), lw=0.9)
    arr(ax, (4.38, -0.12), (4.38, -d + 0.12), ms=8, style='<|-|>')
    ax.text(4.72, -d / 2, r'$d$', ha='left', va='center', fontsize=12)
    # dashed stubs on the lower row flanking B
    seg(ax, (-0.85, -d), (-0.4, -d), ls=(0, (4, 3)), lw=0.9)
    seg(ax, (0.4, -d), (0.85, -d), ls=(0, (4, 3)), lw=0.9)
    save(fig, '30')


# ---------------------------------------------------------------- Fig. 31
def fig_31():
    fig = plt.figure(figsize=(4.3, 2.55))
    ax = ax_on(fig, [0.02, 0.02, 0.96, 0.96], (-0.75, 6.35), (-0.75, 3.9))
    xs = [0.7, 2.1, 3.5, 4.9]
    ys = [2.9, 1.8, 0.7]
    a = 1.4
    # dashed verticals (full height)
    for xv in [0.0, 1.4, 2.8, 4.2, 5.6]:
        seg(ax, (xv, -0.55), (xv, 3.75), ls=(0, (4, 3)), lw=1.0)
    # horizontal dashed half-segments, alternating stagger
    for j, yv in enumerate([3.45, 2.35, 1.25, 0.15]):
        if j % 2 == 0:
            spans = [(0.0, 1.4), (2.8, 4.2)]
        else:
            spans = [(1.4, 2.8), (4.2, 5.6)]
        for s0, s1 in spans:
            seg(ax, (s0, yv), (s1, yv), ls=(0, (4, 3)), lw=1.0)
    # spins
    pat = [[1, -1, 1, -1], [-1, 1, -1, 1], [1, -1, 1, -1]]
    for yi, row in zip(ys, pat):
        for xi, s in zip(xs, row):
            seg(ax, (xi - 0.52, yi), (xi + 0.52, yi), lw=1.1)
            arr(ax, (xi + 0.16 * s, yi), (xi + 0.52 * s, yi), ms=8)
            ax.add_patch(plt.Circle([xi, yi], 0.085, facecolor='k',
                                    zorder=5))
    save(fig, '31')


# ---------------------------------------------------------------- Fig. 32
def fig_32():
    fig = plt.figure(figsize=(4.85, 2.7))
    ax = ax_on(fig, [0.01, 0.02, 0.98, 0.96], (0, 16.6), (-0.4, 8.0))

    # ---------------- (a) Normal process --------------------------------
    z0 = np.array([1.3, 2.3]); zs = 4.4
    zone = plt.Rectangle(z0, zs, zs, fill=False, lw=1.3)
    ax.add_patch(zone)
    ax.text(z0[0] + zs / 2, z0[1] + zs + 0.28, 'Zone', ha='center',
            va='bottom', fontsize=10.5)
    O = np.array([-0.5, 0.35])
    kt = np.array([4.05, 5.7])       # tip of k
    Kt = np.array([5.3, 4.25])       # tip of K = q
    ax.add_patch(plt.Circle(O, 0.075, facecolor='k', zorder=6))
    ax.add_patch(plt.Circle(kt, 0.075, facecolor='k', zorder=6))
    seg(ax, O, kt)
    arr(ax, O + 0.55 * (kt - O), O + 0.72 * (kt - O), ms=12)
    ax.text(1.7, 3.0, r'$\mathbf{k}$', ha='right', va='center', fontsize=12)
    seg(ax, kt, Kt)
    arr(ax, kt + 0.35 * (Kt - kt), kt + 0.68 * (Kt - kt), ms=11)
    ax.text(4.82, 6.28, r'$\mathbf{K}=\mathbf{q}$', ha='center',
            va='center', fontsize=11.5)
    seg(ax, O, Kt)
    arr(ax, O + 0.5 * (Kt - O), O + 0.68 * (Kt - O), ms=12)
    ax.text(3.9, 2.75, r"$\mathbf{k}'$", ha='left', va='center',
            fontsize=12)
    ax.text(3.5, 0.3, '($a$)', ha='center', va='center', fontsize=11)

    # ---------------- (b) Umklapp process --------------------------------
    z0 = np.array([7.6, 2.3]); zs = 4.4
    zone = plt.Rectangle(z0, zs, zs, fill=False, lw=1.3)
    ax.add_patch(zone)
    zdash = plt.Rectangle(z0 + [zs, 0], zs, zs, fill=False, lw=1.0,
                          ls=(0, (4, 3)))
    ax.add_patch(zdash)
    ax.text(z0[0] + zs / 2, z0[1] + zs + 0.28, 'Zone', ha='center',
            va='bottom', fontsize=10.5)
    # dashed downward extensions of the zone edges
    seg(ax, (z0[0], z0[1]), (z0[0], 0.15), ls=(0, (4, 3)), lw=1.0)
    seg(ax, (z0[0] + zs, z0[1]), (z0[0] + zs, 0.15), ls=(0, (4, 3)), lw=1.0)
    O = np.array([5.9, 0.3])
    kt = np.array([10.35, 5.65])         # tip of k (inside zone)
    qt = np.array([14.1, 5.65])          # q point (end of g)
    Kt = np.array([13.8, 4.15])          # tip of K / k'
    ax.add_patch(plt.Circle(O, 0.075, facecolor='k', zorder=6))
    ax.add_patch(plt.Circle(kt, 0.075, facecolor='k', zorder=6))
    seg(ax, O, kt)
    arr(ax, O + 0.55 * (kt - O), O + 0.72 * (kt - O), ms=12)
    ax.text(8.7, 3.0, r'$\mathbf{k}$', ha='left', va='center',
            fontsize=12)
    seg(ax, kt, qt, ls=(0, (4, 3)), lw=1.1)
    arr(ax, (13.5, 5.65), (13.85, 5.65), ms=10)
    ax.add_patch(plt.Circle(qt, 0.075, facecolor='k', zorder=6))
    ax.text(14.5, 5.65, r'$\mathbf{q}$', ha='left', va='center',
            fontsize=12)
    seg(ax, kt, Kt)
    arr(ax, kt + 0.42 * (Kt - kt), kt + 0.72 * (Kt - kt), ms=11)
    ax.text(12.45, 4.42, r'$\mathbf{K}$', ha='center', va='top',
            fontsize=12)
    seg(ax, O, Kt)
    arr(ax, O + 0.6 * (Kt - O), O + 0.76 * (Kt - O), ms=12)
    ax.text(11.85, 2.6, r"$\mathbf{k}'$", ha='left', va='center',
            fontsize=12)
    spring(ax, qt, Kt, amp=0.11, waves=5.5, arrow_at=None, lw=1.0)
    ax.text(10.0, 0.3, '($b$)', ha='center', va='center', fontsize=11)
    save(fig, '32')


# ---------------------------------------------------------------- Fig. 33
def fig_33():
    fig = plt.figure(figsize=(4.6, 2.25))
    ax = ax_on(fig, [0.01, 0.02, 0.98, 0.96], (0, 16.2), (0, 7.8))

    # ---------------- (a) phonon absorption ------------------------------
    V = np.array([5.3, 4.3])
    kin = np.array([3.45, 0.95])
    kout = np.array([3.6, 7.35])
    ph0 = np.array([8.1, 4.62])
    seg(ax, kin, V)
    arr(ax, kin + 0.5 * (V - kin), kin + 0.72 * (V - kin), ms=12)
    ax.text(4.0, 2.5, r'$\mathbf{k}$', ha='right', va='center', fontsize=12)
    seg(ax, V, kout)
    arr(ax, V + 0.45 * (kout - V), V + 0.72 * (kout - V), ms=12)
    ax.text(4.15, 5.85, r"$\mathbf{k}'$", ha='left', va='center',
            fontsize=12)
    spring(ax, ph0, V + 0.05 * (ph0 - V), amp=0.13, waves=6.5,
           arrow_at='end', lw=1.1)
    ax.text(6.35, 3.6, r'$\mathbf{q}$', ha='center', va='top', fontsize=12)
    ax.text(4.7, 0.7, '($a$)', ha='center', va='center', fontsize=11)

    # ---------------- (b) phonon emission --------------------------------
    V = np.array([11.5, 4.35])
    kin = np.array([10.8, 0.7])
    kout = np.array([10.45, 7.5])
    ph1 = np.array([14.45, 5.75])
    seg(ax, kin, V)
    arr(ax, kin + 0.5 * (V - kin), kin + 0.75 * (V - kin), ms=12)
    ax.text(11.35, 2.2, r'$\mathbf{k}$', ha='left', va='center', fontsize=12)
    seg(ax, V, kout)
    arr(ax, V + 0.45 * (kout - V), V + 0.75 * (kout - V), ms=12)
    ax.text(11.3, 6.25, r"$\mathbf{k}'$", ha='left', va='center',
            fontsize=12)
    ax.add_patch(plt.Circle(V, 0.11, facecolor='k', zorder=6))
    spring(ax, V, ph1, amp=0.13, waves=6.5, arrow_at='end', lw=1.1)
    ax.text(13.15, 3.95, r'$\mathbf{q}$', ha='center', va='top',
            fontsize=12)
    ax.text(11.4, 0.7, '($b$)', ha='center', va='center', fontsize=11)
    save(fig, '33')


# ---------------------------------------------------------------- Fig. 34
def fig_34():
    fig = plt.figure(figsize=(4.65, 3.35))
    ax = fig.add_axes([0.09, 0.11, 0.86, 0.87])
    ax.set_xlim(-1.05, 3.95)
    ax.set_ylim(-1.4, 2.8)
    ax.axis('off')
    ax.set_aspect('auto')
    xp = np.array([0.28, 0.55, 0.83, 1.12, 1.42, 1.75])  # last = nu_max
    yM, y1 = 2.0, 1.0
    xL, xR = -0.75, 3.75
    ytop, ybot = 2.8, -1.4
    # axes
    seg(ax, (xL, 0), (xR + 0.1, 0), lw=1.1)
    arr(ax, (xR, 0), (xR + 0.18, 0), ms=11)
    ax.text(xR + 0.22, -0.14, r'$\nu$', ha='left', va='center', fontsize=12)
    seg(ax, (0, ybot), (0, ytop), lw=1.1)
    ax.text(-0.16, 2.52, r'$f(\nu^2)$', ha='right', va='center',
            fontsize=12)
    ax.text(-0.14, -0.2, r'$O$', ha='right', va='center', fontsize=12)
    # pole lines (dashed)
    for xq in xp:
        seg(ax, (xq, ytop - 0.02), (xq, ybot + 0.02), ls=(0, (4, 3)),
            lw=1.0)
    ax.text(xp[2], -0.22, r'$\nu_q$', ha='center', va='top', fontsize=11)
    ax.text(xp[5], -0.22, r'$\nu_{\mathrm{max}}$', ha='center', va='top',
            fontsize=11)
    # levels 1 and -M/dM
    seg(ax, (xL, y1), (xR, y1), lw=1.0)
    ax.text(-0.12, y1, '1', ha='right', va='bottom', fontsize=11)
    seg(ax, (xL, yM), (xR, yM), lw=1.0)
    ax.text(xR + 0.06, yM, r'$\dfrac{M}{-\delta M}$', ha='left',
            va='center', fontsize=13)
    # ---- curve pieces (schematic, as in the original) ----
    ytop_c, ybot_c = 3.4, -3.4   # values beyond the clipped window
    # left branch: approaches 1 from below, descends through O, plunges
    left = cr([(-0.72, 1.10), (-0.45, 0.88), (-0.22, 0.55), (0.0, 0.0),
               (0.09, -0.42), (0.16, -0.95), (0.21, -1.8), (0.24, -3.2)],
              26)
    polyline(ax, left, lw=1.25)
    # interior branches between successive poles
    for k in range(5):
        g = xp[k + 1] - xp[k]
        x0 = xp[k]
        br = cr([(x0 + 0.05 * g, ytop_c), (x0 + 0.14 * g, 3.2),
                 (x0 + 0.30 * g, yM), (x0 + 0.45 * g, y1),
                 (x0 + 0.55 * g, 0.0), (x0 + 0.68 * g, -1.2),
                 (x0 + 0.80 * g, -3.0), (x0 + 0.95 * g, ybot_c)], 30)
        polyline(ax, br, lw=1.25)
    # tail beyond nu_max: descends, crosses -M/dM (localized mode),
    # then flattens towards 1
    tail = cr([(xp[5] + 0.03, ytop_c), (xp[5] + 0.14, 3.0),
               (xp[5] + 0.30, 2.32), (xp[5] + 0.55, yM),
               (xp[5] + 0.87, 1.80), (xp[5] + 1.25, 1.60),
               (xp[5] + 1.60, 1.44), (xp[5] + 1.87, 1.30),
               (xp[5] + 2.05, 1.18)], 36)
    polyline(ax, tail, lw=1.25)
    # dots on the -M/dM line and zeros on the axis
    dots = [xp[k] + 0.30 * (xp[k + 1] - xp[k]) for k in range(5)]
    xloc = xp[5] + 0.55
    dots.append(xloc)
    for xd in dots:
        ax.add_patch(plt.Circle([xd, yM], 0.045, facecolor='k', zorder=6))
    for k in range(5):
        xz = xp[k] + 0.55 * (xp[k + 1] - xp[k])
        ax.plot([xz], [0], marker='x', ms=5.5, mew=1.4, color='k',
                ls='none')
    ax.text(xloc + 0.16, yM + 0.38, 'localized mode', ha='left',
            va='center', fontsize=9.5)
    arr(ax, (xloc + 0.14, yM + 0.30), (xloc + 0.04, yM + 0.06), ms=8)
    save(fig, '34')


# ---------------------------------------------------------------- Fig. 35
def fig_35():
    fig = plt.figure(figsize=(4.85, 2.15))
    ax = ax_on(fig, [0.01, 0.02, 0.98, 0.96], (0, 16.4), (0, 7.6))

    # ---------------- (a) localized mode above the band ------------------
    yb = 5.75
    seg(ax, (0.95, yb), (6.3, yb), lw=1.0)
    xs = np.linspace(1.15, 6.05, 23)
    xc, c0, A = 3.45, 1.05, 0.62
    for x in xs:
        if abs(x - xc) < 0.15:
            continue          # impurity site itself
        xp_ = x - xc
        u = A * (1 - 2 * c0 ** 2 * xp_ ** 2) * np.exp(-c0 ** 2 * xp_ ** 2)
        ax.add_patch(plt.Circle([x, yb + u], 0.07, facecolor='k',
                                zorder=5))
    # impurity (open circle) at the peak
    ax.add_patch(plt.Circle([xc, yb + A], 0.10, facecolor='white',
                            edgecolor='k', lw=1.2, zorder=6))
    # phonon band (ruled block)
    bx0, bx1, by0, by1 = 0.95, 6.05, 1.15, 4.35
    seg(ax, (bx0, by1), (bx1, by1), lw=1.3)
    yy = np.linspace(by0 + 0.12, by1 - 0.12, 17)
    for yv in yy:
        seg(ax, (bx0, yv), (bx1, yv), lw=0.8)
    ax.text(bx1 + 0.15, by1 + 0.05, r'$\nu_{\mathrm{max}}$', ha='left',
            va='bottom', fontsize=10.5)
    ax.text(3.5, 0.45, '($a$)', ha='center', va='center', fontsize=11)

    # ---------------- (b) resonance mode within the band -----------------
    bx0, bx1, by0, by1 = 8.6, 13.9, 1.15, 4.35
    seg(ax, (bx0, by1), (bx1, by1), lw=1.3)
    yy = np.linspace(by0 + 0.12, by1 - 0.12, 17)
    for yv in yy:
        seg(ax, (bx0, yv), (bx1, yv), lw=0.8)
    ax.text(bx1 + 0.15, by1 + 0.05, r'$\nu_{\mathrm{max}}$', ha='left',
            va='bottom', fontsize=10.5)
    x = np.linspace(bx0 + 0.05, bx1 - 0.05, 400)
    xc2 = 11.25
    y = 4.0 + 0.075 * np.sin(2 * np.pi * (x - bx0) / 0.95) \
        + 1.05 * np.exp(-((x - xc2) / 0.42) ** 2)
    polyline(ax, np.column_stack([x, y]), lw=1.5)
    # atoms strung on the mode
    for xa in np.arange(bx0 + 0.35, bx1 - 0.2, 0.42):
        ya = (4.0 + 0.075 * np.sin(2 * np.pi * (xa - bx0) / 0.95)
              + 1.05 * np.exp(-((xa - xc2) / 0.42) ** 2))
        if abs(xa - xc2) < 0.25:
            continue
        ax.add_patch(plt.Circle([xa, ya], 0.045, facecolor='white',
                                edgecolor='k', lw=0.8, zorder=6))
    ax.add_patch(plt.Circle([xc2, y.max()], 0.09, facecolor='k',
                            zorder=7))
    ax.text(11.25, 0.45, '($b$)', ha='center', va='center', fontsize=11)
    save(fig, '35')


if __name__ == '__main__':
    for fn in (fig_26, fig_27, fig_28, fig_29, fig_30, fig_31,
               fig_32, fig_33, fig_34, fig_35):
        fn()
