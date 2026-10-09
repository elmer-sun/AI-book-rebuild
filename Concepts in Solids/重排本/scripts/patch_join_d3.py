# -*- coding: utf-8 -*-
# ch3_D3.tex: D2-TAIL 起始加 %JOIN%（承接 D2 末句 "The lower iron-series oxides,"）
import io, re

p = r"E:\AI整理书籍\安德森\重排本\chapters\parts\ch3_D3.tex"
s = io.open(p, encoding="utf-8").read()
m = re.search(r"%--D2-TAIL--\s*\n", s)
assert m, "D2-TAIL marker missing"
if "%JOIN%" not in s:
    s = s[:m.end()] + "%JOIN%\n" + s[m.end():]
    io.open(p, "w", encoding="utf-8").write(s)
    print("JOIN added to D3 tail")
else:
    print("JOIN already present")
