# -*- coding: utf-8 -*-
# 公式编号审计（卡罗尔本）：\tag 序列（章内连续 (N.M)；附录 (A.1)…）
# + "式 (N.M)" 引用闭环 + 图号序列（图 N.M 章内唯一）
import io, os, re, collections

BASE = r"E:\AI整理书籍\卡罗尔\重排本\chapters"

files = [f for f in os.listdir(BASE)
         if re.match(r"ch\d+(_appendix|_bib)?\.tex$", f)]
tag_pat = re.compile(r"\\tag\{([A-J]?\d*\.\d+[a-z]?)\}")
ref_pat = re.compile(r"式\s*\(([A-J]?\d*\.\d+[a-z]?)\)")
figdef_pat = re.compile(r"%FIG\{([A-J]?\d*\.\d+)\}")
figref_pat = re.compile(r"图\s*([A-J]?\d*\.\d+)")

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
    print(f"{fn}: tags={[t for t, _ in tags[fn]]}")
    print(f"   FIG defs={figs[fn]}")

all_tags = collections.Counter(t for fn in files for t, _ in tags[fn])
dups = {t: c for t, c in all_tags.items() if c > 1}
print("\n重复 tag（同章内不允许）：")
for t, c in sorted(dups.items()):
    ch = t.split(".")[0]
    if ch.isdigit():
        n = sum(1 for fn in files for tt, _ in tags[fn]
                if tt == t and re.match(rf"ch{ch}(?:\D|$)", fn))
    else:
        n = c
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

# 图号：章内应唯一；章内连续（1.1, 1.2, ...）
all_figs = collections.Counter(f for fn in files for f in figs[fn])
fdups = {f: c for f, c in all_figs.items() if c > 1}
print("\n重复图号：", fdups or "（无）")
per_ch = collections.defaultdict(list)
for f, c in all_figs.items():
    ch = f.split(".")[0]
    per_ch[ch].append(float(f) if ch.isdigit() else 0)
for ch, lst in sorted(per_ch.items()):
    lst = sorted(lst)
    nums = [int(x) if ch.isdigit() else 0 for x in lst]
    gaps = [n for n in range(nums[0], nums[-1] + 1) if n not in nums] \
        if ch.isdigit() else []
    print(f"  图 {ch}.x: {len(nums)} 幅，范围 {lst[0]:g}–{lst[-1]:g}，"
          f"缺号：{[f'{ch}.{g}' for g in gaps] or '（无）'}")
