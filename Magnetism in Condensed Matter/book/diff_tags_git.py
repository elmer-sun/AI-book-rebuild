# -*- coding: utf-8 -*-
"""对比 git HEAD 与工作区：每个文件消失/新增的公式 tag。"""
import subprocess

FILES = ['ch1.tex', 'ch2.tex', 'ch3.tex', 'ch4.tex', 'ch5.tex', 'ch6.tex',
         'ch7.tex', 'ch8.tex', 'appA.tex', 'appB.tex', 'appC.tex', 'appD.tex',
         'appE.tex', 'answers.tex', 'preface.tex', 'symbols.tex']

def tags(text):
    out = []
    for i, ln in enumerate(text.split('\n'), 1):
        if r'\tag{' in ln:
            t = ln[ln.find(r'\tag{') + 5:]
            t = t[:t.find('}')]
            out.append((t, i))
    return out

for f in FILES:
    try:
        old = subprocess.run(['git', 'show', f'HEAD:book/{f}'],
                             capture_output=True, text=True, encoding='utf-8').stdout
    except Exception:
        continue
    if not old:
        continue
    new = open(f, encoding='utf-8').read()
    ot = [t for t, _ in tags(old)]
    nt = [t for t, _ in tags(new)]
    gone = [t for t in ot if t not in nt]
    added = [t for t in nt if t not in ot]
    if gone or added:
        print(f'{f}: 消失={gone} 新增={added}')
print('tag diff done')
