# -*- coding: utf-8 -*-
"""Crop a specific box (fractions of page) from a 300dpi render and magnify."""
import sys, os
import pymupdf
from PIL import Image

PDF = r"E:\AI整理书籍\朗道理论物理教程\卷2场论\原书_卷2场论_高教社中文第8版.pdf"
OUT = r"E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本\_zoom\fn12"
os.makedirs(OUT, exist_ok=True)

# args: page x0 y0 x1 y1 scale   (fractions 0-1)
p = int(sys.argv[1]); x0 = float(sys.argv[2]); y0 = float(sys.argv[3])
x1 = float(sys.argv[4]); y1 = float(sys.argv[5]); sc = float(sys.argv[6]) if len(sys.argv) > 6 else 2.0
doc = pymupdf.open(PDF)
pix = doc[p-1].get_pixmap(matrix=pymupdf.Matrix(300/72, 300/72))
img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
w, h = img.size
crop = img.crop((int(w*x0), int(h*y0), int(w*x1), int(h*y1)))
crop = crop.resize((int(crop.width*sc), int(crop.height*sc)), Image.LANCZOS)
fp = os.path.join(OUT, f"box_p{p:03d}_{int(y0*100)}.png")
crop.save(fp); print(fp, crop.size)
doc.close()
