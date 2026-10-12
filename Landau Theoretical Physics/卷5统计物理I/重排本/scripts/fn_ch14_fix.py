# -*- coding: utf-8 -*-
"""ch14 脚注转录补充：最后 2 处（#26 p419、#70 p450）"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

P = r'chapters\ch14.tex'
t = open(P, encoding='utf-8').read()

reps = [
("（或者 $\\delta\\rho=\\eta(\\varphi_1-\\varphi_2)/\\sqrt{2}$，结果相同）①",
 "在两种情形下 $\\gamma_1$ 和 $\\gamma_2$ 只不过是数，这是由于 $\\Phi$ 中只有一项（依赖于 $\\gamma_1,\\gamma_2$）.如果有多个不同的四次不变式，则使 $\\Phi$ 取极小的一组 $\\gamma_i$ 中某些会依赖于P，T."),
("只依赖于微商 $(\\partial P/\\partial V)_T$ 变为零①",
 "热力学量作为变量P，T的函数，这时可有由于变量变换的雅可比式变为零而引起的奇异性."),
]
for anchor, text in reps:
    new = anchor[:-1] + '\\footnote{' + text + '}'
    c = t.count(anchor)
    print('count', c, anchor[:24])
    assert c == 1
    t = t.replace(anchor, new)
open(P, 'w', encoding='utf-8', newline='\n').write(t)
left = sum(t.count(m) for m in '①②③④')
print('剩余圈码(含注释):', left)
print('footnote 总数:', t.count('\\footnote{'))
