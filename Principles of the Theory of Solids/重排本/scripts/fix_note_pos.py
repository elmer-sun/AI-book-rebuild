# -*- coding: utf-8 -*-
"""把误插进 equation* 内部的两条译注移到环境之后"""
import io
import os
import re

P = r"E:\AI整理书籍\齐曼\重排本\chapters\parts"

for fn in ("ch7_a.tex", "ch7_b.tex", "ch7_c.tex", "ch7_d.tex", "ch7_e.tex"):
    p = os.path.join(P, fn)
    s = io.open(p, encoding="utf-8").read()
    orig = s
    # 模式：equation* 环境内部的“（译注：…）”整段搬到 \end{equation*} 之后
    pat = re.compile(
        r"（译注：（按式 \(7\.(?:78|39)\）[^）]*）。）(%)([^%]*?)\\end\{equation\*\}",
        re.S)
    def repl(m):
        note, percent, rest = m.group(1), m.group(2), m.group(3)
        # percent 段是环境内部剩余内容（含 \tag 行），还原到原位
        return percent + rest + "\\end{equation*}\n" + note
    s2 = pat.sub(repl, s)
    if s2 != s:
        io.open(p, "w", encoding="utf-8").write(s2)
        print("fixed", fn)
print("done")
