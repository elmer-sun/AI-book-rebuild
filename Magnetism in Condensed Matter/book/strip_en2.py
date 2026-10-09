# -*- coding: utf-8 -*-
"""清除全部英文图注/表注行：
1) 全文范围 {\\footnotesize\\itshape Fig.|Table ...} 括号配平删除（连同其前 \\\\）
2) 中文图注内嵌的 (Fig. x.y ...) 括号英文删除
"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
FILES = ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8',
         'appB', 'appC', 'appD']


def match_brace(s, i):
    depth = 0
    j = i
    while j < len(s):
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return j
        j += 1
    raise ValueError('unbalanced')


total = 0
for base in FILES:
    path = base + '.tex'
    if not os.path.exists(path):
        continue
    s = open(path, encoding='utf-8').read()
    n0 = len(s)
    removed = 0
    # 1) 整组删除（从后往前，位置不失效）
    spans = []
    for m in re.finditer(r'\{\\footnotesize\s*\\itshape\s*(?:Fig\.|Table)',
                         s):
        k = m.start()
        try:
            g_end = match_brace(s, k)
        except ValueError:
            continue
        spans.append((k, g_end + 1))
    for k, e in reversed(spans):
        before = s[:k]
        m = re.search(r'\\\\(?:\[[^\]]*\])?\s*$', before)
        if m:
            s = before[:m.start()] + s[e:]
        else:
            s = before + s[e:]
        removed += 1
    # 2) 中文图注内嵌（Fig.~x.y ...）括号英文（全角/半角括号均可）
    pat = re.compile(r'[（(]\s*(?:Fig\.|Table)~?[^（）]*[)）]')
    s, n2 = pat.subn('', s)
    removed += n2
    if s != open(path, encoding='utf-8').read():
        open(path, 'w', encoding='utf-8', newline='\n').write(s)
    print('%-6s removed %d (组%d 括号%d), %d -> %d chars' %
          (base, removed, len(spans), n2, n0, len(s)))
    total += removed
print('TOTAL', total)
