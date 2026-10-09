# -*- coding: utf-8 -*-
"""Redraw Ziman, Principles of the Theory of Solids, 2nd ed., Chapter 7
figures 122-135 (black-and-white textbook style)."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle, Wedge, Arc, Polygon, PathPatch
from matplotlib.path import Path

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, 'figures')
PREV = os.path.join(OUT, 'preview')
os.makedirs(PREV, exist_ok=True)

DASH = (0, (4, 3))
LDASH = (0, (5, 4))
GRAY = '0.87'          # stipple substitute


def save(fig, key):
    fig.savefig(os.path.join(OUT, f'fig_{key}.pdf'), bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREV, f'fig_{key}.png'), bbox_inches='tight', pad_inches=0.03, dpi=200)
    plt.close(fig)
    print('saved fig', key)


def arrow(ax, xy0, xy1, lw=1.1, ms=11, ls='-', rad=0.0, color='k', zorder=3):
    """small solid-head arrow"""
    p = dict(arrowstyle='-|>', color=color, lw=lw, mutation_scale=ms,
             shrinkA=0, shrinkB=0, zorder=zorder)
    if rad:
        p['connectionstyle'] = f'arc3,rad={rad}'
    if ls != '-':
        p['linestyle'] = ls
    ax.annotate('', xy=xy1, xytext=xy0, arrowprops=p)


def line(ax, p0, p1, lw=1.2, ls='-', color='k'):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], ls=ls, lw=lw, color=color,
            solid_capstyle='butt')


def zig(ax, p0, p1, amp=0.05, turns=6, lw=1.1, color='k'):
    """phonon spring line from p0 to p1"""
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float)
    t = np.linspace(0, 1, 120)
    base = p0[None, :] + t[:, None] * (p1 - p0)[None, :]
    d = p1 - p0
    nvec = np.array([-d[1], d[0]])
    nvec = nvec / (np.hypot(*nvec) + 1e-12)
    off = amp * np.sin(2 * np.pi * turns * t)
    pts = base + off[:, None] * nvec[None, :]
    ax.plot(pts[:, 0], pts[:, 1], '-', lw=lw, color=color)


def open_head(ax, tip, direction, size=0.16, ang=24.0, lw=1.2):
    """open V arrowhead at tip pointing along direction (radians)"""
    d = np.array([np.cos(direction), np.sin(direction)])
    for s in (+1, -1):
        b = ang * np.pi / 180 * s
        back = np.array([np.cos(direction + np.pi + b), np.sin(direction + np.pi + b)])
        line(ax, tip, tip + size * back, lw=lw)


def open_darrow(ax, p0, p1, w=0.10, hl=0.30, lw=1.2):
    """double-stroke open arrow (=>) from p0 to p1"""
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float)
    d = p1 - p0
    ang = np.arctan2(d[1], d[0])
    nvec = np.array([-d[1], d[0]]); nvec /= np.hypot(*nvec)
    for s in (+1, -1):
        a0 = p0 + 0.5 * w * s * nvec
        a1 = p1 - hl * (d / np.hypot(*d)) + 0.5 * w * s * nvec
        line(ax, a0, a1, lw=lw)
    open_head(ax, p1, ang, size=hl * 1.05, ang=25, lw=lw)


def curved_open_arrow(ax, r, a0, a1, center=(0, 0), lw=1.3, double=True):
    """open curved arrow along a circle, from angle a0 to a1 (deg)"""
    t = np.linspace(np.radians(a0), np.radians(a1), 80)
    xs = center[0] + r * np.cos(t); ys = center[1] + r * np.sin(t)
    ax.plot(xs, ys, '-', lw=lw, color='k')
    if double:  # second, shorter inner stroke
        t2 = np.linspace(np.radians(a0), np.radians(a1 - 14), 80)
        r2 = r - 0.075
        ax.plot(center[0] + r2 * np.cos(t2), center[1] + r2 * np.sin(t2),
                '-', lw=lw, color='k')
    # head direction = tangent at a1
    tangent = np.radians(a1) + (np.pi / 2) * np.sign(np.radians(a1) - np.radians(a0))
    open_head(ax, (xs[-1], ys[-1]), tangent, size=0.17, ang=26, lw=lw)


def cr_spline(pts, n=22, closed=False):
    """Catmull-Rom smooth spline through points."""
    pts = np.asarray(pts, float)
    if closed:
        P = np.vstack([pts[-1], pts, pts[0], pts[1]])
        segs = range(1, len(P) - 2)
    else:
        P = np.vstack([pts[0], pts, pts[-1]])
        segs = range(1, len(P) - 2)
    out = []
    for i in segs:
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                              + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(pts[-1])
    return np.array(out)


def arc_pts(center, r, a0, a1, n=60):
    t = np.linspace(np.radians(a0), np.radians(a1), n)
    return np.stack([center[0] + r * np.cos(t), center[1] + r * np.sin(t)], axis=1)


# ----------------------------------------------------------------------
def fig_122():
    """(a) Displaced Fermi surface; (b) displaced Fermi distribution."""
    fig, axs = plt.subplots(1, 2, figsize=(4.8, 2.0),
                            gridspec_kw=dict(width_ratios=[1.0, 1.65]))

    # (a)
    ax = axs[0]
    ax.set_xlim(-1.5, 1.6)
    ax.set_ylim(-1.85, 1.55)
    ax.axis('off')
    ax.set_aspect('equal')
    cA = np.array([-0.13, 0.0])   # unshifted sphere
    cB = np.array([0.15, 0.0])    # shifted sphere
    # shifted sphere stippled
    ax.add_patch(Circle(cB, 1.0, facecolor=GRAY, edgecolor='k', lw=1.3, zorder=1))
    # hatched crescent = shifted minus unshifted (right part)
    a0, a1 = -78, 78
    p_out = arc_pts(cB, 1.0, a1, a0, 40)
    # points on circle A at same y as circle-B arc endpoints
    def on_A(pt):
        dx, dy = pt[0] - cA[0], pt[1] - cA[1]
        r = np.hypot(dx, dy)
        return np.array([cA[0] + dx / r, cA[1] + dy / r])
    q0 = on_A(p_out[-1]); q1 = on_A(p_out[0])
    aA0 = np.degrees(np.arctan2(q0[1] - cA[1], q0[0] - cA[0]))
    aA1 = np.degrees(np.arctan2(q1[1] - cA[1], q1[0] - cA[0]))
    p_in = arc_pts(cA, 1.0, aA0, aA1, 40)
    verts = np.vstack([p_out, p_in])
    codes = [Path.MOVETO] + [Path.LINETO] * (len(verts) - 1)
    ax.add_patch(PathPatch(Path(verts, codes), facecolor='none', edgecolor='none',
                           hatch='/////', zorder=2))
    ax.plot(p_out[:, 0], p_out[:, 1], 'k-', lw=1.3, zorder=3)
    # unshifted circle outline (full)
    ax.add_patch(Circle(cA, 1.0, facecolor='none', edgecolor='k', lw=1.3, zorder=4))
    # displacement arrow e*tau*E/hbar with a dot at its tail
    ax.plot([-0.06], [-0.05], 'ko', ms=3.2, zorder=6)
    arrow(ax, (-0.04, -0.05), (0.38, -0.05), lw=1.0, ms=9, zorder=6)
    ax.text(0.16, 0.10, r'$\boldsymbol{e}\boldsymbol{\tau}\mathbf{E}/\hbar$',
            ha='center', va='bottom', fontsize=10, zorder=6)
    # v vector out of the hatched crescent
    a = np.radians(52)
    p0 = cB + np.array([np.cos(a), np.sin(a)])
    p1 = p0 + 0.42 * np.array([np.cos(a - 8), np.sin(a - 8)])
    arrow(ax, p0, p1, lw=1.2, ms=11)
    ax.text(p1[0] + 0.06, p1[1] + 0.10, r'$\mathbf{v}$', ha='left', va='bottom')
    ax.text(0.0, -1.72, '($a$)', ha='center', va='center')

    # (b)
    ax = axs[1]
    ax.set_xlim(0.0, 1.13)
    ax.set_ylim(-0.62, 1.12)
    ax.axis('off')
    # horizontal energy axis
    arrow(ax, (0.02, 0), (1.10, 0), lw=1.2, ms=12)
    ax.text(1.075, -0.10, r'$\mathcal{E}$', ha='center', va='top')
    # f0 band (stippled -> light grey), bounded by the solid displaced curve
    f = cr_spline([(0.07, 0.0), (0.115, -0.30), (0.165, -0.36), (0.215, -0.10),
                   (0.27, 0.28), (0.35, 0.60), (0.45, 0.625), (0.60, 0.625),
                   (0.70, 0.60), (0.78, 0.38), (0.84, 0.10), (0.87, 0.0)])
    ypos = np.where(f[:, 1] > 0, f[:, 1], 0.0)
    ax.fill_between(f[:, 0], 0, ypos, color=GRAY, lw=0, zorder=1)
    ax.plot(f[:, 0], f[:, 1], 'k-', lw=1.4, zorder=4)
    # hatch the left dip (below axis part of the solid curve)
    dip = f[f[:, 1] < 0]
    ax.fill_between(dip[:, 0], 0, dip[:, 1], facecolor='none', hatch='///',
                    edgecolor='none', zorder=3)
    ax.plot(dip[:, 0], dip[:, 1], 'k-', lw=1.4, zorder=4)
    # Gaussian peak -df0/dE at the right edge (hatched)
    gx = np.linspace(0.685, 0.885, 100)
    gy = 0.80 * np.exp(-((gx - 0.775) / 0.045) ** 2)
    ax.fill_between(gx, 0, gy, facecolor='none', hatch='///', edgecolor='none', zorder=2)
    ax.plot(gx, gy, 'k-', lw=1.1, zorder=3)
    ax.text(0.895, 0.72, r'$-\,\partial f^0/\partial\mathcal{E}$',
            ha='left', va='center', fontsize=10)
    # vertical lines marking e*tau*v.E and a double arrow between them
    for xl in (0.44, 0.515):
        ax.plot([xl, xl], [0, 0.84], 'k-', lw=1.1)
    ax.plot([0.44, 0.515], [0.84, 0.84], 'k-', lw=1.0)
    arrow(ax, (0.44, 0.84), (0.465, 0.84), lw=1.0, ms=8)
    arrow(ax, (0.515, 0.84), (0.49, 0.84), lw=1.0, ms=8)
    ax.text(0.478, 0.92, r'$\boldsymbol{e}\boldsymbol{\tau}\mathbf{v}\cdot\mathbf{E}$',
            ha='center', va='bottom', fontsize=10)
    ax.text(0.565, -0.70, '($b$)', ha='center', va='center')

    fig.subplots_adjust(wspace=0.06, left=0.005, right=0.995, top=0.99, bottom=0.02)
    save(fig, 122)


# ----------------------------------------------------------------------
def fig_123():
    """Electron-phonon N-processes: (a) high T; (b) low T."""
    fig, axs = plt.subplots(1, 2, figsize=(4.4, 2.35))
    th = {'a': 52, 'b': 15}

    for i, key in enumerate('ab'):
        ax = axs[i]
        ax.set_xlim(-1.45, 1.55)
        ax.set_ylim(-1.45, 1.5)
        ax.axis('off')
        ax.set_aspect('equal')
        ax.add_patch(Circle((0, 0), 1.0, facecolor=GRAY, edgecolor='k', lw=1.3))
        t = np.radians(th[key])
        kp = np.array([np.cos(t), np.sin(t)])
        arrow(ax, (0, 0), 0.72 * kp, lw=1.2, ms=11)
        arrow(ax, (0, 0), (0.72, 0), lw=1.2, ms=11)
        kt = np.array([1.0, 0.0])
        # phonon q joins tip of k to tip of k'
        arrow(ax, kt, kp, lw=1.2, ms=11)
        if key == 'a':
            ax.text(0.60, -0.26, r'$\mathbf{k}$', ha='center', va='top')
            mid = 0.62 * np.array([np.cos(t), np.sin(t)])
            ax.text(mid[0] - 0.18, mid[1], r"$\mathbf{k'}$",
                    ha='right', va='center')
            mq = 0.5 * (kt + kp)
            ax.text(mq[0] + 0.02, mq[1] + 0.12, r'$\mathbf{q}$',
                    ha='center', va='bottom')
            ax.text(0.36, 0.14, r'$\theta$', ha='left', va='center')
        else:
            ax.text(0.60, -0.24, r'$\mathbf{k}$', ha='center', va='top')
            ax.text(0.52 * np.cos(t) + 0.02, 0.52 * np.sin(t) + 0.14,
                    r"$\mathbf{k'}$", ha='center', va='bottom')
            ax.text(1.06, 0.24, r'$\mathbf{q}$', ha='left', va='center')
            ax.text(0.38, -0.13, r'$\theta$', ha='left', va='top')
        ax.text(0, -1.34, f'($\\boldsymbol{{{key}}}$)', ha='center', va='center')
    fig.subplots_adjust(wspace=0.02, left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 123)


# ----------------------------------------------------------------------
def fig_124():
    """Electron-phonon U-processes: (a) free-electron sphere; (b) repeated zone."""
    fig, axs = plt.subplots(1, 2, figsize=(4.9, 2.3),
                            gridspec_kw=dict(width_ratios=[1.0, 1.35]))

    # ---------------- (a)
    ax = axs[0]
    ax.set_xlim(-1.95, 1.95)
    ax.set_ylim(-1.65, 1.7)
    ax.axis('off')
    ax.set_aspect('equal')
    ax.add_patch(Circle((0, 0), 1.0, facecolor=GRAY, edgecolor='k', lw=1.3))
    a1, a2 = np.radians(20), np.radians(157)
    P1 = np.array([np.cos(a1), np.sin(a1)])
    P2 = np.array([np.cos(a2), np.sin(a2)])
    arrow(ax, (0, 0), 0.62 * P1, lw=1.2, ms=11)
    ax.text(0.55, 0.04, r'$\mathbf{k}$', ha='center', va='top')
    arrow(ax, (0, 0), 0.62 * P2, lw=1.2, ms=11)
    ax.text(-0.62, -0.24, r"$\mathbf{k'}$", ha='center', va='top')
    # K from tip of k to tip of k'
    arrow(ax, P1, P2, lw=1.7, ms=13)
    ax.text(-0.10, 0.18, r'$\mathbf{K}$', ha='center', va='center')
    # dashed g line, horizontal at the height of P1, arrow at left end
    T = np.array([P1[0] - 2.45, P1[1]])
    line(ax, (P1[0] - 0.06, P1[1]), (T[0] + 0.14, P1[1]), lw=1.1, ls=DASH)
    arrow(ax, (T[0] + 0.14, P1[1]), T, lw=1.1, ms=10)
    ax.text(-0.95, P1[1] + 0.14, r'$\mathbf{g}$', ha='center', va='bottom')
    # q zigzag from k' tip out to near the g tip
    Q1 = np.array([P2[0] - 0.42, P2[1] + 0.16])
    zig(ax, P2, Q1, amp=0.035, turns=4, lw=1.1)
    arrow(ax, P2 + 0.82 * (Q1 - P2), Q1, lw=1.1, ms=10)
    ax.text(-1.28, 0.06, r'$\mathbf{q}$', ha='right', va='top')
    # theta near the centre
    ax.text(0.26, -0.18, r'$\theta$', ha='left', va='top')
    # zone boundary (solid) at right, outside the sphere
    line(ax, (1.38, -1.38), (1.38, 1.42), lw=1.5)
    ax.text(1.38, -1.58, 'Z.B.', ha='center', va='top')
    ax.text(0.05, -1.85, '($\\boldsymbol{a}$)', ha='center', va='center')

    # ---------------- (b)
    ax = axs[1]
    ax.set_xlim(-1.45, 3.75)
    ax.set_ylim(-1.65, 1.6)
    ax.axis('off')
    ax.set_aspect('equal')
    O1 = np.array([0.0, 0.0]); O2 = np.array([2.45, 0.0])
    ax.add_patch(Circle(O1, 1.0, facecolor=GRAY, edgecolor='k', lw=1.3))
    ax.add_patch(Circle(O2, 1.0, facecolor=GRAY, edgecolor='k', lw=1.2,
                        linestyle=DASH))
    ax.text(O1[0] - 0.06, -0.18, r'$O$', ha='right', va='top')
    ax.text(O2[0] + 0.10, -0.18, r'$O$', ha='left', va='top')
    # g along the line of centres
    arrow(ax, O1, O1 + 0.42 * (O2 - O1), lw=1.7, ms=13)
    line(ax, O1 + 0.46 * (O2 - O1), O2, lw=1.7)
    ax.text(0.95, -0.26, r'$\mathbf{g}$', ha='center', va='top')
    # k in the first zone
    ak = np.radians(26)
    A = np.array([np.cos(ak), np.sin(ak)])
    arrow(ax, O1, O1 + 0.62 * A, lw=1.2, ms=11)
    ax.text(0.34, 0.32, r'$\mathbf{k}$', ha='right', va='bottom')
    # final state on the repeated sphere
    akp = np.radians(166)
    B = O2 + np.array([np.cos(akp), np.sin(akp)])
    arrow(ax, O2, O2 + 0.60 * (B - O2), lw=1.2, ms=11)
    ax.text(1.80, 0.30, r"$\mathbf{k'}$", ha='left', va='bottom')
    # phonon q across the boundary
    zig(ax, A, B, amp=0.045, turns=5, lw=1.1)
    arrow(ax, A + 0.80 * (B - A), B, lw=1.1, ms=10)
    ax.text(1.16, 0.52, r'$\mathbf{q}$', ha='center', va='bottom')
    # zone boundary (dashed)
    line(ax, (1.22, -1.42), (1.22, 1.48), lw=1.1, ls=DASH)
    ax.text(1.22, -1.60, 'Z.B.', ha='center', va='top')
    # q_min between the two spheres
    yq = -0.60
    line(ax, (1.0, yq + 0.10), (1.0, yq - 0.10), lw=1.0)
    line(ax, (1.45, yq + 0.10), (1.45, yq - 0.10), lw=1.0)
    ax.plot([1.0, 1.45], [yq, yq], 'k-', lw=1.0)
    arrow(ax, (1.13, yq), (1.0, yq), lw=1.0, ms=8)
    arrow(ax, (1.32, yq), (1.45, yq), lw=1.0, ms=8)
    ax.text(1.22, -0.84, r'$\mathbf{q}_{\rm min.}$', ha='center', va='top')
    ax.text(0.35, -1.88, '($\\boldsymbol{b}$)', ha='center', va='center')

    fig.subplots_adjust(wspace=0.04, left=0.005, right=0.995, top=0.99, bottom=0.01)
    save(fig, 124)


# ----------------------------------------------------------------------
def fig_125():
    """Typical structure factor of a liquid metal."""
    fig, ax = plt.subplots(figsize=(3.9, 3.3))
    ax.set_xlim(-1.55, 12.6)
    ax.set_ylim(-1.05, 3.15)
    ax.axis('off')
    X = 11.5  # axis length unit
    # axes
    line(ax, (0, 0), (0, 2.92), lw=1.4)
    line(ax, (0, 0), (X, 0), lw=1.4)
    for yv in (1, 2):
        line(ax, (-0.13, yv), (0.30, yv), lw=1.2)
        ax.text(-0.35, yv, f'{yv}', ha='right', va='center')
    ax.text(-1.05, 1.55, r'$S(K)$', ha='center', va='center', rotation=90,
            fontsize=11)

    solid = cr_spline([(0.0, 0.03), (1.2, 0.035), (2.3, 0.06), (3.45, 0.18),
                       (4.03, 0.55), (4.38, 1.17), (4.72, 2.10), (5.01, 2.80),
                       (5.23, 2.45), (5.41, 1.75), (5.63, 1.06), (5.98, 0.80),
                       (6.33, 0.71), (6.70, 0.68), (7.13, 0.72), (7.48, 0.80),
                       (7.82, 0.93), (8.22, 1.08), (8.58, 1.13)])
    dash = cr_spline([(0.0, 0.08), (1.2, 0.10), (2.3, 0.14), (3.22, 0.25),
                      (3.80, 0.55), (4.38, 1.30), (4.72, 1.72), (4.95, 1.83),
                      (5.18, 1.78), (5.41, 1.55), (5.63, 1.28), (5.88, 1.08),
                      (6.22, 0.86), (6.56, 0.845), (6.90, 0.845), (7.35, 0.86),
                      (7.71, 0.91), (8.05, 0.97), (8.28, 1.00)])
    ax.plot(solid[:, 0], solid[:, 1], 'k-', lw=1.6)
    ax.plot(dash[:, 0], dash[:, 1], '--', lw=1.4, color='k', dashes=(4, 2.6))
    ax.text(5.28, 2.68, r'$313K$', ha='left', va='center')
    ax.text(5.32, 1.86, r'$633K$', ha='left', va='center')

    # 2k_F markers for Z = 1..5
    marks = [(4.38, 1.17, ''), (5.63, 1.06, ''), (6.22, 0.86, ''),
             (6.80, 0.845, 'cap'), (7.35, 0.86, 'cap')]
    for x, top, cap in marks:
        ax.plot([x, x], [0, top], 'k-', lw=1.1)
        if cap:
            ax.plot([x - 0.16, x + 0.16], [top, top], 'k-', lw=1.1)
    ax.text(4.38, -0.34, r'Z = 1', ha='center', va='top', fontsize=10)
    for x, s in ((5.63, '2'), (6.22, '3'), (6.80, '4'), (7.35, '5')):
        ax.text(x, -0.34, s, ha='center', va='top', fontsize=10)
    ax.text(4.38, -0.90, r'$2k_F$', ha='center', va='top')
    ax.text(X - 0.3, -0.55, r'$Kr_1$', ha='center', va='top')
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.02)
    save(fig, 125)


# ----------------------------------------------------------------------
def fig_126():
    """Fermi distribution in thermal conductivity."""
    fig, ax = plt.subplots(figsize=(4.9, 2.3))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(-1.15, 2.45)
    ax.axis('off')
    # baseline
    line(ax, (0.2, 0), (10.2, 0), lw=1.2)
    # origin marker: vertical arrow + O, small arrow on the axis with E label
    arrow(ax, (5.0, 0), (5.0, 1.45), lw=1.2, ms=11)
    ax.text(4.93, -0.16, r'$O$', ha='center', va='top')
    arrow(ax, (5.7, 0), (6.25, 0), lw=1.0, ms=9)
    ax.text(6.0, -0.18, r'$\mathcal{E}$', ha='center', va='top', fontsize=10)

    # equilibrium f0 (stippled band)
    f0 = cr_spline([(1.15, 0.0), (1.45, 0.10), (1.85, 0.52), (2.35, 0.95),
                    (2.8, 1.05), (5.0, 1.05), (7.3, 1.05), (7.9, 0.92),
                    (8.4, 0.55), (8.75, 0.18), (8.95, 0.0)])
    ax.fill_between(f0[:, 0], 0, f0[:, 1], color=GRAY, lw=0, zorder=1)
    ax.plot(f0[:, 0], f0[:, 1], 'k-', lw=0.9, zorder=2)

    # perturbed solid curve f_k
    fk = cr_spline([(0.90, 0.0), (1.15, -0.24), (1.42, -0.30), (1.70, -0.08),
                    (2.05, 0.42), (2.45, 0.92), (2.9, 1.11), (3.35, 1.13),
                    (3.9, 1.06), (4.6, 1.05), (6.9, 1.05), (7.5, 0.99),
                    (8.05, 0.78), (8.45, 0.42), (8.7, 0.12), (8.82, 0.0)])
    ax.plot(fk[:, 0], fk[:, 1], 'k-', lw=1.5, zorder=5)
    # hatched dip below the axis (left) and lens at the right edge
    d = fk[fk[:, 1] < 0]
    ax.fill_between(d[:, 0], 0, d[:, 1], facecolor='none', hatch='///',
                    edgecolor='none', zorder=4)
    ax.plot(d[:, 0], d[:, 1], 'k-', lw=1.5, zorder=5)
    # hatched lenses between the two curves where they cross
    f0k = np.interp(fk[:, 0], f0[:, 0], f0[:, 1])
    up = (fk[:, 1] > f0k) & (fk[:, 0] > 1.75) & (fk[:, 0] < 3.4)
    if up.any():
        ax.fill_between(fk[up, 0], f0k[up], fk[up, 1], facecolor='none',
                        hatch='///', edgecolor='none', zorder=3)
    dn = (fk[:, 1] < f0k) & (fk[:, 0] > 7.75)
    if dn.any():
        ax.fill_between(fk[dn, 0], fk[dn, 1], f0k[dn], facecolor='none',
                        hatch='///', edgecolor='none', zorder=3)
    # right dip below axis
    dip = cr_spline([(7.15, 0.0), (7.45, -0.20), (7.75, -0.24), (8.05, -0.06),
                     (8.2, 0.0)])
    ax.fill_between(dip[:, 0], 0, dip[:, 1], facecolor='none', hatch='///',
                    edgecolor='none', zorder=4)
    ax.plot(dip[:, 0], dip[:, 1], 'k-', lw=1.2, zorder=5)

    # dashed Gaussians (Cold / Hot) with dashed vertical zeta lines
    for xc, name, dy in ((2.0, 'Cold', 0.14), (8.45, 'Hot', 0.0)):
        gx = np.linspace(xc - 1.15, xc + 1.15, 120)
        gy = 1.85 * np.exp(-((gx - xc) / 0.42) ** 2)
        gy = np.where(gy > 0.015, gy, np.nan)
        ax.plot(gx, gy, '--', lw=1.1, color='k', dashes=(3.5, 2.4), zorder=3)
        ax.plot([xc, xc], [0, 1.80], '--', lw=1.0, color='k',
                dashes=(3.5, 2.4), zorder=3)
        ax.text(xc, 2.05, name, ha='center', va='bottom')
        ax.text(xc - 0.13, 0.92, r'$\zeta$', ha='right', va='center')
        ax.text(xc + 0.58, 1.30 + dy, r'$-\,\partial f^0/\partial\mathcal{E}$',
                ha='left', va='center', fontsize=10)
    # curve labels
    ax.text(2.22, 1.14, r'$f_{\mathbf{k}}$', ha='left', va='bottom', fontsize=10)
    ax.text(8.02, 1.12, r'$f^0$', ha='left', va='bottom', fontsize=10)
    # label of the perturbation with pointer arrow
    arrow(ax, (7.55, -0.62), (7.72, -0.30), lw=0.9, ms=8)
    ax.text(7.62, -0.78,
            r'$(\mathcal{E}-\zeta)(-\,\partial f^0/\partial\mathcal{E})'
            r'\tau\mathbf{v}\cdot(-\nabla T)$',
            ha='right', va='center', fontsize=10)
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.03)
    save(fig, 126)


# ----------------------------------------------------------------------
def fig_127():
    """Electron distributions and scattering processes."""
    fig, axs = plt.subplots(1, 2, figsize=(4.9, 2.75))

    def ring(ax):
        ax.add_patch(Circle((0, 0), 1.0, facecolor='none', edgecolor='k', lw=1.4,
                            zorder=3))
        ax.add_patch(Circle((0, 0), 0.885, facecolor='none', edgecolor='k',
                            lw=0.8, zorder=3))
        ax.add_patch(Circle((0, 0), 0.943, facecolor=GRAY, edgecolor='none',
                            zorder=1))
        ax.add_patch(Circle((0, 0), 0.885, facecolor='white', edgecolor='none',
                            zorder=2))
        ax.text(0.06, -0.80, 'Fermi level', ha='center', va='center',
                fontsize=9, zorder=5)

    def dot(ax, r, adeg, open_=False):
        a = np.radians(adeg)
        x, y = r * np.cos(a), r * np.sin(a)
        if open_:
            ax.plot([x], [y], 'o', ms=4.6, mfc='white', mec='k', mew=1.0, zorder=6)
        else:
            ax.plot([x], [y], 'ko', ms=4.0, zorder=6)

    # ---------- (a)
    ax = axs[0]
    ax.set_xlim(-2.05, 2.15)
    ax.set_ylim(-2.25, 1.85)
    ax.axis('off')
    ax.set_aspect('equal')
    ring(ax)
    # dashed displaced arc, upper left, with arrowhead at its lower end
    t = np.linspace(np.radians(102), np.radians(163), 60)
    ax.plot(1.08 * np.cos(t), 1.08 * np.sin(t), '--', lw=1.1, color='k',
            dashes=(3.5, 2.4))
    aend = np.radians(163)
    tang = aend - np.pi / 2
    open_head(ax, (1.08 * np.cos(aend), 1.08 * np.sin(aend)), tang,
              size=0.13, ang=26, lw=1.1)
    # hot electrons (filled): outside right, inside left
    for rr, aa in ((1.06, 68), (1.10, 52), (1.16, 38), (1.09, 24), (1.15, 10),
                   (1.08, -2), (1.13, 80)):
        dot(ax, rr, aa)
    for rr, aa in ((0.84, 172), (0.80, 184), (0.85, 196), (0.80, 208),
                   (0.86, 160), (0.83, 220)):
        dot(ax, rr, aa)
    # cold states (open): outside left, inside right
    for rr, aa in ((1.07, 150), (1.13, 163), (1.08, 176), (1.14, 189),
                   (1.08, 202), (1.12, 215), (1.06, 138)):
        dot(ax, rr, aa, open_=True)
    for rr, aa in ((0.82, 14), (0.86, 30), (0.81, 46), (0.85, -4), (0.83, 62)):
        dot(ax, rr, aa, open_=True)
    ax.text(1.52, 0.38, 'Hot', ha='left', va='center')
    ax.text(-1.50, -0.30, 'Cold', ha='right', va='center')
    ax.text(0.0, 1.62, 'Horizontal process', ha='center', va='bottom', fontsize=10)
    arrow(ax, (0.98, 0.03), (0.55, 0.01), lw=0.9, ms=9)
    ax.text(1.02, -0.42, 'Vertical', ha='left', va='center', fontsize=10)
    ax.text(1.02, -0.68, 'process', ha='left', va='center', fontsize=10)
    # heat current and current arrows
    ax.text(-0.18, -1.62, r'$\mathbf{U}$', ha='center', va='center')
    arrow(ax, (0.10, -1.62), (0.62, -1.62), lw=1.1, ms=10)
    arrow(ax, (0.10, -1.98), (-0.42, -1.98), lw=1.1, ms=10)
    ax.text(0.28, -1.98, r'$\mathbf{J}$', ha='left', va='center')
    ax.text(0.0, -2.28, '($\\boldsymbol{a}$)', ha='center', va='center')

    # ---------- (b)
    ax = axs[1]
    ax.set_xlim(-2.05, 2.15)
    ax.set_ylim(-2.25, 1.85)
    ax.axis('off')
    ax.set_aspect('equal')
    ring(ax)
    # drift arrow through the middle
    arrow(ax, (0.78, 0.12), (-0.52, 0.10), lw=1.1, ms=11)
    for rr, aa in ((1.06, 60), (1.12, 46), (1.08, 32), (1.14, 18), (1.08, 5),
                   (1.12, -8), (1.07, 74)):
        dot(ax, rr, aa)
    for rr, aa in ((0.84, 178), (0.80, 190), (0.85, 202), (0.81, 214),
                   (0.86, 166)):
        dot(ax, rr, aa)
    for rr, aa in ((1.07, 146), (1.13, 159), (1.08, 172), (1.14, 185),
                   (1.09, 198), (1.12, 211), (1.06, 133)):
        dot(ax, rr, aa, open_=True)
    for rr, aa in ((0.82, 8), (0.86, 24), (0.81, 40), (0.85, -10), (0.83, 56)):
        dot(ax, rr, aa, open_=True)
    ax.text(-0.30, -1.62, r'$\boldsymbol{e}\mathbf{J}$', ha='center', va='center')
    arrow(ax, (0.16, -1.62), (0.70, -1.62), lw=1.1, ms=10)
    ax.text(0.0, -2.28, '($\\boldsymbol{b}$)', ha='center', va='center')

    fig.subplots_adjust(wspace=0.03, left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 127)


# ----------------------------------------------------------------------
def fig_128():
    """The Seebeck effect."""
    fig, ax = plt.subplots(figsize=(3.5, 3.6))
    ax.set_xlim(-1.75, 1.75)
    ax.set_ylim(-2.0, 1.45)
    ax.axis('off')
    ax.set_aspect('equal')
    Ri, Ro = 0.88, 1.0
    # metal A (top half, hatched)
    ax.add_patch(Wedge((0, 0), Ro, 0, 180, width=Ro - Ri, facecolor='white',
                       edgecolor='k', lw=1.3, hatch='////'))
    # metal B (bottom half) with a gap at the bottom for the voltmeter
    for a0, a1 in ((180, 247), (293, 360)):
        w = Wedge((0, 0), Ro, a0, a1, width=Ro - Ri, facecolor='white',
                  edgecolor='k', lw=1.3)
        ax.add_patch(w)
    # junction marks
    for a in (180, 0):
        ar = np.radians(a)
        line(ax, (Ri * np.cos(ar), Ri * np.sin(ar)),
             (Ro * np.cos(ar), Ro * np.sin(ar)), lw=1.3)
    # leads to the voltmeter
    pL = np.array([Ro * np.cos(np.radians(247)), Ro * np.sin(np.radians(247))])
    pR = np.array([Ro * np.cos(np.radians(293)), Ro * np.sin(np.radians(293))])
    leadL = cr_spline([pL + 0.01 * np.array([0, -1]), (-0.40, -1.14),
                       (-0.30, -1.32), (-0.155, -1.38)])
    leadR = cr_spline([pR + 0.01 * np.array([0, -1]), (0.40, -1.14),
                       (0.30, -1.32), (0.155, -1.38)])
    for L in (leadL, leadR):
        ax.plot(L[:, 0], L[:, 1], 'k-', lw=1.2)
    # voltmeter: circle with a needle
    ax.add_patch(Circle((0, -1.56), 0.17, facecolor='white', edgecolor='k', lw=1.3))
    arrow(ax, (-0.09, -1.64), (0.09, -1.48), lw=1.1, ms=9)
    # labels
    ax.text(-1.38, -0.02, r'$\mathbf{T_1}$', ha='right', va='center')
    ax.text(1.38, -0.02, r'$\mathbf{T_2}$', ha='left', va='center')
    ax.text(0.60, 0.86, r'$\mathbf{A}$', ha='left', va='center')
    ax.text(0.58, -1.02, r'$\mathbf{B}$', ha='left', va='center')
    ax.text(-0.30, -0.76, r'$\mathbf{T_0}$', ha='right', va='center')
    ax.text(0.30, -0.76, r'$\mathbf{T_0}$', ha='left', va='center')
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 128)


# ----------------------------------------------------------------------
def fig_129():
    """The Peltier effect."""
    fig, ax = plt.subplots(figsize=(3.8, 3.9))
    ax.set_xlim(-2.35, 2.55)
    ax.set_ylim(-2.15, 1.75)
    ax.axis('off')
    ax.set_aspect('equal')
    Ri, Ro = 0.88, 1.0
    ax.add_patch(Wedge((0, 0), Ro, 0, 180, width=Ro - Ri, facecolor='white',
                       edgecolor='k', lw=1.3, hatch='////'))
    for a0, a1 in ((180, 250), (290, 360)):
        ax.add_patch(Wedge((0, 0), Ro, a0, a1, width=Ro - Ri, facecolor='white',
                           edgecolor='k', lw=1.3))
    for a in (180, 0):
        ar = np.radians(a)
        line(ax, (Ri * np.cos(ar), Ri * np.sin(ar)),
             (Ro * np.cos(ar), Ro * np.sin(ar)), lw=1.3)
    # leads down to the battery
    pL = np.array([Ro * np.cos(np.radians(250)), Ro * np.sin(np.radians(250))])
    pR = np.array([Ro * np.cos(np.radians(290)), Ro * np.sin(np.radians(290))])
    leadL = cr_spline([pL, (-0.34, -1.06), (-0.50, -1.18), (-0.50, -1.30)])
    leadR = cr_spline([pR, (0.34, -1.04), (0.50, -1.16), (0.50, -1.30)])
    for L in (leadL, leadR):
        ax.plot(L[:, 0], L[:, 1], 'k-', lw=1.2)
    line(ax, (-0.50, -1.30), (-0.26, -1.30), lw=1.2)
    line(ax, (0.50, -1.30), (0.26, -1.30), lw=1.2)
    # battery plates (long-short alternated)
    yb = -1.30
    for x, h in ((-0.20, 0.36), (-0.10, 0.19), (0.0, 0.36), (0.10, 0.19),
                 (0.20, 0.36)):
        line(ax, (x, yb - h / 2), (x, yb + h / 2), lw=1.3)
    # current J inside the ring (clockwise, arrow on the right)
    t = np.linspace(np.radians(78), np.radians(-58), 80)
    rJ = 0.80
    ax.plot(rJ * np.cos(t), rJ * np.sin(t), 'k-', lw=1.2)
    tang = np.radians(-58) - np.pi / 2
    open_head(ax, (rJ * np.cos(np.radians(-58)), rJ * np.sin(np.radians(-58))),
              tang, size=0.17, ang=26, lw=1.2)
    ax.text(0.42, -0.06, r'$\mathbf{J}$', ha='left', va='center')
    # heat current carried round each metal (curved open arrows)
    curved_open_arrow(ax, 1.18, 150, 34, lw=1.2)
    ax.text(0.0, 1.50, r'$\Pi_A\mathbf{J}$', ha='center', va='bottom')
    curved_open_arrow(ax, 1.32, -6, -56, lw=1.2)
    ax.text(1.44, -1.02, r'$\Pi_B\mathbf{J}$', ha='left', va='center')
    # Peltier heat at the junctions (double open arrows)
    open_darrow(ax, (-2.05, 0.0), (-1.22, 0.0), lw=1.2)
    ax.text(-2.12, 0.0, r'$(\Pi_A-\Pi_B)\mathbf{J}$', ha='right', va='center')
    open_darrow(ax, (1.22, 0.0), (2.05, 0.0), lw=1.2)
    ax.text(2.12, 0.0, r'$(\Pi_A-\Pi_B)\mathbf{J}$', ha='left', va='center')
    ax.text(-0.55, 0.74, r'$\mathbf{A}$', ha='right', va='center')
    ax.text(-0.62, -1.02, r'$\mathbf{B}$', ha='right', va='center')
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 129)


# ----------------------------------------------------------------------
def fig_130():
    """Alternative models for thermo-electric power."""
    fig, axs = plt.subplots(1, 2, figsize=(4.8, 2.3),
                            gridspec_kw=dict(width_ratios=[1.15, 1.0]))
    # (a) electron Fermi surface: white circle in a filled block
    ax = axs[0]
    ax.set_xlim(-1.45, 1.45)
    ax.set_ylim(-1.55, 1.35)
    ax.axis('off')
    ax.set_aspect('equal')
    ax.add_patch(Rectangle((-1.12, -1.05), 2.24, 2.10, facecolor='0.80',
                           edgecolor='k', lw=1.2))
    ax.add_patch(Circle((0, 0), 0.64, facecolor='white', edgecolor='k', lw=1.5,
                        zorder=3))
    arrow(ax, (-0.48, 0.38), (0.06, 0.10), lw=1.1, ms=10, zorder=5)
    ax.text(-0.40, 0.44, r'$\mathcal{E}_e$ increasing', ha='left', va='bottom',
            fontsize=9.5, zorder=5)
    arrow(ax, (-0.46, -0.38), (0.10, -0.14), lw=1.1, ms=10, zorder=5)
    ax.text(-0.34, -0.46, r'$-|e|\boldsymbol{v}$', ha='left', va='top',
            fontsize=9, zorder=5)
    ax.text(0.0, -1.42, '($\\boldsymbol{a}$)', ha='center', va='center')
    # (b) hole Fermi surface: filled circle, arrows outward
    ax = axs[1]
    ax.set_xlim(-1.25, 1.85)
    ax.set_ylim(-1.55, 1.35)
    ax.axis('off')
    ax.set_aspect('equal')
    ax.add_patch(Circle((0, 0), 0.72, facecolor='0.80', edgecolor='k', lw=1.5))
    arrow(ax, (0.46, 0.46), (0.92, 0.74), lw=1.1, ms=10)
    ax.text(0.98, 0.80, r'$|e|\boldsymbol{v}$', ha='left', va='center',
            fontsize=10)
    arrow(ax, (0.50, -0.42), (0.96, -0.70), lw=1.1, ms=10)
    ax.text(1.00, -0.80, r'$\mathcal{E}_h$ increasing', ha='left', va='center',
            fontsize=10)
    ax.text(0.0, -1.42, '($\\boldsymbol{b}$)', ha='center', va='center')
    fig.subplots_adjust(wspace=0.05, left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 130)


# ----------------------------------------------------------------------
def fig_131():
    """Phonon-phonon U-processes."""
    fig, ax = plt.subplots(figsize=(4.3, 2.0))
    ax.set_xlim(-0.55, 6.35)
    ax.set_ylim(-1.55, 2.1)
    ax.axis('off')
    A = np.array([0.0, 0.0]); B = np.array([5.6, 0.0])
    C = np.array([1.8, 1.15]); D = np.array([3.6, 1.15])
    arrow(ax, A, A + 0.62 * (C - A), lw=1.4, ms=12)
    line(ax, A + 0.66 * (C - A), C, lw=1.4)
    ax.text(0.42, 0.72, r'$\mathbf{q}$', ha='right', va='bottom')
    arrow(ax, C, C + 0.62 * (D - C), lw=1.4, ms=12)
    line(ax, C + 0.66 * (D - C), D, lw=1.4)
    ax.text(2.62, 1.32, r"$\mathbf{q'}$", ha='center', va='bottom')
    arrow(ax, D, D + 0.62 * (B - D), lw=1.4, ms=12)
    line(ax, D + 0.66 * (B - D), B, lw=1.4)
    ax.text(4.72, 0.66, r"$\mathbf{q''}$", ha='left', va='center')
    arrow(ax, A, 0.55 * (B - A), lw=1.6, ms=13)
    line(ax, 0.58 * (B - A), B, lw=1.6)
    ax.text(3.52, -0.30, r'$\mathbf{g}$', ha='left', va='top')
    # zone boundary, broken for its label
    xb = 3.30
    line(ax, (xb, 0.0), (xb, 1.85), lw=1.4)
    line(ax, (xb, -0.42), (xb, -0.55), lw=1.4)
    line(ax, (xb, -1.02), (xb, -1.35), lw=1.4)
    ax.text(xb, -0.78, 'Z.B.', ha='center', va='center')
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 131)


# ----------------------------------------------------------------------
def fig_132():
    """Phonon drag by electrons: (a) N-processes; (b) U-processes."""
    fig, axs = plt.subplots(1, 2, figsize=(4.7, 2.75))

    # ---------- (a)
    ax = axs[0]
    ax.set_xlim(-2.0, 2.0)
    ax.set_ylim(-2.45, 1.6)
    ax.axis('off')
    ax.set_aspect('equal')
    ax.add_patch(Circle((0, 0), 1.0, facecolor=GRAY, edgecolor='k', lw=1.3))
    h = 0.86
    E1 = np.array([-np.sqrt(1 - h * h), h])
    E2 = np.array([np.sqrt(1 - h * h), h])
    arrow(ax, (0, 0), 0.80 * E2 / np.linalg.norm(E2), lw=1.2, ms=11)
    arrow(ax, (0, 0), 0.80 * E1 / np.linalg.norm(E1), lw=1.2, ms=11)
    zig(ax, E2, E1, amp=0.04, turns=4, lw=1.1)
    arrow(ax, E2 + 0.40 * (E1 - E2), E2 + 0.64 * (E1 - E2), lw=1.2, ms=12)
    ax.text(0.0, 1.14, r'$\mathbf{q}$', ha='center', va='bottom')
    ax.text(0.54, 0.46, r'$\mathbf{k}$', ha='left', va='center')
    ax.text(-0.54, 0.46, r"$\mathbf{k'}$", ha='right', va='center')
    ax.text(-0.15, -1.50, r'$\mathbf{U}$', ha='center', va='center')
    arrow(ax, (0.12, -1.50), (0.64, -1.50), lw=1.1, ms=10)
    arrow(ax, (0.12, -1.86), (-0.40, -1.86), lw=1.1, ms=10)
    ax.text(0.30, -1.86, r'$\mathbf{J}$', ha='left', va='center')
    ax.text(0, -2.28, '($\\boldsymbol{a}$)', ha='center', va='center')

    # ---------- (b)
    ax = axs[1]
    ax.set_xlim(-2.35, 2.0)
    ax.set_ylim(-2.45, 1.6)
    ax.axis('off')
    ax.set_aspect('equal')
    ax.add_patch(Circle((0, 0), 1.0, facecolor=GRAY, edgecolor='k', lw=1.3))
    y = 0.58
    Ex = np.sqrt(1 - y * y)
    E1 = np.array([-Ex, y]); E2 = np.array([Ex, y])
    line(ax, E1, E2, lw=1.1, ls=DASH)
    arrow(ax, (-0.25, y), (0.28, y), lw=1.1, ms=10)
    ax.text(0.10, y + 0.14, r'$\mathbf{g}$', ha='center', va='bottom')
    arrow(ax, (0, 0), 0.82 * E2 / np.linalg.norm(E2), lw=1.2, ms=11)
    ax.text(0.42, 0.30, r'$\mathbf{k}$', ha='left', va='center')
    arrow(ax, (0, 0), 0.82 * E1 / np.linalg.norm(E1), lw=1.2, ms=11)
    ax.text(-0.72, 0.30, r"$\mathbf{k'}$", ha='right', va='center')
    Q1 = np.array([-Ex - 0.62, y - 0.16])
    zig(ax, E1, Q1, amp=0.04, turns=4, lw=1.1)
    arrow(ax, E1 + 0.75 * (Q1 - E1), Q1, lw=1.1, ms=10)
    ax.text(-1.28, 0.24, r'$\mathbf{q}$', ha='right', va='top')
    arrow(ax, (0.42, -1.50), (-0.10, -1.50), lw=1.1, ms=10)
    ax.text(0.60, -1.50, r'$\mathbf{U}$', ha='left', va='center')
    arrow(ax, (0.42, -1.86), (-0.10, -1.86), lw=1.1, ms=10)
    ax.text(0.60, -1.86, r'$\mathbf{J}$', ha='left', va='center')
    ax.text(0, -2.28, '($\\boldsymbol{b}$)', ha='center', va='center')

    fig.subplots_adjust(wspace=0.04, left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 132)


# ----------------------------------------------------------------------
def fig_133():
    """Vector solution E = A + (e*tau/mc) H^A."""
    fig, ax = plt.subplots(figsize=(4.4, 1.9))
    ax.set_xlim(-0.15, 4.6)
    ax.set_ylim(-0.55, 1.75)
    ax.axis('off')
    ax.set_aspect('equal')
    O = np.array([0.0, 0.0]); Et = np.array([2.9, 0.0]); At = np.array([2.28, 1.28])
    # E along the bottom
    arrow(ax, O, O + 0.68 * (Et - O), lw=1.3, ms=12)
    line(ax, O + 0.72 * (Et - O), Et, lw=1.3)
    ax.text(1.45, -0.26, r'$\mathbf{E}$', ha='center', va='top')
    # A hypotenuse
    arrow(ax, O, O + 0.55 * (At - O), lw=1.3, ms=12)
    line(ax, O + 0.60 * (At - O), At, lw=1.3)
    ax.text(1.02, 0.80, r'$\mathbf{A}$', ha='center', va='bottom')
    # (e tau/mc) H ^ A  from A tip down to E tip
    arrow(ax, At, At + 0.55 * (Et - At), lw=1.3, ms=12)
    line(ax, At + 0.60 * (Et - At), Et, lw=1.3)
    # dashed completion of the rectangle
    line(ax, At, (Et[0], At[1]), lw=1.0, ls=DASH)
    line(ax, (Et[0], At[1]), Et, lw=1.0, ls=DASH)
    ax.text(3.12, 0.62,
            r'$\dfrac{\boldsymbol{e\tau}}{m\boldsymbol{c}}\,'
            r'\mathbf{H}{\wedge}\mathbf{A}$',
            ha='left', va='center')
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.02)
    save(fig, 133)


# ----------------------------------------------------------------------
def fig_134():
    """(a) sphere of electrons, m* positive; (b) sphere of holes, m* negative."""
    fig, axs = plt.subplots(1, 2, figsize=(4.4, 2.35))
    # (a)
    ax = axs[0]
    ax.set_xlim(-1.35, 1.75)
    ax.set_ylim(-1.75, 1.3)
    ax.axis('off')
    ax.set_aspect('equal')
    ax.add_patch(Circle((0, 0), 0.92, facecolor=GRAY, edgecolor='k', lw=1.4))
    ax.plot([0], [0], 'ko', ms=3)
    arrow(ax, (0, 0), (0.92, 0), lw=1.2, ms=11)
    ax.text(0.40, 0.10, r'$\mathbf{k}_F$', ha='center', va='bottom')
    a = np.radians(-38)
    p0 = 0.92 * np.array([np.cos(a), np.sin(a)])
    p1 = p0 + 0.52 * np.array([np.cos(a + 6), np.sin(a + 6)])
    arrow(ax, p0, p1, lw=1.2, ms=11)
    ax.text(p1[0] - 0.05, p1[1] - 0.22, r'$\mathbf{v}_F$', ha='center', va='top')
    ax.text(0, -1.62, '($\\boldsymbol{a}$)', ha='center', va='center')
    # (b)
    ax = axs[1]
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.75, 1.3)
    ax.axis('off')
    ax.set_aspect('equal')
    ax.add_patch(Circle((0, 0), 1.12, facecolor='0.78', edgecolor='none'))
    ax.add_patch(Circle((0, 0), 0.98, facecolor='0.88', edgecolor='none'))
    ax.add_patch(Circle((0, 0), 0.80, facecolor='white', edgecolor='k', lw=1.4,
                        zorder=3))
    ax.plot([0], [0], 'ko', ms=3, zorder=5)
    arrow(ax, (0, 0), (0.80, 0), lw=1.2, ms=11, zorder=6)
    ax.text(0.34, 0.10, r'$\mathbf{k}_F$', ha='center', va='bottom', zorder=6)
    a = np.radians(133)
    p0 = 0.82 * np.array([np.cos(a), np.sin(a)])
    p1 = 0.24 * np.array([np.cos(a), np.sin(a)])
    arrow(ax, p0, p1, lw=1.2, ms=11, zorder=6)
    ax.text(-0.62, 0.66, r'$\mathbf{v}_F$', ha='right', va='bottom', zorder=6)
    ax.text(0, -1.62, '($\\boldsymbol{b}$)', ha='center', va='center')
    fig.subplots_adjust(wspace=0.02, left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 134)


# ----------------------------------------------------------------------
def fig_135():
    """Hall-effect contributions from two bands of carriers."""
    fig, ax = plt.subplots(figsize=(4.9, 2.6))
    ax.set_xlim(-0.4, 9.9)
    ax.set_ylim(-2.6, 2.6)
    ax.axis('off')
    ax.set_aspect('equal')
    O = np.array([0.0, 0.0])
    aU = np.radians(26)
    aL = np.radians(-27)
    P1 = 3.05 * np.array([np.cos(aU), np.sin(aU)])
    P2 = 3.95 * np.array([np.cos(aU), np.sin(aU)])   # J1 tip
    P3 = 2.62 * np.array([np.cos(aL), np.sin(aL)])
    P4 = 3.50 * np.array([np.cos(aL), np.sin(aL)])   # J2 tip
    T = np.array([4.15, 0.62])                        # tip of E
    Q = np.array([9.3, 0.60])                         # tip of J (dashed)
    # upper band: (1/sigma1)J1 then beta1 H^J1 / sigma1 ; J1 beyond
    line(ax, O, P2, lw=1.4)
    arrow(ax, O, O + 0.52 * (P1 - O), lw=1.4, ms=12)
    arrow(ax, P1 * 0.98 + P2 * 0.02, P2, lw=1.4, ms=12)
    arrow(ax, P1, P1 + 0.55 * (T - P1), lw=1.4, ms=12)
    line(ax, P1 + 0.60 * (T - P1), T, lw=1.4)
    ax.text(0.72, 0.94, r'$(1/\sigma_1)\mathbf{J}_1$', ha='left', va='bottom')
    ax.text(3.02, 1.98, r'$\mathbf{J}_1$', ha='right', va='bottom')
    ax.text(3.34, 0.88, r'$\beta_1\mathbf{H}{\wedge}\mathbf{J}_1/\sigma_1$',
            ha='left', va='center')
    # lower band
    line(ax, O, P4, lw=1.4)
    arrow(ax, O, O + 0.52 * (P3 - O), lw=1.4, ms=12)
    arrow(ax, P3 * 0.98 + P4 * 0.02, P4, lw=1.4, ms=12)
    arrow(ax, P3, P3 + 0.55 * (T - P3), lw=1.4, ms=12)
    line(ax, P3 + 0.60 * (T - P3), T, lw=1.4)
    ax.text(0.62, -1.10, r'$(1/\sigma_2)\mathbf{J}_2$', ha='left', va='top')
    ax.text(2.72, -1.95, r'$\mathbf{J}_2$', ha='left', va='top')
    ax.text(2.66, -0.50, r'$\beta_2\mathbf{H}{\wedge}\mathbf{J}_2/\sigma_2$',
            ha='left', va='center')
    # E common to both bands
    arrow(ax, O, O + 0.55 * (T - O), lw=1.4, ms=12)
    line(ax, O + 0.60 * (T - O), T, lw=1.4)
    ax.text(1.72, 0.44, r'$\mathbf{E}$', ha='center', va='bottom')
    # total current J (dashed) with the dashed completion
    line(ax, O, Q, lw=1.1, ls=DASH)
    arrow(ax, O + 0.42 * (Q - O), O + 0.52 * (Q - O), lw=1.1, ms=11)
    line(ax, P2, Q, lw=1.1, ls=DASH)
    line(ax, P4, Q, lw=1.1, ls=DASH)
    ax.text(4.35, 0.10, r'$\mathbf{J}$', ha='left', va='top')
    fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
    save(fig, 135)


# ----------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    keys = sys.argv[1:] or ['122', '123', '124', '125', '126', '127', '128',
                            '129', '130', '131', '132', '133', '134', '135']
    for k in keys:
        globals()['fig_' + k]()
