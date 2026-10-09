# -*- coding: utf-8 -*-
# 1) ch7: 移除 enlargethispage hack
s = open('ch7.tex', encoding='utf-8').read()
bs = chr(92)
hack = bs + 'enlargethispage{-' + bs + 'baselineskip}' + '\n'
if hack in s:
    s = s.replace(hack, '')
    print('ch7 hack removed')
open('ch7.tex', 'w', encoding='utf-8').write(s)

# 2) main.tex: 加 raggedbottom（消除 flushbottom 垂直拉伸空洞）
m = open('main.tex', encoding='utf-8').read()
if 'raggedbottom' not in m:
    marker = bs + 'setstretch{1.18}'
    m = m.replace(marker, marker + '\n' + bs + 'raggedbottom')
    open('main.tex', 'w', encoding='utf-8').write(m)
    print('raggedbottom added')
