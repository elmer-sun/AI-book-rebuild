# -*- coding: utf-8 -*-
"""修复 ch4_a/ch4_b 的两处接缝错位（2026-10-07）。
ch4_a: 文件顶部 %--A-TAIL-- + 重复残句删除（该句 ch4_b 开头已有）。
ch4_b: A-TAIL 区误放的本块收尾句移回正文末尾。
"""
import io

BP = r"E:\AI整理书籍\文小刚\重排本\chapters\parts"

# --- ch4_a ---
p = BP + r"\ch4_a.tex"
s = io.open(p, encoding="utf-8").read()
lines = s.split("\n")
# 找到 marker 行与后续空行，删除到第一个空行为止（残句+空行）
assert lines[1].strip() == "%--A-TAIL--", "ch4_a line2 不是 marker: " + lines[1][:40]
j = 2
while j < len(lines) and lines[j].strip():
    j += 1
# lines[2:j] 是残句，lines[j] 是空行——一并删掉
del lines[1:j + 1]
io.open(p, "w", encoding="utf-8").write("\n".join(lines))
print("ch4_a: 顶部重复残句已删")

# --- ch4_b ---
p = BP + r"\ch4_b.tex"
s = io.open(p, encoding="utf-8").read()
MARK = "%--A-TAIL--"
i = s.find(MARK)
assert i >= 0
after = s[i + len(MARK):]
nl = after.find("\n")
sent = after[:nl]          # marker 后那一行 = 收尾句
rest = after[nl + 1:]
# 删除 marker 行 + 收尾句行 + 紧随的空行
if rest.startswith("\n"):
    rest = rest[1:]
s = s[:i] + rest
# 收尾句插到文件尾部代理注释区之前（若无注释区则追加到末尾）
k = s.find("\n% ")
tail_para = "\n" + sent
if k >= 0:
    s = s[:k] + tail_para + s[k:]
else:
    s = s.rstrip("\n") + "\n" + tail_para
io.open(p, "w", encoding="utf-8").write(s)
print("ch4_b: 收尾句已归位到正文末尾 ->", sent[:40])
