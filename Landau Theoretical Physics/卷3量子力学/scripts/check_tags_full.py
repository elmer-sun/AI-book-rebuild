# -*- coding: utf-8 -*-
"""全书编号公式审计：从编译 PDF 提取 (节.式) 编号序列，与 OCR tag 序列逐节对比。
用法: python check_tags_full.py <卷目录> <章节文件...>"""
import io, os, re, subprocess, sys, glob

BASE = sys.argv[1]
PDF = os.path.join(BASE, "重排本", "main.pdf")
MIN = os.path.join(BASE, "MinerU", "full_merged.md")

# 1) OCR tag 序列（按文档顺序）
s = io.open(MIN, encoding="utf-8").read()
ocr = re.findall(r"\\tag\{([0-9]+\.[0-9]+[a-z]?)\}", s)
ocr_sections = {}
for t in ocr:
    sec = t.split(".")[0]
    ocr_sections.setdefault(sec, []).append(t)

# 2) PDF 提取（Windows 下 pdftotext 管道编码不稳，走临时文件）
tmp = PDF + ".tags.txt"
subprocess.run(["pdftotext", "-layout", "-enc", "UTF-8", PDF, tmp], check=True)
txt = io.open(tmp, encoding="utf-8", errors="ignore").read()
# 只取行尾（display 公式右侧编号），排除正文引用
got = re.findall(r"\((\d{1,3}\.\d{1,3}[a-z]?)\)\s*$", txt, re.M)
# 只保留看起来像公式编号的（节号在 1-200，式号 1-99）
got = [g for g in got if 0 < int(g.split(".")[0]) <= 200 and 0 < int(re.sub(r"[a-z]", "", g.split(".")[1]) or 0) <= 99]
got_sections = {}
for t in got:
    sec = t.split(".")[0].lstrip("0") or "0"
    got_sections.setdefault(sec, []).append(t)

print(f"OCR tags total: {len(ocr)}   PDF eq-numbers found: {len(got)}")
bad = 0
for sec in sorted(ocr_sections, key=lambda x: int(x)):
    o = ocr_sections[sec]
    g = got_sections.get(sec, [])
    # 去重连续（PDF 提取可能有重复渲染文本如目录/引用）
    dedup = []
    for x in g:
        if not dedup or dedup[-1] != x:
            dedup.append(x)
    if len(dedup) != len(o):
        print(f"  §{sec}: OCR {len(o)} vs PDF {len(dedup)}  << MISMATCH")
        # show first diff
        for i in range(max(len(o), len(dedup))):
            a = o[i] if i < len(o) else "--"
            b = dedup[i] if i < len(dedup) else "--"
            if a != b:
                print(f"     first diff at #{i+1}: OCR {a} vs PDF {b}")
                break
        bad += 1
    else:
        mism = [i for i in range(len(o)) if o[i] != dedup[i]]
        if mism:
            print(f"  §{sec}: count ok but #{mism[0]+1}: OCR {o[mism[0]]} vs PDF {dedup[mism[0]]}")
            bad += 1
print("sections checked:", len(ocr_sections), " mismatched:", bad)
