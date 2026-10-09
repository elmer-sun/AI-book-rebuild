# -*- coding: utf-8 -*-
import io

p = r"E:\AI整理书籍\齐曼\重排本\chapters\parts\ch1_c.tex"
s = io.open(p, encoding="utf-8").read()
k = s.find("在复数域中")
print("found at", k)
print(repr(s[k - 12:k + 40]))
seg = s[k - 3:k]
print("before:", [hex(ord(c)) for c in seg])
j = s.find("之和", k)
print("after:", [hex(ord(c)) for c in s[j + 2:j + 4]])
