# -*- coding: utf-8 -*-
"""装配器：把拆半的 chNNa/chNNb.tex 按 %JOIN% / %--TAIL-- 标记合并成 chNN.tex。
TAIL = b文件顶部到第一个 \\section 之间的内容（可含多段文字与公式）。
用法: python assemble.py
"""
import os, re

CH = os.path.dirname(os.path.abspath(__file__)) + r'\..\重排本\chapters'

def read(p):
    with open(p, encoding='utf-8') as f: return f.read()

def write(p, s):
    with open(p, 'w', encoding='utf-8', newline='\n') as f: f.write(s)

def assemble(chap):
    parts = []
    for suf in ['a', 'b', 'c', 'd']:
        p = os.path.join(CH, f'ch{chap:02d}{suf}.tex')
        if os.path.exists(p): parts.append(p)
    if not parts: return False
    merged = read(parts[0])
    for nxt in parts[1:]:
        body = read(nxt)
        # 以第一个 \section 为界切出 TAIL（其前可有头注释与 %--TAIL-- 标记）
        m = re.search(r'^\\section', body, re.M)
        tail_part, rest = (body[:m.start()], body[m.start():]) if m else (body, '')
        tl = [ln for ln in tail_part.split('\n') if not ln.lstrip().startswith('%')]
        tail = '\n'.join(tl).strip()
        if merged.rstrip().endswith('%JOIN%'):
            # 句中断：去掉标记，tail直接续接（同段），rest首行按命令/文字决定接法
            merged = merged.rstrip()[:-len('%JOIN%')].rstrip()
            if tail:
                merged = merged + tail
            rl = rest.lstrip('\n').split('\n')
            first = rl[0].strip() if rl else ''
            if not first:
                pass
            elif first.startswith('\\'):
                merged = merged + '\n\n' + first
            else:
                merged = merged + ' ' + first
            rest = '\n'.join(rl[1:]) if len(rl) > 1 else ''
        else:
            if tail:
                merged = merged.rstrip() + '\n' + tail + '\n'
        merged = merged.rstrip() + '\n\n' + rest.lstrip('\n')
    out = os.path.join(CH, f'ch{chap:02d}.tex')
    write(out, merged)
    print(f'ch{chap:02d}.tex assembled from {len(parts)} parts ({len(merged)} chars)')
    return True

if __name__ == '__main__':
    any_ = False
    for n in range(1, 17):
        any_ |= assemble(n)
    if not any_: print('no split chapters found')
