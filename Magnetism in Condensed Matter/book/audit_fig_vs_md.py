# -*- coding: utf-8 -*-
"""全量审计 v2：ch1/ch2 现场提取环境编号；其余用 fig_inventory JSON。"""
import json
import os
import re

WORK = r'E:\AI整理书籍\磁学\上半_扫描提取\work'
WORK2 = r'E:\AI整理书籍\磁学\下半_扫描提取\work'
BOOK = r'E:\AI整理书籍\磁学\book'

MD = {
    'ch1': ['ch1.md'], 'ch2': ['ch2.md'], 'ch3': ['ch3.md'], 'ch4': ['ch4.md'],
    'ch5': ['ch5.md'], 'ch6': ['ch6.md'], 'ch7': ['ch7.md'],
    'ch8': ['ch8a.md', 'ch8b.md'],
    'appB': ['appB.md'], 'appC': ['appC.md'], 'appD': ['appD.md'],
}

def tex_fig_nums(texfile, letter_default=None):
    """按 \begin{figure} 顺序 + setcounter 计算环境编号。"""
    src = open(texfile, encoding='utf-8').read()
    counters = []
    lines = src.split('\n')
    nums = []
    cur = 0
    prefix = letter_default
    for ln in lines:
        m = re.search(r'\\setcounter\{figure\}\{(\d+)\}', ln)
        if m:
            cur = int(m.group(1))
            continue
        if '\\begin{figure}' in ln:
            cur += 1
            nums.append(cur)
    return nums

for ch, mdf in MD.items():
    caps = set()
    for f in mdf:
        p = os.path.join(WORK, f)
        if not os.path.exists(p):
            p = os.path.join(WORK2, f)
        txt = open(p, encoding='utf-8').read()
        for m in re.finditer(r'^\s*Fig\.\s*(\d+)\.(\d+)', txt, re.M):
            caps.add(int(m.group(2)))
    texfile = os.path.join(BOOK, ch + '.tex')
    tex_nums = tex_fig_nums(texfile)
    md_nums = sorted(caps)
    only_tex = sorted(n for n in tex_nums if n not in md_nums)
    only_md = sorted(n for n in md_nums if n not in tex_nums)
    flag = '' if not only_tex and not only_md else '   <<<'
    print(f'{ch}: tex {len(tex_nums)}个: {tex_nums}')
    print(f'   md {len(md_nums)}个: {md_nums}{flag}')
    if only_tex:
        print(f'   仅tex有(嫌疑公式图!): {only_tex}')
    if only_md:
        print(f'   仅md有(缺图): {only_md}')
