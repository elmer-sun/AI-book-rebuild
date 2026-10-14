# -*- coding: utf-8 -*-
"""fig2-10 R(ω) 移轴下方; fig5-4 公式标签缩号贴箭头。"""
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

patch_file(A, [
    ("ctext(ax, 0.47, 0.06, r'$R(" + BS + "omega)$', fontsize=10.5)",
     "ctext(ax, 0.47, -0.065, r'$R(" + BS + "omega)$', fontsize=10.5)"),
])

patch_file(B, [
    ("ax.text(-0.22, 0.55,\n"
     "            r\"$" + BS + "boldsymbol{k+q+K}_n=" + BS + "boldsymbol{k'}$\", fontsize=8,\n"
     "            ha='center', va='center')",
     "ax.text(-0.22, 0.50,\n"
     "            r\"$" + BS + "boldsymbol{k+q+K}_n=" + BS + "boldsymbol{k'}$\", fontsize=7.5,\n"
     "            ha='center', va='center')")
])
