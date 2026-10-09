# -*- coding: utf-8 -*-
# 图 6.18 La0.7Pb0.3MnO3 (T=10 K) 自旋波色散（Perring et al. 1996），
# 沿高对称路径 (1/2,1/2,0)-G-X-M-R | G-X-R，按扫描特征重建
import sys
sys.path.insert(0, r'E:\AI整理书籍\磁学\book\fig_src')
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mplstyle import save_fig

fig, ax = plt.subplots(figsize=(5.2, 3.6))


def catmull_rom(pts, n=60):
    """Catmull-Rom 样条插值（不依赖 scipy）。"""
    P = np.asarray(pts, float)
    if len(P) < 3:
        return P[:, 0], P[:, 1]
    Pe = np.vstack([P[0] + (P[0] - P[1]), P, P[-1] + (P[-1] - P[-2])])
    xs, ys = [], []
    for i in range(1, len(Pe) - 2):
        p0, p1, p2, p3 = Pe[i - 1], Pe[i], Pe[i + 1], Pe[i + 2]
        t = np.linspace(0, 1, n, endpoint=False)[:, None]
        v = 0.5 * ((2 * p1) + (-p0 + p2) * t
                   + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t**2
                   + (-p0 + 3 * p1 - 3 * p2 + p3) * t**3)
        xs.append(v[:, 0]); ys.append(v[:, 1])
    xs.append([Pe[-2, 0]]); ys.append([Pe[-2, 1]])
    return np.concatenate(xs), np.concatenate(ys)


# ---- 路径节点横坐标 ----
XH = 0.0        # (1/2,1/2,0)  M point
XG = 1.35       # G
XX = 2.35       # X
XM = 3.15       # M
XR = 4.30       # R (peak)
GB1, GB2 = 5.30, 5.40   # axis break
XG2 = 5.80      # second-zone G
XX2 = 6.20      # second-zone X
XE = 7.20       # (1/2,1/2,1/2) end

cps = [(XH, 73), (0.55, 46), (0.8, 34), (1.0, 26), (1.1, 20), (1.2, 12),
       (XG, 0), (1.5, 8), (1.65, 13), (1.9, 20), (2.1, 25), (XX, 40),
       (2.55, 38.5), (2.75, 48), (2.9, 54), (XM, 71), (3.6, 93), (3.95, 105),
       (XR, 110), (4.55, 100), (4.8, 76), (5.05, 58), (GB1, 38),
       (GB2, 33), (5.6, 15), (XG2, 0), (5.95, 10), (6.1, 28), (XX2, 48),
       (6.5, 78), (6.8, 95), (7.05, 104), (XE, 108)]
cx, cy = catmull_rom(cps, n=80)
m1 = cx <= GB1
m2 = cx >= GB2
ax.plot(cx[m1], cy[m1], 'k-', lw=1.6, zorder=3)
ax.plot(cx[m2], cy[m2], 'k-', lw=1.6, zorder=3)

# ---- 数据点（带小竖直误差棒） ----
data = [(0.55, 46), (0.78, 38), (0.85, 34), (1.02, 26), (1.10, 20), (1.16, 15),
        (1.50, 8), (1.62, 10), (1.72, 13), (1.9, 20), (2.0, 22), (2.1, 25),
        (2.45, 40), (2.78, 48), (2.9, 54), (XM, 71), (3.95, 103),
        (4.55, 97), (4.9, 69), (5.1, 58), (5.25, 39),
        (6.12, 48), (6.6, 85), (6.85, 95)]
data = np.array(data)
ax.errorbar(data[:, 0], data[:, 1], yerr=np.full(len(data), 3.0),
            fmt='o', color='k', mfc='k', ms=5, elinewidth=1.0,
            capsize=2, capthick=1.0, ls='none', zorder=4)

# ---- 分区竖线与轴断裂 ----
for xv in [XH, XG, XX, XM, XR, XG2, XX2]:
    ax.axvline(xv, color='k', lw=0.9)
ax.add_patch(Rectangle((GB1, -8), GB2 - GB1, 132, fc='white', ec='none', zorder=5))
for xv in [GB1, GB2]:
    ax.plot([xv, xv], [0, 112], 'k-', lw=0.9, zorder=6)

# ---- 轴 ----
ax.set_xlim(-0.02, 7.4)
ax.set_ylim(-4, 116)
ax.set_yticks(range(0, 101, 20))
ax.set_xticks([XH, XG, XX, XM, XR, XG2, XX2, XE])
ax.set_xticklabels(['½½½0', '000', '½00', '½½½0', '½½½½',
                    '000', '½00', '½½½½'], fontsize=9)
ax.set_ylabel('Energy (meV)')
ax.tick_params(axis='x', length=0)

# ---- 顶部惯用记号 ----
tops = [('M', XH), (r'$\Gamma$', XG), ('X', XX), ('M', XM), ('R', XR),
        (r'$\Gamma$', XG2), ('X', XX2), ('R', XE)]
for lab, xv in tops:
    ax.text(xv, 119, lab, ha='center', va='bottom', fontsize=11)

# ---- 左上参数框 ----
ax.text(0.28, 108, 'La$_{0.7}$Pb$_{0.3}$MnO$_3$\nT = 10 K',
        ha='left', va='top', fontsize=11, zorder=7,
        bbox=dict(fc='white', ec='k', pad=4.5))

fig.subplots_adjust(left=0.11, right=0.98, bottom=0.12, top=0.85)
save_fig(fig, 'ch6', 'fig6_18')
