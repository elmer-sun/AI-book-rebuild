# -*- coding: utf-8 -*-
"""fig11-16: 1/2D 标签移到竖箭头下段旁; ω_b/ω_c 标签避开发散线（照原书 p464）。"""
import io

BS = chr(92)
p = r"E:\AI整理书籍\李正中\重排本\scripts\draw_figs_E.py"
s = io.open(p, encoding="utf-8").read()

old1 = ("    ax.text(0.322, yb - 0.048, r'$1/2D$', fontsize=9.5, ha='left',\n"
        "            va='center')")
new1 = ("    ax.text(0.335, 0.20, r'$1/2D$', fontsize=9, ha='left',\n"
        "            va='center')")
assert s.count(old1) == 1
s = s.replace(old1, new1)

old2 = ("    for x0, lab in [(wa, r'$" + BS + "omega_{" + BS + "rm a}$'), (Dn, r'$-D$'),\n"
        "                    (wb, r'$" + BS + "omega_{" + BS + "rm b}$'), (wc, r'$" + BS + "omega_{" + BS + "rm c}$'),\n"
        "                    (Dp, r'$D$'), (wd, r'$" + BS + "omega_{" + BS + "rm d}$')]:\n"
        "        tick(ax, x0, yb, 0, -0.02)\n"
        "        ax.text(x0, yb - 0.033, lab, fontsize=9.5, ha='center', va='top')")
new2 = ("    for x0, lab, ha in [(wa, r'$" + BS + "omega_{" + BS + "rm a}$', 'center'), (Dn, r'$-D$', 'center'),\n"
        "                    (wb, r'$" + BS + "omega_{" + BS + "rm b}$', 'right'), (wc, r'$" + BS + "omega_{" + BS + "rm c}$', 'left'),\n"
        "                    (Dp, r'$D$', 'center'), (wd, r'$" + BS + "omega_{" + BS + "rm d}$', 'center')]:\n"
        "        tick(ax, x0, yb, 0, -0.02)\n"
        "        off = -0.012 if ha == 'right' else (0.012 if ha == 'left' else 0.0)\n"
        "        ax.text(x0 + off, yb - 0.033, lab, fontsize=9.5, ha=ha, va='top')")
assert s.count(old2) == 1
s = s.replace(old2, new2)

io.open(p, "w", encoding="utf-8").write(s)
print("patched fig_11_16")
