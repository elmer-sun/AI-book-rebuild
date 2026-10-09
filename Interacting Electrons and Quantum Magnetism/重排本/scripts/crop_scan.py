# -*- coding: utf-8 -*-
"""从渲染好的扫描页 PNG 上裁剪图/表区域。
用法: python scripts/crop_scan.py <src.png> <x0> <y0> <x1> <y1> <out.png>
坐标为页高宽的比例 (0-1)。可选第7参数 = 放大倍数(默认2)。
"""
import sys
from PIL import Image

def main():
    src, x0, y0, x1, y1, out = sys.argv[1:7]
    zoom = float(sys.argv[7]) if len(sys.argv) > 7 else 2.0
    im = Image.open(src)
    W, H = im.size
    box = (int(float(x0) * W), int(float(y0) * H), int(float(x1) * W), int(float(y1) * H))
    crop = im.crop(box)
    if zoom != 1.0:
        crop = crop.resize((int(crop.width * zoom), int(crop.height * zoom)), Image.LANCZOS)
    crop.save(out)
    print(out, crop.size)

if __name__ == '__main__':
    main()
