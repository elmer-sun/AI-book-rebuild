# -*- coding: utf-8 -*-
import io
import os

P = r"E:\AI整理书籍\齐曼\重排本\chapters\parts"


def ctx(fn, key, before=40, after=60):
    s = io.open(os.path.join(P, fn), encoding="utf-8").read()
    k = s.find(key)
    if k < 0:
        print("== %s: NOT FOUND %r" % (fn, key))
        return
    print("== %s: ...%s..." % (fn, s[max(0, k - before):k + after].replace("\n", "\\n")))


ctx("ch5_b.tex", "如同用高频电", 20, 80)
ctx("ch5_b.tex", "晶序", 30, 60)
ctx("ch5_b.tex", "一罐", 30, 40)
ctx("ch11_c.tex", "\\AA", 30, 30)
ctx("ch11_c.tex", "A(\\mathbf{r}):", 40, 20)
ctx("ch11_b.tex", "和Schrieffer", 30, 20)
ctx("ch1_c.tex", "烦冗", 20, 20)
ctx("ch2_a.tex", "对偶力", 25, 25)
ctx("ch9_c.tex", "积分回归", 25, 30)
ctx("ch9_a.tex", "薄片", 30, 40)
ctx("ch9_a.tex", "闭合轨迹", 25, 40)
ctx("ch10_f.tex", "%JOIN%", 10, 80)
ctx("ch10_d.tex", "\\tag{10.85}", 60, 20)
