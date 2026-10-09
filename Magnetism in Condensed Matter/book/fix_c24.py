# -*- coding: utf-8 -*-
"""appC: C.24-C.25 逐行编号修正 v2"""
import io

B = chr(92)
NL = chr(10)
p = r'E:\AI整理书籍\磁学\book\appC.tex'
s = io.open(p, encoding='utf-8').read()

line1 = (B + 'hbar' + B + 'hat{L}_z = ' + B + 'mathrm{i}' + B + 'hbar' + B + 'left[y'
         + B + 'frac{' + B + 'partial}{' + B + 'partial x} - x' + B + 'frac{'
         + B + 'partial}{' + B + 'partial y}' + B + 'right] = -' + B + 'mathrm{i}'
         + B + 'hbar' + B + 'frac{' + B + 'partial}{' + B + 'partial'
         + B + 'phi}' + B + 'tag{C.24}')
old = (B + 'begin{equation*}' + NL + line1 + NL +
       B + 'begin{equation*}' + NL +
       B + 'vphantom{' + B + 'frac{' + B + 'partial}{' + B + 'partial'
       + B + 'phi}}' + B + 'tag{C.25}' + NL +
       B + 'end{equation*}')
new = (B + 'begin{align*}' + NL +
       B + 'hbar' + B + 'hat{L}_z = ' + B + 'mathrm{i}' + B + 'hbar' + B + 'left[y'
       + B + 'frac{' + B + 'partial}{' + B + 'partial x} - x' + B + 'frac{'
       + B + 'partial}{' + B + 'partial y}' + B + 'right]' + B + 'tag{C.24}' + B * 2 + NL +
       '= -' + B + 'mathrm{i}' + B + 'hbar' + B + 'frac{' + B + 'partial}{'
       + B + 'partial' + B + 'phi}' + B + 'tag{C.25}' + NL +
       B + 'end{align*}')
assert old in s, 'C.24 block still not found'
s = s.replace(old, new, 1)
io.open(p, 'w', encoding='utf-8').write(s)
print('ok appC C.24/25 fixed')
