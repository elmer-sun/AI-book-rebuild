# -*- coding: utf-8 -*-
"""建立 图N -> (原书PDF页码, MinerU裁剪图) 清单"""
import json, re, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MD = os.path.join(BASE, 'MinerU', '原书_卷1力学_高教社中文第5版', 'full.md')
CL = os.path.join(BASE, 'MinerU', '原书_卷1力学_高教社中文第5版',
                  '0a8e72a1-add5-4c65-be64-76b5d9118b46_content_list.json')
OUT = os.path.join(BASE, '重排本', 'figures_manifest.md')

cl = json.load(open(CL, encoding='utf-8'))
hash2page = {}
for item in cl:
    if item.get('type') == 'image':
        h = os.path.basename(item['img_path'].replace('\\', '/'))
        hash2page[h] = item.get('page_idx', -1)

lines = open(MD, encoding='utf-8').read().split('\n')
figs = {}   # figN -> list of (page_idx, hash)
for i, ln in enumerate(lines):
    m = re.match(r'^图\s*(\d+)\s*$', ln.strip())
    if m:
        n = int(m.group(1))
        for j in range(i - 1, max(-1, i - 15), -1):
            im = re.search(r'images/([0-9a-f]+\.jpg)', lines[j])
            if im:
                figs.setdefault(n, [])
                if (hash2page.get(im.group(1)), im.group(1)) not in figs[n]:
                    figs[n].append((hash2page.get(im.group(1), -1), im.group(1)))
                break

# 图16 caption 被 OCR 吞掉：手动补（两张裁剪图在 full.md 行2331/2333）
if 16 not in figs:
    cand = []
    for i, ln in enumerate(lines[2320:2345], start=2321):
        im = re.search(r'images/([0-9a-f]+\.jpg)', ln)
        if im:
            cand.append((hash2page.get(im.group(1), -1), im.group(1)))
    figs[16] = cand

# 特殊多面板：图14(a)(b) 检查上下文里是否有第二张图
def extra_hashes(n, lo, hi):
    got = {h for _, h in figs.get(n, [])}
    out = []
    for i in range(lo - 1, hi):
        for im in re.finditer(r'images/([0-9a-f]+\.jpg)', lines[i]):
            if im.group(1) not in got:
                out.append((hash2page.get(im.group(1), -1), im.group(1)))
    return out

rep = ['# 《力学》插图清单（图N → 原书页码 → MinerU裁剪图）', '',
       '- 原书页码 = PDF物理页（pages/p-NNN.png, 3位补零）。',
       '- MinerU裁剪图在 `MinerU/原书_卷1力学_高教社中文第5版/images/<hash>.jpg`。',
       '- 重绘目标：`重排本/figures/figN.pdf`（黑白教材风矢量图，多面板合一个文件）。',
       '']
for n in sorted(figs):
    entries = ' ; '.join(f'p{p+1:03d} {h[:12]}' for p, h in figs[n])
    rep.append(f'- 图{n:>2} → {entries}')
# 未匹配图
open(OUT, 'w', encoding='utf-8').write('\n'.join(rep) + '\n')
print('\n'.join(rep))
print('\ntotal figures:', len(figs))
