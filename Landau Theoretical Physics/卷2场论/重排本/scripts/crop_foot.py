# -*- coding: utf-8 -*-
"""Crop bottom portion of page PNGs and upscale for footnote reading."""
import sys, os
from PIL import Image

SRC = r"E:\AI整理书籍\朗道理论物理教程\卷2场论\原书转换\pages"
DST = r"E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本\_zoom"
os.makedirs(DST, exist_ok=True)

frac = float(sys.argv[1]) if len(sys.argv) > 1 else 0.26
scale = int(sys.argv[2]) if len(sys.argv) > 2 else 2
pages = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else []

for n in pages:
    p = os.path.join(SRC, "p-%03d.png" % n)
    im = Image.open(p)
    w, h = im.size
    box = (0, int(h * (1 - frac)), w, h)
    crop = im.crop(box)
    crop = crop.resize((crop.width * scale, crop.height * scale), Image.LANCZOS)
    out = os.path.join(DST, "fn_p-%03d.png" % n)
    crop.save(out)
    print(out, crop.size)
