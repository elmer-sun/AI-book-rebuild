# -*- coding: utf-8 -*-
"""重绘图 3.1：二维正方布拉维人物、格子的前三个布里渊区。"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle
import numpy as np

plt.rcParams['font.family'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['axes.unicode_minus'] = False

fig, ax = plt.subplots(figsize=(8.4, 6.4))

LW = 1.0
DASH = dict(color='0.35', linestyle='--', linewidth=0.9)

# ---- 分区填充 ----
# 第一区：[-1,1]^2，斜线阴影
ax.add_patch(Rectangle((-1, -1), 2, 2, facecolor='#f2f2f2',
                       edgecolor='none', zorder=1))
ax.add_patch(Rectangle((-1, -1), 2, 2, facecolor='none', hatch='////',
                       edgecolor='0.55', linewidth=0.0, zorder=1))
# 第二区：菱形减去正方形，点状阴影（4 个三角形）
tris = [
    [(1, -1), (1, 1), (2, 0)],
    [(-1, -1), (-1, 1), (-2, 0)],
    [(-1, 1), (1, 1), (0, 2)],
    [(-1, -1), (1, -1), (0, -2)],
]
for t in tris:
    ax.add_patch(Polygon(t, closed=True, facecolor='#ffffff',
                         edgecolor='none', zorder=1.5))
    ax.add_patch(Polygon(t, closed=True, facecolor='none', hatch='...',
                         edgecolor='0.40', linewidth=0.0, zorder=1.6))
# 第三区：四个黑色角方块 [1,2]^2 及对称位置
for sx in (1, -1):
    for sy in (1, -1):
        ax.add_patch(Rectangle((min(sx, sx * 2), min(sy, sy * 2)), 1, 1,
                               facecolor='#1a1a1a', edgecolor='none', zorder=2))

# ---- 垂直/水平虚线（区界平分线）----
for x in (-3, -2, -1, 1, 2, 3):
    ax.plot([x, x], [-3.2, 3.2], **DASH, zorder=0.5)
for y in (-3, -2, -1, 1, 2, 3):
    ax.plot([-4.35, 4.35], [y, y], **DASH, zorder=0.5)
# 对角虚线 |kx±ky| = 2（长）与 = 4（短，过黑方块外角）
d = np.tan(np.pi / 4)
for c in (-2, 2):  # kx + ky = c
    xs = np.array([-3.2, 3.2])
    ax.plot(xs, c - xs, **DASH, zorder=0.5)
    ax.plot(xs, xs - c, **DASH, zorder=0.5)
for c in (-4, 4):  # 只画角附近的短段
    ax.plot([1.0, 3.2], [c - 1.0, c - 3.2], **DASH, zorder=0.5)
    ax.plot([-3.2, -1.0], [c + 3.2, c + 1.0], **DASH, zorder=0.5)
    ax.plot([1.0, 3.2], [1.0 - c, 3.2 - c], **DASH, zorder=0.5)
    ax.plot([-3.2, -1.0], [-3.2 - c, -1.0 - c], **DASH, zorder=0.5)

# ---- 倒格点 ----
pts = [(2 * m, 2 * n) for m in range(-2, 3) for n in range(-2, 3)]
skip = {(0, 0), (0, 2), (2, 0), (0, -4), (0, 4)}
for p in pts:
    if p in skip or abs(p[0]) > 4.2 or abs(p[1]) > 3.4:
        continue
    ax.plot(*p, marker='o', ms=4.5, color='0.15', zorder=3)

# ---- 箭头 ----
AW = dict(head_width=0.13, head_length=0.18, length_includes_head=True,
          linewidth=1.2, color='black', zorder=4)
ax.arrow(0, 0, 0, 1.85, **AW)
ax.arrow(0, 0, 1.85, 0, **AW)
ax.arrow(0, 2.25, 0, 0.75, **AW)
ax.arrow(4.15, 0, 0.75, 0, **AW)
ax.text(0.13, 1.55, r'$\mathbf{g}_1$', fontsize=13, zorder=5)
ax.text(1.45, 0.16, r'$\mathbf{g}_2$', fontsize=13, zorder=5)
ax.text(-0.42, 3.15, r'$k_y$', fontsize=13)
ax.text(4.35, -0.45, r'$k_x$', fontsize=13)
ax.text(-0.28, -0.30, r'$O$', fontsize=12)

ax.set_xlim(-4.7, 5.1)
ax.set_ylim(-3.6, 3.7)
ax.set_aspect('equal')
ax.axis('off')
fig.tight_layout(pad=0.3)
fig.savefig(r'E:\AI整理书籍\群论\重排本\figures\fig3_1.pdf')
fig.savefig(r'E:\AI整理书籍\群论\重排本\figures\fig3_1_preview.png', dpi=110)
print('fig3_1 done')
