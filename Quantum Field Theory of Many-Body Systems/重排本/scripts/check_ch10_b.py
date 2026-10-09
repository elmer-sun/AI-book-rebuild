# -*- coding: utf-8 -*-
import io, re
t = io.open(r'E:\AI整理书籍\文小刚\重排本\chapters\parts\ch10_b.tex', encoding='utf-8').read()
print('tags:', re.findall(r'\\tag\{([0-9.]+)\}', t))
print('figs:', re.findall(r'%FIG\{([0-9.]+)\}', t))
print('equation* pairs:', t.count('\\begin{equation*}'), t.count('\\end{equation*}'))
print('align* pairs:', t.count('\\begin{align*}'), t.count('\\end{align*}'))
print('keypoints pairs:', t.count('\\begin{keypoints}'), t.count('\\end{keypoints}'))
print('sections:', re.findall(r'\\(?:sub)?section\*?\{[^}]*\}', t))
print('brace balance:', t.count('{') - t.count('}'))
body = [l for l in t.split('\n') if l.strip() and not l.strip().startswith('%')]
print('first body line:', body[0][:24])
print('last body line:', body[-1][-24:])
susp = [l[:70] for l in body if re.search(r'[A-Za-z]+ [A-Za-z]+ [A-Za-z]+ [A-Za-z]+', l)]
print('suspicious english lines:', len(susp))
for s in susp:
    print('  ', s)
