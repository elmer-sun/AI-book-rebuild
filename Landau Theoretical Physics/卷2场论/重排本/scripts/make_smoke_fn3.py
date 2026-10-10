# -*- coding: utf-8 -*-
"""Create smoke_fn3.tex: main.tex with only ch07/ch08/ch09 inputs, section counter at 52."""
import io

txt = io.open("main.tex", encoding="utf-8").read()
out = []
for line in txt.split("\n"):
    s = line.strip()
    if s.startswith("\\input{chapters/ch"):
        name = s[len("\\input{chapters/"):-1]
        if name not in ("ch07", "ch08", "ch09"):
            line = "% " + line
    out.append(line)
txt = "\n".join(out)
txt = txt.replace("\\begin{document}\n", "\\begin{document}\n\n\\setcounter{section}{52}\n", 1)
io.open("smoke_fn3.tex", "w", encoding="utf-8", newline="\n").write(txt)
print("written")
