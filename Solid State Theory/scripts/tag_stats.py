# -*- coding: utf-8 -*-
"""按章统计 OCR tag 数（任务合同基准）。"""
import re, io

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
tot = 0
alltags = []
for k, (a, b) in ranges.items():
    seg = '\n'.join(lines[a-1:b])
    tags = re.findall(r'\\tag\{([^}]+)\}', seg)
    tot += len(tags)
    alltags += [(k, t) for t in tags]
    seen = {}
    for t in tags:
        seen[t] = seen.get(t, 0) + 1
    dup = {t: c for t, c in seen.items() if c > 1}
    print(f"{k}: tags={len(tags)} dup={len(dup)} {list(dup)[:8]}")
print('TOTAL tags:', tot)

# 编号连续性抽查: 每(章,节)内是否从1连续
from collections import defaultdict
seq = defaultdict(list)
for k, t in alltags:
    m = re.match(r'^(\d+)\.(\d+)\.(\d+)([a-z]?)$', t)
    if m:
        seq[(k, int(m.group(1)), int(m.group(2)))].append((int(m.group(3)), m.group(4)))
gaps = []
for key, lst in sorted(seq.items()):
    nums = sorted(set(n for n, s in lst))
    expect = list(range(1, max(nums) + 1))
    if nums != expect:
        gaps.append((key, nums[:20]))
print('non-continuous (章,节) sequences:', len(gaps))
for g in gaps[:30]:
    print('  ', g)
