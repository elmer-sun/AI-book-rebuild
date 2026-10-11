# 核查 6 个奇数引号段落中弯引号的配对方向
import re

def check(f, key):
    txt = open(f, encoding='utf-8').read()
    paras = re.split(r'\n\s*\n', txt)
    for p in paras:
        if key in p:
            # 排除 \" 变音符
            q = [m.start() for m in re.finditer('["\u201c\u201d]', p)]
            seq = []
            for i in q:
                # 前一个字符是反斜杠 -> 变音符, 跳过
                if i > 0 and p[i - 1] == chr(92):
                    continue
                seq.append(p[i])
            s = ''.join(seq)
            # 校验交替: 必须是 "..." "..." 形式
            ok = re.fullmatch(r'(\u201c[^\u201c\u201d]*\u201d)+', s) if s else True
            print(('OK  ' if ok else 'BAD '), f.split(chr(92))[-1], key[:16], '->', s[:60])
            if not ok:
                # 逐对列出
                pos = 0
                print('   上下文:')
                for m in re.finditer('["\u201c\u201d]', p):
                    i = m.start()
                    if i > 0 and p[i - 1] == chr(92):
                        continue
                    print('   ...', p[max(0, i - 18):i + 18].replace(chr(10), ' '))
            return

check('chapters/ch04.tex', '方法论的转折点')
check('chapters/ch04.tex', '本节对应原书4.1节')
check('chapters/ch04.tex', '第一步：常数波动率')
check('chapters/ch04.tex', '第三步：随机波动率')
check('chapters/ch04b.tex', '薛定谔方程与能量本征态')
check('chapters/chC_glossary.tex', 'Greeks')
