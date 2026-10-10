# -*- coding: utf-8 -*-
"""Zoom helper: crop bottom fraction of a page PNG and upscale for footnote reading.
Usage: python zoom_fn.py <n> [frac] [scale]
Reads  E:\\AI整理书籍\\朗道理论物理教程\\卷2场论\\原书转换\\pages\\p-<n>.png
Writes E:\\AI整理书籍\\朗道理论物理教程\\卷2场论\\重排本\\_zoom\\fn<n>_bot.png
frac: fraction of page height to keep from the bottom (default 0.28)
scale: upscale factor (default 2)
"""
import sys
from PIL import Image

n = sys.argv[1]
frac = float(sys.argv[2]) if len(sys.argv) > 2 else 0.28
scale = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0

src = r"E:\AI整理书籍\朗道理论物理教程\卷2场论\原书转换\pages\p-{}.png".format(n)
dst = r"E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本\_zoom\fn{}_bot.png".format(n)

im = Image.open(src)
w, h = im.size
box = (0, int(h * (1 - frac)), w, h)
crop = im.crop(box)
crop = crop.resize((int(crop.width * scale), int(crop.height * scale)), Image.LANCZOS)
crop.save(dst)
print("saved", dst, crop.size)
