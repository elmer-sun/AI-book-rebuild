# -*- coding: utf-8 -*-
"""扫描 chapters/*.tex：单个 $...$ math span 内部的全角标点（会触发缺字）。"""
import io, re, glob, os

CH = r"E:\AI整理书籍\李正中\重排本\chapters"
hits = 0
for fn in sorted(glob.glob(os.path.join(CH, "*.tex"))):
    if fn.endswith("symbols.tex"):
        continue
    lines = io.open(fn, encoding="utf-8").read().split("\n")
    for i, ln in enumerate(lines):
        if "$" not in ln:
            continue
        parts = ln.split("$")
        for j in range(1, len(parts), 2):  # 奇数段=math 内部
            seg = re.sub(r"\\text\{[^{}]*\}", "", parts[j])
            seg = re.sub(r"\\mbox\{[^{}]*\}", "", seg)
            for ch in ("，", "、", "；", "：", "（", "）"):
                if ch in seg:
                    k = seg.find(ch)
                    s = max(0, k - 30)
                    print(f"{os.path.basename(fn)}:{i+1}: ...{seg[s:k+30]}...")
                    hits += 1
                    break
print("total:", hits)
