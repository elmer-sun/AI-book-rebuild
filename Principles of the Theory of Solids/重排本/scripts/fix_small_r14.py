# -*- coding: utf-8 -*-
"""小修：图196图注句号 + 前言/文献目录页眉标记"""
import io

# 1) 图 196 图注补句号
p = r"E:\AI整理书籍\齐曼\重排本\chapters\parts\ch10_f.tex"
s = io.open(p, encoding="utf-8").read()
old = "%FIG{196}: 反铁磁系统的量子化轴\n"
if old in s:
    s = s.replace(old, "%FIG{196}: 反铁磁系统的量子化轴。\n")
    io.open(p, "w", encoding="utf-8").write(s)
    print("fig196 caption: ok")

# 2) markboth
for fn, titles in [
    (r"E:\AI整理书籍\齐曼\重排本\chapters\ch12_bib.tex", ["文献目录"]),
    (r"E:\AI整理书籍\齐曼\重排本\chapters\ch00_preface.tex",
     ["前言", "第二版前言"]),
]:
    s = io.open(fn, encoding="utf-8").read()
    changed = False
    for t in titles:
        anchor = "\\chapter*{%s}" % t
        if anchor in s and ("\\markboth{%s}" % t) not in s:
            s = s.replace(anchor, anchor + "\n\\markboth{%s}{}" % t, 1)
            changed = True
    if changed:
        io.open(fn, "w", encoding="utf-8").write(s)
    print(fn.split("\\")[-1], "markboth:", "ok" if changed else "skip")
