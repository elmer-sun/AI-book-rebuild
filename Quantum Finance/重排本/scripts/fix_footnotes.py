# 修复"公式后悬挂脚注标记" v2：把紧跟 \end{equation*} 等环境之后的
# \footnote{...} 搬到该公式之前正文段末尾。保留 \end{...}，只删 footnote。
import re, glob, os

CH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'chapters')
EQ_END = re.compile(r'\\end\{(equation\*|align\*|gather\*|multline\*|eqnarray\*)\}')

def grab_footnote(text, start):
    i = text.index('{', start)
    depth, j = 0, i
    while j < len(text):
        if text[j] == '{':
            depth += 1
        elif text[j] == '}':
            depth -= 1
            if depth == 0:
                return text[start:j + 1], j + 1
        j += 1
    raise ValueError('unbalanced footnote')

total = 0
for f in sorted(glob.glob(os.path.join(CH, '*.tex'))):
    t = open(f, encoding='utf-8').read()
    changed = False
    while True:
        hit = None
        for em in EQ_END.finditer(t):
            k = em.end()
            while k < len(t) and t[k] in ' \t\n':
                k += 1
            if t.startswith('\\footnote{', k):
                hit = (em, k)
                break
        if not hit:
            break
        em, k = hit
        fn, fnend = grab_footnote(t, k)
        bname = em.group(1)
        bpos = t.rfind('\\begin{%s}' % bname, 0, em.start())
        j = bpos - 1
        while j >= 0 and t[j] in ' \t\n':
            j -= 1
        ins = j + 1
        # 组装: [0,ins) + fn + [ins, em.end()) + 删除[em.end(), after) + [after,)
        after = fnend
        while after < len(t) and t[after] in ' \t':
            after += 1
        if after < len(t) and t[after] == '\n':
            after += 1
        t = t[:ins] + fn + t[ins:em.end()] + t[after:]
        changed = True
        total += 1
    if changed:
        open(f, 'w', encoding='utf-8').write(t)
        print(os.path.basename(f), 'updated')
print('moved', total, 'footnotes')
