# -*- coding: utf-8 -*-
"""向工作日志追加 ch7 修复台账"""
import io

p = r'E:\AI整理书籍\磁学\工作日志.md'
log = io.open(p, encoding='utf-8').read()
BS = chr(92)
rows = [
 ('ch7 (7.14)(7.26)', "OCR 将 n_%suparrow 读成 n_*" % BS, "统一为 n_%suparrow" % BS, '上下文'),
 ('ch7 (7.25)', 'K.F. 应为 K.E.（OCR）', '改为 K.E.', '上下文'),
 ('ch7 (7.26)', '%sdot{lambda} 应为 lambda；(n_*-n_d^2) 平方错位' % BS, '改正', '数学自检'),
 ('ch7 (7.23)', 'mu_B 缺平方（对照式 2.28）', '补平方', '式 2.28 对照'),
 ('ch7 (7.44)', 'CJK 幻觉字符（E_一）应为 E_perp', '改为 E_perp', '图 7.8 与上下文'),
 ('ch7 (7.48)', 'hbar omega_c^2 应为 hbar^2 omega_c^2', '补平方', '积分计算复核'),
 ('ch7 正文', '“degeneracy p (eqn 7.41)” 应为 (7.42)', '改为 7.42', 'p 的定义在 7.42'),
 ('ch7 (7.57)', '分母 m 应为 m_e', '改正', '上下文'),
 ('ch7 (7.74)-(7.76)', 'tag 垃圾 {7.7}；块归属错乱', '重排：M_q 两行=7.74，积分恒等式=7.75，孤儿=7.76', '原书编号连续性'),
 ('ch7 7.8 节正文', 'paromagnons 应为 paramagnons（OCR）', '改为顺磁振子', '上下文'),
 ('ch7 习题 (7.99)-(7.116)', 'I1/I2 拆分与后续 tag 整体错位', '按原书重新编号（7.99=I1, 7.100=I2, 7.101=链条, 7.102-7.116 顺延）', '原书编号连续性'),
 ('ch7 习题 (7.113)', 'M=(n_+-n_-)^2 应为 M=mu_B(n_+-n_-)', '改正', '量纲自检'),
 ('ch7 图 7.16(b)', '插图漏提取', '从原书第 160 页扫描裁切 fig7_16b_crop.png', '原书第 160 页'),
]
add = ''.join('| 2026-09-11 | %s | %s | %s | %s |\n' % r for r in rows)
anchor = '| 2026-09-11 | ch6 脚注14 | cos θ≈1−H²/2 应为 1−θ²/2 | 改正 | 数学自检 |'
i = log.find(anchor)
assert i >= 0
j = log.find(NL := chr(10), i) + 1
log = log[:j] + add + log[j:]
io.open(p, 'w', encoding='utf-8').write(log)
print('logged', len(rows))
