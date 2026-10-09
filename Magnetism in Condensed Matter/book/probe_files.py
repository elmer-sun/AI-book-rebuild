# -*- coding: utf-8 -*-
"""清点数据库中每个损坏文件的全部 Write/Edit/Read 痕迹，评估恢复材料"""
import json
import sqlite3
import os

DB = os.path.expandvars(r'%USERPROFILE%\.zcode\cli\db\db.sqlite')
con = sqlite3.connect('file:%s?mode=ro' % DB.replace('\\', '/'), uri=True)
cur = con.cursor()

FILES = ['ch1.tex', 'ch2.tex', 'ch3.tex', 'ch4.tex', 'ch5.tex', 'ch6.tex',
         'ch7.tex', 'ch8.tex', 'appB.tex', 'appC.tex', 'appD.tex',
         'main.tex', 'symbols.tex', 'answers.tex', 'appE.tex', 'appA.tex',
         'preface.tex']

cur.execute("select p.id, p.session_id, p.time_created, p.data from part p "
            "order by p.time_created")
parts = cur.fetchall()
print('total parts', len(parts))

# 收集 toolUse 调用：data 里带 file_path / content
events = {}   # fname -> list of (time, kind, size, part_id, session)
read_results = {}  # callID -> (size, data)

for pid, sess, t, data in parts:
    if not data:
        continue
    try:
        d = json.loads(data)
    except Exception:
        continue
    tt = d.get('type')
    if tt == 'tool':
        tool = d.get('tool')
        # 工具参数在 d 里：不同 schema，直接字符串搜
        s = data
        for fn in FILES:
            if fn in s:
                kind = tool
                # 估计内容大小
                size = len(s)
                events.setdefault(fn, []).append(
                    (t, kind, size, pid, sess, 'call'))
    elif tt == 'tool_result':
        # 结果：记录 callID -> 大小
        cid = d.get('callID', '')
        read_results[cid] = (len(data), data[:60])

for fn in FILES:
    evs = events.get(fn, [])
    if not evs:
        print('%-10s -- 无记录' % fn)
        continue
    from collections import Counter
    c = Counter(e[1] for e in evs)
    last = evs[-1]
    print('%-10s events=%d %s last_time=%s' % (fn, len(evs), dict(c),
                                               last[0]))

# 找出两个大 Read 结果对应的 callID 与文件
print('\n---- 大 Read 结果定位 ----')
for pid, sess, t, data in parts:
    if not data or len(data) < 50000:
        continue
    try:
        d = json.loads(data)
    except Exception:
        continue
    if d.get('type') in ('tool', 'tool_result'):
        print('%s len=%d type=%s sess=%s head=%s' % (
            pid, len(data), d.get('type'), sess[:24],
            data[60:140].replace('\n', ' ')))
