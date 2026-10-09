# -*- coding: utf-8 -*-
"""Repair the damaged notation line in s3 (asterisk-fixer collateral)."""
import io

p = 'chapters/ch1_s3.tex'
lines = io.open(p, encoding='utf-8').read().split('\n')
BS = chr(92)

target = None
for i, l in enumerate(lines):
    if '的转置；' in l and 'textit{}' in l:
        target = i
        break
assert target is not None, 'line not found'

lines[target] = (
    '处理矩阵时将使用以下记号：$' + BS + 'mathbf{D}^{T}$ 表示 $' + BS + 'mathbf{D}$ 的转置；'
    '$' + BS + 'mathbf{D}^{' + BS + '*}$ 表示 $' + BS + 'mathbf{D}$ 的复共轭；'
    '$' + BS + 'mathbf{D}^{' + BS + 'dagger}' + BS + ',[=(' + BS + 'mathbf{D}^{' + BS + '*})^{T}]$ '
    '表示 $' + BS + 'mathbf{D}$ 的厄米共轭；'
    '$' + BS + 'tilde{' + BS + 'mathbf{D}}' + BS + ',[=(' + BS + 'mathbf{D}^{-1})^{T}]$ '
    '表示 $' + BS + 'mathbf{D}$ 的逆步矩阵（contragredient）；'
    '$' + BS + 'dim ' + BS + 'mathbf{D}$ 表示 $' + BS + 'mathbf{D}$ 的维数。'
)
io.open(p, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('repaired line', target + 1)
