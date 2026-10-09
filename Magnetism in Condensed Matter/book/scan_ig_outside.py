# -*- coding: utf-8 -*-
"""找 figure 环境之外的 includegraphics（嫌疑：公式被排成图）。"""
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
for f in ['main.tex', 'preface.tex', 'ch1.tex', 'ch2.tex', 'ch3.tex', 'ch4.tex',
          'ch5.tex', 'ch6.tex', 'ch7.tex', 'ch8.tex', 'appA.tex', 'appB.tex',
          'appC.tex', 'appD.tex', 'appE.tex', 'answers.tex', 'symbols.tex']:
    if not os.path.exists(f):
        continue
    lines = open(f, encoding='utf-8').read().split('\n')
    depth_fig = 0
    depth_eq = 0
    for i, ln in enumerate(lines, 1):
        if 'begin{figure}' in ln:
            depth_fig += 1
        elif 'end{figure}' in ln:
            depth_fig -= 1
        if depth_fig == 0 and 'includegraphics' in ln:
            print(f'{f}:{i}: {ln.strip()[:100]}')
print('scan done')
