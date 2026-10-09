# -*- coding: utf-8 -*-
"""把各章 figure 环境里的 hash JPG 引用替换为重绘的 figX_YY.pdf。
- ch2 只替换三幅遗留（2.1/2.2/2.13，按 hash 映射）；
- 其余章每个 figure 环境的所有 includegraphics 行换成单行 figX_MM.pdf，
  宽度沿用该环境第一条 includegraphics 的宽度；
- 已是新 PDF 引用的环境自动跳过。
"""
import json
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CH2_MAP = {
    '3b4fd7781eb572263e195a6cff6a1ac80b6b5524ec4e445bfeec4232e7524ca7.jpg': 'fig2_01.pdf',
    '58d1dd8440ea31a11cf17ad255f81c4aa1897e02eb878bf90dfecd58c0696ee8.jpg': 'fig2_02.pdf',
    '9128968566efea324abc782d58775c0243b606a4fe6cf00bc979099d3fe': 'fig2_13.pdf',  # 前缀
}

for ch in ['appB', 'appC', 'appD']:
    envs = json.load(open(f'fig_inventory/{ch}_envs.json', encoding='utf-8'))
    lines = open(ch + '.tex', encoding='utf-8').read().split('\n')
    # 找出各 figure 环境的行区间（0-based，含 begin/end）
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
    assert len(spans) == len(envs), f'{ch}: {len(spans)} envs vs {len(envs)} envs json'
    n_swapped = 0
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
        n_swapped += 1
    out = '\n'.join(x for x in lines if x is not None)
    open(ch + '.tex', 'w', encoding='utf-8').write(out)
    print(ch, 'swapped', n_swapped)

# ch2：只替换三幅遗留（按 hash 映射）
lines = open('ch2.tex', encoding='utf-8').read().split('\n')
n = 0
for k, ln in enumerate(lines):
    if 'includegraphics' not in ln:
        continue
    for h, tgt in list(CH2_MAP.items()):
        if h[:8] in ln:
            lines[k] = re.sub(r'\{[^}]+\.jpg\}', '{' + tgt + '}', ln)
            n += 1
open('ch2.tex', 'w', encoding='utf-8').write('\n'.join(lines))
print('ch2 swapped', n)
print('done')
