# 直引号 -> 中文弯引号：按段落内出现顺序交替配对（奇/开，偶/闭）
# 数学模式 $...$ 内的 " 不动；奇数引号段落报告出来人工处理
import re, glob, os, sys

CH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'chapters')

def convert_para(text):
    out, n, open_state = [], 0, True
    i = 0
    while i < len(text):
        c = text[i]
        if c == '$':
            j = text.find('$', i + 1)
            j = j if j != -1 else len(text) - 1
            out.append(text[i:j + 1])
            i = j + 1
            continue
        if c == '"':
            out.append('\u201c' if open_state else '\u201d')
            open_state = not open_state
            n += 1
        else:
            out.append(c)
        i += 1
    return ''.join(out), n, open_state

total = 0
odd_paras = []
for f in sorted(glob.glob(os.path.join(CH, '*.tex'))):
    src = open(f, encoding='utf-8').read()
    paras = re.split(r'\n\s*\n', src)
    done = []
    for p in paras:
        if '"' not in p:
            done.append(p)
            continue
        new, n, balanced = convert_para(p)
        if not balanced:
            odd_paras.append((os.path.basename(f), p[:80]))
        done.append(new)
        total += n
    open(f, 'w', encoding='utf-8').write('\n\n'.join(done))
print('converted', total, 'straight quotes')
print('odd-count paragraphs:', len(odd_paras))
for f, s in odd_paras:
    print(' ', f, '::', s.replace('\n', ' '))
