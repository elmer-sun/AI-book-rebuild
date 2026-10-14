# -*- coding: utf-8 -*-
"""卷9 OCR 产物质量验收：tag 覆盖、节完整性、块边界连续性、噪声扫描"""
import re
from collections import Counter

md = open('MinerU/full_merged.md', encoding='utf-8').read()
lines = md.split('\n')

# 1) tag 总数与节覆盖
tags = re.findall(re.escape(chr(92)) + r'tag\{([0-9a-zA-Z.]+)\}', md)
nums = []
for t in tags:
    m = re.match(r'(\d+)\.(\d+[a-z]?)', t)
    if m:
        nums.append((int(m.group(1)), m.group(2)))
c = Counter(n for n, _ in nums)
print('total tags:', len(tags), ' unique:', len(nums))
print('sections spanned by tags:', min(c), '-', max(c), ' count:', len(c))
zero = [s for s in range(1, 92) if s not in c]
print('sections with no tagged formula:', zero)

# 2) 节标题完整性（## §N）
secs = sorted(set(int(s) for s in re.findall(r'^#{1,3}\s*§\s*(\d+)', md, re.M)))
print('sections with headers:', len(secs), ' missing:', [i for i in range(1, 92) if i not in secs])

# 3) 章标题完整性（正文 ## 第N章）
chs = re.findall(r'^#{1,3}\s*(第[一二三四五六七八九十]+章[^…]*)$', md, re.M)
print('body chapter headers:', len(chs))
for x in chs:
    print('  ', x.strip()[:40])

# 4) 块边界连续性：p160/161、p320/321 前后各 2 行
def show_around(page_lines, label):
    print('---', label)
    for ln in page_lines:
        print('   ', ln.strip()[:60] or '(blank)')

# content_list 页锚定：直接按 merged 行号找块边界不好定位，改抽查文本连续性
# 第一章 §1 起始（p013 附近应有 "§1 费米型量子液体的元激发"）
i1 = md.find('费米型量子液体的元激发')
print('--- §1 header context:')
print('   ', md[i1-60:i1+30].replace('\n', ' | ')[:150])

# 5) OCR 噪声扫描
for pat in ['第章', '相対', 'ぁ', 'ぃ', 'ぅ', 'ǹ', '᷈', 'Ώ']:
    n = md.count(pat)
    if n:
        print('noise', repr(pat), n)
print('mathtt artifacts:', md.count('mathtt'), ' mathbf pmb:', md.count('pmb'))
print('日文汉字風 check 風:', md.count('風'), ' 対:', md.count('対'), ' 巣:', md.count('巣'))
