# -*- coding: utf-8 -*-
"""ch3/ch4 最后四处修正"""
import io

B = chr(92)

p = r'E:\AI整理书籍\磁学\recovery\build\ch3.tex'
s = io.open(p, encoding='utf-8').read()

old = '（ recall $B_0$ 沿 $z$ 轴）'
assert old in s, 'recall pattern'
s = s.replace(old, '（回顾 $B_0$ 沿 $z$ 轴）')

old = (B + 'gamma(' + B + 'mathbf{M}' + B + 'times' + B
       + 'mathbf{B})_y - ' + B + 'frac{M_x}{T_2}')
assert old in s, 'bloch pattern'
s = s.replace(old, (B + 'gamma(' + B + 'mathbf{M}' + B + 'times' + B
                    + 'mathbf{B})_x - ' + B + 'frac{M_x}{T_2}'))

old = '角分布（最能量更高的正电子的期望'
assert old in s, 'energetic pattern'
s = s.replace(old, '角分布（能量最高的正电子的期望')
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ch3 done')

p = r'E:\AI整理书籍\磁学\recovery\build\ch4.tex'
s = io.open(p, encoding='utf-8').read()
old = '单态（反对称），因此交换积分很可能为负'
assert old in s, 'ch4 pattern'
s = s.replace(old, '更倾向于单态（反对称），因此交换积分很可能为负', 1)
io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('ch4 done')
