# -*- coding: utf-8 -*-
"""ch7: 7.74-7.76 与 appC: C.24-C.25 逐行编号修正"""
import io

B = chr(92)
NL = chr(10)

def fix(path, subs):
    s = io.open(path, encoding='utf-8').read()
    for old, new in subs:
        if old not in s:
            print('MISS in', path, ':', old[:60].replace(NL, '|'))
            continue
        s = s.replace(old, new, 1)
        print('ok  ', path, ':', new[:50].replace(NL, '|'))
    io.open(path, 'w', encoding='utf-8').write(s)

# --- ch7 7.74-7.76 ---
s = io.open(r'E:\AI整理书籍\磁学\book\ch7.tex', encoding='utf-8').read()
# 第一行（M_q 积分行）行尾是 \\（后跟 &= 第二行）
i = s.find('&= ' + B + 'frac{k_{' + B + 'mathrm{F}}m_{' + B + 'mathrm{e}}g^{2}')
# 向前找本 align* 的第一个行尾 \\
j = s.rfind(B * 2, 0, i)
s = s[:j] + B + 'tag{7.74}' + s[j:]
# 第二行 tag 7.74 -> 7.75
s = s.replace(B + 'right]' + B + 'tag{7.74}' + NL + B + 'end{align*}' + NL + '态密度',
              B + 'right]' + B + 'tag{7.75}' + NL + B + 'end{align*}' + NL + '态密度', 1)
# 积分式 7.75 -> 7.76，删除 phantom
old3 = (B + 'right]' + B + 'tag{7.75}' + NL + B + 'end{align*}' + NL +
        B + 'begin{equation*}' + NL +
        B + 'vphantom{' + B + 'frac{' + B + 'pi k_{' + B + 'mathrm{F}}}{2}}' + B + 'tag{7.76}' + NL +
        B + 'end{equation*}')
new3 = B + 'right]' + B + 'tag{7.76}' + NL + B + 'end{align*}'
if old3 in s:
    s = s.replace(old3, new3, 1)
    print('ok ch7 7.76 phantom removed')
else:
    print('MISS ch7 integral block')
io.open(r'E:\AI整理书籍\磁学\book\ch7.tex', 'w', encoding='utf-8').write(s)

# --- appC C.24-C.25 ---
p = r'E:\AI整理书籍\磁学\book\appC.tex'
s = io.open(p, encoding='utf-8').read()
old = (B + 'begin{equation*}' + NL +
       B + 'hbar' + B + 'hat{L}_z = ' + B + 'mathrm{i}' + B + 'hbar' + B + 'left[y'
       + B + 'frac{' + B + 'partial}{' + B + 'partial x} - x' + B + 'frac{'
       + B + 'partial}{' + B + 'partial y}' + B + 'right] = -' + B + 'mathrm{i}'
       + B + 'hbar' + B + 'frac{' + B + 'partial}{' + B + 'partial'
       + B + 'phi}' + B + 'tag{C.24}' + NL +
       B + 'begin{equation*}' + NL +
       B + 'vphantom{' + B + 'frac{' + B + 'partial}{' + B + 'partial'
       + B + 'phi}}' + B + 'tag{C.25}' + NL +
       B + 'end{equation*}')
new = (B + 'begin{align*}' + NL +
       B + 'hbar' + B + 'hat{L}_z = ' + B + 'mathrm{i}' + B + 'hbar'
       + B + 'left[y' + B + 'frac{' + B + 'partial}{' + B + 'partial x} - x'
       + B + 'frac{' + B + 'partial}{' + B + 'partial y}' + B + 'right]' + B
       + 'tag{C.24}' + B * 2 + NL +
       '= -' + B + 'mathrm{i}' + B + 'hbar' + B + 'frac{' + B + 'partial}{'
       + B + 'partial' + B + 'phi}' + B + 'tag{C.25}' + NL +
       B + 'end{align*}')
if old in s:
    s = s.replace(old, new, 1)
    print('ok appC C.24/25')
else:
    print('MISS appC C.24 block')
io.open(p, 'w', encoding='utf-8').write(s)
