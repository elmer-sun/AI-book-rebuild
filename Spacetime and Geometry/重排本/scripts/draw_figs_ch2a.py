# -*- coding: utf-8 -*-
"""Redraw Chapter 2 figures (2.1 - 2.14) of Carroll, Spacetime and Geometry
as black-and-white textbook-style vector graphics.

Figures 2.1-2.14: Gravity as geometry / What is a manifold?
Output:  figures/fig_<key>.pdf  and  figures/preview/fig_<key>.png
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import (FancyArrowPatch, Ellipse, Polygon, Circle,
                                Rectangle)

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
})

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIGDIR = os.path.join(BASE, 'figures')
PREVIEW = os.path.join(FIGDIR, 'preview')
os.makedirs(PREVIEW, exist_ok=True)


# ----------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------
def save_fig(key, fig):
    fig.savefig(os.path.join(FIGDIR, 'fig_%s.pdf' % key),
                bbox_inches='tight', pad_inches=0.03)
    fig.savefig(os.path.join(PREVIEW, 'fig_%s.png' % key),
                dpi=200, bbox_inches='tight', pad_inches=0.03)
    plt.close(fig)


def arrow(ax, p0, p1, lw=1.2, ms=13, color='k', style='-|>', zorder=6,
          linestyle='-'):
    ax.annotate('', xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle=style, color=color, lw=lw,
                                mutation_scale=ms, shrinkA=0, shrinkB=0,
                                linestyle=linestyle), zorder=zorder)


def farrow(ax, p0, p1, rad=0.0, lw=2.2, ms=18, color='k', style='-|>',
           zorder=6, linestyle='-'):
    """Curved thick arrow (FancyArrowPatch)."""
    p = FancyArrowPatch(p0, p1, connectionstyle='arc3,rad=%g' % rad,
                        arrowstyle=style, mutation_scale=ms, lw=lw,
                        color=color, linestyle=linestyle,
                        shrinkA=0, shrinkB=0, zorder=zorder)
    ax.add_patch(p)
    return p


def blob(cx, cy, rx, ry, a1=0.14, a2=0.08, p1=0.8, p2=2.6, n=140, rot=0.0):
    """Closed organic blob (unit-radius modulated circle), scaled rx, ry."""
    th = np.linspace(0, 2 * np.pi, n)
    r = 1 + a1 * np.cos(3 * th + p1) + a2 * np.cos(2 * th + p2)
    x, y = rx * r * np.cos(th), ry * r * np.sin(th)
    if rot:
        c, s = np.cos(rot), np.sin(rot)
        x, y = c * x - s * y, s * x + c * y
    return cx + x, cy + y


def ellipse_poly(cx, cy, rx, ry, rot=0.0, n=100):
    th = np.linspace(0, 2 * np.pi, n)
    x, y = rx * np.cos(th), ry * np.sin(th)
    if rot:
        c, s = np.cos(rot), np.sin(rot)
        x, y = c * x - s * y, s * x + c * y
    return np.column_stack([cx + x, cy + y])


def clip_convex(subject, clipper):
    """Sutherland-Hodgman polygon clipping (clipper must be convex)."""
    out = [tuple(p) for p in subject]
    m = len(clipper)
    for i in range(m):
        a, b = clipper[i], clipper[(i + 1) % m]
        inp, out = out, []
        if not inp:
            break
        ax_, ay_ = float(a[0]), float(a[1])
        bx_, by_ = float(b[0]), float(b[1])

        def side(p, ax_=ax_, ay_=ay_, bx_=bx_, by_=by_):
            return (bx_ - ax_) * (p[1] - ay_) - (by_ - ay_) * (p[0] - ax_)

        prev = inp[-1]
        s_prev = side(prev)
        for p in inp:
            s = side(p)
            if s >= 0:
                if s_prev < 0:
                    q = np.asarray(prev, float); r = np.asarray(p, float)
                    t = s_prev / (s_prev - s)
                    out.append(tuple(q + t * (r - q)))
                out.append(p)
            elif s_prev >= 0:
                q = np.asarray(prev, float); r = np.asarray(p, float)
                t = s_prev / (s_prev - s)
                out.append(tuple(q + t * (r - q)))
            prev = p
            s_prev = s
    return np.array(out) if out else np.zeros((0, 2))


def homography(p00, p10, p11, p01, dst):
    """3x3 projective map of the unit square (0,0)(1,0)(1,1)(0,1) to the
    quadrilateral dst=[BL,BR,TR,TL]."""
    src = np.array([(0, 0), (1, 0), (1, 1), (0, 1)], float)
    dst = np.array(dst, float)
    A = []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y, -u])
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y, -v])
    A = np.array(A)
    _, _, Vt = np.linalg.svd(A)
    return Vt[-1].reshape(3, 3)


def apply_h(H, pts):
    pts = np.atleast_2d(pts)
    q = np.c_[pts, np.ones(len(pts))] @ H.T
    return q[:, 0] / q[:, 2], q[:, 1] / q[:, 2]


def shaded_surface(ax, X, Y, Z, light=(0.4, -0.5, 1.0), gmin=0.80, gmax=1.0,
                   lw=0.35, edge='0.15'):
    """mplot3d surface, white-to-light-gray Lambert shading, black mesh."""
    from matplotlib.colors import to_rgba
    L = np.array(light, float)
    L /= np.linalg.norm(L)
    M, N = X.shape
    FC = np.zeros((M, N, 4))
    for i in range(M - 1):
        for j in range(N - 1):
            p00 = np.array([X[i, j], Y[i, j], Z[i, j]])
            p10 = np.array([X[i + 1, j], Y[i + 1, j], Z[i + 1, j]])
            p01 = np.array([X[i, j + 1], Y[i, j + 1], Z[i, j + 1]])
            n = np.cross(p10 - p00, p01 - p00)
            nn = np.linalg.norm(n)
            nd = abs(np.dot(n, L)) / nn if nn > 0 else 1.0
            g = gmin + (gmax - gmin) * nd
            FC[i, j] = to_rgba((g, g, g))
    FC[-1] = FC[-2]
    FC[:, -1] = FC[:, -2]
    ax.plot_surface(X, Y, Z, facecolors=FC, shade=False,
                    edgecolor=edge, linewidth=lw)


def torus_mesh(R=1.0, r=0.42, nu=40, nv=20, cx=0.0, cy=0.0):
    u = np.linspace(0, 2 * np.pi, nu)
    v = np.linspace(0, 2 * np.pi, nv)
    U, V = np.meshgrid(u, v, indexing='ij')
    X = (R + r * np.cos(V)) * np.cos(U) + cx
    Y = (R + r * np.cos(V)) * np.sin(U) + cy
    Z = r * np.sin(V) * np.ones_like(U)
    return X, Y, Z


def sphere_mesh(R=1.0, nu=36, nv=18, squash=0.94):
    u = np.linspace(0, 2 * np.pi, nu)
    v = np.linspace(0, np.pi, nv)
    U, V = np.meshgrid(u, v, indexing='ij')
    X = R * np.sin(V) * np.cos(U)
    Y = R * np.sin(V) * np.sin(U)
    Z = squash * R * np.cos(V)
    return X, Y, Z


def genus2_mesh(A=1.5, B=1.1, r=0.34, nu=72, nv=18):
    """Genus-2 look: a tube of radius r swept along a figure-8 (Gerono
    lemniscate) in the xy-plane.  One smooth parametrization whose two
    lobes read as a fused two-holed pretzel, matching the book's render."""
    u = np.linspace(0, 2 * np.pi, nu)
    phi = np.linspace(0, 2 * np.pi, nv)
    U, PH = np.meshgrid(u, phi, indexing='ij')
    xC = A * np.cos(U)
    yC = B * np.sin(U) * np.cos(U)
    tx = -A * np.sin(U)
    ty = B * np.cos(2 * U)
    L = np.hypot(tx, ty)
    tx, ty = tx / L, ty / L
    nx_, ny_ = ty, -tx               # in-plane unit normal
    X = xC + r * np.cos(PH) * nx_
    Y = yC + r * np.cos(PH) * ny_
    Z = r * np.sin(PH)
    return X, Y, Z


def setup3d(ax, elev=25, azim=-55, aspect=(1, 1, 1), proj='persp'):
    ax.set_proj_type(proj)
    ax.view_init(elev=elev, azim=azim)
    ax.set_axis_off()
    ax.set_box_aspect(aspect)


# ----------------------------------------------------------------------
# Figure 2.1  Failure of global frames (redrawn as line art)
# ----------------------------------------------------------------------
def fig_2_1():
    fig = plt.figure(figsize=(3.6, 2.5))
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.axis('off')

    # starfield (sparse gray dots)
    rng = np.random.default_rng(7)
    sx, sy = rng.uniform(0, 1, 55), rng.uniform(0, 1, 55)
    ss = rng.uniform(0.5, 2.5, 55)
    ax.scatter(sx, sy, s=ss, c='0.68', marker='.', zorder=1, lw=0)

    # rigid lattice plane in perspective (homography of unit-square grid)
    TL, TR, BR, BL = (0.03, 0.96), (0.97, 0.76), (0.95, 0.38), (0.05, 0.48)
    H = homography((0, 0), (1, 0), (1, 1), (0, 1), [BL, BR, TR, TL])
    nx, nz = 7, 5                       # columns, rows
    # cell fills
    for i in range(nx):
        for j in range(nz):
            corners = np.array([(i / nx, j / nz), ((i + 1) / nx, j / nz),
                                ((i + 1) / nx, (j + 1) / nz),
                                (i / nx, (j + 1) / nz)])
            px, py = apply_h(H, corners)
            ax.add_patch(Polygon(np.c_[px, py], closed=True, fc='0.90',
                                 ec='none', zorder=2))
    # grid lines
    for i in range(nx + 1):
        px, py = apply_h(H, np.c_[np.full(nz + 1, i / nx),
                                  np.linspace(0, 1, nz + 1)])
        ax.plot(px, py, color='k', lw=0.6, zorder=3)
    for j in range(nz + 1):
        px, py = apply_h(H, np.c_[np.linspace(0, 1, nx + 1),
                                  np.full(nx + 1, j / nz)])
        ax.plot(px, py, color='k', lw=0.6, zorder=3)

    # planet below
    pc = (0.44, 0.165); pr = 0.125
    ax.add_patch(Circle(pc, pr, fc='0.86', ec='k', lw=1.0, zorder=4))
    th = np.linspace(-0.9, 0.9, 40)
    ax.plot(pc[0] + 0.55 * pr * np.cos(th) - 0.02,
            pc[1] + 0.72 * pr * np.sin(th), color='0.55', lw=0.7, zorder=5)
    th = np.linspace(2.4, 4.0, 40)
    ax.plot(pc[0] + 0.60 * pr * np.cos(th) + 0.03,
            pc[1] - 0.35 * pr + 0.55 * pr * np.sin(th),
            color='0.60', lw=0.7, zorder=5)

    # freely-falling particles: dots on grid nodes, arrows toward planet
    for (u0, v0), p1 in [((0.22, 0.78), (0.315, 0.545)),
                         ((0.44, 0.70), (0.44, 0.345))]:
        px, py = apply_h(H, np.array([(u0, v0)]))
        ax.plot([px[0]], [py[0]], 'o', ms=4.5, color='k', zorder=6)
        arrow(ax, (px[0], py[0]), p1, lw=1.7, ms=15, zorder=6)

    save_fig('2.1', fig)


# ----------------------------------------------------------------------
# Figure 2.2  Doppler shift between two accelerating rockets
# ----------------------------------------------------------------------
def _rocket(ax, x0, y0, ang=33.0, s=2.0):
    """Simple line-art rocket pointing along +x, rotated by ang degrees."""
    from matplotlib.transforms import Affine2D
    tr = Affine2D().rotate_deg(ang).translate(x0, y0) + ax.transData
    # fins
    ax.add_patch(Polygon([(0.06, 0.09), (0.30, 0.09), (0.16, 0.32),
                          (0.02, 0.30)], closed=True, fc='0.85', ec='k',
                         lw=0.9, transform=tr, zorder=4))
    ax.add_patch(Polygon([(0.06, -0.09), (0.30, -0.09), (0.16, -0.32),
                          (0.02, -0.30)], closed=True, fc='0.85', ec='k',
                         lw=0.9, transform=tr, zorder=4))
    # body + nose
    body = [(0.10, 0.115), (0.60, 0.115), (0.62, 0.105),
            (0.86, 0.045), (0.97, 0.0), (0.86, -0.045), (0.62, -0.105),
            (0.60, -0.115), (0.10, -0.115)]
    ax.add_patch(Polygon(body, closed=True, fc='white', ec='k', lw=1.1,
                         transform=tr, zorder=5))
    # nose stripes
    for xs in (0.66, 0.72, 0.78):
        hw = 0.115 * (0.97 - xs) / 0.35
        ax.plot([xs, xs], [-hw, hw], color='k', lw=1.6, transform=tr,
                zorder=6, solid_capstyle='butt')
    # nozzle
    ax.add_patch(Circle((0.045, 0), 0.085, fc='white', ec='k', lw=1.0,
                        transform=tr, zorder=6))
    ax.add_patch(Circle((0.045, 0), 0.042, fc='0.8', ec='k', lw=0.8,
                        transform=tr, zorder=6))
    # window
    ax.add_patch(Circle((0.42, 0), 0.05, fc='white', ec='k', lw=0.9,
                        transform=tr, zorder=6))


def _wave(ax, p0, p1, amp=0.09, nper=6.5, head=0.22, lw=1.1, zorder=7):
    """Sinusoidal photon wave from p0 to p1 with arrowhead at the p1 end."""
    p0 = np.asarray(p0, float); p1 = np.asarray(p1, float)
    d = p1 - p0; L = np.linalg.norm(d)
    u = d / L; n = np.array([-u[1], u[0]])
    t = np.linspace(0, L, 300)
    pts = (p0[None, :] + t[:, None] * u[None, :]
           + (amp * np.sin(2 * np.pi * nper * t / L))[:, None] * n[None, :])
    ax.plot(pts[:-14, 0], pts[:-14, 1], color='k', lw=lw, zorder=zorder)
    tip = pts[-1]; prev = pts[-16]
    arrow(ax, (prev[0], prev[1]), (tip[0], tip[1]), lw=lw, ms=10,
          zorder=zorder)


def fig_2_2():
    fig = plt.figure(figsize=(4.8, 2.35))
    c33, s33 = np.cos(np.radians(33)), np.sin(np.radians(33))
    c18, s18 = np.cos(np.radians(18)), np.sin(np.radians(18))
    for k in range(2):
        ax = fig.add_axes([0.005 + 0.5 * k, 0.02, 0.485, 0.94])
        ax.set_xlim(0, 10); ax.set_ylim(0, 5.5)
        ax.axis('off')
        # z dimension line (left)
        ax.plot([0.85, 0.85], [0.80, 4.20], color='k', lw=0.8)
        ax.plot([0.85, 1.85], [0.80, 0.80], color='k', lw=0.8)
        ax.plot([0.85, 2.35], [4.20, 4.20], color='k', lw=0.8)
        arrow(ax, (0.85, 2.50), (0.85, 4.20), lw=1.0, ms=10)
        arrow(ax, (0.85, 2.50), (0.85, 0.80), lw=1.0, ms=10)
        ax.text(0.55, 2.50, '$z$', fontsize=12, ha='center', va='center')
        # rockets
        _rocket(ax, 1.10, 0.75, ang=33, s=4.4)
        _rocket(ax, 6.10, 2.50, ang=33, s=3.1)
        # acceleration arrows ahead of the noses
        a0 = (1.10 + 4.62 * c33, 0.75 + 4.62 * s33)
        a1 = (a0[0] + 0.95 * c33, a0[1] + 0.95 * s33)
        arrow(ax, a0, a1, lw=1.4, ms=14)
        ax.text(a1[0] + 0.34, a1[1] - 0.10, '$a$', fontsize=12)
        b0 = (6.10 + 3.25 * c33, 2.50 + 3.25 * s33)
        b1 = (b0[0] + 0.80 * c33, b0[1] + 0.80 * s33)
        arrow(ax, b0, b1, lw=1.4, ms=14)
        ax.text(b1[0] + 0.16, b1[1] - 0.32, '$a$', fontsize=12)
        # photon (leaves the trailing rocket / arrives at the leading one)
        if k == 0:
            p0 = (4.80, 2.88)
            p1 = (p0[0] + 2.75 * c18, p0[1] + 2.75 * s18)
            _wave(ax, p0, p1, amp=0.10, nper=7.0)
            ax.text(5.55, 4.32, r'$\lambda_0$', fontsize=12)
        else:
            p1 = (b0[0] - 0.12, b0[1] - 0.20)
            p0 = (p1[0] - 2.45 * c18, p1[1] - 2.45 * s18)
            _wave(ax, p0, p1, amp=0.10, nper=6.0)
        # time label
        tlab = r'$t = t_0$' if k == 0 else r'$t = t_0 + z/c$'
        ax.text(2.2, 0.12, tlab, fontsize=11.5)
    save_fig('2.2', fig)


# ----------------------------------------------------------------------
# Figure 2.3  Gravitational redshift: tower of height z on Earth
# ----------------------------------------------------------------------
def fig_2_3():
    fig = plt.figure(figsize=(2.5, 3.5))
    ax = fig.add_axes([0.03, 0.02, 0.94, 0.96])
    ax.set_xlim(-0.62, 1.10)
    ax.set_ylim(-0.09, 1.34)
    ax.axis('off')

    # ground
    ax.fill_between([-0.62, 1.10], -0.09, 0, color='0.62', zorder=1)
    ax.plot([-0.62, 1.10], [0, 0], color='k', lw=1.4, zorder=3)

    # tower lattice (tapering)
    H = 1.10; hw0, hw1 = 0.135, 0.052; xc = 0.5
    hw = lambda y: hw1 + (hw0 - hw1) * (1 - y / H)
    n_bay = 8
    ys = np.linspace(0, H, n_bay + 1)
    ax.plot(xc - hw(ys), ys, color='k', lw=1.3, zorder=3)
    ax.plot(xc + hw(ys), ys, color='k', lw=1.3, zorder=3)
    for y in ys[1:-1]:
        ax.plot([xc - hw(y), xc + hw(y)], [y, y], color='k', lw=0.8, zorder=3)
    for k in range(n_bay):
        y0, y1 = ys[k], ys[k + 1]
        ax.plot([xc - hw(y0), xc + hw(y1)], [y0, y1], color='k', lw=0.7,
                zorder=2)
        ax.plot([xc + hw(y0), xc - hw(y1)], [y0, y1], color='k', lw=0.7,
                zorder=2)
        # central zigzag
        ym = 0.5 * (y0 + y1)
        if k % 2 == 0:
            ax.plot([xc - 0.4 * hw(y0), xc + 0.4 * hw(ym)],
                    [y0, ym], color='k', lw=0.9, zorder=3)
            ax.plot([xc + 0.4 * hw(ym), xc - 0.4 * hw(y1)],
                    [ym, y1], color='k', lw=0.9, zorder=3)
        else:
            ax.plot([xc + 0.4 * hw(y0), xc - 0.4 * hw(ym)],
                    [y0, ym], color='k', lw=0.9, zorder=3)
            ax.plot([xc - 0.4 * hw(ym), xc + 0.4 * hw(y1)],
                    [ym, y1], color='k', lw=0.9, zorder=3)
    # cabin
    ax.add_patch(Rectangle((xc - 0.105, H), 0.21, 0.055, fc='white',
                           ec='k', lw=1.1, zorder=4))
    ax.add_patch(Polygon([(xc - 0.135, H + 0.055), (xc + 0.135, H + 0.055),
                          (xc, H + 0.105)], closed=True, fc='white', ec='k',
                         lw=1.1, zorder=4))
    for i in range(5):
        xw = xc - 0.08 + i * 0.04
        ax.plot([xw, xw], [H + 0.014, H + 0.042], color='k', lw=0.7,
                zorder=5)

    # height dimension z
    ytop = H + 0.105
    ax.plot([-0.30, 0.34], [ytop, ytop], color='k', lw=0.7)
    arrow(ax, (-0.30, 0.62), (-0.30, ytop), lw=0.9, ms=9)
    arrow(ax, (-0.30, 0.62), (-0.30, 0.0), lw=0.9, ms=9)
    ax.text(-0.43, 0.60, '$z$', fontsize=12, ha='center', va='center',
            rotation=90)

    # photon waves (emitted lambda_0 near ground; arriving near top)
    def vwave(x, y0, y1, amp=0.016, nper=5.0):
        t = np.linspace(0, 1, 240)
        xs = x + amp * np.sin(2 * np.pi * nper * t)
        ax.plot(xs[:-12], (y0 + (y1 - y0) * t)[:-12], color='k', lw=1.0,
                zorder=5)
        arrow(ax, (x, y0 + (y1 - y0) * t[-16]), (x, y1), lw=1.0, ms=9,
              zorder=5)
    vwave(0.88, 0.02, 0.44)
    ax.text(0.97, 0.30, r'$\lambda_0$', fontsize=12)
    vwave(0.88, 0.78, 1.24)

    save_fig('2.3', fig)


# ----------------------------------------------------------------------
# Figure 2.4  Spacetime diagram of the redshift experiment
# ----------------------------------------------------------------------
def fig_2_4():
    fig = plt.figure(figsize=(3.6, 2.5))
    ax = fig.add_axes([0.09, 0.13, 0.88, 0.84])
    ax.set_xlim(-0.55, 7.6)
    ax.set_ylim(-0.45, 6.6)
    ax.axis('off')

    z0, z1 = 2.3, 5.7
    # axes
    arrow(ax, (0, 0), (0, 6.45), lw=1.1, ms=11)
    arrow(ax, (0, 0), (7.35, 0), lw=1.1, ms=11)
    ax.text(0.18, 6.28, '$t$', fontsize=12)
    ax.text(7.28, -0.42, '$z$', fontsize=12)
    ax.text(z0, -0.48, '$z_0$', fontsize=12, ha='center')
    ax.text(z1, -0.48, '$z_1$', fontsize=12, ha='center')

    # static worldlines
    for z in (z0, z1):
        ax.plot([z, z], [0.35, 6.1], color='k', lw=1.0, zorder=3)

    # photon worldlines (congruent S-curves)
    def curve(t0, dt):
        s = np.linspace(0, 1, 160)
        tau = s ** 1.28
        f = 3 * tau ** 2 - 2 * tau ** 3
        zz = z0 + (z1 - z0) * s
        tt = t0 + dt * f
        return zz, tt

    for (t0, dt) in [(0.85, 1.65), (2.55, 2.45)]:
        zz, tt = curve(t0, dt)
        ax.plot(zz[:-12], tt[:-12], color='k', lw=1.5, zorder=4)
        arrow(ax, (zz[-16], tt[-16]), (zz[-1], tt[-1]), lw=1.5, ms=14,
              zorder=4)

    # interval markers
    def dim(ta, tb, z, side, lab):
        sgn = side
        ax.plot([z, z + sgn * 0.85], [ta, ta], color='k', lw=0.7)
        ax.plot([z, z + sgn * 0.85], [tb, tb], color='k', lw=0.7)
        xm = z + sgn * 0.62
        arrow(ax, (xm, 0.5 * (ta + tb)), (xm, tb), lw=0.9, ms=9)
        arrow(ax, (xm, 0.5 * (ta + tb)), (xm, ta), lw=0.9, ms=9)
        ax.text(xm + sgn * 0.30, 0.5 * (ta + tb), lab, fontsize=12,
                ha='center', va='center')

    dim(0.85, 2.55, z0, -1, r'$\Delta t_0$')
    dim(2.50, 5.00, z1, +1, r'$\Delta t_1$')
    save_fig('2.4', fig)


# ----------------------------------------------------------------------
# Figure 2.5  Torus T^2 from identifying opposite sides of a square
# ----------------------------------------------------------------------
def fig_2_5():
    fig = plt.figure(figsize=(4.8, 1.75))
    # left: square with identification arrows
    ax = fig.add_axes([0.005, 0.04, 0.42, 0.92])
    ax.set_xlim(-0.62, 2.30)
    ax.set_ylim(-0.30, 1.62)
    ax.axis('off')
    sq = Rectangle((0, 0), 1, 1, fc='none', ec='k', lw=1.8)
    ax.add_patch(sq)
    # top/bottom identification (dashed arc over the top)
    farrow(ax, (0.06, 1.02), (0.94, 1.02), rad=-0.42, lw=1.1, ms=10,
           style='<|-|>', linestyle='--')
    # left/right identification (solid arc on the left)
    farrow(ax, (-0.02, 0.94), (-0.02, 0.06), rad=0.42, lw=1.1, ms=10,
           style='<|-|>')
    ax.text(1.10, 0.50, 'identifying opposite\nsides', fontsize=8.5,
            ha='left', va='center')

    # right: 3D torus
    ax3 = fig.add_axes([0.46, -0.32, 0.52, 1.55], projection='3d')
    X, Y, Z = torus_mesh(R=1.0, r=0.44, nu=44, nv=22)
    shaded_surface(ax3, X, Y, Z, light=(0.5, -0.4, 1.0), lw=0.3)
    setup3d(ax3, elev=28, azim=-62, aspect=(1.55, 1.15, 0.7))
    ax3.set_xlim(-1.55, 1.55); ax3.set_ylim(-1.55, 1.55)
    ax3.set_zlim(-0.62, 0.62)
    save_fig('2.5', fig)


# ----------------------------------------------------------------------
# Figure 2.6  Riemann surfaces of genus 0, 1, 2
# ----------------------------------------------------------------------
def fig_2_6():
    fig = plt.figure(figsize=(4.8, 1.75))
    labels = ['genus 0', 'genus 1', 'genus 2']
    for k in range(3):
        ax3 = fig.add_axes([0.30 * k + 0.035, -0.34, 0.30, 1.58],
                           projection='3d')
        if k == 0:
            X, Y, Z = sphere_mesh(R=1.0, nu=36, nv=18, squash=0.96)
            setup3d(ax3, elev=16, azim=-58, aspect=(1, 1, 0.9))
            ax3.set_xlim(-1.15, 1.15); ax3.set_ylim(-1.15, 1.15)
            ax3.set_zlim(-1.15, 1.15)
        elif k == 1:
            X, Y, Z = torus_mesh(R=1.0, r=0.44, nu=44, nv=22)
            setup3d(ax3, elev=28, azim=-62, aspect=(1.5, 1.1, 0.68))
            ax3.set_xlim(-1.55, 1.55); ax3.set_ylim(-1.55, 1.55)
            ax3.set_zlim(-0.62, 0.62)
        else:
            X, Y, Z = genus2_mesh()
            shaded_surface(ax3, X, Y, Z, light=(0.4, -0.5, 1.0), lw=0.28)
            setup3d(ax3, elev=32, azim=-90, aspect=(2.4, 1.5, 0.45),
                    proj='ortho')
            ax3.set_xlim(-1.90, 1.90); ax3.set_ylim(-1.05, 1.05)
            ax3.set_zlim(-0.42, 0.42)
        if k < 2:
            shaded_surface(ax3, X, Y, Z, light=(0.4, -0.5, 1.0), lw=0.28)
        ax2d = fig.add_axes([0.30 * k + 0.035, 0.0, 0.30, 0.10])
        ax2d.axis('off')
        ax2d.text(0.5, 0.1, labels[k], fontsize=10, ha='center')
    save_fig('2.6', fig)


# ----------------------------------------------------------------------
# Figure 2.7  Not manifolds: line ending on a plane; two cones at vertices
# ----------------------------------------------------------------------
def fig_2_7():
    fig = plt.figure(figsize=(4.2, 2.9))
    # left: vertical plane with a line ending on it
    ax3 = fig.add_axes([0.02, 0.02, 0.46, 0.96], projection='3d')
    y = np.linspace(-1, 1, 13)
    z = np.linspace(-1.2, 1.2, 13)
    Y, Z = np.meshgrid(y, z, indexing='ij')
    X = np.zeros_like(Y)
    shaded_surface(ax3, X, Y, Z, light=(1.0, 0.3, 0.4), lw=0.3)
    ax3.plot([-2.3, 0], [0, 0], [0.45, 0.45], color='k', lw=1.8, zorder=10)
    ax3.scatter([0], [0], [0.45], s=18, color='k', zorder=11)
    setup3d(ax3, elev=10, azim=-65, aspect=(2.0, 1.5, 1.7))
    ax3.set_xlim(-2.3, 0.35); ax3.set_ylim(-1.05, 1.05)
    ax3.set_zlim(-1.25, 1.25)

    # right: two cones meeting at their vertices
    ax3 = fig.add_axes([0.50, 0.02, 0.46, 0.96], projection='3d')
    u = np.linspace(0, 2 * np.pi, 40)
    t = np.linspace(0, 1, 14)
    U, T = np.meshgrid(u, t, indexing='ij')
    Rr = 0.95
    for sgn in (+1, -1):
        Xc = Rr * T * np.cos(U)
        Yc = Rr * T * np.sin(U)
        Zc = sgn * 1.15 * T
        shaded_surface(ax3, Xc, Yc, Zc, light=(0.4, -0.4, 1.0), lw=0.3)
    th = np.linspace(0, 2 * np.pi, 100)
    ax3.plot(Rr * np.cos(th), Rr * np.sin(th), 1.15, color='k', lw=0.8)
    ax3.plot(Rr * np.cos(th), Rr * np.sin(th), -1.15, color='k', lw=0.8)
    setup3d(ax3, elev=12, azim=-58, aspect=(1, 1, 1.15))
    ax3.set_xlim(-1.05, 1.05); ax3.set_ylim(-1.05, 1.05)
    ax3.set_zlim(-1.25, 1.25)
    save_fig('2.7', fig)


# ----------------------------------------------------------------------
# Figure 2.8  Subtle examples: single cone; line segment
# ----------------------------------------------------------------------
def fig_2_8():
    fig = plt.figure(figsize=(4.6, 1.8))
    # cone
    ax3 = fig.add_axes([0.01, -0.42, 0.60, 1.75], projection='3d')
    u = np.linspace(0, 2 * np.pi, 40)
    t = np.linspace(0, 1, 14)
    U, T = np.meshgrid(u, t, indexing='ij')
    Rr = 0.95
    Xc = Rr * T * np.cos(U)
    Yc = Rr * T * np.sin(U)
    Zc = -1.15 * T                 # apex up at z=0, base below
    shaded_surface(ax3, Xc, Yc, Zc, light=(0.4, -0.4, 1.0), lw=0.3)
    th = np.linspace(0, 2 * np.pi, 100)
    ax3.plot(Rr * np.cos(th), Rr * np.sin(th), -1.15, color='k', lw=0.8)
    setup3d(ax3, elev=14, azim=-60, aspect=(1, 1, 1.0))
    ax3.set_xlim(-1.0, 1.0); ax3.set_ylim(-1.0, 1.0)
    ax3.set_zlim(-1.2, 0.1)

    # line segment with endpoints
    ax = fig.add_axes([0.60, 0.30, 0.39, 0.40])
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    ax.axis('off')
    ax.plot([0.08, 0.92], [0.5, 0.5], color='k', lw=1.6, zorder=3)
    ax.plot([0.08, 0.92], [0.5, 0.5], 'o', ms=4.5, color='k', zorder=4,
            markerfacecolor='k')
    save_fig('2.8', fig)


# ----------------------------------------------------------------------
# Figure 2.9  Composition of maps psi o phi : A -> C
# ----------------------------------------------------------------------
def fig_2_9():
    fig = plt.figure(figsize=(3.9, 1.7))
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(0, 3.9); ax.set_ylim(-0.18, 1.74)
    ax.axis('off')
    A = Ellipse((0.62, 1.06), 0.95, 0.44, fc='none', ec='k', lw=1.4)
    C = Ellipse((3.12, 1.38), 0.95, 0.44, fc='none', ec='k', lw=1.4)
    B = Ellipse((1.92, 0.30), 0.95, 0.44, fc='none', ec='k', lw=1.4)
    for e in (A, C, B):
        ax.add_patch(e)
    ax.text(0.05, 1.22, '$A$', fontsize=12)
    ax.text(3.66, 1.44, '$C$', fontsize=12)
    ax.text(1.85, -0.12, '$B$', fontsize=12, va='bottom')
    farrow(ax, (1.10, 1.24), (2.62, 1.44), rad=0.10, lw=2.4, ms=22)
    ax.text(1.72, 1.62, r'$\psi \circ \phi$', fontsize=11.5)
    farrow(ax, (1.02, 0.86), (1.52, 0.50), rad=0.10, lw=2.0, ms=18)
    ax.text(0.92, 0.62, r'$\phi$', fontsize=11.5)
    farrow(ax, (2.36, 0.52), (2.86, 1.20), rad=0.10, lw=2.0, ms=18)
    ax.text(2.76, 0.80, r'$\psi$', fontsize=11.5)
    save_fig('2.9', fig)


# ----------------------------------------------------------------------
# Figure 2.10  Types of maps (one-to-one / onto)
# ----------------------------------------------------------------------
def fig_2_10():
    fig = plt.figure(figsize=(4.8, 1.42))
    data = [
        (lambda x: np.exp(x), (-2.6, 1.15), (-0.5, 3.2), -2.0,
         'one-to-one, not onto'),
        (lambda x: x ** 3 - x, (-1.65, 1.65), (-1.35, 1.35), -1.05,
         'onto, not one-to-one'),
        (lambda x: x ** 3, (-1.45, 1.45), (-1.6, 1.6), -1.15, 'both'),
        (lambda x: x ** 2, (-1.5, 1.5), (-0.55, 2.3), -1.1, 'neither'),
    ]
    for k, (f, (xa, xb), (ya, yb), yax, lab) in enumerate(data):
        ax = fig.add_axes([0.012 + 0.25 * k, 0.13, 0.225, 0.85])
        ax.set_xlim(-3.0, 2.2); ax.set_ylim(ya, yb)
        ax.axis('off')
        xs = np.linspace(xa, xb, 200)
        ax.plot(xs, f(xs), color='k', lw=1.3, zorder=4)
        # axes through origin-like position
        x0 = yax
        arrow(ax, (x0, ya + 0.06 * (yb - ya)), (x0, yb - 0.05 * (yb - ya)),
              lw=0.9, ms=8)
        ax.text(x0 + 0.12, yb - 0.02 * (yb - ya), r'$\phi(x)$', fontsize=10,
                va='top')
        z0 = 0.0
        arrow(ax, (xa + 0.05, z0), (2.05, z0), lw=0.9, ms=8)
        ax.text(2.05, z0 - 0.10 * (yb - ya), '$x$', fontsize=10, ha='center')
        ax.text(0.5, -0.30, lab, fontsize=8.8, ha='center', transform=ax.transAxes)
    save_fig('2.10', fig)


# ----------------------------------------------------------------------
# Figure 2.11  A map and its inverse
# ----------------------------------------------------------------------
def fig_2_11():
    fig = plt.figure(figsize=(2.6, 2.35))
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_xlim(0, 2.6); ax.set_ylim(0, 2.35)
    ax.axis('off')
    M = Ellipse((0.74, 1.18), 1.02, 0.56, fc='none', ec='k', lw=1.5)
    N = Ellipse((1.90, 1.18), 1.02, 0.56, fc='none', ec='k', lw=1.5)
    ax.add_patch(M); ax.add_patch(N)
    ax.text(0.06, 1.24, '$M$', fontsize=12)
    ax.text(2.46, 1.24, '$N$', fontsize=12)
    farrow(ax, (0.72, 1.62), (1.92, 1.60), rad=-0.48, lw=2.4, ms=22)
    ax.text(1.32, 2.14, r'$\phi$', fontsize=12.5, ha='center')
    farrow(ax, (1.92, 0.74), (0.72, 0.76), rad=-0.48, lw=2.4, ms=22)
    ax.text(1.32, 0.20, r'$\phi^{-1}$', fontsize=12.5, ha='center')
    save_fig('2.11', fig)


# ----------------------------------------------------------------------
# Figure 2.12  An open ball in R^n
# ----------------------------------------------------------------------
def fig_2_12():
    fig = plt.figure(figsize=(2.6, 2.7))
    ax = fig.add_axes([0.10, 0.08, 0.86, 0.88])
    ax.set_xlim(-0.45, 3.85); ax.set_ylim(-0.45, 3.95)
    ax.axis('off')
    arrow(ax, (0, 0), (3.65, 0), lw=1.1, ms=11)
    arrow(ax, (0, 0), (0, 3.80), lw=1.1, ms=11)
    ax.text(3.55, -0.34, '$x^1$', fontsize=12)
    ax.text(0.16, 3.72, '$x^2$', fontsize=12)
    c, r = (2.0, 2.25), 1.15
    ax.add_patch(Circle(c, r, fc='none', ec='k', lw=1.1, linestyle=(0, (5, 4)),
                        zorder=3))
    ax.plot([c[0]], [c[1]], 'o', ms=4, color='k', zorder=4)
    ax.text(c[0] - 0.06, c[1] - 0.26, '$y$', fontsize=12, ha='center')
    ang = np.radians(42)
    p1 = (c[0] + r * np.cos(ang), c[1] + r * np.sin(ang))
    arrow(ax, c, p1, lw=1.1, ms=12)
    ax.text(c[0] + 0.30 * r * np.cos(ang) - 0.18,
            c[1] + 0.30 * r * np.sin(ang) + 0.16, '$r$', fontsize=12)
    ax.text(c[0] + 0.74 * r, c[1] - 0.86 * r, 'open ball', fontsize=10.5)
    save_fig('2.12', fig)


# ----------------------------------------------------------------------
# Figure 2.13  A coordinate chart covering an open subset U of M
# ----------------------------------------------------------------------
def fig_2_13():
    fig = plt.figure(figsize=(4.4, 1.75))
    ax = fig.add_axes([0.01, 0.02, 0.98, 0.96])
    ax.set_xlim(0, 4.4); ax.set_ylim(0, 1.78)
    ax.axis('off')
    # M with U
    ax.add_patch(Ellipse((1.02, 0.92), 1.52, 1.00, fc='none', ec='k',
                         lw=1.5, zorder=3))
    bx, by = blob(0.98, 0.90, 0.45, 0.28, a1=0.12, a2=0.06)
    ax.plot(bx, by, color='k', lw=1.0, linestyle=(0, (4, 3)), zorder=4)
    ax.text(0.03, 1.00, '$M$', fontsize=12)
    ax.text(0.70, 0.88, '$U$', fontsize=11.5)
    # arrow phi
    farrow(ax, (1.78, 0.90), (2.62, 0.86), rad=0.10, lw=2.2, ms=20)
    ax.text(2.14, 1.10, r'$\phi$', fontsize=12)
    # box R^n with phi(U)
    ax.add_patch(Rectangle((2.68, 0.18), 1.62, 1.44, fc='none', ec='k',
                           lw=1.3, zorder=2))
    cx, cy = blob(3.52, 0.88, 0.52, 0.32, a1=0.15, a2=0.05, p1=2.0, p2=0.6)
    ax.plot(cx, cy, color='k', lw=1.0, linestyle=(0, (4, 3)), zorder=4)
    ax.text(4.22, 1.46, r'$\mathbf{R}^n$', fontsize=11.5, ha='right')
    ax.text(3.36, 0.84, r'$\phi(U)$', fontsize=11.5)
    save_fig('2.13', fig)


# ----------------------------------------------------------------------
# Figure 2.14  Overlapping coordinate charts
# ----------------------------------------------------------------------
def fig_2_14():
    fig = plt.figure(figsize=(4.0, 3.0))
    ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
    ax.set_xlim(0, 4.0); ax.set_ylim(0, 3.04)
    ax.axis('off')

    # --- manifold M with overlapping U_beta, U_alpha ---
    mx, my = blob(1.18, 2.40, 0.72, 0.42, a1=0.07, a2=0.04, p1=1.2, p2=4.0)
    ax.plot(mx, my, color='k', lw=1.5, zorder=3)
    ax.text(0.16, 2.40, '$M$', fontsize=12)
    e1 = ellipse_poly(1.00, 2.44, 0.28, 0.20, rot=np.radians(14))
    e2 = ellipse_poly(1.40, 2.42, 0.29, 0.21, rot=np.radians(-10))
    lens = clip_convex(e1, e2)
    ax.add_patch(Polygon(e1, closed=True, fc='none', ec='k', lw=0.9,
                         linestyle=(0, (4, 3)), zorder=4))
    ax.add_patch(Polygon(e2, closed=True, fc='none', ec='k', lw=0.9,
                         linestyle=(0, (4, 3)), zorder=4))
    ax.add_patch(Polygon(lens, closed=True, fc='0.78', ec='none', zorder=3))
    ax.text(0.66, 2.72, r'$U_\beta$', fontsize=11)
    ax.text(1.64, 2.70, r'$U_\alpha$', fontsize=11)

    # --- chart box: phi_alpha(U_alpha) ---
    ax.add_patch(Rectangle((2.48, 1.86), 1.44, 1.14, fc='none', ec='k',
                           lw=1.3, zorder=2))
    b1x, b1y = blob(3.24, 2.38, 0.47, 0.33, a1=0.13, a2=0.06, p1=2.2, p2=1.0)
    ax.plot(b1x, b1y, color='k', lw=0.9, linestyle=(0, (4, 3)), zorder=4)
    hid1 = ellipse_poly(2.88, 2.40, 0.17, 0.23, rot=np.radians(8))
    lens2 = clip_convex(np.column_stack([b1x, b1y]), hid1)
    ax.add_patch(Polygon(lens2, closed=True, fc='0.78', ec='none', zorder=3))
    ax.text(3.84, 2.86, r'$\mathbf{R}^n$', fontsize=11, ha='right')
    ax.text(3.30, 2.34, r'$\phi_\alpha(U_\alpha)$', fontsize=10,
            ha='center', zorder=5)

    # --- chart box: phi_beta(U_beta) ---
    ax.add_patch(Rectangle((0.66, 0.14), 1.46, 1.22, fc='none', ec='k',
                           lw=1.3, zorder=2))
    b2x, b2y = blob(1.36, 0.73, 0.51, 0.37, a1=0.12, a2=0.05, p1=0.6, p2=2.2)
    ax.plot(b2x, b2y, color='k', lw=0.9, linestyle=(0, (4, 3)), zorder=4)
    hid2 = ellipse_poly(1.88, 0.72, 0.18, 0.25, rot=np.radians(-6))
    lens3 = clip_convex(np.column_stack([b2x, b2y]), hid2)
    ax.add_patch(Polygon(lens3, closed=True, fc='0.78', ec='none', zorder=3))
    ax.text(0.80, 1.16, r'$\mathbf{R}^n$', fontsize=11)
    ax.text(1.14, 0.70, r'$\phi_\beta(U_\beta)$', fontsize=10, zorder=5)

    # --- arrows ---
    farrow(ax, (1.94, 2.36), (2.44, 2.28), rad=0.08, lw=2.2, ms=20)
    ax.text(2.14, 2.52, r'$\phi_\alpha$', fontsize=11)
    farrow(ax, (0.95, 1.98), (1.06, 1.40), rad=0.10, lw=2.2, ms=20)
    ax.text(1.22, 1.64, r'$\phi_\beta$', fontsize=11)
    # transition maps between the two shaded regions
    farrow(ax, (1.80, 0.98), (2.70, 2.28), rad=0.08, lw=2.4, ms=20)
    ax.text(2.14, 1.62, r'$\phi_\alpha \circ \phi_\beta^{-1}$',
            fontsize=10.5, ha='right')
    farrow(ax, (3.02, 2.22), (2.06, 0.90), rad=0.08, lw=2.4, ms=20)
    ax.text(2.48, 1.26, r'$\phi_\beta \circ \phi_\alpha^{-1}$',
            fontsize=10.5)

    # note with leader lines
    ax.text(2.62, 0.62, 'These maps are only\ndefined on the shaded\n'
            'regions, and must be\nsmooth here.', fontsize=9.3, va='top')
    ax.plot([2.60, 2.18], [0.74, 1.54], color='k', lw=0.55)
    ax.plot([2.62, 2.52], [0.74, 1.22], color='k', lw=0.55)
    save_fig('2.14', fig)


FIGS = [fig_2_1, fig_2_2, fig_2_3, fig_2_4, fig_2_5, fig_2_6, fig_2_7,
        fig_2_8, fig_2_9, fig_2_10, fig_2_11, fig_2_12, fig_2_13, fig_2_14]

if __name__ == '__main__':
    for f in FIGS:
        f()
        print('done:', f.__name__)
