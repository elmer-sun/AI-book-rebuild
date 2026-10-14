# -*- coding: utf-8 -*-
"""第三轮插图修复: fig2-2 标注重排 / fig2-10 R(ω) 移到轴上方 / fig5-4 公式标签移入圆内。"""
import io, re

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

# ---- fig_2_2: 标注位置与白底（照原书 p046 布局） ----
patch_file(A, [
    # Σ：原书位于斜线下侧紧贴，加白底防穿
    ("ctext(ax, 1.50, 1.42, r'$" + BS + "Sigma$', fontsize=10.5)",
     "ctext(ax, 1.50, 1.42, r'$" + BS + "Sigma$', fontsize=10.5,\n"
     "          bbox=dict(fc='white', ec='none', pad=1.0))"),
    # Δ 支 T 标注：移入对角线与虚线之间的空袋并加白底
    ("ctext(ax, 1.45, 1.32, r'$T$', fontsize=10)",
     "ctext(ax, 1.58, 1.31, r'$T$', fontsize=10,\n"
     "          bbox=dict(fc='white', ec='none', pad=1.0))"),
    # k_z：移出虚线（原书位于虚线上方、Σ 右下空袋）
    ("ctext(ax, 1.72, 1.24, r'$k_z$', fontsize=10)",
     "ctext(ax, 1.66, 1.37, r'$k_z$', fontsize=10,\n"
     "          bbox=dict(fc='white', ec='none', pad=1.0))"),
    # L(Σ) 加白底
    ("ctext(ax, 1.73, 1.52, r'$L$', fontsize=10)",
     "ctext(ax, 1.76, 1.55, r'$L$', fontsize=10,\n"
     "          bbox=dict(fc='white', ec='none', pad=1.0))"),
    # Z 加白底
    ("ctext(ax, 1.90, 1.18, r'$Z$', fontsize=10.5)",
     "ctext(ax, 1.88, 1.15, r'$Z$', fontsize=10.5,\n"
     "          bbox=dict(fc='white', ec='none', pad=1.0))"),
])

# ---- fig_2_10: R(ω) 移到轴上方（原书 R(ω) 写在轴上箭头旁、线之上） ----
patch_file(A, [
    ("ctext(ax, 0.47, 0, r'$R(" + BS + "omega)$', fontsize=10.5)",
     "ctext(ax, 0.47, 0.06, r'$R(" + BS + "omega)$', fontsize=10.5)"),
])

# ---- fig_5_4: k+q+K_n=k' 移入左圆内、K_n 箭头上方（原书 p163 布局） ----
patch_file(B, [
    ("ax.text(-0.86, 0.30,\n"
     "            r\"$" + BS + "boldsymbol{k+q+K}_n=" + BS + "boldsymbol{k'}$\", fontsize=9,\n"
     "            ha='left', va='center')",
     "ax.text(-0.28, 0.66,\n"
     "            r\"$" + BS + "boldsymbol{k+q+K}_n=" + BS + "boldsymbol{k'}$\", fontsize=9,\n"
     "            ha='center', va='center')")
])
