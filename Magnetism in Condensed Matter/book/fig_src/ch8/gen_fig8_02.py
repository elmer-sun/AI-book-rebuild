# -*- coding: utf-8 -*-
"""生成 fig8_02.tex：kagomé 晶格有限片段（六边形轮廓，每边约 3 个三角形）。"""
import math

S3 = math.sqrt(3.0)

def B(i, j):                       # up-triangle base point
    return (2.0 * i + 1.0 * j, S3 * j)

tris = []                          # list of 3-vertex tuples
for i in range(-4, 5):
    for j in range(-4, 5):
        bx, by = B(i, j)
        up = ((bx, by), (bx + 1, by), (bx + 0.5, by + S3 / 2))
        dn = ((bx + 1, by), (bx + 2, by), (bx + 1.5, by - S3 / 2))
        tris.append(up)
        tris.append(dn)

# keep triangles whose centroid lies in a hexagon centred at c0
c0 = (1.0, S3 / 6.0)
R = 2.95
norm = [(1, 0), (0.5, S3 / 2), (-0.5, S3 / 2)]
sel = []
for t in tris:
    cx = sum(p[0] for p in t) / 3.0 - c0[0]
    cy = sum(p[1] for p in t) / 3.0 - c0[1]
    if all(abs(cx * nx + cy * ny) <= R for nx, ny in norm):
        sel.append(t)

# unique vertices
vid, verts = {}, []
key = lambda p: (round(p[0], 3), round(p[1], 3))
for t in sel:
    for p in t:
        if key(p) not in vid:
            vid[key(p)] = len(verts)
            verts.append(key(p))

edges = set()
for t in sel:
    a, b, c = (vid[key(p)] for p in t)
    for u, v in ((a, b), (b, c), (c, a)):
        edges.add((min(u, v), max(u, v)))

xs = [p[0] for p in verts]
ys = [p[1] for p in verts]
x0, y0 = (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0

lines = ["% 图 8.2 kagomé 晶格有限片段：corner-sharing 三角形网络",
         r"\documentclass[tikz,border=5pt]{standalone}",
         r"\usetikzlibrary{arrows.meta}",
         r"\usepackage{amsmath}",
         r"\usepackage{bm}",
         r"\usepackage{fontspec}",
         r"\setmainfont{Times New Roman}",
         r"\begin{document}",
         r"\begin{tikzpicture}[line width=0.8pt,>=Stealth]"]
for u, v in sorted(edges):
    (x1, y1), (x2, y2) = verts[u], verts[v]
    lines.append(r"  \draw[line width=0.6] (%.3f,%.3f) -- (%.3f,%.3f);"
                 % (x1 - x0, y1 - y0, x2 - x0, y2 - y0))
for (x, y) in verts:
    lines.append(r"  \fill (%.3f,%.3f) circle (0.095);" % (x - x0, y - y0))
lines += [r"\end{tikzpicture}", r"\end{document}", ""]

out = r"E:\AI整理书籍\磁学\book\fig_src\ch8\fig8_02.tex"
with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("wrote", out, "| verts", len(verts), "edges", len(edges), "tris", len(sel))
