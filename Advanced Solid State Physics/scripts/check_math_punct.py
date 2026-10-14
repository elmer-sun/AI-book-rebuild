# -*- coding: utf-8 -*-
"""扫描各章 tex：数学环境内部的全角标点（\text{} 内的除外）。"""
import re, glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)) + r'\..\重排本\chapters')
BEGIN = re.compile(r'\\begin\{(equation\*?|align\*?|gather\*?|cases|eqnarray\*?|split|aligned|array|multline\*?)\}')
END = re.compile(r'\\end\{(equation\*?|align\*?|gather\*?|cases|eqnarray\*?|split|aligned|array|multline\*?)\}')
BAD = re.findall
for f in sorted(glob.glob('ch[0-9][0-9].tex')):
    env = 0
    for i, ln in enumerate(open(f, encoding='utf-8'), 1):
        s = ln.rstrip('\n')
        st = s.strip()
        if st.startswith('%'):
            continue
        if BEGIN.search(st):
            env += 1
        if END.search(st):
            env -= 1
        if env > 0:
            stripped = re.sub(r'\\text\{[^}]*\}', '', st)
            stripped = re.sub(r'\\mbox\{[^}]*\}', '', stripped)
            bad = re.findall(r'[，。；：（）""'']', stripped)
            if bad:
                print(f, i, ''.join(bad), '|', st[:100])
