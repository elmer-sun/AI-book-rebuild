# -*- coding: utf-8 -*-
"""补齐所有剩余的历史内容修正（以冻结 PDF 为准）"""
import io
import os

B = chr(92)
NL = chr(10)
BUILD = r'E:\AI整理书籍\磁学\recovery\build'


def apply(fname, fixes):
    p = os.path.join(BUILD, fname)
    s = io.open(p, encoding='utf-8').read()
    changed = False
    for old, new in fixes:
        if old in s:
            s = s.replace(old, new, 1)
            changed = True
            print('%s <- %r' % (fname, old[:40]))
    if changed:
        io.open(p, 'w', encoding='utf-8', newline=NL).write(s)


# ---- ch3：I=0 原文如此、recall、Bloch _y->_x、energetic 残留、3.24/3.25、3.43 标签
apply('ch3.tex', [
    ('目前设 I=0（原文如此，指暂不考虑电子自旋 J），从',
     '此处先设 J=0，从'),
    ('目前设 I=0（原文如此，指暂不考虑电子自旋J），从',
     '此处先设 J=0，从'),
    ('（ recall ' + B + 'B_0' + B + ' 沿 ' + B + 'z' + B + ' 轴）',
     '（回顾 ' + B + 'B_0' + B + ' 沿 ' + B + 'z' + B + ' 轴）'),
    ('（recall ' + B + 'B_0' + B + ' 沿 ' + B + 'z' + B + ' 轴）',
     '（回顾 ' + B + 'B_0' + B + ' 沿 ' + B + 'z' + B + ' 轴）'),
])

p = os.path.join(BUILD, 'ch3.tex')
s = io.open(p, encoding='utf-8').read()
# Bloch 方程第一行 _y -> _x
old = ('frac{' + B + 'mathrm{d}M_x}{dt} = ' + B + 'gamma(' + B
       + 'mathbf{M}' + B + 'times' + B + 'mathbf{B})_y - ' + B
       + 'frac{M_x}{T_2}')
if old in s:
    s = s.replace(old, old.replace(')_y', ')_x'))
    print('ch3 Bloch _y->_x')
# energetic 残留
import re
for m in set(re.findall(r'.{6}energetic.{6}', s)):
    print('energetic 残留:', repr(m))
s = s.replace('更energetic的光子', '能量更高的光子')
s = s.replace('energetic', '能量更高的')  # 兜底（应无残留）
# 3.24/3.25 合并
old = (B + 'begin{align*}' + NL
       + B + 'frac{' + B + 'mathrm{d}E}{' + B + 'mathrm{d}t} &= n(t)'
       + B + 'hbar' + B + 'omega W' + B * 2 + NL
       + '&= n_0' + B + 'hbar' + B + 'omega' + B + 'frac{W}{1+2WT_1}.'
       + B + 'tag{3.24}' + NL
       + B + 'end{align*}' + NL
       + B + 'begin{equation*}' + NL
       + B + 'vphantom{' + B + 'frac{W}{1+2WT_1}}' + B + 'tag{3.25}' + NL
       + B + 'end{equation*}')
new = (B + 'begin{align*}' + NL
       + B + 'frac{' + B + 'mathrm{d}E}{' + B + 'mathrm{d}t} &= n(t)'
       + B + 'hbar' + B + 'omega W' + B + 'tag{3.24}' + B * 2 + NL
       + '&= n_0' + B + 'hbar' + B + 'omega' + B + 'frac{W}{1+2WT_1}.'
       + B + 'tag{3.25}' + NL
       + B + 'end{align*}')
if old in s:
    s = s.replace(old, new)
    print('ch3 3.24/3.25 合并')
else:
    print('ch3 3.24 块未匹配，需检查')
# 3.43：tag 移出 resizebox
old = ',' + B + 'tag{3.43}' + NL + B + 'end{aligned}'
if old in s:
    s = s.replace(old, ',' + NL + B + 'end{aligned}')
    s = s.replace(B + 'end{aligned}$}' + NL,
                  B + 'end{aligned}$}' + B + 'qquad(3.43)' + NL, 1)
    print('ch3 3.43 tag 外置')
io.open(p, 'w', encoding='utf-8', newline=NL).write(s)

# ---- ch4：favor 系列
apply('ch4.tex', [
    (' favor 三重态', '更倾向于三重态'),
    (' favor 单态', '更倾向于单态'),
    ('单态基态更 favor。', '单态基态更稳定。'),
    ('favor 跳跃', '有利于跳跃'),
    ('动能更大。这 favor', '动能更大。这更倾向于'),
    ('代表电子排斥， favor 铁磁基态', '代表电子排斥，更倾向于铁磁基态'),
    ('两个相互作用的预自旋', '两个相互作用的自旋'),
])

# ---- ch5：task/order/residing/环境温度
apply('ch5.tex', [
    ('本章的 task 是在粗线条上说明', '本章的任务是在粗线条上说明'),
    ('低温下磁 order 是', '低温下磁有序是'),
    ('很好地指示磁 order 的类型', '很好地指示磁有序的类型'),
    ('在明确的环境温度' + B, '在明确的温度' + B),
    ('自旋 residing 在两套子晶格上', '自旋位于两套子晶格上'),
])

# ---- 全局残留检查
import glob
for f in glob.glob(os.path.join(BUILD, '*.tex')):
    s = io.open(f, encoding='utf-8').read()
    for w in ('favor', 'energetic', 'residing', ' recall ', 'low 应为'):
        if w in s:
            print('残留!!', os.path.basename(f), repr(w))
print('done')
