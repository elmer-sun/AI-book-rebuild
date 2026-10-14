# -*- coding: utf-8 -*-
"""生成任务单数据: 每章 节区间(OCR行号)/tag跳号明细/插图清单 -> 重排本/任务单数据.md"""
import re, io
from collections import defaultdict

lines = io.open(r'E:\AI整理书籍\李正中\MinerU\full_merged.md', encoding='utf-8').read().split('\n')
ranges = {
 'ch01': (433, 1141), 'ch02': (1142, 3226), 'ch03': (3227, 4428),
 'ch04': (4429, 6403), 'ch05': (6404, 7197), 'ch06': (7198, 9954),
 'ch07': (9955, 11123), 'ch08': (11124, 13328), 'ch09': (13329, 14461),
 'ch10': (14462, 15207), 'ch11': (15208, 18877), 'ch12': (18878, 20664),
 'appA': (20665, 20924), 'appB': (20925, 21058), 'appC': (21059, 21198),
 'appD': (21199, 21369), 'appE': (21370, 21447), 'appF': (21448, 21565),
 'appG': (21566, 21671), 'appH': (21672, 21731), 'xiti': (21732, 22264),
}
out = ["# 任务单数据（生成于 merge 后，重排代理逐项核对）", ""]
for k, (a, b) in ranges.items():
    seg = lines[a-1:b]
    tags = re.findall(r'\\tag\{([^}]+)\}', '\n'.join(seg))
    # 节标题行
    secs = [(i+a, ln.strip()) for i, ln in enumerate(seg) if re.match(r'^## ', ln)]
    # tag 跳号明细
    seq = defaultdict(list)
    for t in tags:
        m = re.match(r'^(\d+)\.(\d+)\.(\d+)$', t)
        if m:
            seq[(int(m.group(1)), int(m.group(2)))].append(int(m.group(3)))
        else:
            m2 = re.match(r'^([A-H])\.(\d+)$', t)
            if m2:
                seq[(m2.group(1), 0)].append(int(m2.group(2)))
    gaps = []
    for key in sorted(seq, key=str):
        nums = sorted(set(seq[key]))
        missing = [n for n in range(1, max(nums)+1) if n not in nums]
        if missing:
            gaps.append((key, missing))
    pat = re.compile(r'^图\s*\d+\.(\d+)')
    figs = sorted(set(int(pat.match(ln.strip()).group(1))
                  for ln in seg if pat.match(ln.strip())))
    out.append(f"## {k}  行{a}–{b}  tags={len(tags)}")
    if k.startswith('ch'):
        out.append(f"- 节标题行: " + "; ".join(f"L{n}:{s[3:20].strip()}" for n, s in secs[:40]))
    if gaps:
        out.append("- tag跳号(需对照原书页面判定 原书跳号/OCR漏检): " +
                   "; ".join(f"{key[0]}.{key[1]} 缺{missing}" for key, missing in gaps))
    if figs:
        out.append(f"- 行首图号: {figs}")
    out.append("")
io.open(r'E:\AI整理书籍\李正中\重排本\任务单数据.md', 'w', encoding='utf-8').write('\n'.join(out))
print('written, lines:', len(out))
