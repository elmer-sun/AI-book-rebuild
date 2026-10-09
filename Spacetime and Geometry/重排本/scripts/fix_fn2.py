# -*- coding: utf-8 -*-
"""ch9_c 脚注2移位：挂到句中术语后，避免行尾标记脱落。"""
import io
import re

f = r"E:\AI整理书籍\卡罗尔\重排本\chapters\parts\ch9_c.tex"
s = io.open(f, encoding="utf-8").read()

pat = re.compile(
    r"这种现象被称为引力场导致的粒子产生（particle production by gravitational fields）"
    r"；相关的物理例子包括早期宇宙和黑洞。\\nobreak\\footnote\{([^}]*)\}")
m = pat.search(s)
assert m, "pattern not found"
fn = m.group(1)
new = ("这种现象被称为引力场导致的粒子产生（particle production by gravitational fields）"
       "\\footnote{" + fn + "}；相关的物理例子包括早期宇宙和黑洞。")
s = s[:m.start()] + new + s[m.end():]
io.open(f, "w", encoding="utf-8").write(s)
print("footnote moved OK")
