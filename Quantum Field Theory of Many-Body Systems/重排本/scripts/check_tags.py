# -*- coding: utf-8 -*-
# 公式编号审计（文小刚本，三级编号 N.M.K）：
#   - 装配后各章 \tag 序列 vs 蓝本基线(blueprint/_baseline.json)对比（多/少/乱序）
#   - "式 (N.M.K)" 引用闭环（悬空引用列出）
#   - 组编号 (2.3.12a) 归一化
import io
import json
import os
import re

BASE = r"E:\AI整理书籍\文小刚\重排本"
CH = os.path.join(BASE, "chapters")
BL = json.load(io.open(os.path.join(BASE, "blueprint", "_baseline.json"),
                       encoding="utf-8"))

tag_pat = re.compile(r"\\tag\{(\d+\.\d+\.\d+[a-z]?)\}")
ref_pat = re.compile(r"式\s*\((\d+\.\d+\.\d+[a-z]?)\)")

chapter_of = {}   # 文件名 -> 章号
files = []
for f in sorted(os.listdir(CH)):
    m = re.match(r"ch(\d+)(?:_bib)?\.tex$", f)
    if m:
        files.append(f)
        chapter_of[f] = int(m.group(1))


def strip_merges(seq):
    """报告用：把连续重复压缩（原文引用组）。"""
    out = []
    for t in seq:
        if not out or out[-1] != t:
            out.append(t)
    return out


tags, refs = {}, {}
for fn in files:
    s = io.open(os.path.join(CH, fn), encoding="utf-8").read()
    tags[fn] = [(m.group(1), i) for i, l in enumerate(s.split("\n"), 1)
                for m in [tag_pat.search(l)] if m]
    refs[fn] = [(m.group(1), i) for i, l in enumerate(s.split("\n"), 1)
                for m in [ref_pat.search(l)] if m]

print("== 各章 tag 数：译文 vs 蓝本基线 ==")
bad = 0
for fn in files:
    ch = "ch%02d" % chapter_of[fn]
    base = BL.get(ch, {}).get("tags", [])
    got = [t for t, _ in tags[fn]]
    n_b, n_g = len(base), len(got)
    flag = "OK" if n_b == n_g else "!!!"
    if n_b != n_g:
        bad += 1
    print(f"{fn}: {flag} 译文 {n_g} vs 基线 {n_b}")
    if n_b != n_g:
        sb, sg = set(base), set(got)
        miss = [t for t in base if t not in sg]
        extra = [t for t in got if t not in sb]
        if miss:
            print(f"    基线有而译文缺: {miss[:20]}")
        if extra:
            print(f"    译文有而基线无: {extra[:20]}")

print("\n== 顺序核对（译文 tag 出现序 vs 基线序，同章内） ==")
for fn in files:
    ch = "ch%02d" % chapter_of[fn]
    base = BL.get(ch, {}).get("tags", [])
    got = [t for t, _ in tags[fn]]
    common_base = [t for t in base]
    # 只检查"都在两边"的 tag 的相对顺序
    common = [t for t in got if t in set(base)]
    idx = {t: i for i, t in enumerate(common_base)}
    filtered = [t for t in common]
    # 稳定排序后与原顺序比较
    sorted_filtered = sorted(filtered, key=lambda t: idx[t])
    if filtered != sorted_filtered:
        first_diff = next((i for i, (a, b) in enumerate(zip(filtered, sorted_filtered)) if a != b), None)
        print(f"{fn}: 顺序异常于第 {first_diff} 个: {filtered[first_diff:first_diff+4]} vs 基线 {sorted_filtered[first_diff:first_diff+4]}")

print("\n== 悬空引用（正文引用了但全书无该 tag；跨章引用允许） ==")
all_tags = set(t for fn in files for t, _ in tags[fn])
n_ref = 0
for fn in files:
    for t, ln in refs[fn]:
        if t not in all_tags:
            print(f"  {fn}:{ln+1} 式 ({t}) 无 tag")
            n_ref += 1
if not n_ref:
    print("  （无）")

# 同章重复 tag
seen = {}
dups = []
for fn in files:
    for t, ln in tags[fn]:
        key = (chapter_of[fn], t)
        if key in seen:
            dups.append((fn, t, seen[key], ln))
        seen[key] = ln
if dups:
    print("\n== 同章重复 tag ==")
    for fn, t, l0, l1 in dups[:30]:
        print(f"  {fn}: {t} 第{l0+1}行 与 第{l1+1}行")

print("\n缺 tag 文件数:", bad)
