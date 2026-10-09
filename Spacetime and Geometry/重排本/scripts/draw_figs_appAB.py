# -*- coding: utf-8 -*-
"""Redraw Appendix A & B figures of Carroll, Spacetime and Geometry.

Figures:
  A.1 pullback of a function (p.423)          A.2 pushforward of a vector (p.425)
  A.3 pullback of a one-form (p.426)          A.4 pull back / push forward tensors (p.426)
  B.1 coordinate change from a diffeomorphism (p.430)
  B.2 diffeomorphism of S^2 by rotation (p.431)
  B.3 rate of change of a tensor along integral curves (p.432)
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path
from matplotlib.patches import FancyArrowPatch, Ellipse, Circle, Rectangle

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

BASE = r'E:\AI整理书籍\卡罗尔\重排本'
OUT = os.path.join(BASE, 'figures')
PRE = os.path.join(OUT, 'preview')
os.makedirs(PRE, exist_ok=True)


def new_ax(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def save(fig, key):
    fig.savefig(os.path.join(OUT, f'fig_{key}.pdf'),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PRE, f'fig_{key}.png'),
                bbox_inches='tight', pad_inches=0.03, dpi=200)
    plt.close(fig)


def farrow(ax, p0, p1, lw=2.4, ms=22, rad=0.0, color='k', zorder=5):
    """Straight (or slightly bowed) fat arrow, as in the original diagrams."""
    ax.add_patch(FancyArrowPatch(
        p0, p1, arrowstyle='-|>', mutation_scale=ms, lw=lw, color=color,
        shrinkA=0, shrinkB=0, zorder=zorder,
        connectionstyle=f'arc3,rad={rad}'))


def path_arrow(ax, pts, lw=1.9, ms=17, color='k', zorder=5):
    """Smooth arrow following a polyline (for curved arrows)."""
    pts = np.asarray(pts, float)
    path = Path(pts, [Path.MOVETO] + [Path.LINETO] * (len(pts) - 1))
    ax.add_patch(FancyArrowPatch(
        path=path, arrowstyle='-|>', mutation_scale=ms, lw=lw,
        color=color, shrinkA=0, shrinkB=0, zorder=zorder))


def dashed_arrow(ax, pts, lw=1.1, ms=15, color='k', zorder=4):
    """Dashed curved leader line with an arrowhead at its end."""
    pts = np.asarray(pts, float)
    ax.plot(pts[:-1, 0], pts[:-1, 1], ls=(0, (5, 4)), color=color, lw=lw,
            zorder=zorder)
    farrow(ax, pts[-2], pts[-1], lw=lw, ms=ms, zorder=zorder)


def arc_pts(center, a, b, th1, th2, n=60):
    """Points on the ellipse (center, semi-axes a,b) from angle th1 to th2 (deg)."""
    th = np.radians(np.linspace(th1, th2, n))
    return np.column_stack([center[0] + a * np.cos(th),
                            center[1] + b * np.sin(th)])


def catmull(points, closed=False, n=24):
    """Catmull-Rom spline through control points (smooth blob/curve)."""
    P = np.asarray(points, float)
    if closed:
        P = np.vstack([P[-1], P, P[0], P[1]])
    else:
        P = np.vstack([P[0], P, P[-1]])
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        ts = np.linspace(0, 1, n, endpoint=(i == len(P) - 3))
        for t in ts:
            t2, t3 = t * t, t * t * t
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t
                              + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    return np.array(out)


# ---------------------------------------------------------------- Figure A.1
def fig_A_1():
    fig, ax = new_ax(4.5, 2.85, (0.4, 10.3), (0, 6.35))

    # manifolds
    ax.add_patch(Ellipse((2.1, 3.35), 2.6, 1.55, fill=False, lw=1.3, zorder=3))
    ax.add_patch(Ellipse((6.75, 3.35), 2.6, 1.55, fill=False, lw=1.3, zorder=3))
    ax.text(0.95, 4.25, r'$M$', fontsize=12)
    ax.text(5.75, 4.25, r'$N$', fontsize=12)

    # the real line R (slanted) at upper right
    ax.plot([8.6, 9.95], [5.95, 3.55], color='k', lw=1.3, zorder=3)
    ax.text(9.05, 5.5, r'$\mathbf{R}$', fontsize=12)

    # arrows
    farrow(ax, (3.05, 4.35), (8.5, 5.6), rad=-0.12)         # phi* f = f o phi
    ax.text(5.35, 5.62, r'$\phi^* f = f \circ \phi$', fontsize=12)
    farrow(ax, (3.55, 3.35), (5.3, 3.35))                   # phi : M -> N
    ax.text(4.4, 3.62, r'$\phi$', fontsize=12)
    farrow(ax, (8.1, 3.6), (9.0, 4.6))                      # f : N -> R
    ax.text(8.3, 4.42, r'$f$', fontsize=12)
    farrow(ax, (2.1, 2.52), (2.1, 1.72))                    # chart x^mu
    ax.text(2.32, 2.08, r'$x^\mu$', fontsize=12)
    farrow(ax, (6.75, 2.52), (6.75, 1.72))                  # chart y^alpha
    ax.text(6.97, 2.08, r'$y^\alpha$', fontsize=12)

    # coordinate charts as squares
    ax.add_patch(Rectangle((1.2, 0.1), 1.85, 1.62, fill=False, lw=1.3, zorder=3))
    ax.text(2.88, 1.56, r'$\mathbf{R}^m$', fontsize=12, ha='right', va='top')
    ax.add_patch(Rectangle((5.85, 0.1), 1.85, 1.62, fill=False, lw=1.3, zorder=3))
    ax.text(7.53, 1.56, r'$\mathbf{R}^n$', fontsize=12, ha='right', va='top')

    save(fig, 'A.1')


# ---------------------------------------------------------------- Figure A.2
def fig_A_2():
    fig, ax = new_ax(4.35, 2.15, (1.7, 10.0), (0, 4.15))

    # the reals as a horizontal line
    ax.plot([2.9, 6.1], [3.55, 3.55], color='k', lw=1.3, zorder=3)
    ax.text(3.15, 3.78, r'$\mathbf{R}$', fontsize=12)

    ax.text(2.9, 0.5, r'$\mathcal{F}(M)$', fontsize=12, ha='center')
    ax.text(7.9, 0.5, r'$\mathcal{F}(N)$', fontsize=12, ha='center')

    farrow(ax, (3.55, 0.82), (3.55, 3.3))                   # V(p): F(M) -> R
    ax.text(2.95, 2.0, r'$V(p)$', fontsize=12, ha='right')
    farrow(ax, (7.0, 0.5), (4.1, 0.5))                      # phi*: F(N) -> F(M)
    ax.text(5.65, 0.9, r'$\phi^*$', fontsize=12)
    farrow(ax, (7.35, 0.8), (5.35, 3.3))                   # phi_*(V(p))
    ax.text(6.75, 2.05, r'$\phi_*(V(p)) = V(p) \circ \phi^*$', fontsize=12)

    save(fig, 'A.2')


# ---------------------------------------------------------------- Figure A.3
def fig_A_3():
    fig, ax = new_ax(4.4, 1.8, (0.2, 10.2), (0, 4.1))

    ax.plot([5.6, 8.9], [3.5, 3.5], color='k', lw=1.3, zorder=3)
    ax.text(8.6, 3.73, r'$\mathbf{R}$', fontsize=12)

    ax.text(2.6, 0.5, r'$T_p M$', fontsize=12, ha='center')
    ax.text(7.9, 0.5, r'$T_{\phi(p)} N$', fontsize=12, ha='center')

    farrow(ax, (3.6, 0.55), (6.7, 0.55))                    # phi_*
    ax.text(5.15, 0.93, r'$\phi_*$', fontsize=12)
    farrow(ax, (7.75, 0.85), (7.75, 3.3))                   # omega
    ax.text(8.03, 2.0, r'$\omega$', fontsize=12)
    farrow(ax, (2.75, 0.85), (5.05, 3.3))                   # phi*(omega)
    ax.text(0.55, 2.0, r'$\phi^*(\omega) = \omega \circ \phi_*$', fontsize=12)

    save(fig, 'A.3')


# ---------------------------------------------------------------- Figure A.4
def fig_A_4():
    fig, ax = new_ax(4.4, 2.05, (0, 10.4), (-0.2, 4.8))

    # (k,0) tensors pushed forward
    ax.text(2.2, 4.0, r'$\binom{k}{0}$', fontsize=13, ha='center', va='center')
    ax.text(8.2, 4.0, r'$\binom{k}{0}$', fontsize=13, ha='center', va='center')
    farrow(ax, (3.4, 4.0), (6.6, 4.0))
    ax.text(5.0, 4.35, r'$\phi_*$', fontsize=12, ha='center')

    # manifolds
    ax.add_patch(Ellipse((2.2, 2.2), 2.9, 1.6, fill=False, lw=1.3, zorder=3))
    ax.add_patch(Ellipse((8.2, 2.2), 2.9, 1.6, fill=False, lw=1.3, zorder=3))
    ax.text(1.0, 3.15, r'$M$', fontsize=12)
    ax.text(7.0, 3.15, r'$N$', fontsize=12)
    farrow(ax, (3.8, 2.2), (6.6, 2.2))
    ax.text(5.2, 2.5, r'$\phi$', fontsize=12, ha='center')

    # (0,l) tensors pulled back
    ax.text(2.2, 0.5, r'$\binom{0}{l}$', fontsize=13, ha='center', va='center')
    ax.text(8.2, 0.5, r'$\binom{0}{l}$', fontsize=13, ha='center', va='center')
    farrow(ax, (6.9, 0.5), (3.5, 0.5))
    ax.text(5.2, 0.85, r'$\phi^*$', fontsize=12, ha='center')

    save(fig, 'A.4')


# ---------------------------------------------------------------- Figure B.1
def fig_B_1():
    fig, ax = new_ax(4.6, 1.9, (-0.5, 10.3), (-0.45, 4.0))

    # manifold M with a flow loop (phi_t : M -> M)
    ax.add_patch(Ellipse((2.1, 1.6), 3.0, 1.7, fill=False, lw=1.3, zorder=3))
    ax.text(1.5, 1.68, r'$M$', fontsize=12)
    loop = arc_pts((1.1, 2.8), 0.8, 0.8, 150, -25, n=80)        # over the top
    path_arrow(ax, loop, lw=2.2, ms=20)

    # three maps M -> R^n
    farrow(ax, (3.8, 2.15), (6.8, 2.15), rad=-0.45, lw=2.2, ms=19)
    ax.text(5.1, 3.0, r'$x^\mu$', fontsize=12, ha='center')
    farrow(ax, (3.8, 1.6), (6.82, 1.6), lw=2.2, ms=19)
    ax.text(5.15, 1.9, r'$y^\mu$', fontsize=12, ha='center')
    farrow(ax, (3.8, 1.05), (6.8, 1.05), rad=0.45, lw=2.2, ms=19)
    ax.text(4.95, 0.0, r'$(\phi^* x)^\mu$', fontsize=12, ha='center')

    # coordinate space
    ax.add_patch(Rectangle((6.9, 0.45), 2.6, 2.4, fill=False, lw=1.3, zorder=3))
    ax.text(9.32, 2.68, r'$\mathbf{R}^n$', fontsize=12, ha='right', va='top')

    save(fig, 'B.1')


# ---------------------------------------------------------------- Figure B.2
def fig_B_2():
    fig, ax = new_ax(3.3, 3.6, (-1.45, 1.45), (-1.55, 1.62))
    R = 1.0
    sina, cosa = 0.30, np.sqrt(1 - 0.30 ** 2)

    # sphere (flat light-gray, black outline)
    ax.add_patch(Circle((0, 0), R, facecolor='0.93', edgecolor='k',
                        lw=1.2, zorder=2))

    # rotation axis (outside the sphere only)
    ax.plot([0, 0], [R, 1.5], color='k', lw=1.2, zorder=3)
    ax.plot([0, 0], [-R, -1.5], color='k', lw=1.2, zorder=3)

    # rotation arrow around the axis near the north pole
    loop = arc_pts((0, 1.3), 0.30, 0.09, 140, 410, n=100)
    path_arrow(ax, loop, lw=1.7, ms=17)
    ax.text(0.36, 1.5, r'$\phi$', fontsize=12)

    # latitude circles with flow dots and arrows
    clist = [0.60, 0.32, 0.06, -0.22, -0.50, -0.78]
    nflows = [1, 3, 3, 3, 3, 1]
    for c, nf in zip(clist, nflows):
        r = np.sqrt(R * R - c * c)
        cy = c * cosa
        b = r * sina
        ax.add_patch(Ellipse((0, cy), 2 * r, 2 * b, fill=False, lw=0.9,
                             zorder=3))
        ths = [268] if nf == 1 else [222, 270, 318]
        for th0 in ths:
            p0 = (r * np.cos(np.radians(th0)), cy + b * np.sin(np.radians(th0)))
            ax.add_patch(Circle(p0, 0.028, color='k', zorder=6))
            p1 = arc_pts((0, cy), r, b, th0 + 2, th0 + 22, n=12)[-1]
            farrow(ax, p0, p1, lw=2.0, ms=13, zorder=6)

    save(fig, 'B.2')


# ---------------------------------------------------------------- Figure B.3
def fig_B_3():
    fig, ax = new_ax(4.8, 2.02, (0, 10), (0, 4.2))

    # blob for the manifold M
    outline = [(4.75, 3.62), (5.5, 3.85), (6.3, 3.72), (7.1, 3.95),
               (8.3, 3.8), (9.35, 3.35), (9.7, 2.5), (9.3, 1.55),
               (8.3, 0.95), (7.0, 0.7), (5.9, 0.95), (4.9, 0.62),
               (3.6, 0.5), (2.5, 0.75), (1.45, 1.3), (0.8, 2.2),
               (1.05, 3.0), (1.9, 3.45), (3.0, 3.42), (3.7, 3.6),
               (4.15, 3.38)]
    blob = catmull(outline, closed=True, n=18)
    ax.fill(blob[:, 0], blob[:, 1], facecolor='0.82', edgecolor='k',
             lw=1.3, zorder=1)
    ax.text(1.75, 3.5, r'$M$', fontsize=12)

    # integral curve x^mu(t)
    curve = catmull([(1.6, 0.72), (2.9, 1.15), (4.3, 1.5), (5.7, 1.85),
                     (7.05, 2.15), (7.9, 2.6), (8.55, 3.28)], n=14)
    path_arrow(ax, curve, lw=1.1, ms=14)
    ax.text(8.7, 3.3, r'$x^\mu(t)$', fontsize=12)

    # points
    p = (2.9, 1.15)
    ptp = (7.05, 2.15)
    ax.add_patch(Circle(p, 0.045, color='k', zorder=6))
    ax.add_patch(Circle(ptp, 0.045, color='k', zorder=6))
    ax.text(2.9, 0.82, r'$p$', fontsize=12, ha='center')
    ax.text(7.05, 1.75, r'$\phi_t(p)$', fontsize=12, ha='center')

    # tensors as thick arrows
    farrow(ax, p, (1.8, 1.45), lw=2.6, ms=22)               # T(p)
    ax.text(1.95, 1.68, r'$T(p)$', fontsize=12)
    farrow(ax, p, (3.02, 2.3), lw=2.6, ms=22)               # pullback at p
    ax.text(3.3, 2.52, r'$\phi_t^*[\,T(\phi_t(p))\,]$', fontsize=12)
    farrow(ax, ptp, (7.3, 3.2), lw=2.6, ms=22)              # T at phi_t(p)
    ax.text(7.15, 3.28, r'$T[(\phi_t(p))]$', fontsize=12, ha='right')

    # dashed pull-back leader from phi_t(p) toward p
    dashed_arrow(ax, [(6.85, 2.35), (5.4, 2.42), (4.2, 2.15), (3.35, 1.78)])

    save(fig, 'B.3')


if __name__ == '__main__':
    for key, fn in [('A.1', fig_A_1), ('A.2', fig_A_2), ('A.3', fig_A_3),
                    ('A.4', fig_A_4), ('B.1', fig_B_1), ('B.2', fig_B_2),
                    ('B.3', fig_B_3)]:
        fn()
        print('done', key)
