# -*- coding: utf-8 -*-
"""检查装配后各章 includegraphics 的图片文件是否都存在。"""
import re, os
BASE = os.path.dirname(os.path.abspath(__file__)) + r'\..\重排本'
total = 0
missing = []
for n in range(1, 17):
    p = os.path.join(BASE, 'chapters', f'ch{n:02d}.tex')
    t = open(p, encoding='utf-8').read()
    pat = re.compile(r'\\includegraphics\[[^\]]*\]\{([^}]+)\}')
    figs = pat.findall(t)
    total += len(figs)
    for f in figs:
        if not os.path.exists(os.path.join(BASE, f.replace('/', os.sep))):
            missing.append((n, f))
print('assembled includegraphics total:', total)
print('missing files:', missing if missing else '无')
