# -*- coding: utf-8 -*-
"""源码级编号公式审计（本书体例：公式按 (章.节.式) 三段编号，节号每章重排；
附录为 (A.1) 两段编号）。按 main.tex 的 input 顺序解析 chapters/*.tex，
章号由 \chapter 递增，节号每章复位累计；xiti 内不占计数。
用法: python check_tags_src.py"""
import io, os, re, sys

BASE = r"E:\AI整理书籍\李正中"
MAIN = os.path.join(BASE, "重排本", "main.tex")
CH = os.path.join(BASE, "重排本", "chapters")

s = io.open(os.path.join(BASE, "MinerU", "full_merged.md"), encoding="utf-8").read()
ocr = re.findall(r"\\tag\{(\d+)\.(\d+)\.(\d+)([a-z]?)\}", s)
ocr_sec = {}
for c, sec, e, suf in ocr:
    k = (int(c), int(sec))
    ocr_sec[k] = ocr_sec.get(k, 0) + 1
# 附录 tag (A.1)
ocr_ap = {}
for c, e, suf in re.findall(r"\\tag\{([A-H])\.(\d+)([a-z]?)\}", s):
    ocr_ap[c] = ocr_ap.get(c, 0) + 1

CH_RE = re.compile(r"\\chapter\*?\{")
SEC_RE = re.compile(r"\\section\*?\{")
XTI_BEGIN = chr(92) + "begin{xiti}"
XTI_END = chr(92) + "end{canKao}"

tex_sec, tex_ap = {}, {}
chap, sec = 0, 0
in_appendix = False
for fn in [l.strip().replace(chr(92) + "input{chapters/", "").replace("}", "") + ".tex"
           for l in io.open(MAIN, encoding="utf-8")
           if l.strip().startswith(chr(92) + "input{chapters/")]:
    if fn == "symbols.tex" or fn == "xiti.tex":
        continue
    if fn.startswith("app"):
        in_appendix = True
    lines = io.open(os.path.join(CH, fn), encoding="utf-8").read().split("\n")
    in_refs = False
    for l in lines:
        ls = l.strip()
        if ls.startswith(chr(92) + "setcounter"):
            continue
        if ls.startswith(chr(92) + "chapter"):
            if in_appendix:
                chap += 1  # appA..appH 依次 A..H
                letter = chr(ord("A") + chap - 1)
            else:
                chap += 1
                sec = 0
            continue
        if SEC_RE.match(ls):
            sec += 1
            continue
        if ls.startswith(chr(92) + "begin{canKao}"):
            in_refs = True
            continue
        if ls.startswith(XTI_END):
            in_refs = False
            continue
        if in_refs:
            continue
        if re.match(r"\\begin\{equation\}", ls):
            if in_appendix:
                k = letter
                tex_ap[k] = tex_ap.get(k, 0) + 1
            else:
                k = (chap, sec)
                tex_sec[k] = tex_sec.get(k, 0) + 1

print(f"OCR tags(正文): {sum(ocr_sec.values())} in {len(ocr_sec)} (章,节); tex: {sum(tex_sec.values())} in {len(tex_sec)}")
bad = 0
for k in sorted(set(ocr_sec) | set(tex_sec)):
    o = ocr_sec.get(k, 0)
    t = tex_sec.get(k, 0)
    if o != t:
        print(f"  章{k[0]}节{k[1]}: OCR {o} vs tex {t}  << DIFF")
        bad += 1
print(f"OCR tags(附录): {sum(ocr_ap.values())} in {len(ocr_ap)} letters; tex: {sum(tex_ap.values())} in {len(tex_ap)}")
for k in sorted(set(ocr_ap) | set(tex_ap)):
    o = ocr_ap.get(k, 0)
    t = tex_ap.get(k, 0)
    if o != t:
        print(f"  附录{k}: OCR {o} vs tex {t}  << DIFF")
        bad += 1
print("OK" if bad == 0 else f"{bad} 处不一致")
