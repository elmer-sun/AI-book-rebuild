# -*- coding: utf-8 -*-
"""修复解答册中反斜杠塌缩：`,\\[1ex]` 类行距断行被写成 `,\\[`（单反斜杠）。
扫描 chapters/*.tex，把 (前一字符非反斜杠) 的 `\\[<数字>` 修复为 `\\\\[<数字>`。
合法的 `\\[`（display math 开括号）按体例不应出现，一并列出供人工确认。"""
import glob
import io
import re

DIR = r"E:\AI整理书籍\文小刚\习题解答\chapters"

pat = re.compile(r'(?<!\\)\\(\[[0-9][0-9.a-z]*\])')

for p in sorted(glob.glob(DIR + r"\*.tex")):
    s = io.open(p, encoding="utf-8").read()
    hits = list(pat.finditer(s))
    if not hits:
        continue
    ctx = [s[max(0, m.start()-25):m.end()+3].replace("\n", "⏎") for m in hits[:6]]
    print(p.split("\\")[-1], len(hits), "处")
    for c in ctx:
        print("   …" + c + "…")
    s2 = pat.sub(lambda m: "\\\\" + m.group(1), s)
    io.open(p, "w", encoding="utf-8").write(s2)
print("done")
