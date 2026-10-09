# -*- coding: utf-8 -*-
# 公式编号审计（齐曼本）：\tag 序列（章内连续 (N.M)）+ “式 (N.M)” 引用闭环 + 图号序列
import io, os, re, collections

BASE = r"E:\AI整理书籍\齐曼\重排本\chapters"

files = [f for f in os.listdir(BASE) if re.match(r"ch\d+(_bib)?\.tex$", f)]
tag_pat = re.compile(r"\\tag\{(\d+\.\d+[a-z]?)\}")
ref_pat = re.compile(r"式\s*\((\d+\.\d+[a-z]?)\)")
figdef_pat = re.compile(r"%FIG\{(\d+)\}")
figref_pat = re.compile(r"图\s*(\d+)")

tags, refs, figs, figrefs = {}, {}, {}, {}
for fn in sorted(files):
    s = io.open(os.path.join(BASE, fn), encoding="utf-8").read()
    tags[fn] = [(m.group(1), i) for i, l in enumerate(s.split("\n"), 1)
                for m in [tag_pat.search(l)] if m]
    refs[fn] = [(m.group(1), i) for i, l in enumerate(s.split("\n"), 1)
                for m in [ref_pat.search(l)] if m]
    figs[fn] = [m.group(1) for m in figdef_pat.finditer(s)]
    figrefs[fn] = [m.group(1) for m in figref_pat.finditer(s)]

for fn in sorted(files):
    print(f"{fn}: tags={[t for t,_ in tags[fn]]}")
    print(f"   FIG defs={figs[fn]}")

all_tags = collections.Counter(t for fn in files for t, _ in tags[fn])
dups = {t: c for t, c in all_tags.items() if c > 1}
print("\n重复 tag（同章内不允许）：")
for t, c in sorted(dups.items()):
    ch = t.split(".")[0]
    n = sum(1 for fn in files for tt, _ in tags[fn] if tt == t
            and re.match(rf"ch{int(ch):02d}(\D|$)", fn))
    if n > 1:
        print(f"  {t}: {n} 处在同章")

tag_set = set(all_tags)
print("\n引用了但无对应 tag 的编号（悬空引用，需人工核对原书）：")
bad = 0
for fn in sorted(files):
    for t, ln in refs[fn]:
        if t not in tag_set:
            print(f"  {fn}:{ln+1} 式 ({t}) 无 tag")
            bad += 1
if not bad:
    print("  （无）")

# 图号：全书应唯一且连续
all_figs = collections.Counter(f for fn in files for f in figs[fn])
fdups = {f: c for f, c in all_figs.items() if c > 1}
print("\n重复图号：", fdups or "（无）")
nums = sorted(int(x) for x in all_figs)
gaps = [n for n in range(nums[0], nums[-1] + 1) if n not in nums] if nums else []
print(f"图号范围 {nums[0] if nums else '-'}–{nums[-1] if nums else '-'}，缺号：{gaps or '（无）'}")
