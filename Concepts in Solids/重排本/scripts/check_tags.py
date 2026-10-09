# -*- coding: utf-8 -*-
# 公式编号审计：\tag 序列 + “式 (N)” 引用闭环
import io, os, re, sys, collections

BASE = r"E:\AI整理书籍\安德森\重排本\chapters"

files = [f for f in os.listdir(BASE) if re.match(r"ch0\d+\.tex$", f)]
tags = {}      # file -> [(N, line)]
refs = {}      # file -> [(N, line)]
tag_pat = re.compile(r"\\tag\{(\d+[a-z']?)\}")
ref_pat = re.compile(r"式\s*\((\d+[a-z']?)\)")

for fn in sorted(files):
    s = io.open(os.path.join(BASE, fn), encoding="utf-8").read()
    tags[fn] = [(m.group(1), i) for i, l in enumerate(s.split("\n"), 1)
                for m in [tag_pat.search(l)] if m]
    refs[fn] = [(m.group(1), i) for i, l in enumerate(s.split("\n"), 1)
                for m in [ref_pat.search(l)] if m]

for fn in sorted(files):
    tl = [t for t, _ in tags[fn]]
    print(f"{fn}: tags={tl}")
    # 引用闭环：本文件引用的编号应在本文件或同章相邻文件有 tag（章内编号可能跨文件）
print()
all_tags = collections.Counter(t for fn in files for t, _ in tags[fn])
dups = {t: c for t, c in all_tags.items() if c > 1}
print("duplicated tag numbers across book (原书编号可跨章重复，第2章内部 (1)-(9) 与第3章 (1)-(10) 各自成序列):")
print(dict(dups))
# 引用无 tag 的（只报告，人工判断是否原书悬空引用）
all_tag_set = set(all_tags)
print("\n引用了但无对应 tag 的编号:")
for fn in sorted(files):
    for t, ln in refs[fn]:
        if t not in all_tag_set:
            print(f"  {fn}:{ln+1} 式 ({t}) 无 tag")
