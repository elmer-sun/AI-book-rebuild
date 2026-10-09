# -*- coding: utf-8 -*-
# 批6/批7脚本：去掉图内 "Figure NN" 题注并重新生成
import io, re, subprocess, sys

for p in [r"E:\AI整理书籍\安德森\重排本\scripts\draw_figs_ch3e.py",
          r"E:\AI整理书籍\安德森\重排本\scripts\draw_figs_ch3d.py"]:
    s = io.open(p, encoding="utf-8").read()
    s2 = re.sub(r"^\s*ax\.text\([^)]*'Figure \d+'[^)]*\)\n", "", s, flags=re.M)
    n = len(re.findall(r"ax\.text\([^)]*'Figure \d+'", s)) - len(re.findall(r"ax\.text\([^)]*'Figure \d+'", s2))
    io.open(p, "w", encoding="utf-8").write(s2)
    print(p.split(chr(92))[-1], "removed", n)
    r = subprocess.run([sys.executable, p], capture_output=True, text=True, encoding="utf-8")
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])
