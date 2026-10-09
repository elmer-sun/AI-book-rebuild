import io

p = r"E:\AI整理书籍\群论\直接识别_ch1\md\p028.md"
s = io.open(p, encoding="utf-8").read()
BS = "\x08"
before = s.count(BS)
s = s.replace(BS + "oldsymbol{" + "\\" + "Delta}", "boldsymbol{" + "\\" + "Delta}")
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("BS before:", before, "BS after:", s.count(BS))
print("boldsymbol count:", s.count("boldsymbol{" + "\\" + "Delta}"))
