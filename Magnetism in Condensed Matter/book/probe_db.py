# -*- coding: utf-8 -*-
"""探查 zcode 会话数据库中被损坏章节文件的内容覆盖情况"""
import sqlite3
import os

DB = os.path.expandvars(r'%USERPROFILE%\.zcode\cli\db\db.sqlite')
con = sqlite3.connect('file:%s?mode=ro' % DB.replace('\\', '/'), uri=True)
cur = con.cursor()

# 每个损坏文件的特征串（该文件必有、且出现在 figure 环境区域附近）
probes = {
    'ch1': '元磁矩',
    'ch2': '抗磁性',
    'ch3': '自旋回波',
    'ch4': '居里温度',
    'ch5': '布里渊',
    'ch6': '灯柱',
    'ch7': '斯托纳',
    'ch8': '自旋阀',
    'appB': '电磁学',
    'appC': '矢量',
    'appD': '公式',
}

for name, probe in probes.items():
    cur.execute(
        "select p.id, p.session_id, length(p.data), substr(p.data,1,80), "
        "p.time_created from part p where p.data like ? order by length(p.data) desc limit 3",
        ('%' + probe + '%',))
    rows = cur.fetchall()
    print('== %s (probe=%s)' % (name, probe))
    for r in rows:
        print('  len=%-8d sess=%s part=%s' % (r[2], r[1][:24], r[0]))
        print('    %s' % r[3].replace('\n', ' ')[:75])
