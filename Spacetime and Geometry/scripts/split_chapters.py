# -*- coding: utf-8 -*-
"""Carroll《Spacetime and Geometry》按章拆分。
书页 N = PDF 页 N+15（PDF 1-based）。输出文件名 p 范围 = 书页范围。
"""
import os
from pypdf import PdfReader, PdfWriter

SRC = r"E:\AI整理书籍\Spacetime and Geometry An Introduction to General Relativity (Sean Carroll).pdf"
OUT = r"E:\AI整理书籍\卡罗尔\章节拆分"
OFFSET = 15  # book page N -> pdf 1-based page N+15

# (文件名, 书页起, 书页止)  含端点
PARTS = [
    ("00_前言与目录_pVII-XIV", 0, 0),          # 特殊：PDF 1-15
    ("01_狭义相对论与平直时空_p001-047", 1, 47),
    ("02_流形_p048-092", 48, 92),
    ("03_曲率_p093-150", 93, 150),
    ("04_引力_p151-192", 151, 192),
    ("05_史瓦西解_p193-237", 193, 237),
    ("06_更一般的黑洞_p238-273", 238, 273),
    ("07_微扰理论与引力辐射_p274-322", 274, 322),
    ("08_宇宙学_p323-375", 323, 375),
    ("09_弯曲时空量子场论_p376-422", 376, 422),
    ("10_附录_p423-494", 423, 494),
    ("11_文献目录_p495-500", 495, 500),
    ("12_索引_p501-513", 501, 513),
]

def pdf_range(book_lo, book_hi):
    if book_lo == 0:  # 前言与目录 = PDF 1..15
        return 1, OFFSET
    return book_lo + OFFSET, book_hi + OFFSET

def main():
    os.makedirs(OUT, exist_ok=True)
    reader = PdfReader(SRC)
    total = len(reader.pages)
    print(f"source pages: {total}")
    for name, lo, hi in PARTS:
        a, b = pdf_range(lo, hi)
        w = PdfWriter()
        for i in range(a - 1, b):
            w.add_page(reader.pages[i])
        path = os.path.join(OUT, name + ".pdf")
        with open(path, "wb") as f:
            w.write(f)
        print(f"{name}.pdf  <- pdf {a}-{b}  ({b-a+1} pages)")

if __name__ == "__main__":
    main()
