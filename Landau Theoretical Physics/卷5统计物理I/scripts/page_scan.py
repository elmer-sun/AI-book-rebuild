# -*- coding: utf-8 -*-
"""像素级页面体检：检测 (a) 非空白页的页底大空白（内容止于版心<62%），
(b) 水平溢出版心的墨迹。输出可疑页清单。"""
import glob, os, sys
from PIL import Image
import numpy as np

d = sys.argv[1] if len(sys.argv) > 1 else r"E:\AI整理书籍\朗道理论物理教程\卷5统计物理I\重排本\render"
lo = int(sys.argv[2]) if len(sys.argv) > 2 else 244
hi = int(sys.argv[3]) if len(sys.argv) > 3 else 406

files = sorted(glob.glob(os.path.join(d, "pg-*.png")))
print(f"scanning {lo}..{hi}")
sus_blank, sus_overflow = [], []
for f in files:
    n = int(os.path.basename(f)[3:6])
    if not (lo <= n <= hi):
        continue
    im = Image.open(f).convert("L")
    a = np.array(im)
    h, w = a.shape
    ink = a < 128
    rows = ink.sum(axis=1)
    cols = ink.sum(axis=0)
    total_ink = rows.sum()
    if total_ink < 200:      # 整页空白（章前反页）
        continue
    # 版心（参考 A4 100dpi：边距 2.3cm ≈ 91px）
    ml, mr = int(w*0.085), int(w*0.915)
    # 页底大空白：最后一行有≥3个墨点的位置
    ys = np.where(rows >= 3)[0]
    # 排除页脚页码（最底部 ~60px 内的孤立行）：取除页脚外主体末行
    body = ys[ys < h - 55]
    if len(body) == 0:
        continue
    last = body[-1] / h
    if last < 0.60:
        sus_blank.append((n, round(last*100)))
    # 水平溢出：版心外墨点（排除页眉区域顶部 7%）
    band = ink[int(h*0.07):int(h*0.93), :]
    left_ink = band[:, :ml-6].sum()
    right_ink = band[:, mr+6:].sum()
    if left_ink > 40 or right_ink > 40:
        sus_overflow.append((n, int(left_ink), int(right_ink)))

print("== 页底大空白（内容止于<60%版心）==")
for n, pct in sus_blank:
    print(f"  pg-{n:03d}: content ends at {pct}%")
print("== 水平溢出 ==")
for n, l, r in sus_overflow:
    print(f"  pg-{n:03d}: left={l} right={r}")
