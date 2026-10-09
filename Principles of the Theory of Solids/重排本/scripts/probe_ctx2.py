# -*- coding: utf-8 -*-
import io
import os

P = r"E:\AI整理书籍\齐曼\重排本\chapters\parts"


def tail(fn, key, n=3):
    s = io.open(os.path.join(P, fn), encoding="utf-8").read()
    k = s.find(key)
    if k < 0:
        print("== %s: NOT FOUND %r" % (fn, key))
        return
    print("== %s: ...%r..." % (fn, s[k:k + 160]))


tail("ch5_b.tex", "如同用长波长的高频电")
tail("ch9_c.tex", "%JOIN%", 120)
tail("ch11_b.tex", "Schrieffer")
s = io.open(os.path.join(P, "ch11_c.tex"), encoding="utf-8").read()
k = s.find("(11.82)")
print("== ch11_c (11.82) ctx:", repr(s[k:k + 260]) if k >= 0 else "NOT FOUND")
