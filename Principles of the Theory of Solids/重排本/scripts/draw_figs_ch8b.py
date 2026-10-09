# -*- coding: utf-8 -*-
"""Redraw Ziman, Principles of the Theory of Solids, 2nd ed., Chapter 8, Figs. 145-152.
Black-and-white textbook-style vector figures."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.path import Path
import matplotlib.patches as mpatches

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
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle='-|>', color='k', lw=lw, linestyle=ls,
                                mutation_scale=ms, shrinkA=0, shrinkB=0))


def brace(ax, p0, p1, depth, lw=1.0):
    """Curly brace from p0 to p1.

    The body runs at depth |depth|*0.45 and the tip at |depth|, both on the
    same side of the p0->p1 line; sign(depth) picks that side (side = -sign).
    """
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float)
    d = p1 - p0
    L = float(np.hypot(*d))
    u = d / L
    n = np.array([u[1], -u[0]])  # right-hand normal of direction
    s = -np.sign(depth)

    def M(sa, t):
        return p0 + u * sa + n * t

    e = 0.16 * L
    b = 0.45 * abs(depth)
    tb = s * b
    xm = 0.5 * L
    pts = [tuple(M(0, 0))]; codes = [Path.MOVETO]

    def C(c1, c2, p):
        pts.append(tuple(c1)); codes.append(Path.CURVE4)
        pts.append(tuple(c2)); codes.append(Path.CURVE4)
        pts.append(tuple(p)); codes.append(Path.CURVE4)

    C(M(0, s * 0.5 * b), M(0, tb), M(e, tb))
    pts.append(tuple(M(xm - e, tb))); codes.append(Path.LINETO)
    C(M(xm - 0.55 * e, tb), M(xm - 0.12 * e, tb), M(xm, -depth))
    C(M(xm + 0.12 * e, tb), M(xm + 0.55 * e, tb), M(xm + e, tb))
    pts.append(tuple(M(L - e, tb))); codes.append(Path.LINETO)
    C(M(L, tb), M(L, s * 0.5 * b), M(L, 0))
    ax.add_patch(mpatches.PathPatch(Path(pts, codes), facecolor='none',
                                    edgecolor='k', lw=lw))


def cr_closed(P, n=80):
    """Closed Catmull-Rom spline through control points P (list of xy)."""
    P = np.asarray(P, float)
    m = len(P)
    out = []
    for i in range(m):
        p0, p1, p2, p3 = P[(i - 1) % m], P[i], P[(i + 1) % m], P[(i + 2) % m]
        t = np.linspace(0, 1, n, endpoint=False)[:, None]
        a = 2 * p1
        b = -p0 + p2
        c = 2 * p0 - 5 * p1 + 4 * p2 - p3
        d = -p0 + 3 * p1 - 3 * p2 + p3
        out.append(0.5 * (a + b * t + c * t ** 2 + d * t ** 3))
    return np.vstack(out)


def cr_open(P, n=80):
    """Open Catmull-Rom spline (clamped ends)."""
    P = np.asarray(P, float)
    m = len(P)
    ext = np.vstack([2 * P[0] - P[1], P, 2 * P[-1] - P[-2]])
    out = []
    for i in range(m - 1):
        p0, p1, p2, p3 = ext[i], ext[i + 1], ext[i + 2], ext[i + 3]
        t = np.linspace(0, 1, n, endpoint=False)[:, None]
        a = 2 * p1
        b = -p0 + p2
        c = 2 * p0 - 5 * p1 + 4 * p2 - p3
        d = -p0 + 3 * p1 - 3 * p2 + p3
        out.append(0.5 * (a + b * t + c * t ** 2 + d * t ** 3))
    out.append(P[-1][None, :])
    return np.vstack(out)


# ----------------------------------------------------------------------
# Fig. 145  Optical transitions at F-centre (configuration-coordinate diagram)
# ----------------------------------------------------------------------
def fig_145():
    fig, ax = plt.subplots(figsize=(4.0, 3.55))
    ua, ub = 2.2, 4.6
    ya, yb = 1.55, 4.2
    ca, cb = 0.130, 0.2256

    def pa(x):
        return ya + ca * (x - ua) ** 2

    def pb(x):
        return yb + cb * (x - ub) ** 2

    # axes
    ax.plot([0.3, 0.3], [0, 6.15], color='k', lw=1.2)
    arrow(ax, (0.3, 0), (7.35, 0), lw=1.2, ms=13)
    ax.text(0.10, 3.85, r'$\mathcal{E}$', ha='right', va='center', fontsize=12)
    ax.text(7.45, -0.38, r'$u$', ha='center', va='center')

    xs = np.linspace(0.60, 5.35, 200)
    ax.plot(xs, pa(xs), color='k', lw=1.4)
    xs = np.linspace(1.68, 6.62, 200)
    ax.plot(xs, pb(xs), color='k', lw=1.4)
    ax.text(5.55, 2.62, r'$|a\rangle$', fontsize=12)
    ax.text(6.75, 4.95, r'$|b\rangle$', fontsize=12)

    A = (ua, pa(ua)); Ap = (ub, pa(ub)); B = (ub, pb(ub)); Bp = (ua, pb(ua))
    # dashed verticals to axis
    ax.plot([ua, ua], [0, pa(ua)], 'k--', lw=0.9)
    ax.plot([ub, ub], [0, pa(ub)], 'k--', lw=0.9)
    ax.text(ua, -0.38, r'$u_a$', ha='center')
    ax.text(ub, -0.38, r'$u_b$', ha='center')

    # vibrational levels (dashed chords)
    for y in (1.70, 1.84, 1.98):
        w = np.sqrt((y - ya) / ca)
        ax.plot([ua - w, ua + w], [y, y], 'k--', lw=0.9)
    for y in (4.40, 4.55, 4.68):
        w = np.sqrt((y - yb) / cb)
        ax.plot([ub - w, ub + w], [y, y], 'k--', lw=0.9)

    # absorption  A -> B'
    ax.plot([ua, ua], [pa(ua), pb(ua)], 'k-', lw=1.1)
    arrow(ax, (ua, 2.85), (ua, 3.55))
    ax.text(1.98, 2.62, r'$\hbar\omega_{ab}$', ha='right')
    # emission  B -> A'
    ax.plot([ub, ub], [pb(ub), pa(ub)], 'k-', lw=1.1)
    arrow(ax, (ub, 3.55), (ub, 2.90))
    ax.text(4.78, 3.62, r'$\hbar\omega_{ba}$', ha='left')

    # phonon-assisted  A'' <-> B''  (double arrow capsule)
    xc = 3.35
    yAl = pa(xc)          # on lower parabola right arm
    yBb = pb(xc)          # on upper parabola left arm
    ax.plot([xc - 0.045, xc - 0.045], [yAl, yBb], 'k-', lw=1.1)
    ax.plot([xc + 0.045, xc + 0.045], [yAl, yBb], 'k-', lw=1.1)
    arrow(ax, (xc - 0.045, 2.9), (xc - 0.045, 3.5))
    arrow(ax, (xc + 0.045, 3.5), (xc + 0.045, 2.9))
    for (px, py) in ((xc, yAl), (xc, yBb)):
        ax.plot(px, py, 'ko', ms=4.5)
    ax.text(xc - 0.16, yAl - 0.05, r"$A''$", ha='right')
    ax.text(xc - 0.18, yBb + 0.30, r"$B''$", ha='right')

    # marked points
    for (px, py, tx, ty, ha) in ((A[0], A[1], -0.14, -0.22, 'right'),
                                 (Ap[0], Ap[1], 0.20, 0.02, 'left'),
                                 (B[0], B[1], 0.20, -0.10, 'left'),
                                 (Bp[0], Bp[1], 0.20, 0.05, 'left')):
        ax.plot(px, py, 'ko', ms=4.5)
        ax.text(px + tx, py + ty, {'A': 'A', 'Ap': "A'", 'B': 'B', 'Bp': "B'"}[
            {(A[0], A[1]): 'A', (Ap[0], Ap[1]): 'Ap', (B[0], B[1]): 'B',
             (Bp[0], Bp[1]): 'Bp'}[(px, py)]], ha=ha)

    ax.set_xlim(-0.55, 7.75)
    ax.set_ylim(-0.75, 6.5)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, '145')


# ----------------------------------------------------------------------
# Fig. 146  X-ray emission
# ----------------------------------------------------------------------
def fig_146():
    fig, ax = plt.subplots(figsize=(3.2, 3.7))
    bw = 1.55          # band width
    ytop, yF, ybot = 3.15, 2.62, 2.10

    # energy axis
    arrow(ax, (0, 0.15), (0, 3.75), lw=1.1, ms=12)
    ax.text(-0.10, 3.62, r'$\mathcal{E}$', ha='right', fontsize=12)

    # conduction band: upper part (empty, grey), lower part (filled, hatched)
    ax.add_patch(mpatches.Rectangle((0, yF), bw, ytop - yF,
                                    facecolor='0.78', edgecolor='none'))
    band_lo = mpatches.Rectangle((0, ybot), bw, yF - ybot,
                                 facecolor='white', edgecolor='none')
    ax.add_patch(band_lo)
    x = -0.52
    while x < bw:
        xa, xb = max(x, 0.0), min(x + (yF - ybot), bw)
        if xb > xa:
            ax.plot([xa, xb], [ybot + (xa - x), ybot + (xb - x)], 'k-', lw=0.7)
        x += 0.28
    for y in (ytop, yF, ybot):
        ax.plot([0, bw], [y, y], 'k-', lw=1.1)
    ax.text(-0.09, yF, r'$\mathcal{E}_F$', ha='right', va='center')

    # brackets + labels
    ax.plot([bw + 0.10, bw + 0.10], [ybot, ytop], 'k-', lw=1.0)
    for y in (ybot, ytop):
        ax.plot([bw, bw + 0.10], [y, y], 'k-', lw=1.0)
    ax.text(bw + 0.22, (ybot + ytop) / 2 + 0.07, 'Conduction\nband', va='center')
    ya1, ya2 = 1.86, 0.35
    ax.plot([bw + 0.10, bw + 0.10], [ya2, ya1], 'k-', lw=1.0)
    for y in (ya2, ya1):
        ax.plot([bw * 0.78, bw + 0.10], [y, y], 'k-', lw=0.0)
    ax.text(bw + 0.22, (ya2 + ya1) / 2 + 0.05, 'Atomic\nlevels', va='center')

    # atomic levels: two triplets + one deep line
    for y in (1.86, 1.80, 1.73):
        ax.plot([0, bw * 0.78], [y, y], 'k-', lw=0.9)
    for y in (1.10, 1.04, 0.97):
        ax.plot([0, bw * 0.78], [y, y], 'k-', lw=0.9)
    ax.plot([0, bw * 0.78], [0.35, 0.35], 'k-', lw=0.9)

    # radiative transition: filled dot in band -> open circle on deep level
    xd = 0.62
    ax.plot(xd, 2.35, 'ko', ms=5)
    arrow(ax, (xd, 2.30), (xd, 0.46), lw=1.1, ms=12)
    ax.add_patch(mpatches.Circle((xd, 0.35), 0.055, facecolor='white',
                                 edgecolor='k', lw=1.0, zorder=5))

    ax.set_xlim(-0.55, 3.15)
    ax.set_ylim(-0.1, 3.95)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, '146')


# ----------------------------------------------------------------------
# Fig. 147  Photo-emission
# ----------------------------------------------------------------------
def fig_147():
    fig, ax = plt.subplots(figsize=(4.3, 3.9))
    xsurf = 6.1      # metal surface (right edge of drawn metal)
    xstep = 2.6      # potential step (left edge of metal block)
    yvac = 4.5       # vacuum level (thick line, outside)
    yF = 3.95        # Fermi level
    ytop = 7.0       # detected-electron energy line
    ybot = 1.45

    # metal block with explicit horizontal-line hatching
    ax.plot([xstep, xsurf], [yF, yF], 'k-', lw=1.1)
    y = yF - 0.09
    while y > 2.45:
        ax.plot([xstep, xsurf], [y, y], 'k-', lw=0.55)
        y -= 0.09
    ax.plot([xstep, xsurf], [2.45, 2.45], 'k-', lw=0.55)
    # deeper narrow band
    yb2 = 2.08
    while yb2 > 1.70:
        ax.plot([xstep, xsurf], [yb2, yb2], 'k-', lw=0.55)
        yb2 -= 0.09
    # lens-shaped deep DOS blob attached at right of the deep band
    th = np.linspace(-np.pi / 2, np.pi / 2, 60)
    lx = xsurf + 0.85 * np.cos(th)
    ly = 1.90 + 0.20 * np.sin(th)
    ax.plot(np.r_[lx, lx[::-1]], np.r_[ly, ly[::-1]], 'k-', lw=0.9)
    for yy in (2.02, 1.90, 1.78):
        xe = xsurf + 0.85 * np.sqrt(max(0.0, 1 - ((yy - 1.90) / 0.20) ** 2))
        ax.plot([xstep, xe], [yy, yy], 'k-', lw=0.55)

    # surface & step verticals
    ax.plot([xsurf, xsurf], [ybot, 10.2], 'k-', lw=1.1)
    ax.plot([xstep, xstep], [ybot, yvac], 'k-', lw=1.1)
    # vacuum level (thick) and dashed Fermi level outside
    ax.plot([0.55, xstep], [yvac, yvac], 'k-', lw=2.4)
    ax.plot([0.55, xstep], [yF, yF], 'k--', lw=1.1)
    ax.text(xstep + 0.12, yF + 0.18, r'$\mathcal{E}_F$')

    # work function and outgoing energy markers
    arrow(ax, (1.45, yF), (1.45, yvac)); arrow(ax, (1.45, yvac), (1.45, yF))
    ax.text(1.28, 4.2, r'$\phi_W$', ha='right')
    arrow(ax, (1.35, yvac), (1.35, ytop)); arrow(ax, (1.35, ytop), (1.35, yvac))
    ax.text(1.50, 5.72, r'$\mathcal{E}$', ha='left')

    # n(E,w) line with left arrowhead, dashed to rho_f peak
    arrow(ax, (xsurf, ytop), (0.60, ytop), lw=1.1, ms=12)
    ax.plot([0.60, xsurf], [ytop, ytop], 'k-', lw=1.1)
    ax.plot([xsurf, 7.55], [ytop, ytop], 'k--', lw=1.0)
    ax.text(1.75, ytop + 0.22, r'$n(\mathcal{E},\,\omega)$')

    # vertical optical transition
    xd = 4.15
    ax.plot(xd, 3.10, 'ko', ms=5)
    ax.plot(xd, ytop, 'ko', ms=5)
    ax.plot([xd, xd], [3.18, ytop - 0.35], 'k-', lw=1.1)
    arrow(ax, (xd, 4.9), (xd, 5.55), ms=12)
    ax.text(xd + 0.18, 5.55, r'$\hbar\omega$')
    ax.plot([xd, 7.35], [3.10, 3.10], 'k--', lw=1.0)

    # density-of-states blob chain (rho_f big lobe, rho_i lobe)
    yy = np.linspace(10.2, 2.35, 400)
    xx = xsurf + 1.55 * np.exp(-0.5 * ((yy - 7.0) / 1.05) ** 2) \
        + 1.35 * np.exp(-0.5 * ((yy - 3.10) / 0.85) ** 2)
    ax.plot(xx, yy, 'k-', lw=1.2)
    ax.text(7.72, 7.05, r'$\rho_f(\mathcal{E})$', va='center')
    ax.text(7.42, 3.02, r'$\rho_i(\mathcal{E}-\hbar\omega)$', va='center')

    ax.set_xlim(0.1, 10.7)
    ax.set_ylim(1.15, 10.65)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, '147')


# ----------------------------------------------------------------------
# Fig. 148  Schematic behaviour of optical properties of metals
# ----------------------------------------------------------------------
def fig_148():
    fig, ax = plt.subplots(figsize=(4.4, 4.5))
    x0, x1 = 0.15, 10.3     # plot box (x)
    yb, yt = -3.0, 8.6      # bottom / top of left axis values (log10)
    xHR, xRel = 3.5, 7.1    # 1/tau and omega_p positions

    # axes
    ax.plot([x0, x0], [yb, 8.35], 'k-', lw=1.2)
    arrow(ax, (x0, 8.35), (x0, 8.95), lw=1.2, ms=13)
    arrow(ax, (x1, yb), (11.15, yb), lw=1.2, ms=13)
    ax.plot([x0, x1], [yb, yb], 'k-', lw=1.2)
    # right axis (for 1-R)
    ax.plot([x1, x1], [-2.9, 6.0], 'k-', lw=1.1)

    # left ticks
    for yv, lab in ((8, r'$10^{8}$'), (6, r'$10^{6}$'), (4, r'$10^{4}$'),
                    (2, r'$10^{2}$'), (0, r'$1$'), (-2, r'$10^{-2}$')):
        ax.plot([x0 - 0.14, x0], [yv, yv], 'k-', lw=1.0)
        ax.text(x0 - 0.24, yv, lab, ha='right', va='center', fontsize=10)
    for dy, lab in ((7.9, r'$\eta$'), (7.35, r'$n$'), (6.8, r'$k$')):
        ax.text(0.55, dy, lab, fontsize=12)
    # right ticks
    for yv, lab in ((6, r'$1$'), (4, r'$10^{-2}$'), (2, r'$10^{-4}$'),
                    (0, r'$10^{-6}$'), (-2, r'$10^{-8}$')):
        ax.plot([x1, x1 + 0.14], [yv, yv], 'k-', lw=1.0)
        ax.text(x1 + 0.26, yv, lab, va='center', fontsize=10)
    ax.text(x1 + 0.26, 4.95, r'$1-R$', va='center')

    # reference horizontal line at 1
    ax.plot([x0, x1], [0, 0], 'k-', lw=0.9)
    # plateau guide at 1-R = 1
    ax.plot([5.2, x1], [6.0, 6.0], 'k-', lw=1.1)
    # dashed region separators
    for xd in (xHR, xRel):
        ax.plot([xd, xd], [yb, 8.2], 'k--', lw=1.1)

    # ---- curves ----
    # eta: flat then single straight fall (slope ~ -2.1), exits bottom after omega_p
    xe = np.linspace(x0, 3.15, 60)
    ye = 7.85 + 0.13 * np.tanh((xe - 1.6) * 1.2)
    xf = np.linspace(3.5, 8.55, 80)
    yf = 7.52 - 2.09 * (xf - xHR)
    ax.plot(np.r_[xe, xf], np.r_[ye, yf], 'k-', lw=1.3)
    ax.text(4.28, 5.45, r'$\eta$', fontsize=13, ha='right')

    # n: dashed, falls ~w^-1/2, steep fall, min before omega_p, rises to 1
    xn = np.linspace(x0, xHR, 80)
    yn = 5.95 - 0.62 * (xn - x0) ** 0.92
    xs1 = np.linspace(xHR, 6.55, 60)
    ys1 = 3.60 - 1.95 * (xs1 - xHR) ** 1.06
    mn = -2.55
    xs2 = np.linspace(6.55, 6.85, 30)
    ys2 = ys1[-1] + (mn - ys1[-1]) * ((xs2 - 6.55) / 0.30) ** 1.4
    xr = np.linspace(6.85, 8.9, 60)
    yr = mn + (0 - mn) * (1 - np.exp(-2.1 * (xr - 6.85))) ** 1.5
    ax.plot(np.r_[xn, xs1, xs2, xr], np.r_[yn, ys1, ys2, yr], 'k--', lw=1.2)
    ax.text(5.05, 0.80, r'$n$', fontsize=13)

    # k: dashed, forks from n at 1/tau, straight fall, steep exit at bottom
    xk1 = np.linspace(xHR, xRel, 60)
    yk1 = 3.60 - 1.08 * (xk1 - xHR)
    xk2 = np.linspace(xRel, 7.85, 40)
    yk2 = yk1[-1] - (yk1[-1] + 3.0) * ((xk2 - xRel) / 0.75) ** 1.6
    ax.plot(np.r_[xk1, xk2], np.r_[yk1, yk2], 'k--', lw=1.2)
    ax.text(4.62, 3.12, r'$k$', fontsize=13)

    # 1-R: solid, rises w^1/2, flat in relaxation, S-rise to 1 plateau
    xr1 = np.linspace(0.3, xHR, 60)
    yr1 = 0.72 + 0.90 * (xr1 - 0.3) ** 0.92
    xr2 = np.linspace(xHR, 6.35, 30)
    yr2 = 2.62 + 0.02 * (xr2 - xHR)
    xs3 = np.linspace(6.35, 7.7, 60)
    yr3 = 2.64 + (6.0 - 2.64) * (1 - np.exp(-2.0 * (xs3 - 6.35))) ** 1.8
    ax.plot(np.r_[xr1, xr2, xs3], np.r_[yr1, yr2, yr3], 'k-', lw=1.3)
    ax.text(7.55, 4.85, r'$1-R$')

    # ln w label with small arrow
    ax.text(1.05, -2.45, r'$\ln\ \omega$')
    arrow(ax, (2.25, -2.45), (3.15, -2.45), lw=1.0, ms=10)

    # region braces and labels
    brace(ax, (0.25, yb), (xHR - 0.08, yb), -0.42, lw=1.0)
    brace(ax, (xHR + 0.08, yb), (xRel - 0.08, yb), -0.42, lw=1.0)
    brace(ax, (xRel + 0.08, yb), (10.22, yb), -0.42, lw=1.0)
    ax.text(1.58, -3.72, 'Hagen–Rubens', ha='center', va='top',
            fontsize=9)
    ax.text(xHR, -3.72, r'$1/\tau$', ha='center', va='top', fontsize=9)
    ax.text((xHR + xRel) / 2, -3.72, 'Relaxation', ha='center', va='top',
            fontsize=9)
    ax.text(xRel, -3.72, r'$\omega_p$', ha='center', va='top', fontsize=9)
    ax.text(9.45, -3.72, 'U.V. transparent',
            ha='center', va='top', fontsize=9)

    ax.set_xlim(-1.5, 12.4)
    ax.set_ylim(-4.9, 9.3)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, '148')


# ----------------------------------------------------------------------
# Fig. 149  Only electrons in the skin depth are 'effective'
# ----------------------------------------------------------------------
def fig_149():
    fig, ax = plt.subplots(figsize=(4.6, 1.95))
    W, H = 9.9, 4.3
    ax.add_patch(mpatches.Rectangle((0, 0), W, H, facecolor='0.82',
                                    edgecolor='none'))
    ax.plot([-0.15, 11.05], [H, H], 'k-', lw=2.4)

    # reflected trajectory (V)
    ax.plot([1.35, 3.5], [0.70, H], 'k-', lw=1.2)
    arrow(ax, (2.2, 2.10), (2.55, 2.85), lw=1.2)
    ax.plot([3.5, 4.75], [H, 0.30], 'k-', lw=1.2)
    arrow(ax, (4.35, 1.35), (4.62, 0.75), lw=1.2)
    # grazing trajectory within skin depth
    ax.plot([5.7, 9.25], [H - 0.03, 2.60], 'k-', lw=1.2)
    arrow(ax, (8.55, 3.05), (9.05, 2.73), lw=1.2)

    # mean-free-path brace under grazing trajectory
    brace(ax, (5.85, 2.05), (8.85, 2.05), -0.38, lw=1.0)
    ax.text(7.35, 1.30, r'$\Lambda$', ha='center', fontsize=12)
    # skin-depth brace at right (tip pointing right, like '}')
    brace(ax, (11.2, H), (11.2, 2.45), 0.42, lw=1.0)
    ax.text(11.78, 3.35, r'$\delta$', fontsize=12)

    ax.set_xlim(-0.35, 12.35)
    ax.set_ylim(-0.35, 5.0)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, '149')


# ----------------------------------------------------------------------
# helpers for Fermi-surface blob figures (150, 152)
# ----------------------------------------------------------------------
def _nearest_idx(poly, p):
    d = np.hypot(poly[:, 0] - p[0], poly[:, 1] - p[1])
    return int(np.argmin(d))


def _edge_interp(edge_pts, x):
    return np.interp(x, edge_pts[:, 0], edge_pts[:, 1])


def draw_fs_blob(ax, ctrl, belt_top, belt_bot, ticks=True, cx=0.0, cy=0.0,
                 scale=1.0, tick_step=0.075):
    """Fermi-surface blob with equatorial belt; shading below belt darker."""
    poly = cr_closed(ctrl) * scale + np.array([cx, cy])
    bt = cr_open(belt_top) * scale + np.array([cx, cy])
    bb = cr_open(belt_bot) * scale + np.array([cx, cy])

    # whole blob light grey
    ax.add_patch(mpatches.Polygon(poly, closed=True, facecolor='0.88',
                                  edgecolor='none', zorder=1))
    ax.plot(np.r_[poly[:, 0], poly[0, 0]], np.r_[poly[:, 1], poly[0, 1]],
            'k-', lw=1.3, zorder=4)

    # darker region below the belt
    iL = _nearest_idx(poly, bb[0]); iR = _nearest_idx(poly, bb[-1])
    m = len(poly)
    arcA = poly[np.arange(iL, iR + 1) % m]
    arcB = np.vstack([poly[np.arange(iR, m) % m], poly[np.arange(0, iL + 1) % m]])
    if len(arcA) == 0:
        arc = arcB
    elif len(arcB) == 0:
        arc = arcA
    else:
        arc = arcA if arcA[:, 1].mean() < arcB[:, 1].mean() else arcB
    region = np.vstack([bb[::-1], arc])
    ax.add_patch(mpatches.Polygon(region, closed=True, facecolor='0.70',
                                  edgecolor='none', zorder=2))

    # white belt band + ticks
    band = np.vstack([bt, bb[::-1]])
    ax.add_patch(mpatches.Polygon(band, closed=True, facecolor='white',
                                  edgecolor='none', zorder=3))
    if ticks:
        xlo = max(bt[:, 0].min(), bb[:, 0].min()) + 0.02
        xhi = min(bt[:, 0].max(), bb[:, 0].max()) - 0.02
        for x in np.arange(xlo, xhi, tick_step * scale):
            y1 = _edge_interp(bt, x); y0 = _edge_interp(bb, x)
            ax.plot([x, x], [y0, y1], 'k-', lw=0.7, zorder=3.5)
    ax.plot(bt[:, 0], bt[:, 1], 'k-', lw=1.1, zorder=4)
    ax.plot(bb[:, 0], bb[:, 1], 'k-', lw=1.1, zorder=4)
    return poly, bt, bb


# ----------------------------------------------------------------------
# Fig. 150  Belt of effective electrons on a Fermi surface
# ----------------------------------------------------------------------
def fig_150():
    fig, ax = plt.subplots(figsize=(4.3, 3.5))

    # ---- (a) coordinate frame at the metal surface ----
    ax.plot([-1.85, 2.3], [0, 0], 'k-', lw=1.2)
    for x in np.arange(-1.78, 2.25, 0.24):
        ax.plot([x, x - 0.24], [0, -0.32], 'k-', lw=0.8)
    arrow(ax, (0.35, 0.30), (0.35, 1.60), lw=1.2)          # z (unlabelled)
    arrow(ax, (0.35, 0.30), (1.55, 0.30), lw=1.2)
    ax.text(1.08, 0.08, r'$x$')
    arrow(ax, (0.35, 0.30), (-0.32, -0.55), lw=1.2)
    ax.text(0.10, 0.10, r'$y$')
    ax.text(1.72, 0.66, r'$\mathbf{E}$', fontsize=12)
    arrow(ax, (2.02, 0.70), (2.42, 0.70), lw=1.1)

    # ---- (b) Fermi surface with belt ----
    cx, cy, sc = 0.15, -3.80, 1.30
    ctrl = [(-0.28, 0.82), (0.12, 0.95), (0.52, 0.70), (0.80, 0.42),
            (1.08, 0.24), (1.24, -0.02), (1.02, -0.32), (0.60, -0.52),
            (0.22, -0.88), (-0.18, -0.94), (-0.62, -0.52), (-1.02, -0.20),
            (-1.14, 0.04), (-0.92, 0.30), (-0.55, 0.55)]
    belt_top = [(-1.08, -0.02), (-0.55, -0.18), (0.0, -0.30), (0.62, -0.22),
                (1.18, -0.06)]
    belt_bot = [(-1.04, -0.22), (-0.45, -0.48), (0.10, -0.60), (0.68, -0.50),
                (1.06, -0.32)]
    draw_fs_blob(ax, ctrl, belt_top, belt_bot, ticks=True, cx=cx, cy=cy, scale=sc)

    # P and v
    ax.text(cx + 0.46 * sc, cy - 0.52 * sc, r'$P$', fontsize=12)
    arrow(ax, (cx + 0.56 * sc, cy - 0.70 * sc), (cx + 1.06 * sc, cy - 1.10 * sc), lw=1.2)
    ax.text(cx + 1.14 * sc, cy - 1.22 * sc, r'$\mathbf{v}$')

    # three 'effective electrons' arrows + brace
    p0 = (cx + 1.16 * sc, cy - 0.04 * sc)
    arrow(ax, p0, (cx + 1.80 * sc, cy + 0.28 * sc), lw=1.1)
    arrow(ax, p0, (cx + 1.90 * sc, cy - 0.02 * sc), lw=1.1)
    arrow(ax, p0, (cx + 1.74 * sc, cy - 0.38 * sc), lw=1.1)
    brace(ax, (cx + 2.00 * sc, cy + 0.34 * sc), (cx + 2.00 * sc, cy - 0.44 * sc),
          0.15, lw=1.0)
    ax.text(cx + 2.22 * sc, cy - 0.05 * sc, 'Effective\nelectrons', va='center')

    ax.set_xlim(-2.4, 4.9)
    ax.set_ylim(-6.2, 2.0)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, '150')


# ----------------------------------------------------------------------
# Fig. 151  Surf-riding resonance
# ----------------------------------------------------------------------
def fig_151():
    fig, ax = plt.subplots(figsize=(4.7, 1.65))
    L = 9.9

    def yt(x):
        return 0.45 * np.sin(2 * np.pi * (x - 4.85) / 9.8) + 0.10

    def yb(x):
        return 0.45 * np.sin(2 * np.pi * (x - 5.45) / 9.8) - 0.70

    xs = np.linspace(0.05, L, 400)
    ax.plot(xs, yt(xs), 'k-', lw=1.3)
    ax.plot(np.linspace(0.30, L, 400), yb(np.linspace(0.30, L, 400)), 'k-', lw=1.3)

    # vertical hatch with varying density
    def s(x):  # local spacing
        pts = [(0.5, 0.13), (2.4, 0.16), (3.2, 0.45), (6.6, 0.50),
               (6.75, 0.08), (7.7, 0.08), (8.3, 0.50), (9.8, 0.60)]
        return np.interp(x, [p[0] for p in pts], [p[1] for p in pts])

    x = 0.55
    while x < 9.8:
        ax.plot([x, x], [yb(x), yt(x)], 'k-', lw=0.7)
        x += s(x)

    # phonon wave-vector q
    yq = -0.55
    arrow(ax, (3.50, yq), (5.10, yq), lw=1.2, ms=13)
    ax.text(3.95, -0.92, r'$\mathbf{q}$', fontsize=13)

    # electron velocity v (nearly normal to crests), dashed tail
    arrow(ax, (6.95, -1.28), (7.32, -0.78), lw=1.1, ls=(0, (4, 2.5)))
    arrow(ax, (7.32, -0.78), (8.06, 0.66), lw=1.2, ms=13)
    ax.text(8.16, -0.05, r'$\mathbf{v}$', fontsize=13)
    ax.text(8.42, 1.02, r'$\mathbf{v}\cdot\mathbf{q}$', fontsize=12)

    ax.set_xlim(-0.35, 10.45)
    ax.set_ylim(-2.05, 1.75)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, '151')


# ----------------------------------------------------------------------
# Fig. 152  Belt of electrons interacting with phonon q
# ----------------------------------------------------------------------
def fig_152():
    fig, ax = plt.subplots(figsize=(4.3, 2.6))
    cx, cy, sc = 0.0, 0.0, 1.0
    ctrl = [(-0.30, 0.80), (0.12, 0.95), (0.52, 0.70), (0.82, 0.42),
            (1.10, 0.26), (1.26, 0.12), (1.08, -0.14), (0.60, -0.40),
            (0.20, -0.85), (-0.20, -1.00), (-0.62, -0.55), (-1.02, -0.22),
            (-1.14, -0.04), (-0.92, 0.24), (-0.55, 0.50)]
    belt_top = [(-1.06, -0.02), (-0.50, -0.12), (0.20, -0.18), (0.80, -0.04),
                (1.20, 0.18)]
    belt_bot = [(-1.03, -0.16), (-0.50, -0.27), (0.20, -0.33), (0.80, -0.19),
                (1.17, 0.04)]
    draw_fs_blob(ax, ctrl, belt_top, belt_bot, ticks=False, cx=cx, cy=cy, scale=sc)

    # phonon q (vertical, left)
    arrow(ax, (cx - 1.45, cy - 0.10), (cx - 1.45, cy + 0.75), lw=1.2, ms=13)
    ax.text(cx - 1.31, cy + 0.48, r'$\mathbf{q}$', fontsize=13)
    # belt-direction arrows
    arrow(ax, (cx - 1.10, cy - 0.05), (cx - 1.85, cy - 0.06), lw=1.2)
    arrow(ax, (cx + 1.26, cy + 0.24), (cx + 2.00, cy + 0.27), lw=1.2)
    ax.text(cx + 1.72, cy + 0.02, r'$\mathbf{v}$', fontsize=13)
    arrow(ax, (cx + 1.06, cy - 0.24), (cx + 1.66, cy - 0.27), lw=1.2)
    # inner arrow (electron velocity in lower belt region)
    arrow(ax, (cx - 0.48, cy - 0.30), (cx - 0.10, cy - 0.64), lw=1.1)

    ax.set_xlim(-2.45, 2.65)
    ax.set_ylim(-1.65, 1.40)
    ax.set_aspect('equal')
    ax.axis('off')
    save(fig, '152')


if __name__ == '__main__':
    for f in (fig_145, fig_146, fig_147, fig_148, fig_149, fig_150, fig_151,
              fig_152):
        f()
