# -*- coding: utf-8 -*-
"""校对修复第三轮：三处接缝/残留"""
import io
import os

P = r"E:\AI整理书籍\齐曼\重排本\chapters\parts"
n = 0


def fix(fn, old, new):
    global n
    p = os.path.join(P, fn)
    s = io.open(p, encoding="utf-8").read()
    if old in s:
        s = s.replace(old, new, 1)
        io.open(p, "w", encoding="utf-8").write(s)
        print("ok [%s]" % fn)
        n += 1
    else:
        print("MISS [%s]: %r" % (fn, old[:40]))


# ch5_b/ch5_c 接缝句重组
fix("ch5_c.tex",
    "%JOIN%对于长波长的场，我们可以写出介质的一个",
    "%JOIN%场所测得的那样——我们可以写出介质的一个")
# ch9_b/ch9_c 接缝标点
fix("ch9_c.tex",
    "%JOIN%\n其直径随",
    "%JOIN%\n，其直径随")
# (11.82) 行尾半角冒号
fix("ch11_c.tex",
    "\\mathbf{A}(\\mathbf{r}): \\tag{11.82}",
    "\\mathbf{A}(\\mathbf{r}) \\tag{11.82}")
# ch11_b Bardeen/Cooper/Schrieffer 空格
s = io.open(os.path.join(P, "ch11_b.tex"), encoding="utf-8").read()
k = s.find("Bardeen")
if k >= 0:
    print("ch11_b Bardeen ctx:", repr(s[k - 10:k + 40]))
print("TOTAL:", n)
