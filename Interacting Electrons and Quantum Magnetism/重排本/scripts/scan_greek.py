# -*- coding: utf-8 -*-
"""扫描全部章节中残留的裸希腊字母（任何上下文），打印上下文供人工判断。"""
import glob, re

keys = 'σΘΥπδρχθφκηΣΓΩμτβζελωαγψξνΔΠΦΨΛ'
pat = re.compile('(?<!\\\\)([' + keys + '])')
for f in sorted(glob.glob('chapters/*.tex')) + ['main.tex']:
    s = open(f, encoding='utf-8').read()
    for m in pat.finditer(s):
        ctx = s[max(0, m.start() - 40):m.end() + 40].replace('\n', ' ')
        print(f, repr(m.group(0)), '::', ctx)
