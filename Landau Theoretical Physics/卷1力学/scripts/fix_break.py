# -*- coding: utf-8 -*-
"""修复 wrap_figs.py 写入的 \\[0.3em]（误为显示数学）→ \\\\[0.3em]（换行+间距）"""
import glob, os

os.chdir(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      '重排本', 'chapters'))
bad = '\\[0.3em]'
good = '\\\\[0.3em]'
for f in sorted(glob.glob('ch0*.tex')):
    s = open(f, encoding='utf-8').read()
    n = s.count(bad)
    if n:
        s = s.replace(bad, good)
        open(f, 'w', encoding='utf-8').write(s)
    print(f, n)
