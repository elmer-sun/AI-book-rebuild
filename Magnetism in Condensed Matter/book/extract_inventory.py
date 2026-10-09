# -*- coding: utf-8 -*-
"""盘点全书 figure 环境：图号、中英图注、图片文件 -> fig_inventory/*.json 与 summary.md"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
os.makedirs('fig_inventory', exist_ok=True)

FILES = ['ch2', 'ch3', 'ch4', 'ch5', 'ch6', 'ch7', 'ch8',
         'appA', 'appB', 'appC', 'appD', 'appE', 'answers', 'symbols', 'preface']

summary = []
for base in FILES:
    path = base + '.tex'
    if not os.path.exists(path):
        continue
    src = open(path, encoding='utf-8').read()
    items = []
    for m in re.finditer(r'\\begin\{figure\}(.*?)\\end\{figure\}', src,
                         re.S):
        body = m.group(1)
        imgs = re.findall(r'\\includegraphics\[[^]]*\]\{([^}]+)\}', body)
        cap = re.search(r'\\caption\{(.*)\}\s*\\end\{figure\}', body, re.S)
        cap_text = cap.group(1) if cap else ''
        # 去掉嵌套括号简化处理：英文图注行
        en = re.search(r'Fig\.~?([A-E]?\d+\.\d+)', cap_text)
        fig_no = en.group(1) if en else '?'
        zh = cap_text.split('\\\\')[0]
        items.append({
            'fig_no': fig_no,
            'images': imgs,
            'zh_head': re.sub(r'\s+', '', zh)[:60],
            'env_start_line': src[:m.start()].count('\n') + 1,
        })
    n_imgs = sum(len(it['images']) for it in items)
    summary.append((base, len(items), n_imgs))
    with open('fig_inventory/%s.json' % base, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=1)

print('%-8s %5s %5s' % ('file', 'figs', 'imgs'))
for b, nf, ni in summary:
    print('%-8s %5d %5d' % (b, nf, ni))
print('TOTAL figs %d, imgs %d' % (sum(x[1] for x in summary),
                                  sum(x[2] for x in summary)))
