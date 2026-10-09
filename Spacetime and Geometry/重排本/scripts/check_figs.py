# -*- coding: utf-8 -*-
# 图号审计（卡罗尔本）：从装配后章节文件的 \caption*{图 N.M 前缀统计全书图号
# 章内唯一、章内连续（1.1, 1.2, ...）。
import io
import os
import re
import collections

CH = r"E:\AI整理书籍\卡罗尔\重排本\chapters"
pat = re.compile(r"\\caption\*\{图 ([A-J]?\d*\.\d+)")

nums = []
for fn in sorted(os.listdir(CH)):
    if not fn.endswith(".tex"):
        continue
    s = io.open(os.path.join(CH, fn), encoding="utf-8").read()
    for m in pat.finditer(s):
        nums.append((fn, m.group(1)))

print("captions:", len(nums))
per_ch = collections.defaultdict(list)
for fn, k in nums:
    ch = k.split(".")[0]
    per_ch[ch].append(int(k.split(".")[1]))
for ch, lst in sorted(per_ch.items()):
    n = sorted(lst)
    dups = [i for i, c in collections.Counter(n).items() if c > 1]
    gaps = [i for i in range(n[0], n[-1] + 1) if i not in n]
    print(f"  图 {ch}.x: {len(n)} 幅, range {ch}.{n[0]}-{ch}.{n[-1]}, "
          f"dups={dups or 'none'}, gaps={[f'{ch}.{g}' for g in gaps] or 'none'}")
