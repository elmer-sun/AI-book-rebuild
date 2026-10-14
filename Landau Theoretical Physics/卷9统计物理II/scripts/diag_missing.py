# -*- coding: utf-8 -*-
"""定性 25 个 OCR-tag-in-PDF 缺失：align 环境 / 脚注内 / aux 未捕获 / 真缺"""
import io, os, re

BASE = r"E:\AI整理书籍\朗道理论物理教程\卷9统计物理II"
RB = os.path.join(BASE, "重排本")
CH = os.path.join(RB, "chapters")

missing = ["2.4a", "5.14", "6.16", "35*.2", "35*.3", "35*.5", "35*.6",
           "35*.8", "35*.9", "35*.10", "35*.11", "35*.12",
           "37.8a", "37.8b", "74*.1", "74*.2", "74*.3", "74*.5", "74*.7",
           "74*.9", "74*.10", "74*.11", "74*.12", "74*.13", "79.18"]

aux = io.open(os.path.join(RB, "main.aux"), encoding="utf-8").read()
labels = dict(re.findall(r"\\newlabel\{([^}]*)\}\{\{([^}]*)\}", aux))

# 正文里搜每个编号的形态
files = [f for f in os.listdir(CH) if f.endswith(".tex")]
corpus = {f: io.open(os.path.join(CH, f), encoding="utf-8").read() for f in files}

for m in missing:
    hits = []
    for f, s in corpus.items():
        for i, ln in enumerate(s.split(chr(10)), 1):
            if ("{" + m + "}") in ln:
                kind = "?"
                if "tag{" in ln:
                    kind = "manual-tag"
                elif "label{" in ln:
                    kind = "label"
                hits.append((f, i, kind, ln.strip()[:60]))
    in_aux = [k for k, v in labels.items() if v == m]
    print("%-8s aux=%-12s src=%s" % (m, in_aux or "-", hits[:2] if hits else "NOT IN SRC"))
