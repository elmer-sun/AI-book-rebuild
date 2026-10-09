# -*- coding: utf-8 -*-
"""appC: C.24-C.25 逐行编号修正 v3（只在两个 equation* 的片段上操作）"""
import io

B = chr(92)
NL = chr(10)
p = r'E:\AI整理书籍\磁学\book\appC.tex'
s = io.open(p, encoding='utf-8').read()

i = s.find(B + 'tag{C.24}')
a = s.rfind(B + 'begin{equation*}', 0, i)
b1 = s.find(B + 'end{equation*}', i) + len(B + 'end{equation*}')
block1 = s[a:b1]
# 第二个 equation*（phantom C.25）
j = s.find(B + 'begin{equation*}', b1)
b2 = s.find(B + 'end{equation*}', j) + len(B + 'end{equation*}')
block2 = s[j:b2]

assert B + 'tag{C.24}' in block1 and B + 'tag{C.25}' in block2

# 提取 block1 的公式体
body = block1
body = body.replace(B + 'begin{equation*}' + NL, '').replace(NL + B + 'end{equation*}', '')
body = body.replace(B + 'tag{C.24}', '')
# 把 = -i\hbar\frac{\partial}{\partial\phi} 拆成第二行
k = body.find('= -' + B + 'mathrm{i}')
assert k > 0
lhs = body[:k].rstrip()
rhs = body[k:].lstrip()

new = (B + 'begin{align*}' + NL + lhs + B + 'tag{C.24}' + B * 2 + NL +
       '= ' + rhs + B + 'tag{C.25}' + NL + B + 'end{align*}')
s = s[:a] + new + s[b2:]
io.open(p, 'w', encoding='utf-8').write(s)
print(repr(new))
