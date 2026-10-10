# -*- coding: utf-8 -*-
"""Render given pages of the source scan at 300dpi and crop the bottom
portion (where footnotes live), then upscale for readability."""
import sys, os
import pymupdf
from PIL import Image

PDF = r"E:\AI整理书籍\朗道理论物理教程\卷2场论\原书_卷2场论_高教社中文第8版.pdf"
OUT = r"E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本\_zoom\fn12"
os.makedirs(OUT, exist_ok=True)

pages = [int(a) for a in sys.argv[1:]]
doc = pymupdf.open(PDF)
zoom = 300 / 72  # 300 dpi
mat = pymupdf.Matrix(zoom, zoom)
for p in pages:
    page = doc[p - 1]
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    w, h = img.size
    # crop bottom 30% and also keep a bit of the body (anchor context)
    crop = img.crop((0, int(h * 0.68), w, h))
    crop = crop.resize((int(crop.width * 1.4), int(crop.height * 1.4)), Image.LANCZOS)
    fp = os.path.join(OUT, f"bot_p{p:03d}.png")
    crop.save(fp)
    # also save full page at 300dpi (not upscaled) for context if needed
    fp2 = os.path.join(OUT, f"full_p{p:03d}.png")
    img.save(fp2)
    print(fp, crop.size)
doc.close()
