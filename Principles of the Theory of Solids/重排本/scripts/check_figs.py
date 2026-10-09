# -*- coding: utf-8 -*-
# 图号审计：从装配后章节文件的 \caption*{图 N 前缀统计全书图号
import io
import os
import re
import collections

CH = r"E:\AI整理书籍\齐曼\重排本\chapters"
pat = re.compile(r"\\caption\*\{图 (\d+)")

nums = []
for fn in sorted(os.listdir(CH)):
    if not fn.endswith(".tex"):
        continue
    s = io.open(os.path.join(CH, fn), encoding="utf-8").read()
    for m in pat.finditer(s):
        nums.append((fn, int(m.group(1))))

n = [x[1] for x in nums]
print("captions:", len(n))
print("range:", min(n), "-", max(n))
dups = [k for k, v in collections.Counter(n).items() if v > 1]
print("dups:", dups or "none")
gaps = [i for i in range(min(n), max(n) + 1) if i not in n]
print("gaps:", gaps or "none")
per = collections.Counter(fn for fn, _ in nums)
print(dict(sorted(per.items())))
