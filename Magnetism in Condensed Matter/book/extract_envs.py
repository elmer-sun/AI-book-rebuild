# -*- coding: utf-8 -*-
"""Extract figure environments (line, images, caption) per chapter."""
import re, json, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

for ch in ['ch3','ch4','ch5','ch6','ch7','ch8','appB','appC','appD','answers']:
    path = ch + '.tex'
    if not os.path.exists(path):
        continue
    src = open(path, encoding='utf-8').read()
    lines = src.split('\n')
    envs = []
    i = 0
    while i < len(lines):
        if r'\begin{figure}' in lines[i]:
            start = i + 1
            j = i
            depth = 0
            while j < len(lines):
                depth += lines[j].count(r'\begin{figure}') - lines[j].count(r'\end{figure}')
                if depth == 0:
                    break
                j += 1
            block = '\n'.join(lines[start:j])
            imgs = re.findall(r'includegraphics\[[^]]*\]\{([^}]+)\}', block)
            cap_text = ''
            m = re.search(r'\\caption\{(.*)', block, re.S)
            if m:
                t = m.group(1)
                bal = 1
                out = []
                for c in t:
                    if c == '{':
                        bal += 1
                    elif c == '}':
                        bal -= 1
                        if bal == 0:
                            break
                    out.append(c)
                cap_text = ''.join(out)
            envs.append({'line': start + 1, 'images': imgs, 'caption': cap_text})
            i = j + 1
        else:
            i += 1
    json.dump(envs, open(f'fig_inventory/{ch}_envs.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(ch, len(envs), 'figs', sum(len(e['images']) for e in envs), 'imgs')
