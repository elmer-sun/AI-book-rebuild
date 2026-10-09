# -*- coding: utf-8 -*-
"""ch7.tex 习题 tag 编号校正 v3"""
import io, re

p = r'E:\AI整理书籍\磁学\book\ch7.tex'
s = io.open(p, encoding='utf-8').read()
NL = chr(10)
B = chr(92)

# 1) 在 I1 公式行（以 \right|\\ 结束、下一行以 I_2 开头）插入 \tag{7.99}
lines = s.split(NL)
for i, l in enumerate(lines):
    if l.startswith('I_1 ') and l.endswith(B * 2):
        lines[i] = l[:-2] + B + 'tag{7.99}' + B * 2
        break
else:
    raise SystemExit('I1 line not found')
s = NL.join(lines)

# 2) I2 行尾 \tag{7.99} -> \tag{7.100}（此时 7.99 只出现在 I2 行尾）
assert (B + 'tag{7.99}') in s
s = s.replace(B + 'right).' + B + 'tag{7.99}', B + 'right).' + B + 'tag{7.100}')

# 3) 链条 \tag{7.100} -> \tag{7.101}
s = s.replace('F(2k_{' + B + 'mathrm{F}}r),' + B + 'tag{7.100}',
              'F(2k_{' + B + 'mathrm{F}}r),' + B + 'tag{7.101}')

# 4) 7.101..7.115 依次 +1（降序）
for n in range(115, 100, -1):
    s = s.replace(B + 'tag{7.%d}' % n, B + 'tag{7.%d}' % (n + 1))

io.open(p, 'w', encoding='utf-8').write(s)
tags = re.findall(r'tag' + B + '{7.([0-9]+)' + B + '}', s)
print('last 22 tags:', ','.join(tags[-22:]))
