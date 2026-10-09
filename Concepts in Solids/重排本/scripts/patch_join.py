# -*- coding: utf-8 -*-
# 给各续写文件加 %JOIN% 标记 + 修 B1 显示公式接缝
import io, re

P = r"E:\AI整理书籍\安德森\重排本\chapters\parts"

def rd(fn):
    return io.open(P + "\\" + fn, encoding="utf-8").read()

def wr(fn, s):
    io.open(P + "\\" + fn, "w", encoding="utf-8").write(s)

# 1) ch2_C12.tex: tail 起始加 %JOIN%（承接 B4b 句中）
s = rd("ch2_C12.tex")
m = re.search(r"%--B4-TAIL--\s*\n", s)
assert m and "%JOIN%" not in s
s = s[:m.end()] + "%JOIN%\n" + s[m.end():]
wr("ch2_C12.tex", s)

# 2) ch3_D1a.tex: C-TAIL 起始加 %JOIN%（承接 ch3_C 末句“对物理”）
s = rd("ch3_D1a.tex")
m = re.search(r"%--C-TAIL--\s*\n", s)
assert m, "C-TAIL marker missing"
if "%JOIN%" not in s:
    s = s[:m.end()] + "%JOIN%\n" + s[m.end():]
wr("ch3_D1a.tex", s)

# 3) ch3_D1c.tex: 文件体起始加 %JOIN%（承接 D1b 末句“实际上并不”）
s = rd("ch3_D1c.tex")
lines = s.split("\n")
assert lines[0].startswith("%")
if "%JOIN%" not in s:
    # 找到第一条非注释内容行，在其前插入
    for i in range(1, len(lines)):
        if lines[i].strip() and not lines[i].strip().startswith("%"):
            lines.insert(i, "%JOIN%")
            break
wr("ch3_D1c.tex", "\n".join(lines))

# 4) ch3_B1.tex: （由性质 (c)）并入显示公式所在段（去掉公式与注释之间的空行）
s = rd("ch3_B1.tex")
old = "eM\\sum_{Q}\\ f(Q) = eM\n\\end{equation*}\n\n% ---- B.1 收尾"
new = "eM\\sum_{Q}\\ f(Q) = eM\n\\end{equation*}\n% ---- B.1 收尾"
if old in s:
    s = s.replace(old, new, 1)
    wr("ch3_B1.tex", s)
    print("B1 seam joined")
else:
    print("B1 pattern check:", "eM" in s)

print("JOIN markers installed")
