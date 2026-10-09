# -*- coding: utf-8 -*-
"""修正版：每个 figure 环境的 includegraphics 统一为 fig<章><图序两位>.pdf。
fig_no 形如 '7.3' 或 'B.1' → fig7_03.pdf / figB_01.pdf。
"""
import json
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

for ch in ['ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8', 'appB', 'appC', 'appD']:
    envs = json.load(open(f'fig_inventory/{ch}_envs.json', encoding='utf-8'))
    lines = open(ch + '.tex', encoding='utf-8').read().split('\n')
    spans = []
    i = 0
    while i < len(lines):
        if r'\begin{figure}' in lines[i]:
            j, depth = i, 0
            while j < len(lines):
                depth += lines[j].count(r'\begin{figure}') - lines[j].count(r'\end{figure}')
                if depth == 0:
                    break
                j += 1
            spans.append((i, j))
            i = j + 1
        else:
            i += 1
    assert len(spans) == len(envs), f'{ch}: {len(spans)} vs {len(envs)}'
    n_fixed = 0
    for (a, b), e in zip(spans, envs):
        letter, num = e['fig_no'].split('.')
        name = f'fig{letter}_{int(num):02d}.pdf'
        igs = [(k, lines[k]) for k in range(a + 1, b) if 'includegraphics' in lines[k]]
        if not igs:
            continue
        if all(name in ln for _, ln in igs):
            continue
        width = re.search(r'includegraphics\[([^\]]*)\]', igs[0][1])
        width_opt = width.group(1) if width else 'width=0.5\\textwidth'
        first_k = igs[0][0]
        for k, _ in igs:
            lines[k] = None
        lines[first_k] = '\\includegraphics[%s]{%s}' % (width_opt, name)
        n_fixed += 1
    open(ch + '.tex', 'w', encoding='utf-8').write('\n'.join(lines))
    print(ch, 'fixed', n_fixed)
print('done')
