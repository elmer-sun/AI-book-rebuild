# -*- coding: utf-8 -*-
"""Assign actual figure numbers to each figure env (respecting setcounter)."""
import re, json, os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

for ch in ['ch3','ch4','ch5','ch6','ch7','ch8','appB','appC','appD']:
    src = open(ch + '.tex', encoding='utf-8').read()
    lines = src.split('\n')
    # find figure counter adjustments
    setcounters = {}
    for idx, ln in enumerate(lines):
        m = re.search(r'\\setcounter\{figure\}\{(\d+)\}', ln)
        if m:
            setcounters[idx] = int(m.group(1))
    envs = json.load(open(f'fig_inventory/{ch}_envs.json', encoding='utf-8'))
    # envs have 'line' = start line (1-based) pointing at line after \begin{figure}
    counter = 0
    last_idx = -1
    for e in envs:
        begin_idx = e['line'] - 2  # 0-based index of \begin{figure}
        for k in sorted(setcounters):
            if last_idx < k <= begin_idx:
                counter = setcounters[k]
                last_idx = k
        counter += 1
        e['fig_no'] = f"{ch.replace('app','').replace('ch','')}.{counter}" if 'app' not in ch else None
    # for appendices letter prefix
    if 'app' in ch:
        letter = ch[-1].upper()
        counter = 0
        last_idx = -1
        # reset: figure counter in appendix may be letter-based; recompute with letter
        for e in envs:
            begin_idx = e['line'] - 2
            for k in sorted(setcounters):
                if last_idx < k <= begin_idx:
                    counter = setcounters[k]
                    last_idx = k
            counter += 1
            e['fig_no'] = f"{letter}.{counter}"
    json.dump(envs, open(f'fig_inventory/{ch}_envs.json', 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)
    print(ch, '->', [e['fig_no'] for e in envs])
