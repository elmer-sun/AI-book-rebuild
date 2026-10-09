# -*- coding: utf-8 -*-
"""从第三章扫描页裁剪表 3.3 与表 3.4 的图片。"""
import os
from PIL import Image

SRC = r'E:\AI整理书籍\群论\直接识别_ch3\pages'
DST = r'E:\AI整理书籍\群论\重排本\figures'

# (输出名, 页, y0比例, y1比例)
CROPS = [
    ('c3_t33.png',     'p101.png', 0.067, 0.505),
    ('c3_t34_p1.png',  'p101.png', 0.515, 0.865),
    ('c3_t34_p2.png',  'p102.png', 0.075, 0.865),
    ('c3_t34_p3.png',  'p103.png', 0.058, 0.470),
]

cache = {}
def page(p):
    if p not in cache:
        cache[p] = Image.open(os.path.join(SRC, p))
    return cache[p]

for name, pg, y0, y1 in CROPS:
    im = page(pg)
    W, H = im.size
    box = (int(0.04 * W), int(y0 * H), int(0.96 * W), int(y1 * H))
    im.crop(box).save(os.path.join(DST, name))
    print(name, box)

# 拼接对比图供一次性目检
tiles = [Image.open(os.path.join(DST, n)) for n, _, _, _ in CROPS]
tw = max(t.width for t in tiles)
th = sum(t.height for t in tiles) + 30 * (len(tiles) - 1)
sheet = Image.new('RGB', (tw, th), 'white')
y = 0
for t in tiles:
    sheet.paste(t, (0, y))
    y += t.height + 30
sheet.thumbnail((1400, 4000))
sheet.save(os.path.join(DST, '_contact_ch3_t3334.png'))
print('contact sheet ok')
