# -*- coding: utf-8 -*-
"""源码级编号公式审计（全书连续节号，仿 LaTeX counterwithout 行为）：
按主 tex 的 input 顺序解析 chapters/*.tex，节号全书连续累计；
appendix.tex 为字母节号 (a.x)，跳过。xiti 内局部编号不占主计数。
用法: python check_tags_src.py <卷目录> <main.tex路径(缺省 重排本/main.tex)>"""
import io, os, re, sys

BASE = sys.argv[1]
MAIN = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, "重排本", "main.tex")
CH = os.path.join(BASE, "重排本", "chapters")

s = io.open(os.path.join(BASE, "MinerU", "full_merged.md"), encoding="utf-8").read()
ocr = re.findall(r"\\tag\{([0-9]+\.[0-9]+[a-z]?)\}", s)
ocr_sec = {}
for t in ocr:
    sec = str(int(t.split(".")[0]))
    ocr_sec[sec] = ocr_sec.get(sec, 0) + 1

SEC_RE = re.compile(r"\\section\*?\{")
SET_RE = re.compile(r"\\setcounter\{section\}\{(\d+)\)")
BEGIN = chr(92) + "begin{xiti}"
END = chr(92) + "end{xiti}"

tex_sec = {}
sec = 0
for fn in [l.strip().replace(chr(92) + "input{chapters/", "").replace("}", "") + ".tex"
           for l in io.open(MAIN, encoding="utf-8")
           if l.strip().startswith(chr(92) + "input{chapters/")]:
    if fn == "appendix.tex":
        continue  # 字母节号 (a.x)，单独由附录代理核对
    lines = io.open(os.path.join(CH, fn), encoding="utf-8").read().split("\n")
    in_xiti = False
    for l in lines:
        ls = l.strip()
        m = SET_RE.match(ls)
        if m:
            sec = int(m.group(1))
            continue
        if SEC_RE.match(ls):
            sec += 1
            continue
        if ls.startswith(BEGIN):
            in_xiti = True
            continue
        if ls.startswith(END):
            in_xiti = False
            continue
        if in_xiti:
            continue
        if re.match(r"\\begin\{equation\}", ls):
            k = str(sec)
            tex_sec[k] = tex_sec.get(k, 0) + 1

print(f"OCR tags: {len(ocr)} in {len(ocr_sec)} sections; tex main equations: {sum(tex_sec.values())}")
bad = 0
for secn in sorted(ocr_sec, key=int):
    o = ocr_sec[secn]
    t = tex_sec.get(secn, 0)
    if o != t:
        print(f"  section-{secn}: OCR {o} vs tex {t}  << DIFF")
        bad += 1
extra = {k: v for k, v in tex_sec.items() if k not in ocr_sec}
if extra:
    print("  tex-only sections:", extra)
    bad += len(extra)
print("sections:", len(ocr_sec), " diff:", bad)
