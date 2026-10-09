# -*- coding: utf-8 -*-
"""Markdown 后处理：清理图片 alt 文本里残留的 \\quad 等原始命令"""
import io
import os
import re

OUT = r"E:\AI整理书籍\齐曼\markdown"
pat = re.compile(r"(!\[[^\]]*?)\\quad")

for root, dirs, files in os.walk(OUT):
    for f in files:
        if not f.endswith(".md"):
            continue
        p = os.path.join(root, f)
        s = io.open(p, encoding="utf-8").read()
        s2 = pat.sub(r"\1", s)
        if s2 != s:
            io.open(p, "w", encoding="utf-8").write(s2)
            print("fixed", p)
