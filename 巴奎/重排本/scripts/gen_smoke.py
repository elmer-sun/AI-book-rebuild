# 生成单章冒烟编译文件 smoke_NN.tex（含 main.tex 同款导言区）
import sys, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
main = open(os.path.join(ROOT, 'main.tex'), encoding='utf-8').read()
pre = main[:main.index(r'\begin{document}')]
post = r'\end{document}'

for ch in sys.argv[1:]:
    files = [ch]
    # 支持一章多块：ch04 + ch04b 等
    a, b = ch[:-1], ch[-1]
    tex = os.path.join(ROOT, 'chapters', ch + '.tex')
    if not os.path.exists(tex):
        print('missing', tex)
        continue
    body = ''
    for f in files:
        p = os.path.join(ROOT, 'chapters', f + '.tex')
        if os.path.exists(p):
            body += '\\input{chapters/%s}\n' % f
    extra = ''
    if ch == 'chC_glossary':
        extra = ''  # 术语表章自带 \chapter
    out = pre + r'\begin{document}' + '\n' + body + extra + post
    smoke = os.path.join(ROOT, 'smoke_%s.tex' % ch)
    open(smoke, 'w', encoding='utf-8').write(out)
    print('wrote', smoke)
