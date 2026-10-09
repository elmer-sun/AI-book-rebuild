# -*- coding: utf-8 -*-
"""judge 第1路修复：引号方向 / 图注前导句点 / 全角面板括号统一"""
import io
import os
import re

ROOT = r"E:\AI整理书籍\齐曼\重排本"
PARTS = os.path.join(ROOT, "chapters", "parts")
CH = os.path.join(ROOT, "chapters")

# --- 1) ch1_c 引号方向检查与修复 ---
p = os.path.join(PARTS, "ch1_c.tex")
s = io.open(p, encoding="utf-8").read()
k = s.find("的推论：")
seg = s[k:k + 6]
print("context codepoints:", [hex(ord(c)) for c in s[k + 3:k + 5]])
# 期望：开引号 U+201C。若是 U+201D 则换。
fixed = False
if s[k + 4] == "\u201d":
    s = s[:k + 4] + "\u201c" + s[k + 5:]
    fixed = True
# 句尾闭引号（之和"x）也应为 U+201D
m = re.search(r"之和(.)\n", s[k:k + 200])
if m and m.group(1) == "\u201c":
    j = k + m.start(1)
    s = s[:j] + "\u201d" + s[j + 1:]
    fixed = True
if fixed:
    io.open(p, "w", encoding="utf-8").write(s)
    print("ch1_c quotes fixed:", fixed)
else:
    print("ch1_c quotes already ok")

# --- 2) 图注前导句点（caption* 与 %FIG 标记都处理） ---
cap_pat = re.compile(r"(\\caption\*\{图 \d+\\quad)[．。]")
fig_pat = re.compile(r"(%FIG\{\d+\}:\s*)[．。](?=余|图|[^\x00-\x7f])", )
tot = 0
for d in (CH, PARTS):
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".tex"):
            continue
        p2 = os.path.join(d, fn)
        s2 = io.open(p2, encoding="utf-8").read()
        s3, n1 = cap_pat.subn(r"\1", s2)
        if n1:
            io.open(p2, "w", encoding="utf-8").write(s3)
            print("leading-period captions:", fn, n1)
            tot += n1
print("total:", tot)

# --- 3) 图注中的全角面板括号 → 半角（图 52 等） ---
full_pat = re.compile(r"(\\caption\*\{[^}]*)（([a-c])）")
n2 = 0
for fn in sorted(os.listdir(CH)):
    if not fn.endswith(".tex"):
        continue
    p3 = os.path.join(CH, fn)
    s3 = io.open(p3, encoding="utf-8").read()
    s4, k2 = full_pat.subn(lambda m: m.group(1) + "(" + m.group(2) + ")", s3)
    if k2:
        io.open(p3, "w", encoding="utf-8").write(s4)
        print("fullwidth parens:", fn, k2)
        n2 += k2
print("parens total:", n2)
