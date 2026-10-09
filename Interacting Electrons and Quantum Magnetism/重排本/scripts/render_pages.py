# -*- coding: utf-8 -*-
"""渲染 origin.pdf 指定页为 PNG，供对照扫描页核实用。
用法: python scripts/render_pages.py F1 14 15 16-18
F1/F2 选择提取文件夹；页码为 1-based。
输出: render/F1_p014.png 等
"""
import sys, os
import pymupdf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.dirname(ROOT)
DIRS = {
    'F1': os.path.join(BOOK, '978-1-4612-0869-3.pdf-03d00808-9b5c-4ad1-ad42-3bb81e8d1d27'),
    'F2': os.path.join(BOOK, '978-1-4612-0869-3.pdf-2d8250b2-2bf0-47cf-98f7-f191880f24fc'),
}
OUT = os.path.join(ROOT, 'render')
os.makedirs(OUT, exist_ok=True)

def expand(spec):
    if '-' in spec:
        a, b = spec.split('-')
        return range(int(a), int(b) + 1)
    return [int(spec)]

def main():
    tag, specs = sys.argv[1], sys.argv[2:]
    folder = DIRS[tag]
    pdf = [f for f in os.listdir(folder) if f.endswith('_origin.pdf')][0]
    doc = pymupdf.open(os.path.join(folder, pdf))
    for spec in specs:
        for p in expand(spec):
            page = doc[p - 1]
            pix = page.get_pixmap(dpi=200)
            out = os.path.join(OUT, '%s_p%03d.png' % (tag, p))
            pix.save(out)
            print(out)

if __name__ == '__main__':
    main()
