# -*- coding: utf-8 -*-
"""把 full.md 中的脚注圈码行映射到原书 PDF 页码，输出转录任务清单"""
import json, re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(BASE, 'MinerU', '原书_卷1力学_高教社中文第5版', 'full.md')
CL = os.path.join(BASE, 'MinerU', '原书_卷1力学_高教社中文第5版',
                  '0a8e72a1-add5-4c65-be64-76b5d9118b46_content_list.json')

cl = json.load(open(CL, encoding='utf-8'))
# 每个内容块(文本行)的页号：按顺序给 full.md 的源行做页号标注
# content_list 顺序即阅读顺序；把每块的 text 拆行后逐行记页
page_of_line = {}
li = 1
for item in cl:
    if item.get('type') == 'text':
        t = item.get('text', '')
        for seg in t.split('\n'):
            page_of_line[li] = item.get('page_idx', -1)
            li += 1
    elif item.get('type') == 'image':
        page_of_line[li] = item.get('page_idx', -1)
        li += 1

lines = open(MD, encoding='utf-8').read().split('\n')
out = []
for i, ln in enumerate(lines, 1):
    p = ln.find('①') if '①' in ln else min(
        (ln.find(m) for m in '②③④' if m in ln), default=-1)
    if p < 0:
        continue
    marks = ''.join(ch for ch in ln if ch in '①②③④⑤⑥⑦⑧⑨⑩')
    page = page_of_line.get(i, -1)
    ctx = ln.strip()
    if len(ctx) > 60:
        k = ln.find(marks[0])
        ctx = ln[max(0, k-40):k+20]
    out.append(f'full.md 行{i:>5}  原书PDF页 p{page+1:03d}  标记[{marks}]  …{ctx}…')

rep = os.path.join(BASE, '重排本', '脚注页码对照.txt')
open(rep, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
print('\n'.join(out[:15]))
print('...')
print('total marker lines:', len(out), '-> 脚注页码对照.txt')
