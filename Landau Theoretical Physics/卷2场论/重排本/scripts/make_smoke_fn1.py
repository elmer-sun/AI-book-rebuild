# -*- coding: utf-8 -*-
# Create smoke_fn1.tex from main.tex, keeping only symbols/ch01/ch02/ch03 inputs
import io, os

BASE = r"E:\AI整理书籍\朗道理论物理教程\卷2场论\重排本"
src = os.path.join(BASE, "main.tex")
dst = os.path.join(BASE, "smoke_fn1.tex")

with io.open(src, "r", encoding="utf-8") as f:
    text = f.read()

old_block = """\\input{chapters/symbols}
\\input{chapters/ch01}
\\input{chapters/ch02}
\\input{chapters/ch03}
\\input{chapters/ch04}
\\input{chapters/ch05}
\\input{chapters/ch06}
\\input{chapters/ch07}
\\input{chapters/ch08}
\\input{chapters/ch09}
\\input{chapters/ch10}
\\input{chapters/ch11}
\\input{chapters/ch12}
\\input{chapters/ch13}
\\input{chapters/ch14}"""

new_block = """\\input{chapters/symbols}
\\input{chapters/ch01}
\\input{chapters/ch02}
\\input{chapters/ch03}"""

assert old_block in text, "input block not found"
text = text.replace(old_block, new_block)

with io.open(dst, "w", encoding="utf-8") as f:
    f.write(text)
print("written", dst)
