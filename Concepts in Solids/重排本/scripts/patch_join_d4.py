# -*- coding: utf-8 -*-
# ch3_D4.tex: D3-TAIL 起始加 %JOIN%（承接 D3 末句断点）
import io, re

p = r"E:\AI整理书籍\安德森\重排本\chapters\parts\ch3_D4.tex"
s = io.open(p, encoding="utf-8").read()
m = re.search(r"%--D3-TAIL--\s*\n", s)
assert m, "D3-TAIL marker missing"
if "%JOIN%" not in s:
    s = s[:m.end()] + "%JOIN%\n" + s[m.end():]
    io.open(p, "w", encoding="utf-8").write(s)
    print("JOIN added to D4 tail")
else:
    print("JOIN already present")
