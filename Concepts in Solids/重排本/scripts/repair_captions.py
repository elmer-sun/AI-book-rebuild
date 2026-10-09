# -*- coding: utf-8 -*-
# 修复图注中因重复替换产生的 $$...$$ —— 塌缩为 $...$ 并验证 $ 配对
import io, re

BS = chr(92)
CAP = BS + "caption*{"
FILES = [
    r"E:\AI整理书籍\安德森\重排本\chapters\ch02.tex",
    r"E:\AI整理书籍\安德森\重排本\chapters\ch03.tex",
]
pat = re.compile(re.escape(CAP) + r"([^}]*)\}")

for fn in FILES:
    s = io.open(fn, encoding="utf-8").read()
    fixed = []
    def repl(m):
        cap = m.group(1)
        orig = cap
        while "$$" in cap:
            cap = cap.replace("$$", "$")
        # 验证配对
        if cap.count("$") % 2 != 0:
            fixed.append(("ODD", orig[:50], cap[:60]))
        elif cap != orig:
            fixed.append(("FIXED", orig[:50], cap[:60]))
        return CAP + cap + "}"
    s2 = pat.sub(repl, s)
    io.open(fn, "w", encoding="utf-8").write(s2)
    print(fn, len(fixed), "captions touched")
    for kind, a, b in fixed:
        print(" ", kind, "|", a, "=>", b)
