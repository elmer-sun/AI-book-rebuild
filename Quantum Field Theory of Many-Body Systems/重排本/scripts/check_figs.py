# -*- coding: utf-8 -*-
# 图号审计（文小刚本，图号 N.M 含点号）：
#   - %FIG{N.M} 定义序列 vs 蓝本基线的 Fig 引用集（缺号/多号）
#   - 正文 "图 N.M" 引用闭环
import io
import json
import os
import re

BASE = r"E:\AI整理书籍\文小刚\重排本"
CH = os.path.join(BASE, "chapters")
BL = json.load(io.open(os.path.join(BASE, "blueprint", "_baseline.json"),
                       encoding="utf-8"))

figdef_pat = re.compile(r"%FIG\{(\d+\.\d+)\}")
figref_pat = re.compile(r"图\s*(\d+\.\d+)")

chapter_of = {}
files = []
for f in sorted(os.listdir(CH)):
    m = re.match(r"ch(\d+)(?:_bib)?\.tex$", f)
    if m:
        files.append(f)
        chapter_of[f] = int(m.group(1))

defs, refs = {}, {}
for fn in files:
    s = io.open(os.path.join(CH, fn), encoding="utf-8").read()
    defs[fn] = [m.group(1) for m in figdef_pat.finditer(s)]
    refs[fn] = [m.group(1) for m in figref_pat.finditer(s)]

print("== 各章 %FIG 定义 vs 蓝本 Fig 引用基线 ==")
for fn in files:
    ch = "ch%02d" % chapter_of[fn]
    base = set(BL.get(ch, {}).get("fig_refs", []))
    got = set(defs[fn])
    # 基线里可能混入跨章引用(如 ch4 文中引 Fig 6.5)，按章号过滤
    base = {b for b in base if b.startswith(f"{chapter_of[fn]}.")}
    missing = sorted(base - got, key=lambda x: float(x))
    extra = sorted(got - base, key=lambda x: float(x))
    status = "OK" if not missing else "缺:"
    print(f"{fn}: 定义 {len(got)} 幅 {status} {missing or ''}"
          f"{'  基线无而译文有:' + str(extra) if extra else ''}")

print("\n== 图号重复 ==")
seen = {}
dups = []
for fn in files:
    for k in defs[fn]:
        if k in seen:
            dups.append((k, seen[k], fn))
        seen[k] = fn
print(dups or "（无）")

print("\n== 悬空图引用（正文提『图 N.M』但无 %FIG 定义；跨章引用允许） ==")
all_defs = set(k for fn in files for k in defs[fn])
n = 0
for fn in files:
    for r in refs[fn]:
        if r not in all_defs:
            print(f"  {fn}: 图 {r} 无定义")
            n += 1
print("（无）" if not n else f"共 {n} 处")
