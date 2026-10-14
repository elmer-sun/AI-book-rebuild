# -*- coding: utf-8 -*-
import io
p = r"E:\AI整理书籍\李正中\重排本\scripts\draw_figs_E.py"
s = io.open(p, encoding="utf-8").read()
old = "ax.text(0.335, 0.20, r'$1/2D$', fontsize=9, ha='left',"
new = "ax.text(0.295, 0.255, r'$1/2D$', fontsize=8.5, ha='right',"
assert s.count(old) == 1
io.open(p, "w", encoding="utf-8").write(s.replace(old, new))
print("patched")
