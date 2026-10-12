# -*- coding: utf-8 -*-
"""Crop the footnote region (bottom part) of pages300 pages for transcription.
Usage: python crop_fn.py 088 [089 ...]  -> writes 重排本/_zoom/fn_pNNN.png
Optional env FN_TOP=0.68 (fraction of height where crop starts)."""
import sys, os
from PIL import Image
base = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '原书转换', 'pages300')
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '_zoom')
os.makedirs(out, exist_ok=True)
top = float(os.environ.get('FN_TOP', '0.66'))
for num in sys.argv[1:]:
    num = num.zfill(3)
    p = os.path.join(base, f'p-{num}.png')
    im = Image.open(p)
    w, h = im.size
    box = (0, int(h*top), w, h)
    im.crop(box).save(os.path.join(out, f'fn_p{num}.png'))
    print(f'fn_p{num}.png', box)
