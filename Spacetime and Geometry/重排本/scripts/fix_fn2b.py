# -*- coding: utf-8 -*-
"""修复 fix_fn2.py 造成的脚注错位（\emph{Physica} 的 } 截断了捕获组）。"""
import io

f = r"E:\AI整理书籍\卡罗尔\重排本\chapters\parts\ch9_c.tex"
s = io.open(f, encoding="utf-8").read()

bad = ("\\footnote{有意思的是，关于弯曲时空中粒子产生的最早讨论正是 Schrödinger "
       "本人给出的；见 E. Schrödinger (1939), \\emph{Physica}；相关的物理例子"
       "包括早期宇宙和黑洞。 (Utrecht) 6, 899.}")
good = ("\\footnote{有意思的是，关于弯曲时空中粒子产生的最早讨论正是 Schrödinger "
        "本人给出的；见 E. Schrödinger (1939), \\emph{Physica} (Utrecht) 6, 899.}"
        "；相关的物理例子包括早期宇宙和黑洞。")
assert bad in s, "bad pattern not found"
s = s.replace(bad, good)
io.open(f, "w", encoding="utf-8").write(s)
print("footnote text restored OK")
