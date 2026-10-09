# -*- coding: utf-8 -*-
import io
import os

P = r"E:\AI整理书籍\齐曼\重排本\chapters\parts"


def tail(fn, key, n=3, back=0):
    s = io.open(os.path.join(P, fn), encoding="utf-8").read()
    k = s.find(key)
    if k < 0:
        print("== %s: NOT FOUND %r" % (fn, key))
        return
    print("== %s: ...%r..." % (fn, s[max(0, k - back):k + 160]))


tail("ch5_c.tex", "%JOIN%", 3, 10)
tail("ch11_b.tex", "Cooper", 3, 60)
s = io.open(os.path.join(P, "ch11_c.tex"), encoding="utf-8").read()
k = s.find("\\tag{11.82}")
print("== ch11_c tag{11.82}:", repr(s[max(0, k - 200):k + 40]) if k >= 0 else "NF")
