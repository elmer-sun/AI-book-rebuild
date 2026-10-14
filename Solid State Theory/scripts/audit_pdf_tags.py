# -*- coding: utf-8 -*-
"""成品 PDF 级公式编号审计 v2：
- PDF 侧: 提取全部 (章.节.式)/(A.n) 编号按(章,节)归组
- OCR 侧: 按 full_merged.md 的章行号区间取 tag，ch11 区间内 (1.x.y) 归一为 (11.x.y)
比较各(章,节)的编号集合（a/b 变体拆算为独立编号存在性）。"""
import re, io
import pymupdf

BASE = r"E:\AI整理书籍\李正中"
RANGES = {
 'ch01': (433, 1141), 'ch02': (1142, 3226), 'ch03': (3227, 4428),
 'ch04': (4429, 6403), 'ch05': (6404, 7197), 'ch06': (7198, 9954),
 'ch07': (9955, 11123), 'ch08': (11124, 13328), 'ch09': (13329, 14461),
 'ch10': (14462, 15207), 'ch11': (15208, 18877), 'ch12': (18878, 20664),
}

# ---- PDF 侧 ----
doc = pymupdf.open(BASE + r"\重排本\main.pdf")
txt = "\n".join(p.get_text() for p in doc)
pdf_main = {}
for m in re.finditer(r"\((\d{1,2})\.(\d{1,2})\.(\d{1,2})([a-e]?)\)", txt):
    c, s = int(m.group(1)), int(m.group(2))
    if 1 <= c <= 12 and 1 <= s <= 12:
        pdf_main.setdefault((c, s), set()).add(int(m.group(3)))
pdf_ap = {}
for m in re.finditer(r"\(([A-H])\.(\d{1,2})([a-e]?)\)", txt):
    pdf_ap.setdefault(m.group(1), set()).add(int(m.group(2)))

# ---- OCR 侧（按章区间） ----
lines = io.open(BASE + r"\MinerU\full_merged.md", encoding="utf-8").read().split("\n")
ocr_main = {}
for name, (a, b) in RANGES.items():
    ch = int(name[2:])
    seg = "\n".join(lines[a-1:b])
    for m in re.finditer(r"\\tag\{(\d{1,2})\.(\d{1,2})\.(\d{1,2})([a-e]?)\}", seg):
        c = int(m.group(1))
        if c != ch:
            c = ch  # ch11 的 (1.x.y) 误读归一；其余章区间内 tag 章号应=章号
        ocr_main.setdefault((c, int(m.group(2))), set()).add(int(m.group(3)))
ocr_ap = {}
seg = "\n".join(lines[20664:21731])
for m in re.finditer(r"\\tag\{([A-H])\.(\d{1,2})([a-e]?)\}", seg):
    ocr_ap.setdefault(m.group(1), set()).add(int(m.group(2)))

bad = 0
for k in sorted(set(pdf_main) | set(ocr_main)):
    p, o = pdf_main.get(k, set()), ocr_main.get(k, set())
    if p != o:
        bad += 1
        miss, extra = sorted(o - p), sorted(p - o)
        print(f"章{k[0]}节{k[1]}: PDF缺{miss[:12]}{'...' if len(miss)>12 else ''}  PDF多{extra[:12]}{'...' if len(extra)>12 else ''}")
for k in sorted(set(pdf_ap) | set(ocr_ap)):
    p, o = pdf_ap.get(k, set()), ocr_ap.get(k, set())
    if p != o:
        bad += 1
        print(f"附录{k}: PDF缺{sorted(o-p)}  PDF多{sorted(p-o)}  (PDF多=OCR漏检编号, 代理已按页面核实则无碍)")
print(f"\n正文(章,节)组: {len(set(pdf_main)|set(ocr_main))}  不一致组: {bad}")
print(f"PDF 编号式: 正文 {sum(len(v) for v in pdf_main.values())} + 附录 {sum(len(v) for v in pdf_ap.values())}")
