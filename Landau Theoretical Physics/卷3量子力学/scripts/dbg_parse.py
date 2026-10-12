# -*- coding: utf-8 -*-
"""调试 check_tags_src 的解析：打印各章文件的节号轨迹与 xiti 状态。"""
import io, re, sys, glob, os

BASE = sys.argv[1] if len(sys.argv) > 1 else "."
SEC_RE = re.compile(r"\\section\*?\{")
SET_RE = re.compile(r"\\setcounter\{section\}\{(\d+)\}")
BEGIN = chr(92) + "begin{xiti}"
END = chr(92) + "end{xiti}"

for f in sorted(glob.glob(os.path.join(BASE, "重排本", "chapters", "*.tex"))):
    lines = io.open(f, encoding="utf-8").read().split("\n")
    sec = 0
    in_xiti = False
    events = []
    n_eq_out = 0
    n_eq_in = 0
    for i, l in enumerate(lines):
        ls = l.strip()
        m = SET_RE.match(ls)
        if m:
            sec = int(m.group(1))
            events.append((i + 1, "SET" + str(sec)))
            continue
        if SEC_RE.match(ls):
            sec += 1
            events.append((i + 1, "SEC" + str(sec)))
            continue
        if ls.startswith(BEGIN):
            in_xiti = True
            events.append((i + 1, "XITI-BEGIN@" + str(sec)))
            continue
        if ls.startswith(END):
            in_xiti = False
            events.append((i + 1, "XITI-END@" + str(sec)))
            continue
        if re.match(r"\\begin\{equation\}", ls):
            if in_xiti:
                n_eq_in += 1
            else:
                n_eq_out += 1
    print(os.path.basename(f), "final_sec:", sec, "eq_out:", n_eq_out,
          "eq_in:", n_eq_in, "in_xiti_end:", in_xiti)
    if len(events) and os.path.basename(f) in ("ch17a.tex", "ch18.tex"):
        print("   events:", events[:16])
