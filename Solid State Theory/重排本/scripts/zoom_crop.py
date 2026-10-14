# -*- coding: utf-8 -*-
"""裁剪页面 PNG 局部并放大，供插图自检。用法:
python zoom_crop.py p-111 0.05 0.30 0.95 0.62 fig4-1   (页宽高分数 l t r b)
"""
import sys, os
from PIL import Image

BASE = r"E:\AI整理书籍\李正中\原书转换\pages"
OUT = r"E:\AI整理书籍\李正中\重排本\_zoom"
os.makedirs(OUT, exist_ok=True)

page, l, t, r, b, name = sys.argv[1], *map(float, sys.argv[2:6]), sys.argv[6]
im = Image.open(os.path.join(BASE, page + '.png'))
W, H = im.size
box = (int(l * W), int(t * H), int(r * W), int(b * H))
crop = im.crop(box)
crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)
out = os.path.join(OUT, name + '.png')
crop.save(out)
print(out, crop.size)
