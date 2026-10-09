# -*- coding: utf-8 -*-
"""
Ziman, Principles of the Theory of Solids, 2nd ed. — Chapter 4, Figs. 76-85.
Black-and-white textbook-style vector redraws with matplotlib.
Outputs: figures/fig_76.pdf ... fig_85.pdf (+ figures/preview/fig_76.png ...)
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

plt.rcParams.update({
    'font.family': ['Times New Roman', 'SimSun'],
    'mathtext.fontset': 'cm',
    'axes.unicode_minus': False,
    'font.size': 11,
    'lines.linewidth': 1.2,
    'savefig.facecolor': 'white',
    'hatch.linewidth': 0.65,
})

BASE = Path(__file__).resolve().parents[1]
FIGD = BASE / 'figures'
PREV = FIGD / 'preview'
FIGD.mkdir(exist_ok=True)
PREV.mkdir(exist_ok=True)


def save(fig, key):
    fig.savefig(FIGD / f'fig_{key}.pdf', bbox_inches='tight', pad_inches=0.03)
    fig.savefig(PREV / f'fig_{key}.png', bbox_inches='tight', pad_inches=0.03,
                dpi=200, facecolor='white')
    plt.close(fig)
    print(f'fig_{key} done')


def new_fig(wdata, hdata, maxw=4.8):
    """figure with a single full-bleed axes, equal aspect, data coords given."""
    w = maxw
    h = w * hdata / wdata
    fig = plt.figure(figsize=(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, wdata)
    ax.set_ylim(0, hdata)
    ax.set_aspect('equal')
    ax.axis('off')
    return fig, ax


def arrow(ax, x0, y0, x1, y1, lw=1.1, style='-|>', ms=10, **kw):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle=style, lw=lw,
                                mutation_scale=ms, color='k',
                                shrinkA=0, shrinkB=0), **kw)


def brace(ax, x, y0, y1, w, tip=1, lw=1.0):
    """Curly brace spanning y0..y1 at base x, tip pointing +x (tip=1) or -x."""
    P = mpath.Path
    h = y1 - y0
    ym = 0.5 * (y0 + y1)
    s = w * tip
    verts = [(x, y1),
             (x + s, y1), (x + s, y1 - 0.22 * h),
             (x + s, ym - 0.14 * h), (x + 1.18 * s, ym),
             (x + s, ym + 0.14 * h), (x + s, y0 + 0.22 * h),
             (x + s, y0), (x, y0)]
    codes = [P.MOVETO,
             P.CURVE3, P.CURVE3,
             P.CURVE3, P.CURVE3,
             P.CURVE3, P.CURVE3,
             P.CURVE3, P.CURVE3]
    ax.add_patch(mpatches.PathPatch(mpath.Path(verts, codes), fill=False,
                                    lw=lw, edgecolor='k'))


def pchip_eval(x, y, xq):
    """Fritsch-Carlson monotone cubic Hermite interpolation."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    h = np.diff(x); d = np.diff(y) / h
    m = np.zeros(len(x))
    m[0], m[-1] = d[0], d[-1]
    for i in range(1, len(d)):
        if d[i - 1] * d[i] <= 0:
            m[i] = 0.0
        else:
            w1 = 2 * h[i] + h[i - 1]; w2 = h[i] + 2 * h[i - 1]
            m[i] = (w1 + w2) / (w1 / d[i - 1] + w2 / d[i])
    xq = np.asarray(xq, float)
    out = np.empty_like(xq)
    idx = np.clip(np.searchsorted(x, xq) - 1, 0, len(x) - 2)
    for k, (i, xv) in enumerate(zip(idx, xq)):
        t = (xv - x[i]) / h[i]
        t2 = t * t; t3 = t2 * t
        out[k] = ((2 * t3 - 3 * t2 + 1) * y[i] + (t3 - 2 * t2 + t) * h[i] * m[i]
                  + (-2 * t3 + 3 * t2) * y[i + 1] + (t3 - t2) * h[i] * m[i + 1])
    return out


def bilinear_field(x, y, gx, gy, vals):
    """bilinear interpolation of a coarse random grid."""
    x = np.clip(x, gx[0], gx[-1]); y = np.clip(y, gy[0], gy[-1])
    i = np.clip(np.searchsorted(gx, x) - 1, 0, len(gx) - 2)
    j = np.clip(np.searchsorted(gy, y) - 1, 0, len(gy) - 2)
    tx = (x - gx[i]) / (gx[i + 1] - gx[i]); ty = (y - gy[j]) / (gy[j + 1] - gy[j])
    v = (vals[j, i] * (1 - tx) * (1 - ty) + vals[j, i + 1] * tx * (1 - ty)
         + vals[j + 1, i] * (1 - tx) * ty + vals[j + 1, i + 1] * tx * ty)
    return v


# ---------------------------------------------------------------- fig 76
def fig_76():
    fig, ax = new_fig(12.4, 10.6)

    # ---- (a) copper chloride schematic (2D slice) ----
    cl = [(1.35, 9.4), (3.0, 9.4), (4.65, 9.4),
          (1.35, 7.15), (3.0, 7.15), (4.65, 7.15)]
    cu = [(2.17, 8.28), (3.82, 8.28)]
    for x, y in cl:
        ax.add_patch(mpatches.Circle((x, y), 0.60, fc='0.86', ec='k', lw=1.1))
        ax.text(x, y, 'Cl$^-$', ha='center', va='center', fontsize=9.5)
    for x, y in cu:
        ax.add_patch(mpatches.Circle((x, y), 0.46, fc='white', ec='k', lw=1.1))
        ax.text(x, y, 'Cu$^+$', ha='center', va='center', fontsize=9.5)
    ax.text(3.0, 6.05, '$(a)$', ha='center', va='center', fontsize=12)

    # ---- (b) NaCl structure ----
    x0, y0b, u = 7.0, 6.75, 1.15
    def P(i, j, k):
        return (x0 + (i + 0.42 * j) * u, y0b + (k + 0.30 * j) * u)
    edge, pts = [], []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                pts.append((*P(i, j, k), i, j, k))
                if i < 2: edge.append((P(i, j, k), P(i + 1, j, k)))
                if k < 2: edge.append((P(i, j, k), P(i, j, k + 1)))
                if j < 2: edge.append((P(i, j, k), P(i, j + 1, k)))
    for p, q in edge:
        ax.plot([p[0], q[0]], [p[1], q[1]], 'k-', lw=0.8)
    for j in (2, 1, 0):                       # atoms back to front
        for (X, Y, i, jj, kk) in pts:
            if jj == j:
                f = (i + jj + kk) % 2 == 0
                ax.add_patch(mpatches.Circle((X, Y), 0.115,
                             fc='k' if f else 'white', ec='k', lw=0.9))
    ax.text(8.85, 6.2, '$(b)$', ha='center', va='center', fontsize=12)

    # ---- (c) CsCl structure (2x2x2 cells) ----
    x0, y0c, u = 4.35, 1.05, 1.15
    def Q(i, j, k):
        return (x0 + (i + 0.42 * j) * u, y0c + (k + 0.30 * j) * u)
    def C(i, j, k):
        return (x0 + ((i + .5) + 0.42 * (j + .5)) * u,
                y0c + ((k + .5) + 0.30 * (j + .5)) * u)
    edge = []
    for i in range(3):
        for j in range(3):
            for k in range(3):
                if i < 2: edge.append((Q(i, j, k), Q(i + 1, j, k)))
                if k < 2: edge.append((Q(i, j, k), Q(i, j, k + 1)))
                if j < 2: edge.append((Q(i, j, k), Q(i, j + 1, k)))
    for p, q in edge:
        ax.plot([p[0], q[0]], [p[1], q[1]], 'k-', lw=0.8)
    cen_layer = {j: [C(i, j, k) for i in range(2) for k in range(2)]
                 for j in range(3)}
    for j in (2, 1, 0):
        cl = cen_layer[j]                     # inner cube edges, this layer
        for a in range(4):
            for b in range(a + 1, 4):
                ia, ka = a % 2, a // 2
                ib, kb = b % 2, b // 2
                if (abs(ia - ib) + abs(ka - kb)) == 1:
                    ax.plot([cl[a][0], cl[b][0]], [cl[a][1], cl[b][1]],
                            'k-', lw=0.7)
        for i in range(3):
            for k in range(3):
                p = Q(i, j, k)
                ax.add_patch(mpatches.Circle(p, 0.105, fc='k', ec='k', lw=0.9))
        for p in cen_layer[j]:
            ax.add_patch(mpatches.Circle(p, 0.092, fc='white', ec='k', lw=0.9))
    ax.text(6.3, 0.42, '$(c)$', ha='center', va='center', fontsize=12)

    save(fig, 76)


# ---------------------------------------------------------------- fig 77
def _honeycomb(x0, x1, y0, y1, L, sy, rng, jitter=0.0):
    """honeycomb net: A = open O atoms, B = filled Si atoms.
    Returns Apts, Bpts, bonds and per-B-node (present, missing) info."""
    ax_ = 1.5 * L
    ay = np.sqrt(3) / 2 * L
    a1 = np.array([ax_, ay])
    a2 = np.array([ax_, -ay])
    s0 = int(np.floor((x0 - 1.5) / ax_)) - 1
    s1 = int(np.ceil((x1 + 1.5) / ax_)) + 1
    d0 = int(np.floor((y0 - 1.5) / (sy * ay))) - 1
    d1 = int(np.ceil((y1 + 1.5) / (sy * ay))) + 1
    gx = np.linspace(x0 - 2, x1 + 2, 6)
    gy = np.linspace(y0 - 2, y1 + 2, 8)
    f1 = rng.random((8, 6)) * 2 - 1
    f2 = rng.random((8, 6)) * 2 - 1

    def disp(p):
        if jitter == 0.0:
            return np.zeros(2)
        return jitter * np.array([bilinear_field(p[0], p[1], gx, gy, f1),
                                  bilinear_field(p[0], p[1], gx, gy, f2)])

    def pos(i, j):
        return np.array([i * a1[0] + j * a2[0], sy * (i * a1[1] + j * a2[1])])

    Ad, Bd = {}, {}
    for s in range(s0, s1 + 1):
        for d in range(d0, d1 + 1):
            if (s + d) % 2 != 0:
                continue
            i = (s + d) // 2
            j = (s - d) // 2
            pa = pos(i, j)
            Ad[(i, j)] = pa + disp(pa)
            Bd[(i, j)] = pa + np.array([L, 0]) + disp(pa + np.array([L, 0]))

    def inset(p, m=0.02):
        return (x0 + m <= p[0] <= x1 - m) and (y0 + m <= p[1] <= y1 - m)

    bonds = []
    for k, pa in Ad.items():
        i, j = k
        for nb in [(i, j), (i - 1, j), (i, j - 1)]:
            if nb in Bd and inset(pa) and inset(Bd[nb]):
                bonds.append((pa, Bd[nb]))
    Apts = [p for p in Ad.values() if inset(p)]
    Bpts = [p for p in Bd.values() if inset(p)]

    def node_info(nodes, nbr_of, others):
        info = {}
        for k, p in nodes.items():
            if not inset(p):
                continue
            present, missing = [], []
            for na in nbr_of(k):
                q = others.get(na)
                if q is None or not (inset(q) and inset(p)):
                    if q is not None:
                        v = q - p
                        missing.append(v / np.linalg.norm(v))
                else:
                    present.append(q)
            info[tuple(p)] = (present, missing)
        return info

    # A = Si (small filled dots), B = O (large open circles);
    # dangling bonds occur on the Si (A) sublattice at the boundary
    Ainfo = node_info(Ad, lambda k: [(k[0], k[1]), (k[0] - 1, k[1]),
                                     (k[0], k[1] - 1)], Bd)
    return Apts, Bpts, bonds, Ainfo


def _draw_net(ax, x0, x1, y0, y1, L, sy, seed, jitter=0.0):
    rng = np.random.default_rng(seed)
    SI, O, bonds, SIinfo = _honeycomb(x0, x1, y0, y1, L, sy, rng, jitter)
    for p1, p2 in bonds:
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'k-', lw=1.1, zorder=2)
    rO, rB = 0.125, 0.047
    for p in O:
        ax.add_patch(mpatches.Circle(p, rO, fc='white', ec='k', lw=1.0, zorder=3))
    for p in SI:
        ax.add_patch(mpatches.Circle(p, rB, fc='k', ec='k', lw=0.7, zorder=3))
    # crescents at dangling Si: one arc per missing bond direction
    for p, (present, missing) in SIinfo.items():
        if len(present) < 3:
            dirs = missing if missing else []
            if not dirs:
                v = np.array([-np.sign(p[0] - 0.5 * (x0 + x1)) or -1.0, 0.25])
                dirs = [v / np.linalg.norm(v)]
            for v in dirs[:2]:
                ang = np.arctan2(v[1], v[0])
                th = np.linspace(ang - 1.0, ang + 1.0, 26)
                ax.plot(p[0] + 0.105 * np.cos(th), p[1] + 0.105 * np.sin(th),
                        'k-', lw=1.1, zorder=3)


def fig_77():
    fig, ax = new_fig(10.0, 7.3)
    _draw_net(ax, 0.55, 4.35, 0.85, 6.45, L=0.40, sy=1.55, seed=3, jitter=0.0)
    _draw_net(ax, 5.55, 9.35, 0.85, 6.45, L=0.40, sy=1.55, seed=11, jitter=0.32)
    ax.text(2.45, 0.35, '$(a)$', ha='center', va='center', fontsize=12)
    ax.text(7.45, 0.35, '$(b)$', ha='center', va='center', fontsize=12)
    save(fig, 77)


# ---------------------------------------------------------------- fig 78
def _funnel(ax, c, ytop, ybot, half=1.35, lw=1.3, q=5.0):
    """trumpet-shaped potential well: vertical at the neck, tangent to the
    top line at the rim."""
    x = np.linspace(-half, half, 400)
    t = np.abs(x) / half
    y = ytop - (ytop - ybot) * (1.0 - t) ** q
    ax.plot(c + x, y, 'k-', lw=lw, zorder=4)


def fig_78():
    fig, ax = new_fig(12.8, 4.7)

    # ---------------- (a) monatomic gas ----------------
    ytop, ya, ybot = 3.55, 2.95, 0.62
    ax.plot([0.22, 4.45], [ytop, ytop], 'k-', lw=1.1)          # zero line
    arrow(ax, 1.05, 0.55, 1.05, 4.35)                           # E axis
    ax.text(1.28, 4.32, r'$\mathcal{E}$', fontsize=12)
    for c in (1.05, 3.35):
        _funnel(ax, c, ytop, ybot, half=1.38)
    ax.plot([0.45, 4.14], [ya, ya], 'k-', lw=1.0)               # atomic level
    ax.plot([4.14, 4.95], [ya, ya], 'k--', lw=1.0)              # dashed tail
    ax.text(4.55, ya + 0.14, r'$\mathcal{E}_a$', fontsize=11)
    for xd in (1.48, 3.35):
        ax.add_patch(mpatches.Circle((xd, ya), 0.058, fc='k', ec='k'))
    ax.text(1.62, 1.62, r'$v_a(r)$', fontsize=12)
    ax.text(2.35, 0.25, '$(a)$', ha='center', fontsize=12)
    arrow(ax, 4.95, 2.2, 5.6, 2.2, lw=1.6, ms=16)               # arrow between

    # ---------------- (b) metal ----------------
    xs0, xs1 = 5.95, 12.35
    yb0, yb1, yad = 2.40, 3.10, 2.94
    ax.plot([xs0 - 0.05, xs1], [ytop, ytop], 'k-', lw=1.1)      # top (zero) line
    per = 1.15
    for c in np.arange(6.55, 12.6, per):
        _funnel(ax, c, ytop, 0.60, half=0.56, lw=1.2)
    ax.add_patch(mpatches.Rectangle((xs0, yb0), xs1 - xs0, yb1 - yb0,
                 facecolor='none', edgecolor='none', hatch='///', zorder=1))
    ax.plot([xs0 - 0.05, xs1], [yb0, yb0], 'k-', lw=1.1, zorder=3)
    ax.plot([xs0 - 0.05, xs1], [yb1, yb1], 'k-', lw=1.1, zorder=3)
    ax.plot([xs0 - 0.05, xs1 + 0.1], [yad, yad], 'k--', lw=1.0, zorder=3)
    for xd in (7.0, 8.3, 9.9):
        ax.add_patch(mpatches.Circle((xd, yad), 0.05, fc='k', ec='k', zorder=5))
    ax.text(xs0 - 0.18, yb1 + 0.02, r'$\bar{\mathcal{E}}$', fontsize=11,
            ha='right')
    ax.text(4.55, yad + 0.14, '', fontsize=11)
    # dashed atomic-potential funnel across one cell
    c = 10.0
    x = np.linspace(c - 1.02, c + 1.02, 300)
    yd = ytop - 1.00 * 0.09 / (np.abs(x - c) + 0.09)
    ax.plot(x, yd, 'k--', lw=1.0, zorder=3)
    # r_s marks
    for xv, ylo in ((8.85, 2.35), (10.0, 0.62)):
        ax.plot([xv, xv], [3.98, ylo], 'k-', lw=0.8)
    arrow(ax, 8.85, 3.9, 10.0, 3.9, style='<|-|>', lw=1.0, ms=9)
    ax.text(9.42, 4.12, r'$r_s$', ha='center', fontsize=11)
    brace(ax, xs1 + 0.12, yb0, yb1, 0.12, tip=1)
    ax.text(xs1 + 0.55, 0.5 * (yb0 + yb1), r'$\mathcal{E}_F$', fontsize=11,
            va='center')
    ax.annotate(r'$\mathcal{E}(0)$', xy=(10.85, yb0), xytext=(10.62, 1.68),
                fontsize=11,
                arrowprops=dict(arrowstyle='->', lw=0.9, color='k'))
    ax.annotate(r'$\mathcal{V}(r)$', xy=(8.72, 1.95), xytext=(8.35, 0.95),
                fontsize=11,
                arrowprops=dict(arrowstyle='->', lw=0.9, color='k'))
    ax.text(9.1, 0.25, '$(b)$', ha='center', fontsize=12)

    save(fig, 78)


# ---------------------------------------------------------------- fig 79
def fig_79():
    fig, ax = new_fig(10.6, 7.7)
    D = 4.30                        # vertical shift (canvas is 0..7.7)
    ya = 0.55 + D                   # E_a asymptote level
    xs = np.linspace(0.88, 9.45, 300)

    kin_pts = [(0.88, 3.25), (1.1, 2.2), (1.4, 1.35), (1.8, 0.92),
               (2.3, 0.74), (3.0, 0.66), (4.2, 0.60), (6.0, 0.575),
               (7.6, 0.565), (9.45, 0.560)]
    pot_pts = [(0.88, -3.75), (1.1, -2.95), (1.5, -2.3), (2.2, -1.6),
               (3.2, -1.12), (4.5, -0.82), (6.5, -0.62), (8.0, -0.545),
               (9.45, -0.50)]
    tot_pts = [(0.92, 3.05), (1.1, 2.2), (1.35, 1.35), (1.65, 0.62),
               (2.0, 0.05), (2.5, -0.45), (3.1, -0.78), (3.8, -0.97),
               (4.3, -1.03), (5.0, -1.03), (6.0, -0.96), (7.5, -0.82),
               (9.0, -0.66), (9.45, -0.61)]
    kin_pts = [(x, y + D) for x, y in kin_pts]
    pot_pts = [(x, y + D) for x, y in pot_pts]
    tot_pts = [(x, y + D) for x, y in tot_pts]

    ax.plot(xs, pchip_eval(*zip(*kin_pts), xs), 'k-', lw=1.0)
    ax.plot(xs, pchip_eval(*zip(*pot_pts), xs), 'k-', lw=1.0)
    ax.plot(xs, pchip_eval(*zip(*tot_pts), xs), 'k-', lw=2.2)

    ax.plot([0.7, 9.6], [ya, ya], 'k-', lw=1.0)               # E_a asymptote
    ax.plot([0.7, 5.7], [-1.06 + D, -1.06 + D], 'k-', lw=1.0)  # min level
    ax.plot([4.3, 4.3], [1.05 + D, -1.95 + D], 'k-', lw=1.0)   # equil. volume
    arrow(ax, 0.7, -3.95 + D, 0.7, 3.05 + D)                   # E axis
    ax.text(0.88, 3.02 + D, r'$\mathcal{E}$', fontsize=12)

    ax.text(3.45, 1.62 + D, r'Kinetic = $\frac{3}{5}\,\mathcal{E}_F$',
            fontsize=11)
    ax.text(2.95, 0.75 + D, 'Total', fontsize=11)
    ax.text(5.45, -2.05 + D, r'potential = $\mathcal{E}(0)$', fontsize=11)
    ax.text(4.55, 0.80 + D, 'Equilibrium volume', fontsize=11)
    ax.text(9.0, 0.74 + D, r'$\mathcal{E}_a$', fontsize=11)
    arrow(ax, 8.30, -0.28 + D, 9.40, -0.28 + D, lw=1.2, ms=13)
    ax.text(8.85, -0.95 + D, r'$r_s$', ha='center', fontsize=11)

    brace(ax, 0.52, -1.06 + D, ya, 0.14, tip=-1)
    ax.text(0.30, (ya - 1.06 + D) / 2 - 0.25,
            'Cohesive energy'.replace(' ', chr(10)), ha='right', va='center',
            fontsize=10.5, linespacing=1.1)

    save(fig, 79)


# ---------------------------------------------------------------- fig 80
def fig_80():
    fig, ax = new_fig(10.6, 9.5)

    # ---------------- (a) Fermi surface touches zone boundary ----------
    cx, cy, a = 2.7, 6.9, 1.85
    th = np.linspace(0, 2 * np.pi, 400)
    ax.plot(cx + 2.17 * np.cos(th), cy + 2.17 * np.sin(th), 'k--', lw=1.0)
    rc, g = 0.58, np.deg2rad(30)
    side_in = 0.60 * a
    contour = []
    corners = [(cx + a, cy + a), (cx - a, cy + a),
               (cx - a, cy - a), (cx + a, cy - a)]
    # walking counter-clockwise: top side -> TR corner -> right side -> ...
    for i, c in enumerate(corners):
        base = {0: np.pi, 1: 0.0, 2: -np.pi, 3: 0.0}[i]
        # arc centred at corner, spanning the inward diagonal direction
        if i == 0:      a0, a1_ = np.pi + g, 1.5 * np.pi - g
        elif i == 1:    a0, a1_ = 1.5 * np.pi + g, 2 * np.pi - g
        elif i == 2:    a0, a1_ = g, 0.5 * np.pi - g
        else:           a0, a1_ = 0.5 * np.pi + g, np.pi - g
        tt = np.linspace(a0, a1_, 40)
        contour.extend(np.stack([c[0] + rc * np.cos(tt),
                                 c[1] + rc * np.sin(tt)], 1))
        # side endpoints adjoining this corner
        if i == 0:
            contour.append((cx + side_in, cy + a))
            nxt = [(cx - side_in, cy + a)]
        elif i == 1:
            contour.append((cx - a, cy + side_in))
            nxt = [(cx - a, cy - side_in)]
        elif i == 2:
            contour.append((cx - side_in, cy - a))
            nxt = [(cx + side_in, cy - a)]
        else:
            contour.append((cx + a, cy - side_in))
            nxt = [(cx + a, cy + side_in)]
        contour.extend(nxt)
    contour = np.array(contour)
    ax.add_patch(mpatches.Polygon(contour, closed=True, facecolor='none',
                 edgecolor='none', hatch='///'))
    ax.plot(np.append(contour[:, 0], contour[0, 0]),
            np.append(contour[:, 1], contour[0, 1]), 'k-', lw=1.2)
    ax.text(cx, 4.22, '$(a)$', ha='center', fontsize=12)

    # ---------------- (b) energy reduced below free-electron value -------
    ox, oy, kb, hE = 5.8, 4.7, 3.6, 1.95
    EFy = oy + hE
    zb = ox + kb
    arrow(ax, ox, oy, ox, oy + 3.35)
    ax.text(ox - 0.28, oy + 3.15, r'$\mathcal{E}$', fontsize=12)
    ax.plot([ox, zb], [oy, oy], 'k-', lw=1.1)
    ax.plot([zb, zb], [oy - 0.28, oy + 3.15], 'k-', lw=1.1)
    ax.text(ox - 0.12, oy - 0.44, '$O$', fontsize=11, ha='center')
    ax.text(zb, oy - 0.44, 'Z.B.', fontsize=11, ha='center')
    ax.plot([ox, zb], [EFy, EFy], 'k-', lw=1.1)
    u = np.linspace(0, 1, 300)
    S = 3 * u**2 - 2 * u**3
    ys = oy + hE * S
    ax.plot(ox + kb * u, ys, 'k-', lw=1.2)
    ax.fill_between(ox + kb * u, ys, EFy, facecolor='none', hatch='///',
                    edgecolor='k', lw=0)
    # dashed free-electron branch
    u0 = 0.62
    y0 = oy + hE * (3 * u0**2 - 2 * u0**3)
    m = hE * (6 * u0 - 6 * u0**2)
    yend = EFy + 1.18
    c2 = (yend - y0 - m * (1 - u0)) / (1 - u0)**2
    ud = np.linspace(u0, 1, 80)
    yd = y0 + m * (ud - u0) + c2 * (ud - u0)**2
    ax.plot(ox + kb * ud, yd, 'k--', lw=1.0)
    brace(ax, zb + 0.12, EFy, yend, 0.11, tip=1)
    ax.text(zb + 0.60, 0.5 * (EFy + yend), r'$\delta\mathcal{E}$',
            va='center', fontsize=11)
    ax.text(ox + 0.5 * kb, 4.05, '$(b)$', ha='center', fontsize=12)

    # ---------------- (c) density of states ----------------
    ox, oy = 1.9, 1.05
    W, H = 5.2, 2.35
    ax.plot([ox, ox], [oy, oy + 2.95], 'k-', lw=1.1)
    arrow(ax, ox, oy + 2.85, ox, oy + 3.18)
    ax.text(ox - 0.12, oy + 2.86, r'$\mathcal{N}(\mathcal{E})$',
            fontsize=11, ha='right')
    ax.plot([ox, ox + W + 0.5], [oy, oy], 'k-', lw=1.1)
    arrow(ax, ox + W + 0.3, oy, ox + W + 0.62, oy)
    ax.text(ox + W + 0.42, oy - 0.40, r'$\mathcal{E}$', fontsize=12)
    ax.text(ox - 0.12, oy - 0.44, '$O$', fontsize=11, ha='center')
    pts = [(0, 0), (0.04, 0.22), (0.09, 0.30), (0.16, 0.335), (0.24, 0.345),
           (0.32, 0.36), (0.40, 0.44), (0.50, 0.58), (0.62, 0.74),
           (0.72, 0.90), (0.775, 1.0), (0.80, 0.965), (0.84, 0.86),
           (0.885, 0.62), (0.915, 0.30), (0.93, 0.02)]
    uu = np.linspace(0, 0.93, 400)
    nn = pchip_eval(*zip(*pts), uu)
    ax.plot(ox + W * uu, oy + H * nn, 'k-', lw=1.2)
    uF = 0.74
    ax.plot([ox + W * uF, ox + W * uF], [oy, oy + H * 0.97], 'k--', lw=1.0)
    ax.text(ox + W * uF, oy - 0.44, r'$\mathcal{E}_F$', fontsize=11,
            ha='center')
    ax.text(4.3, 0.35, '$(c)$', ha='center', fontsize=12)

    save(fig, 80)


# ---------------------------------------------------------------- fig 81
def fig_81():
    fig, ax = new_fig(10.2, 3.55)
    x0, y0 = 0.55, 0.55
    ax.plot([x0, x0], [y0, 3.02], 'k-', lw=1.1)
    ax.plot([x0, 9.5], [y0, y0], 'k-', lw=1.1)
    arrow(ax, 8.6, y0, 9.35, y0)
    ax.text(8.75, 0.22, r'$\mathcal{E}$', fontsize=12)
    ax.plot([x0 - 0.08, x0 + 0.0], [2.5, 2.5], 'k-', lw=1.0)   # level-1 tick

    xF, kT = 6.0, 0.45
    ax.plot([x0, xF], [2.5, 2.5], 'k-', lw=1.2)                # T=0 step
    ax.plot([xF, xF], [2.5, y0], 'k-', lw=1.2)
    ax.text(xF + 0.68, 2.33, '$T=0$', fontsize=11)

    xs = np.linspace(x0, 9.2, 400)
    f = y0 + 1.95 / (1 + np.exp((xs - xF) / 0.40))
    ax.plot(xs, f, 'k-', lw=1.2)
    ax.text(6.85, 1.42, r'$f^0(\mathcal{E})$', fontsize=11)

    bell = y0 + 2.38 / np.cosh((xs - xF) / 0.78)**2
    ax.plot(xs, bell, 'k--', lw=1.1)
    ax.text(7.18, 2.82, r'$-\,\partial f^0/\partial\mathcal{E}$', fontsize=11)

    for xv in (xF, xF + kT):
        ax.plot([xv, xv], [2.95, y0], 'k--', lw=0.9)
    # |kT| marker
    ax.plot([xF, xF], [y0, 0.14], 'k-', lw=0.9)
    ax.plot([xF + kT, xF + kT], [y0, 0.14], 'k-', lw=0.9)
    arrow(ax, xF, 0.26, xF + kT, 0.26, style='<|-|>', lw=0.9, ms=8)
    ax.text(xF + kT + 0.16, 0.26, r'$|kT|$', fontsize=11, va='center')
    ax.text(xF - 0.12, 0.30, r'$\mathcal{E}_F$', ha='right', fontsize=11)

    save(fig, 81)


# ---------------------------------------------------------------- fig 82
def fig_82():
    fig, ax = new_fig(10.6, 3.6)
    x0, y0 = 0.8, 0.7
    arrow(ax, x0, y0, x0, 3.32)
    ax.text(0.68, 3.12, r'$f_0(\mathcal{E})$', ha='right', fontsize=11)
    ax.plot([x0, 10.35], [y0, y0], 'k-', lw=1.1)
    arrow(ax, 9.6, y0, 10.3, y0)
    ax.text(10.05, 0.38, r'$\mathcal{E}$', fontsize=12)

    EF, top = 7.0, 3.0
    ax.plot([x0, EF], [top, top], 'k-', lw=1.2)
    ax.plot([EF, EF], [top, y0], 'k-', lw=1.2)
    ax.text(EF + 0.28, 2.42, '$T_0$', fontsize=11)

    pars = [((6.55, 0.85), '$T_1$', (6.42, 2.62)),
            ((6.05, 1.55), '$T_2$', (5.62, 2.80)),
            ((5.60, 2.00), '$T_3$', (3.62, 2.72)),
            ((3.60, 3.40), '$T_4$', (2.20, 2.28))]
    xs = np.linspace(x0, 10.2, 500)
    for (z, kt), lab, (lx, ly) in pars:
        fv = 1.0 / (1.0 + np.exp((xs - z) / kt))
        ax.plot(xs, y0 + (top - y0) * fv, 'k-', lw=1.2)
        yz = y0 + (top - y0) * 0.5
        ax.plot([z, z], [yz, y0], 'k--', lw=0.9)
        ax.text(lx, ly, lab, fontsize=11)
    for z, lab in ((3.60, r'$\zeta_4$'), (5.60, r'$\zeta_3$'),
                   (6.05, r'$\zeta_2$'), (6.55, r'$\zeta_1$')):
        ax.text(z, 0.34, lab, ha='center', fontsize=11)
    ax.text(EF, 0.34, r'$\mathcal{E}_F$', ha='center', fontsize=11)

    save(fig, 82)


# ---------------------------------------------------------------- fig 83
def fig_83():
    fig, ax = new_fig(12.6, 5.0)

    # ---------------- (a) absolute energy scheme ----------------
    xa = 1.0
    ax.plot([xa, xa], [0.75, 4.2], 'k-', lw=1.1)
    arrow(ax, xa, 4.1, xa, 4.5)
    ax.text(xa - 0.18, 4.32, r'$\mathcal{E}$', ha='right', fontsize=12)
    ax.text(xa - 0.20, 0.58, '$O$', ha='center', fontsize=11)
    ax.plot([xa - 0.12, xa + 0.12], [0.75, 0.75], 'k-', lw=1.0)
    ec, ev, ez = 3.3, 2.1, 2.7
    xb = 4.6
    ax.add_patch(mpatches.Rectangle((xa, ec), xb - xa, 0.85,
                 facecolor='none', edgecolor='none', hatch='///'))
    ax.add_patch(mpatches.Rectangle((xa, 0.95), xb - xa, ev - 0.95,
                 facecolor='none', edgecolor='none', hatch='///'))
    ax.plot([xa, xb], [ec, ec], 'k-', lw=1.2)
    ax.plot([xa, xb], [ev, ev], 'k-', lw=1.2)
    ax.plot([xa, xb], [ez, ez], 'k--', lw=1.0)
    ax.add_patch(mpatches.Rectangle((3.52, 3.68), 0.16, 0.16, fc='k', ec='k'))
    ax.add_patch(mpatches.Circle((2.35, 1.72), 0.09, fc='white', ec='k', lw=1.1))
    ax.text(xa - 0.16, ec, r'$\mathcal{E}_c$', ha='right', va='center',
            fontsize=11)
    ax.text(xa - 0.16, ev, r'$\mathcal{E}_v$', ha='right', va='center',
            fontsize=11)
    ax.text(xa - 0.16, ez, r'$\zeta$', ha='right', va='center', fontsize=11)
    brace(ax, xb + 0.14, ev, ec, 0.13, tip=1)
    ax.text(xb + 0.62, 0.5 * (ec + ev), r'$\mathcal{E}_{\rm gap}$',
            va='center', fontsize=11)
    ax.text(2.8, 0.30, '$(a)$', ha='center', fontsize=12)

    # ---------------- (b) electron / hole schemes ----------------
    xa = 7.3; xb = 11.15
    ec, ev, ez = 3.55, 2.1, 2.85
    ax.plot([xa, xa], [ec, 4.28], 'k-', lw=1.1)
    arrow(ax, xa, 4.18, xa, 4.55)
    ax.text(xa - 0.18, 4.05, r'$\mathcal{E}_e$', ha='right', fontsize=11)
    ax.plot([xa, xa], [ev - 1.1, ec], 'k--', lw=1.0)
    ax.plot([xb, xb], [4.32, ez], 'k--', lw=1.0)
    ax.plot([xb, xb], [ez, 0.62], 'k-', lw=1.1)
    arrow(ax, xb, 0.72, xb, 0.52)
    ax.text(xb + 0.18, 1.30, r'$\mathcal{E}_h$', fontsize=11)
    ax.add_patch(mpatches.Rectangle((xa, ec), xb - xa, 0.62,
                 facecolor='none', edgecolor='none', hatch='///'))
    ax.add_patch(mpatches.Rectangle((xa, 0.98), xb - xa, ev - 0.98,
                 facecolor='none', edgecolor='none', hatch='///'))
    ax.plot([xa, xb], [ec, ec], 'k-', lw=1.2)
    ax.plot([xa, xb], [ev, ev], 'k-', lw=1.2)
    ax.plot([xa - 0.15, xb + 0.15], [ez, ez], 'k--', lw=1.0)
    ax.add_patch(mpatches.Rectangle((8.42, 3.76), 0.16, 0.16, fc='k', ec='k'))
    ax.add_patch(mpatches.Circle((10.32, 1.52), 0.09, fc='white', ec='k',
                 lw=1.1))
    ax.text(xa - 0.16, ez, r'$-\zeta_e$', ha='right', va='center', fontsize=11)
    ax.text(xa - 0.16, ev, r'$-\mathcal{E}_{\rm gap}$', ha='right',
            va='center', fontsize=11)
    ax.plot([xb + 0.02, xb + 0.18], [ec, ec], 'k-', lw=0.9)
    ax.text(xb + 0.24, ec, r'$\mathcal{E}_{\rm gap}$', va='center',
            fontsize=11)
    ax.text(xb + 0.24, ez, r'$\zeta_h$', va='center', fontsize=11)
    arrow(ax, 7.75, ez, 7.75, ec, style='<|-|>', lw=0.9, ms=8)
    ax.text(7.92, 0.5 * (ez + ec), r'$|\zeta_e|$', fontsize=11)
    arrow(ax, 10.0, ev, 10.0, ez, style='<|-|>', lw=0.9, ms=8)
    ax.text(10.17, 0.5 * (ez + ev), r'$|\zeta_h|$', fontsize=11)
    ax.text(9.2, 0.30, '$(b)$', ha='center', fontsize=12)

    save(fig, 83)


# ---------------------------------------------------------------- fig 84
def fig_84():
    fig, ax = new_fig(13.2, 5.1)

    def panel(x0, y0, imp_label, free=None):
        dx, dy = 1.62, 1.42
        r = 0.52; hw = 0.24; ext = 0.60
        xs = [x0, x0 + dx, x0 + 2 * dx]
        ys = [y0, y0 + dy, y0 + 2 * dy]
        # grey bond bands
        for y in ys:
            ax.add_patch(mpatches.Rectangle((xs[0] - ext, y - hw),
                         (xs[2] - xs[0]) + 2 * ext, 2 * hw,
                         fc='0.84', ec='none', zorder=1))
        for x in xs:
            ax.add_patch(mpatches.Rectangle((x - hw, ys[0] - ext),
                         2 * hw, (ys[2] - ys[0]) + 2 * ext,
                         fc='0.84', ec='none', zorder=1))
        # bond electron pairs: one pair near each atom on every segment
        off = r + 0.30
        for y in ys:
            for x in xs:                # horizontal bonds: pair left & right
                for sgn in (-1, 1):
                    xc = x + sgn * off
                    ax.add_patch(mpatches.Circle((xc, y - 0.115), 0.042,
                                 fc='k', ec='k', zorder=3))
                    ax.add_patch(mpatches.Circle((xc, y + 0.115), 0.042,
                                 fc='k', ec='k', zorder=3))
        for x in xs:
            for y in ys:                # vertical bonds: pair above & below
                for sgn in (-1, 1):
                    yc = y + sgn * off
                    ax.add_patch(mpatches.Circle((x - 0.115, yc), 0.042,
                                 fc='k', ec='k', zorder=3))
                    ax.add_patch(mpatches.Circle((x + 0.115, yc), 0.042,
                                 fc='k', ec='k', zorder=3))
        for y in ys:                    # stubs beyond edge atoms
            for sgn, xe in ((-1, xs[0]), (1, xs[2])):
                xc = xe + sgn * (off + 0.22)
                ax.add_patch(mpatches.Circle((xc, y - 0.115), 0.042,
                             fc='k', ec='k', zorder=3))
                ax.add_patch(mpatches.Circle((xc, y + 0.115), 0.042,
                             fc='k', ec='k', zorder=3))
        for x in xs:
            for sgn, ye in ((-1, ys[0]), (1, ys[2])):
                yc = ye + sgn * (off + 0.22)
                ax.add_patch(mpatches.Circle((x - 0.115, yc), 0.042,
                             fc='k', ec='k', zorder=3))
                ax.add_patch(mpatches.Circle((x + 0.115, yc), 0.042,
                             fc='k', ec='k', zorder=3))
        # atoms
        cx, cy = xs[1], ys[1]
        for i, x in enumerate(xs):
            for j, y in enumerate(ys):
                imp = (i == 1 and j == 1)
                ax.add_patch(mpatches.Circle((x, y), r, fc='white', ec='k',
                             lw=2.0 if imp else 1.1, zorder=4))
                ax.text(x, y, imp_label if imp else 'Ge',
                        ha='center', va='center', fontsize=10, zorder=5)
        return (cx, cy)

    cxa, cya = panel(1.45, 1.15, 'As$^+$')
    ax.add_patch(mpatches.Circle((cxa + 0.82, cya + 0.80), 0.062, fc='k',
                 ec='k', zorder=5))
    ax.text(cxa + 0.66, cya + 1.12, '$e^-$', fontsize=10, zorder=5)
    ax.text(3.85, 0.32, '$(a)$', ha='center', fontsize=12)

    cxb, cyb = panel(7.85, 1.15, 'In$^-$')
    ax.add_patch(mpatches.Circle((cxb + 1.18, cyb), 0.075, fc='white',
                 ec='k', lw=1.2, zorder=5))
    ax.text(cxb + 0.80, cyb + 0.28, '$e^+$', fontsize=10, zorder=5)
    ax.text(10.25, 0.32, '$(b)$', ha='center', fontsize=12)

    save(fig, 84)


# ---------------------------------------------------------------- fig 85
def fig_85():
    fig, ax = new_fig(10.6, 3.65)
    x0, y0 = 0.9, 0.7
    arrow(ax, x0, y0, x0, 3.5)
    ax.text(0.80, 3.28, r'$f_0(\mathcal{E})$', ha='right', fontsize=11)
    ax.plot([x0, 10.2], [y0, y0], 'k-', lw=1.1)
    ax.text(10.05, 0.40, r'$\mathcal{E}$', fontsize=12)

    EF, kT, top = 6.3, 0.62, 3.15
    ax.plot([x0, EF], [top, top], 'k-', lw=1.2)
    ax.plot([EF, EF], [top, y0], 'k-', lw=1.2)
    xs = np.linspace(x0, 9.9, 500)
    f = top / (1 + np.exp((xs - EF) / kT))
    ax.plot(xs, f, 'k-', lw=1.2)
    ax.fill_between(xs, y0, f, where=xs <= EF + 2.0 * kT,
                    facecolor='none', edgecolor='none', hatch='///')
    # excitation arrow
    ax.add_patch(mpatches.Circle((6.12, 2.60), 0.055, fc='k', ec='k', zorder=5))
    ax.add_patch(mpatches.Circle((7.35, 1.05), 0.055, fc='k', ec='k', zorder=5))
    ax.annotate('', xy=(7.32, 1.13), xytext=(6.18, 2.52),
                arrowprops=dict(arrowstyle='-|>', lw=1.1, color='k',
                                connectionstyle='arc3,rad=-0.45',
                                mutation_scale=11))
    # dashed limits + kT dimension
    for xv in (EF - 0.9 * kT, EF + 2.0 * kT):
        yv = top / (1 + np.exp((xv - EF) / kT))
        ax.plot([xv, xv], [yv, y0], 'k--', lw=0.9)
        ax.plot([xv, xv], [y0, 0.14], 'k-', lw=0.9)
    xm = EF + 0.55 * kT
    arrow(ax, EF - 0.9 * kT, 0.22, xm - 0.18, 0.22, style='-|>', lw=0.9, ms=9)
    arrow(ax, EF + 2.0 * kT, 0.22, xm + 0.18, 0.22, style='-|>', lw=0.9, ms=9)
    ax.text(xm, 0.22, r'$kT$', ha='center', va='center', fontsize=11)
    ax.text(EF + 0.02, 0.50, r'$\mathcal{E}_F$', ha='center', fontsize=11)

    save(fig, 85)


if __name__ == '__main__':
    for n in range(76, 86):
        globals()[f'fig_{n}']()
