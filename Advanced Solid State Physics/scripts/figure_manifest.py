# -*- coding: utf-8 -*-
"""生成每章图片清单：md内联图(按出现顺序) -> content_list page_idx -> 文字层 caption 猜测。
输出 Phillips/_勘察/figmanifest_chNN.txt
"""
import os, re, json, glob
import fitz

BASE = os.path.dirname(os.path.abspath(__file__)) + r'\..'
MINERU = os.path.join(BASE, 'MinerU')
ZOOM = os.path.join(BASE, '原书转换')
OUT = os.path.join(BASE, '_勘察')
os.makedirs(OUT, exist_ok=True)

OFFSET = {}  # 章号 -> (分册名, 书页-分册页 偏移)
for n in range(1, 12):
    pass
names = sorted(os.listdir(MINERU))
for name in names:
    if not os.path.isdir(os.path.join(MINERU, name)):
        continue
    if not name.startswith('ch'):
        continue
    ch = int(name[2:4])
    md_p = os.path.join(MINERU, name, 'full.md')
    if not os.path.exists(md_p):
        continue
    md = open(md_p, encoding='utf-8').read()
    inline = re.findall(r'!\[[^\]]*\]\(images/([a-f0-9]+)\.jpg\)', md)
    # content_list: 找 image 块的 page_idx
    cl_p = glob.glob(os.path.join(MINERU, name, '*_content_list.json'))
    page_of = {}
    if cl_p:
        cl = json.load(open(cl_p[0], encoding='utf-8'))
        for blk in cl:
            if blk.get('type') == 'image':
                ip = blk.get('img_path', '')
                h = os.path.splitext(os.path.basename(ip))[0]
                page_of[h] = blk.get('page_idx', -1)
    # 文字层每页的 Fig caption 定义
    part_pdf = os.path.join(ZOOM, name + '.pdf')
    doc = fitz.open(part_pdf)
    page_txt = [p.get_text() for p in doc]
    doc.close()
    chnum = str(ch)
    lines = [f'# {name}  md内联图 {len(inline)} 个']
    for i, h in enumerate(inline):
        pidx = page_of.get(h, -1)
        cap = ''
        if 0 <= pidx < len(page_txt):
            m = re.search(r'Fig\.\s*' + re.escape(chnum) + r'\.(\d+)[\s\.]', page_txt[pidx])
            if m: cap = 'Fig ' + chnum + '.' + m.group(1)
            # 抓 caption 开头文字
            m2 = re.search(r'(A |An |The |Plot|Schematic|Sketch|Comparison)[^\n]{10,90}', page_txt[pidx])
            if m2: cap += ' | ' + m2.group(0)[:80]
        lines.append(f'{i+1:3d}. {h[:16]}...  分册页p{pidx+1:03d}  {cap}')
    open(os.path.join(OUT, f'figmanifest_ch{ch:02d}.txt'), 'w', encoding='utf-8').write('\n'.join(lines))
    print(f'ch{ch:02d}: {len(inline)} imgs -> _勘察/figmanifest_ch{ch:02d}.txt')
