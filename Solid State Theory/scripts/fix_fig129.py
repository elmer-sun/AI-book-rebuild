# -*- coding: utf-8 -*-
"""图12.9 图注孤字修复: minipage 加宽到 10cm（图仍 7cm 居中）。"""
import io
p = r"E:\AI整理书籍\李正中\重排本\chapters\ch12.tex"
s = io.open(p, encoding="utf-8").read()
old = chr(92) + "begin{minipage}{7cm}" + chr(10) + chr(92) + "centering" + chr(10) + chr(92) + "includegraphics[width=7cm]{fig12-9.pdf}"
new = chr(92) + "begin{minipage}{10cm}" + chr(10) + chr(92) + "centering" + chr(10) + chr(92) + "includegraphics[width=7cm]{fig12-9.pdf}"
assert s.count(old) == 1, s.count(old)
io.open(p, "w", encoding="utf-8").write(s.replace(old, new))
print("patched")
