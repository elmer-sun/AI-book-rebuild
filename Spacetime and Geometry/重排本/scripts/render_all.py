# -*- coding: utf-8 -*-
"""把 main.pdf 全部页面渲染为 PNG 供 judge 视觉验收。
输出：重排本/render/pNNN.png（150dpi 彩色）。"""
import os
import fitz

BASE = r"E:\AI整理书籍\卡罗尔\重排本"
SRC = os.path.join(BASE, "main.pdf")
OUT = os.path.join(BASE, "render")

def main():
    os.makedirs(OUT, exist_ok=True)
    doc = fitz.open(SRC)
    n = 0
    for i, page in enumerate(doc, start=1):
        dest = os.path.join(OUT, f"p{i:03d}.png")
        if os.path.exists(dest):
            continue
        pix = page.get_pixmap(dpi=150)
        pix.save(dest)
        n += 1
        if i % 50 == 0:
            print(f"rendered {i}/{len(doc)}")
    print(f"done: {n} new, total {len(doc)} pages -> {OUT}")

if __name__ == "__main__":
    main()
