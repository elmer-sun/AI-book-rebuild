# -*- coding: utf-8 -*-
# 一次性修复：apply_figs 首轮运行时图注外层花括号未剥，产生
#   \caption*{图 N\quad {图 N　...}}
# 把重复的"图 N"前缀与多余花括号收敛为
#   \caption*{图 N\quad ...
# 用法：python fix_double_caption.py [ch04.tex ...]
import io
import os
import re
import sys

CH = r"E:\AI整理书籍\齐曼\重排本\chapters"
pat = re.compile(r"(\\caption\*\{)图 (\d+)\\quad \{图 \2[　\s]*")

targets = sys.argv[1:] or [f for f in os.listdir(CH) if f.endswith(".tex")]
for fn in sorted(targets):
    p = os.path.join(CH, fn)
    s = io.open(p, encoding="utf-8").read()
    s2, n = pat.subn(r"\1图 \2\\quad ", s)
    if n:
        io.open(p, "w", encoding="utf-8").write(s2)
    print(f"{fn}: fixed {n}")
