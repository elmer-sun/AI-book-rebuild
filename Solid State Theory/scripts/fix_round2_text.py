# -*- coding: utf-8 -*-
"""第二轮验收修复: 行首标点 3 处 + 表6.2 原子块。"""
import io

BS = chr(92)
CH = r"E:\AI整理书籍\李正中\重排本\chapters" + BS

def patch(fn, old, new):
    p = CH + fn
    s = io.open(p, encoding="utf-8").read()
    n = s.count(old)
    assert n == 1, (fn, old[:40], n)
    io.open(p, "w", encoding="utf-8").write(s.replace(old, new))
    print(fn, "patched")

patch("ch03.tex",
      "\\approx10^2" + BS + "mathrm{T}$" + chr(10) + "，因此由式(3.5.36)",
      "\\approx10^2" + BS + "mathrm{T}$，因此由式(3.5.36)")

patch("ch04.tex", "（即多体效应）.因此", "（即多体效应）" + BS + "nobreak.因此")

patch("ch05.tex", "（virtual phonon）.由于", "（virtual phonon）" + BS + "nobreak.由于")

patch("ch06.tex",
      "表 6.2" + chr(10) + chr(10) + BS + "begin{center}" + BS + "small" + chr(10) + BS + "begin{tabular}{lcccc}",
      BS + "begin{center}" + chr(10) + BS + "begin{minipage}{10.5cm}" + BS + "centering" + BS + "small" + chr(10)
      + "表 6.2" + BS + BS + "[0.5em]" + chr(10) + BS + "begin{tabular}{lcccc}")

patch("ch06.tex",
      BS + "end{tabular}" + chr(10) + BS + "end{center}" + chr(10) + chr(10) + "为了将在§8中讨论方便起见",
      BS + "end{tabular}" + chr(10) + BS + "end{minipage}" + chr(10) + BS + "end{center}" + chr(10) + chr(10) + "为了将在§8中讨论方便起见")
