# -*- coding: utf-8 -*-
"""把文小刚原书三段扫描 PDF 渲染为 200dpi 灰度 PNG + 逐页导出 OCR 文字层。

三段 origin.pdf 连续覆盖全书 520 个 PDF 页：
  段1 dd48f8fb (200页) -> 全局 p001-p200  (书页 N = p(N+15)，封面起 15 页前置)
  段2 34e20b03 (200页) -> 全局 p201-p400  (局部页 P -> 全局 P+200)
  段3 0239bca3 (120页) -> 全局 p401-p520  (局部页 P -> 全局 P+400)
三段的偏移恰好使全书统一满足：书页 N = pages/p(N+15).png = text/p(N+15).txt
（书页 1 -> p016；书页 505 -> p520；p001-p015 为前置部分）。

输出：文小刚/原书转换/pages/pNNN.png + 文小刚/原书转换/text/pNNN.txt
"""
import glob
import os

import fitz

BOOK = r"E:\AI整理书籍\文小刚"
OUT_IMG = os.path.join(BOOK, "原书转换", "pages")
OUT_TXT = os.path.join(BOOK, "原书转换", "text")

# (glob 片段, 全局起始页号)
PARTS = [
    ("*24be44ee", 1),    # 段1: 全局 p001-p200
    ("*595510ad", 201),  # 段2: 全局 p201-p400
    ("*b5f26360", 401),  # 段3: 全局 p401-p520
]


def main():
    os.makedirs(OUT_IMG, exist_ok=True)
    os.makedirs(OUT_TXT, exist_ok=True)
    zoom = 200 / 72.0
    mat = fitz.Matrix(zoom, zoom)
    done = 0
    for pat, g0 in PARTS:
        pdf = glob.glob(os.path.join(BOOK, pat, "*_origin.pdf"))[0]
        doc = fitz.open(pdf)
        for i, page in enumerate(doc):
            g = g0 + i
            dest = os.path.join(OUT_IMG, f"p{g:03d}.png")
            if not os.path.exists(dest):
                pix = page.get_pixmap(matrix=mat, colorspace=fitz.csGRAY)
                pix.save(dest)
                done += 1
            destt = os.path.join(OUT_TXT, f"p{g:03d}.txt")
            if not os.path.exists(destt):
                t = page.get_text("text")
                with open(destt, "w", encoding="utf-8") as f:
                    f.write(t)
        print(f"{pat}: {len(doc)} pages -> global p{g0:03d}-p{g0+len(doc)-1:03d}")
    print(f"done, {done} newly rendered -> {OUT_IMG}")


if __name__ == "__main__":
    main()
