# -*- coding: utf-8 -*-
"""拼装图 3.2-3.15 题注条带用于核对坐标。"""
import os
from PIL import Image, ImageDraw

SRC = r'E:\AI整理书籍\群论\直接识别_ch3\pages'
OUT = r'E:\AI整理书籍\群论\重排本'

# (页, y0, y1, 标签)
GROUPS = {
    '_capA.png': [('p109.png', 0.50, 0.60, '3.2'), ('p109.png', 0.92, 1.00, '3.3'),
                  ('p110.png', 0.40, 0.52, '3.4'), ('p110.png', 0.88, 1.00, '3.5'),
                  ('p111.png', 0.86, 1.00, '3.6')],
    '_capB.png': [('p113.png', 0.38, 0.56, '3.7'), ('p116.png', 0.36, 0.60, '3.8')],
    '_capC.png': [('p117.png', 0.50, 0.62, '3.9'), ('p119.png', 0.68, 0.85, '3.10'),
                  ('p120.png', 0.55, 0.80, '3.11?')],
    '_capD.png': [('p121.png', 0.60, 0.85, '3.12?'), ('p122.png', 0.55, 0.85, '3.13?'),
                  ('p123.png', 0.50, 0.90, '3.14/15?')],
}

cache = {}
def page(p):
    if p not in cache:
        cache[p] = Image.open(os.path.join(SRC, p))
    return cache[p]

for out, items in GROUPS.items():
    tiles = []
    for pg, y0, y1, lab in items:
        im = page(pg)
        W, H = im.size
        t = im.crop((int(0.03*W), int(y0*H), int(0.97*W), int(y1*H)))
        scale = min(1500 / t.width, 2.2)
        t = t.resize((int(t.width*scale), int(t.height*scale)), Image.LANCZOS)
        bar = Image.new('RGB', (t.width, 30), 'white')
        ImageDraw.Draw(bar).text((8, 6), '== %s (%s) ==' % (lab, pg), fill='red')
        c = Image.new('RGB', (t.width, t.height + 30), 'white')
        c.paste(bar, (0, 0)); c.paste(t, (0, 30))
        tiles.append(c)
    W = max(t.width for t in tiles)
    H = sum(t.height for t in tiles) + 10*len(tiles)
    sheet = Image.new('RGB', (W, H), 'white')
    y = 0
    for t in tiles:
        sheet.paste(t, (0, y)); y += t.height + 10
    sheet.save(os.path.join(OUT, out))
    print(out, sheet.size)
