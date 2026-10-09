# -*- coding: utf-8 -*-
"""安全删除图注英文行（v2）：
逐 figure 环境处理；在 \\caption{...} 内定位最后一个 {\\footnotesize...} 组，
用括号配平找到其结束位置，连同其前的 \\\\ 一起删除。
带完整性断言：环境数不变、无 itshape Fig 残留、每组删除后括号配平。
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)

FILES = ['ch1', 'ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8',
         'appB', 'appC', 'appD']

BEGIN = '\\begin{figure}'
END = '\\end{figure}'


def match_brace(s, i):
    """s[i] == '{'，返回与之配平的 '}' 位置（跳过反斜杠转义）"""
    assert s[i] == '{'
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
    raise ValueError('unbalanced brace')


total_env = 0
total_removed = 0
for base in FILES:
    path = base + '.tex'
    if not os.path.exists(path):
        continue
    s = open(path, encoding='utf-8').read()
    n_env = s.count(BEGIN)
    removed = 0
    out = []
    pos = 0
    while True:
        a = s.find(BEGIN, pos)
        if a < 0:
            out.append(s[pos:])
            break
        b = s.find(END, a)
        assert b > 0
        block = s[a:b]
        # caption 起点
        cm = re.search(r'\\caption\{', block)
        if cm:
            cap_open = cm.end() - 1
            cap_close = match_brace(block, cap_open)
            cap = block[cap_open:cap_close + 1]
            # 定位英文组：最后一个 {\\footnotesize
            k = cap.rfind('{\\footnotesize')
            if k > 0 and re.match(r'\\footnotesize\s*\\itshape\s*Fig\.',
                                  cap[k + 1:]):
                g_end = match_brace(cap, k)
                # 组前应有 \\（换行命令），连同其后的空白一起删
                before = cap[:k]
                m = re.search(r'\\\\(?:\[[^\]]*\])?\s*$', before)
                if m:
                    removed_span = cap[m.start():g_end + 1]
                    new_cap = (before[:m.start()] + cap[g_end + 1:])
                    block = block[:cap_open] + new_cap + block[cap_close + 1:]
                    removed += 1
                    # 完整性检查
                    assert block.count(BEGIN) == 1
                    assert match_brace(block, cap_open) is not None
        out.append(s[pos:a] + block)
        pos = b
    s2 = ''.join(out)
    assert s2.count(BEGIN) == n_env, base
    assert 'itshape Fig' not in s2, base
    if removed:
        open(path, 'w', encoding='utf-8', newline='\n').write(s2)
    print('%-6s env=%d removed=%d' % (base, n_env, removed))
    total_env += n_env
    total_removed += removed
print('TOTAL env=%d removed=%d' % (total_env, total_removed))
