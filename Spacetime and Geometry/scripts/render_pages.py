# -*- coding: utf-8 -*-
"""把 Carroll 原书渲染为 200dpi 灰度 PNG（翻译/插图代理的权威依据）。
输出：卡罗尔/原书转换/pages/pNNN.png，NNN = 原书 PDF 页号（1-based）。
书页 N 对应 p(N+15).png。"""
import os
import fitz

SRC = r"E:\AI整理书籍\卡罗尔\原书转换\Spacetime and Geometry An Introduction to General Relativity (Sean Carroll).pdf"
OUT = r"E:\AI整理书籍\卡罗尔\原书转换\pages"

def main():
    os.makedirs(OUT, exist_ok=True)
    doc = fitz.open(SRC)
    zoom = 200 / 72.0
    mat = fitz.Matrix(zoom, zoom)
    for i, page in enumerate(doc, start=1):
        dest = os.path.join(OUT, f"p{i:03d}.png")
        if os.path.exists(dest):
            continue
        pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
        pix.save(dest)
        if i % 50 == 0:
            print(f"rendered {i}/{len(doc)}")
    print(f"done: {len(doc)} pages -> {OUT}")

if __name__ == "__main__":
    main()
