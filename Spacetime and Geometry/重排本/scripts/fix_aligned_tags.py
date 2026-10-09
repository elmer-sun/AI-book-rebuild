# -*- coding: utf-8 -*-
"""修复 ch8 parts 中 aligned 环境内的 \\tag（amsmath 不允许）：
把 \\tag{...} 从 aligned 内部移到其所在 equation* 的 \\end{aligned} 之后。"""
import io
import re

BASE = r"E:\AI整理书籍\卡罗尔\重排本\chapters\parts"
FILES = ["ch8_a.tex", "ch8_b.tex", "ch8_c.tex", "ch8_d.tex"]

pat = re.compile(r"(\\begin\{aligned\}.*?\\end\{aligned\})", re.S)

for fn in FILES:
    p = BASE + "\\" + fn
    s = io.open(p, encoding="utf-8").read()
    changed = 0

    def fix(m):
        global changed
        block = m.group(1)
        tags = re.findall(r"\\tag\{[^}]*\}", block)
        if not tags:
            return block
        if len(tags) > 1:
            print(f"  WARN {fn}: multiple tags in one aligned: {tags}")
        block2 = re.sub(r"\s*\\tag\{[^}]*\}", "", block)
        replacement = block2 + "\n" + " ".join(tags)
        changed += 1
        return replacement

    s2 = pat.sub(fix, s)
    if changed:
        io.open(p, "w", encoding="utf-8").write(s2)
        print(f"{fn}: fixed {changed} aligned-with-tag blocks")
    else:
        print(f"{fn}: clean")
