# -*- coding: utf-8 -*-
"""fig2-2 / fig5-4 标注第二轮精调。"""
import io

BS = chr(92)

def patch_file(path, subs):
    s = io.open(path, encoding="utf-8").read()
    for old, new in subs:
        n = s.count(old)
        assert n == 1, (path, old[:60], n)
        s = s.replace(old, new)
    io.open(path, "w", encoding="utf-8").write(s)
    print(path, "patched", len(subs))

A = r"E:\AI整理书籍\李正中\重排本\scripts\draw_figs_A.py"
B = r"E:\AI整理书籍\李正中\重排本\scripts\draw_figs_B.py"

# ---- fig_2_2 精调: Σ/k_z/L/Z 依原书布局拉开 ----
patch_file(A, [
    ("ctext(ax, 1.50, 1.42, r'$" + BS + "Sigma$', fontsize=10.5,\n"
     "          bbox=dict(fc='white', ec='none', pad=1.0))",
     "ctext(ax, 1.60, 1.44, r'$" + BS + "Sigma$', fontsize=10,\n"
     "          bbox=dict(fc='white', ec='none', pad=1.0))"),
    ("ctext(ax, 1.76, 1.55, r'$L$', fontsize=10,\n"
     "          bbox=dict(fc='white', ec='none', pad=1.0))",
     "ctext(ax, 1.87, 1.68, r'$L$', fontsize=10,\n"
     "          bbox=dict(fc='white', ec='none', pad=1.0))"),
    ("ctext(ax, 1.66, 1.37, r'$k_z$', fontsize=10,\n"
     "          bbox=dict(fc='white', ec='none', pad=1.0))",
     "ctext(ax, 1.80, 1.40, r'$k_z$', fontsize=9.5,\n"
     "          bbox=dict(fc='white', ec='none', pad=1.0))"),
    ("ctext(ax, 1.88, 1.15, r'$Z$', fontsize=10.5,\n"
     "          bbox=dict(fc='white', ec='none', pad=1.0))",
     "ctext(ax, 1.82, 1.09, r'$Z$', fontsize=10.5,\n"
     "          bbox=dict(fc='white', ec='none', pad=1.0))"),
])

# ---- fig_5_4: 公式标签缩小字号、贴 K_n 箭头上方（原书布局） ----
patch_file(B, [
    ("ax.text(-0.28, 0.66,\n"
     "            r\"$" + BS + "boldsymbol{k+q+K}_n=" + BS + "boldsymbol{k'}$\", fontsize=9,\n"
     "            ha='center', va='center')",
     "ax.text(-0.22, 0.55,\n"
     "            r\"$" + BS + "boldsymbol{k+q+K}_n=" + BS + "boldsymbol{k'}$\", fontsize=8,\n"
     "            ha='center', va='center')")
])
