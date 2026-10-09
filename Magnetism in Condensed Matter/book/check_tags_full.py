# -*- coding: utf-8 -*-
"""公式保真检查：逐章对比 md 源与 tex 的 \\tag 序列；统计公式数量"""
import io, re, os

B = chr(92)
os.chdir(r'E:\AI整理书籍\磁学\book')

pairs = [
    ('ch1.tex', r'E:\AI整理书籍\磁学\上半_扫描提取\work\ch1.md'),
    ('ch2.tex', r'E:\AI整理书籍\磁学\上半_扫描提取\work\ch2.md'),
    ('ch3.tex', r'E:\AI整理书籍\磁学\上半_扫描提取\work\ch3.md'),
    ('ch4.tex', r'E:\AI整理书籍\磁学\上半_扫描提取\work\ch4.md'),
    ('ch5.tex', r'E:\AI整理书籍\磁学\上半_扫描提取\work\ch5.md'),
    ('ch6.tex', r'E:\AI整理书籍\磁学\上半_扫描提取\work\ch6.md'),
    ('ch7.tex', r'E:\AI整理书籍\磁学\上半_扫描提取\work\ch7.md'),
    ('ch8.tex', r'E:\AI整理书籍\磁学\上半_扫描提取\work\ch8a.md'),
    ('answers.tex', r'E:\AI整理书籍\磁学\上半_扫描提取\work\answers.md'),
]

def tags_of(text, pref):
    if pref == B:
        return re.findall(re.escape(B) + r'tag' + re.escape(B) + r'\{([^}]+)\}' + re.escape(B) + B, text) or \
               re.findall(re.escape(B) + B + 'tag' + re.escape(B*2) + r'\{([^}]+)\}', text)
    return []

def tex_tags(s):
    # \tag{...}
    return re.findall(B*2 + 'tag' + r'\{([^}]*)\}', s.replace(B+B, B))

def md_tags(s):
    return re.findall(B*2 + 'tag' + r'\s*\{([^}]*)\}', s)

total_md = total_tex = 0
for texf, mdf in pairs:
    t = io.open(texf, encoding='utf-8').read()
    m = io.open(mdf, encoding='utf-8').read()
    tt = tex_tags(t)
    mt = [x for x in md_tags(m)]
    # ch8 的 md 是两段拼接
    if texf == 'ch8.tex':
        m2 = io.open(mdf.replace('ch8a', 'ch8b'), encoding='utf-8').read()
        mt += md_tags(m2)
    total_md += len(mt); total_tex += len(tt)
    smt, stt = set(mt), set(tt)
    miss = [x for x in mt if x not in stt]
    extra = [x for x in tt if x not in smt]
    status = 'OK ' if not miss and not extra else 'DIFF'
    print('%s %s: md=%d tex=%d' % (status, texf, len(mt), len(tt)))
    if miss: print('   md 有而 tex 无:', miss[:12])
    if extra: print('   tex 有而 md 无:', extra[:12])
print('total: md=%d tex=%d' % (total_md, total_tex))
