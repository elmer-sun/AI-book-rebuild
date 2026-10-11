import glob
BS = chr(92)
for f in glob.glob('chapters/*.tex'):
    t = open(f, encoding='utf-8').read()
    i = t.find('odinger')
    if i == -1:
        continue
    seg = t[i - 12:i + 12]
    print(f, repr(seg))
    for ch in seg:
        if ord(ch) > 127 or ch == BS:
            print(' ', hex(ord(ch)), repr(ch))
# 修复: 反斜杠+弯引号 -> 反斜杠+直引号
n = 0
for f in glob.glob('chapters/*.tex'):
    t = open(f, encoding='utf-8').read()
    bad1 = BS + chr(0x201C)
    bad2 = BS + chr(0x201D)
    if bad1 in t or bad2 in t:
        c1, c2 = t.count(bad1), t.count(bad2)
        t = t.replace(bad1, BS + '"').replace(bad2, BS + '"')
        open(f, 'w', encoding='utf-8').write(t)
        n += c1 + c2
        print('repaired in', f, c1 + c2)
print('total repaired:', n)
