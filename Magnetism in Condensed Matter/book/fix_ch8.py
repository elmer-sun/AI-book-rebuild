# -*- coding: utf-8 -*-
"""ch8.tex 清理：ET 脚注改回 \fn{4}、删 MEM 重复边注、清残留英文"""
import io

p = r'E:\AI整理书籍\磁学\book\ch8.tex'
s = io.open(p, encoding='utf-8').read()
BS = '\\'

# 1) ET 自动脚注 -> \fn{4}
old = ('基于有机分子 ET' + BS + 'footnote{ET 是 BEDT-TTF 的缩写，而 BEDT-TTF 又是' + BS + 'n'
       'bis-ethylenedithiotetrathiafulvalene（双亚乙基二硫代四硫富瓦烯）的缩写。}的一族')
new = '基于有机分子 ET' + BS + 'fn{4}{ET 是 BEDT-TTF 的缩写，而 BEDT-TTF 又是 bis-ethylenedithiotetrathiafulvalene（双亚乙基二硫代四硫富瓦烯）的缩写。}的一族'
if old in s:
    s = s.replace(old, new)
else:
    # 宽松匹配
    import re
    pat = re.compile(r'基于有机分子 ET' + re.escape(BS) + r'footnote\{[^}]*\}的一族')
    s2 = pat.sub(new, s)
    assert s2 != s, 'ET footnote pattern not found'
    s = s2

# 2) 删除 MEM 的重复边注（保留 \fn{1}）
dup = (BS + 'end{figure}' + BS + 'mnote{MEM、TCNQ 与 TTF 是具有冗长化学名称的有机分子。}')
if dup in s:
    s = s.replace(dup, BS + 'end{figure}')

# 3) 残留英文清理
s = s.replace('长程磁 order', '长程磁有序')
s = s.replace('摧毁铁磁 order', '摧毁铁磁有序')
s = s.replace('definitive 理论', '公认的理论')
s = s.replace('segregated 成条纹（stripes）', '分凝成条纹（stripes）')
s = s.replace('又是又一个 red herring', '还是又一个转移视线的干扰项')
s = s.replace('还是又一个 red herring', '还是又一个转移视线的干扰项')
s = s.replace('favor 大的耦合', '有利于大的耦合')

io.open(p, 'w', encoding='utf-8').write(s)

import re
leftover = re.findall(r'[a-zA-Z]{3,}(?![}a-zA-Z])', ' '.join([
    seg for seg in s.split('$') if not seg.startswith(BS + '')
]))
print('mnote dup removed:', dup not in s)
print('fn4 fixed:', BS + 'fn{4}{ET' in s)
