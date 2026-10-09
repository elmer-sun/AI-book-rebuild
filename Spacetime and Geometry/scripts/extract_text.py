# -*- coding: utf-8 -*-
"""把原书 ClearScan 文字层逐页导出为 txt（英文散文交叉核对用；公式乱码勿信）。
输出：卡罗尔/原书转换/text/pNNN.txt（NNN = PDF 页号；书页 N → p(N+15)）。"""
import os
import fitz

SRC = r"E:\AI整理书籍\卡罗尔\原书转换\Spacetime and Geometry An Introduction to General Relativity (Sean Carroll).pdf"
OUT = r"E:\AI整理书籍\卡罗尔\原书转换\text"

def main():
    os.makedirs(OUT, exist_ok=True)
    doc = fitz.open(SRC)
    for i, page in enumerate(doc, start=1):
        dest = os.path.join(OUT, f"p{i:03d}.txt")
        if os.path.exists(dest):
            continue
        t = page.get_text("text")
        with open(dest, "w", encoding="utf-8") as f:
            f.write(t)
    print(f"done: {len(doc)} text pages -> {OUT}")

if __name__ == "__main__":
    main()
