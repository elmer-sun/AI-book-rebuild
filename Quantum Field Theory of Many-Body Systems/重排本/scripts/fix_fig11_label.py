# -*- coding: utf-8 -*-
"""把 draw_figs_ch1ch2.py 中 fig_1_1 的标签修正为 matplotlib 可渲染的 $\\eta$（单反斜杠）。"""
import io

p = r"E:\AI整理书籍\文小刚\重排本\scripts\draw_figs_ch1ch2.py"
s = io.open(p, encoding="utf-8").read()
bad = "$" + "\\" + "\\" + "eta$?"          # 当前文件里的 $\\eta$?（双反斜杠）
good = "$" + "\\" + "eta$?"                # 目标 $\eta$?（单反斜杠）
assert bad in s, "未找到双反斜杠形态: " + repr(bad)
s = s.replace(bad, good, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("fixed ->", good)
