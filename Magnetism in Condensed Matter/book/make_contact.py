# -*- coding: utf-8 -*-
"""把 figs/ 下全部 figX_YY.pdf 渲染成 contact sheet 便于目检。"""
import glob
import os

import pymupdf

ROOT = r'E:\AI整理书籍\磁学\book'
figs = sorted(glob.glob(os.path.join(ROOT, 'figs', 'fig*.pdf')))
print(len(figs), 'figures')
COLS, THUMB_W = 6, 380
per_sheet = 24
os.makedirs(os.path.join(ROOT, 'contact'), exist_ok=True)
rects = []
for i, f in enumerate(figs):
    doc = pymupdf.open(f)
    pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(1.2, 1.2), alpha=False)
    rects.append((os.path.basename(f), pix))
    doc.close()

sheet_id = 0
for start in range(0, len(rects), per_sheet):
    batch = rects[start:start + per_sheet]
    rows = (len(batch) + COLS - 1) // COLS
    cell_h = 300
    sheet = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, COLS * (THUMB_W + 10), rows * (cell_h + 30)), False)
    sheet.clear_with(255)
    # 用 PIL 拼图更简单
    from PIL import Image
    import io
    canvas = Image.new('RGB', (COLS * (THUMB_W + 10), rows * (cell_h + 30)), 'white')
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(canvas)
    for j, (name, pix) in enumerate(batch):
        img = Image.open(io.BytesIO(pix.tobytes('png')))
        img.thumbnail((THUMB_W, cell_h))
        r, c = divmod(j, COLS)
        x, y = c * (THUMB_W + 10) + 5, r * (cell_h + 30) + 22
        canvas.paste(img, (x, y))
        draw.text((c * (THUMB_W + 10) + 5, r * (cell_h + 30) + 4), name, fill='red')
    out = os.path.join(ROOT, 'contact', f'sheet{sheet_id}.png')
    canvas.save(out)
    print('saved', out)
    sheet_id += 1
