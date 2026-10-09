# -*- coding: utf-8 -*-
"""列出数据库中所有针对目标文件的 Write/Edit 工具调用明细 + 两个大 Read 的指向"""
import json
import os
import sqlite3

DB = os.path.expandvars(r'E:\AI整理书籍\磁学\recovery\db.sqlite')
FILES = ['ch1.tex', 'ch2.tex', 'ch3.tex', 'ch4.tex', 'ch5.tex', 'ch6.tex',
         'ch7.tex', 'ch8.tex', 'appB.tex', 'appC.tex', 'appD.tex']

con = sqlite3.connect('file:%s?mode=ro' % DB.replace('\\', '/'), uri=True)
cur = con.cursor()
cur.execute("select p.id, p.session_id, p.time_created, p.data from part p "
            "order by p.rowid")

for pid, sess, t, data in cur.fetchall():
    if not data:
        continue
    try:
        d = json.loads(data)
    except Exception:
        continue
    if d.get('type') != 'tool':
        continue
    tool = d.get('tool', '')
    st = d.get('state', {}) or {}
    inp = st.get('input', {}) or {}
    out = st.get('output', '')
    fp = inp.get('file_path', '')
    base = os.path.basename(fp) if fp else ''
    if tool == 'Write' and base in FILES:
        content = inp.get('content', '')
        print('WRITE %-9s @%d len=%-7d head=%r' % (
            base, t, len(content), content[:40].replace('\n', ' ')))
    elif tool == 'Read' and len(str(out)) > 30000:
        print('READ  %-9s @%d out_len=%-7d out_head=%r' % (
            base or '?', t, len(str(out)),
            str(out)[:60].replace('\n', ' ')))
