# -*- coding: utf-8 -*-
"""标注-线条间距自检：渲染图件，计算文本框与关键线段/圆的最小距离(px)。
用法：作为模块导入后调用 check_fig_2_2() / measure_fig_5_4_label()。
"""
import sys, os
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matplotlib
matplotlib.use('Agg')

DPI = 220.0


def _rect_dist(pts, bb):
    """点到矩形 [x0,y0,x1,y1] 的距离（内部为 0）"""
    x, y = pts[:, 0], pts[:, 1]
    dx = np.maximum(bb[0] - x, np.minimum(x, bb[2]) - bb[2].clip(max=None) if False else x - bb[2])
    dx = np.maximum.reduce([bb[0] - x, np.zeros_like(x), x - bb[2]])
    dy = np.maximum.reduce([bb[1] - y, np.zeros_like(y), y - bb[3]])
    return np.hypot(dx, dy)


def text_bb(t):
    return t.get_window_extent()


def seg_pts(p0, p1, n=600):
    t = np.linspace(0, 1, n)[:, None]
    return np.asarray(p0)[None, :] * (1 - t) + np.asarray(p1)[None, :] * t


def circle_pts(c, r, n=1500):
    a = np.linspace(0, 2 * np.pi, n)
    return np.stack([c[0] + r * np.cos(a), c[1] + r * np.sin(a)], axis=1)


def min_dist(fig, ax, t, pts_data, pad_pt=0.0):
    """文本 t 与数据坐标点集 pts_data 的最小距离（显示 px，含 pad_pt 的白边膨胀）"""
    r = fig.canvas.get_renderer()
    bb = t.get_window_extent(r)
    p0 = np.array([bb.x0, bb.y0]); p1 = np.array([bb.x1, bb.y1])
    # pad 膨胀（pt -> px）
    pad = pad_pt * fig.dpi / 72.0
    lo = p0 - pad; hi = p1 + pad
    disp = ax.transData.transform(pts_data)
    dx = np.maximum.reduce([lo[0] - disp[:, 0], np.zeros(len(disp)), disp[:, 0] - hi[0]])
    dy = np.maximum.reduce([lo[1] - disp[:, 1], np.zeros(len(disp)), disp[:, 1] - hi[1]])
    return float(np.hypot(dx, dy).min())


def box_gap(fig, ta, tb):
    """两文本框间隙 px"""
    r = fig.canvas.get_renderer()
    a = ta.get_window_extent(r); b = tb.get_window_extent(r)
    dx = max(b.x0 - a.x1, a.x0 - b.x1, 0)
    dy = max(b.y0 - a.y1, a.y0 - b.y1, 0)
    return float(np.hypot(dx, dy))


def find_text(ax, needle):
    for t in ax.texts:
        if needle in t.get_text():
            return t
    raise KeyError(needle)


def report(fig, ax, items):
    """items: list of (label_text_obj, name, {seg_name: pts})"""
    r = fig.canvas.get_renderer()
    print(f"--- clearances (px @ {fig.dpi:.0f}dpi, <1.0 = strike) ---")
    for t, name, segs in items:
        bb = t.get_window_extent(r)
        w_in = (bb.x1 - bb.x0) / fig.dpi
        h_in = (bb.y1 - bb.y0) / fig.dpi
        parts = []
        for sname, pts in segs.items():
            d = min_dist(fig, ax, t, pts)
            flag = 'STRIKE' if d < 1.0 else ('tight' if d < 3.0 else '')
            parts.append(f"{sname}={d:.1f}{flag}")
        print(f"[{name}] w={w_in:.3f}in h={h_in:.3f}in  " + "  ".join(parts))


# ---------------------------------------------------------------- fig 2.2
def build_fig_2_2(pos):
    """按 pos 内的坐标重建 fig_2_2（与 draw_figs_A.fig_2_2 一致，仅标注位置参数化）"""
    import draw_figs_A as A
    fig, ax = A.plt.subplots(figsize=(3.1, 3.35))
    A.plain_axes(ax)
    ax.set_xlim(-0.42, 2.62)
    ax.set_ylim(-0.62, 2.42)
    ax.set_aspect('equal')
    ax.plot([0, 2, 2, 0, 0], [0, 0, 2, 2, 0], 'k-', lw=1.4)
    G, M, X = (1, 1), (2, 2), (2, 1)
    Zp = (2, 1.3)
    ax.plot([G[0], M[0]], [G[1], M[1]], 'k-', lw=1.2)
    ax.plot([G[0], X[0]], [G[1], X[1]], 'k-', lw=1.2)
    A.dline(ax, G[0], G[1], Zp[0], Zp[1], lw=1.0)
    for p in [G, M, X, Zp, (2, 1.6), (1.45, 1), (1.55, 1.55)]:
        ax.plot([p[0]], [p[1]], 'k.', ms=5)
    A.arr(ax, 1.60, 1.60, 1.78, 1.78, lw=1.3, ms=11)
    A.arr(ax, 1.51, 1.64, 1.40, 1.75, lw=1.3, ms=11)
    A.ctext(ax, 1.73, 1.52, r'$L$', fontsize=10)
    A.ctext(ax, 1.35, 1.83, r'$T$', fontsize=10)
    A.ctext(ax, *pos['Sigma'], r'$\Sigma$', fontsize=10.5, **pos.get('Sigma_kw', {}))
    A.arr(ax, 1.50, 1.0, 1.68, 1.0, lw=1.3, ms=11)
    A.arr(ax, 1.45, 1.05, 1.45, 1.23, lw=1.3, ms=11)
    A.ctext(ax, *pos['Tdelta'], r'$T$', fontsize=10, **pos.get('Tdelta_kw', {}))
    A.ctext(ax, 1.72, 0.90, r'$L$', fontsize=10)
    A.ctext(ax, 1.36, 0.88, r'$\Delta$', fontsize=10.5)
    A.arr(ax, *pos['kz_arr0'], *pos['kz_arr1'], lw=1.2, ms=10)
    A.ctext(ax, *pos['kz'], r'$k_z$', fontsize=10, **pos.get('kz_kw', {}))
    A.arr(ax, 2.0, 1.3, 2.24, 1.3, lw=1.3, ms=11)
    A.ctext(ax, 2.40, 1.3, r'(2)', fontsize=10)
    A.arr(ax, 2.0, 1.62, 2.0, 1.84, lw=1.3, ms=11)
    A.ctext(ax, 2.14, 1.72, r'(1)', fontsize=10)
    A.ctext(ax, *pos['Z'], r'$Z$', fontsize=10.5)
    A.ctext(ax, 0.87, 0.87, r'$\Gamma$', fontsize=11)
    A.ctext(ax, 2.10, 2.08, r'$M$', fontsize=11)
    A.ctext(ax, 2.15, 0.92, r'$X$', fontsize=11)
    yd = -0.30
    ax.plot([0, 0], [yd - 0.07, yd + 0.07], 'k-', lw=1.0)
    ax.plot([2, 2], [yd - 0.07, yd + 0.07], 'k-', lw=1.0)
    A.arr(ax, 0.62, yd, 0.03, yd, lw=1.0, ms=10)
    A.arr(ax, 1.38, yd, 1.97, yd, lw=1.0, ms=10)
    A.ctext(ax, 1.0, yd, r'$2\pi/a$', fontsize=10, ha='center',
            va='center', bbox=dict(fc='white', ec='none', pad=1.2))
    return fig, ax


DIA = ((1, 1), (2, 2))            # Gamma-M
DAS = ((1, 1), (2, 1.3))          # Gamma-Z dashed
KZA = ((1.78, 1.08), (1.95, 1.265))   # kz 方向小箭头
SLA = ((1.60, 1.60), (1.78, 1.78))    # Sigma-L 箭头
DTA = ((1.45, 1.05), (1.45, 1.23))    # Delta-T 箭头
DLA = ((1.50, 1.0), (1.68, 1.0))      # Delta-L 箭头
A2 = ((2.0, 1.3), (2.24, 1.3))


def check_fig_2_2(pos, verbose=True):
    import draw_figs_A as A
    fig, ax = build_fig_2_2(pos)
    fig.dpi = DPI
    fig.canvas.draw()
    sig = find_text(ax, 'Sigma') if False else None
    # 按位置找文本
    def near(x, y):
        best, bt = 1e9, None
        for t in ax.texts:
            bb = t.get_window_extent(fig.canvas.get_renderer())
            dd = ax.transData.transform([(x, y)])[0]
            d = np.hypot((bb.x0+bb.x1)/2 - dd[0], (bb.y0+bb.y1)/2 - dd[1])
            if d < best:
                best, bt = d, t
        return bt
    items = [
        (near(*pos['Sigma']), 'Sigma', {'diag': seg_pts(*DIA), 'dash': seg_pts(*DAS),
                                        'SigmaL-arr': seg_pts(*SLA), 'dot(1.55,1.55)': np.array([[1.55, 1.55]])}),
        (near(*pos['Tdelta']), 'Tdelta', {'diag': seg_pts(*DIA), 'dash': seg_pts(*DAS),
                                          'own-arr': seg_pts(*DTA)}),
        (near(*pos['kz']), 'kz', {'dash': seg_pts(*DAS), 'kz-arr': seg_pts(*KZA),
                                  'SigmaL-arr': seg_pts(*SLA), '(2)-arr': seg_pts(*A2),
                                  'dotZ': np.array([[2, 1.3]])}),
        (near(*pos['Z']), 'Z', {'dash': seg_pts(*DAS), 'kz-arr': seg_pts(*KZA),
                                '(2)-arr': seg_pts(*A2), 'dotZ': np.array([[2, 1.3]])}),
    ]
    # 文本-文本间距
    gaps = []
    names = ['Sigma', 'Tdelta', 'kz', 'Z']
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            g = box_gap(fig, items[i][0], items[j][0])
            gaps.append(f"{items[i][1]}~{items[j][1]}={g:.1f}{'STRIKE' if g < 1 else ''}")
    if verbose:
        report(fig, ax, items)
        print('text-text: ' + '  '.join(gaps))
    A.plt.close(fig)
    return items


# ---------------------------------------------------------------- fig 5.4
def build_fig_5_4(equ):
    """equ: (x, y, fontsize, ha, va, rotation) 或 None 用原位置"""
    import draw_figs_B as B
    fig, ax = B.plt.subplots(figsize=(4.35, 3.95))
    B.plain_axes(ax)
    ax.set_aspect('equal')
    R = 1.0
    ap = R * np.sqrt(3) / 2

    def hexagon(cx, cy):
        angs = np.deg2rad([90, 150, 210, 270, 330, 30, 90])
        return [(cx + R * np.cos(a), cy + R * np.sin(a)) for a in angs]

    cells = [(0, 0), (2 * ap, 0), (ap, 1.5 * R), (ap, -1.5 * R)]
    for cx, cy in cells:
        pts = hexagon(cx, cy)
        ax.plot([p[0] for p in pts], [p[1] for p in pts], 'k-', lw=1.3)
        ax.add_patch(B.Circle((cx, cy), ap, facecolor='none', edgecolor='k', lw=1.3))
    ax.set_xlim(-1.05, 3.05)
    ax.set_ylim(-1.95, 2.55)
    J = (0.0, 0.0)
    Bv = (0.866 * np.cos(np.deg2rad(-28)), 0.866 * np.sin(np.deg2rad(-28)))
    Q = (0.60, 0.42)
    T = (Bv[0] + Q[0], Bv[1] + Q[1])
    A_pt = (-0.866, T[1])
    B.vec(ax, J[0], J[1], Bv[0], Bv[1], lw=1.2, ms=10)
    B.vec(ax, J[0], J[1], Q[0], Q[1], lw=1.2, ms=10)
    B.vec(ax, Bv[0], Bv[1], T[0], T[1], lw=1.2, ms=10)
    ax.annotate('', xy=A_pt, xytext=T,
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.2,
                                shrinkA=0, shrinkB=0, mutation_scale=13))
    ax.annotate('', xy=(0.25, T[1]), xytext=(0.55, T[1]),
                arrowprops=dict(arrowstyle='-|>', color='k', lw=1.2,
                                shrinkA=0, shrinkB=0, mutation_scale=11))
    ax.text(Bv[0] - 0.10, Bv[1] - 0.15, r'$\boldsymbol{k}$', fontsize=10,
            ha='center', va='center')
    ax.text(Q[0] + 0.09, Q[1] + 0.06, r'$\boldsymbol{q}$', fontsize=10,
            ha='left', va='center')
    ax.text(T[0] + 0.10, T[1] + 0.02, r'$\boldsymbol{k+q}$', fontsize=10,
            ha='left', va='center')
    ax.text(0.28, T[1] - 0.17, r'$\boldsymbol{K}_n$', fontsize=10,
            ha='center', va='center')
    x, y, fs, ha, va, rot = equ
    ax.text(x, y, r"$\boldsymbol{k+q+K}_n=\boldsymbol{k'}$", fontsize=fs,
            ha=ha, va=va, rotation=rot)
    return fig, ax


def check_fig_5_4(equ, verbose=True):
    import draw_figs_B as B
    fig, ax = build_fig_5_4(equ)
    fig.dpi = DPI
    fig.canvas.draw()
    eqt = ax.texts[-1]
    segs = {
        'circleL': circle_pts((0, 0), np.sqrt(3) / 2),
        'q-ray': seg_pts((0, 0), (0.60, 0.42)),
        'k-ray': seg_pts((0, 0), (0.765, -0.406)),
        'long-arr': seg_pts((-0.866, 0.014), (1.35, 0.01)),
        'mid-arr': seg_pts((0.25, 0.01), (0.55, 0.01)),
        'Kn-text': np.array([[0.28, -0.16]]),
    }
    if verbose:
        report(fig, ax, [(eqt, 'equation', segs)])
    B.plt.close(fig)
    return eqt


if __name__ == '__main__':
    print('===== fig 2.2 current =====')
    check_fig_2_2({'Sigma': (1.50, 1.42), 'Tdelta': (1.45, 1.32),
                   'kz': (1.72, 1.24), 'Z': (1.90, 1.18),
                   'kz_arr0': (1.78, 1.08), 'kz_arr1': (1.95, 1.265)})
    print('===== fig 5.4 current =====')
    check_fig_5_4((-0.86, 0.30, 9, 'left', 'center', 0))
