# -*- coding: utf-8 -*-
"""列出数据库中对目标文件的修改类 Bash 命令（sed/python/cp 重定向等）"""
import json
import os
import re
import sqlite3

DB = os.path.expandvars(r'E:\AI整理书籍\磁学\recovery\db.sqlite')
FILES = ['ch1.tex', 'ch2.tex', 'ch3.tex', 'ch4.tex', 'ch5.tex', 'ch6.tex',
         'ch7.tex', 'ch8.tex', 'appB.tex', 'appC.tex', 'appD.tex']
MOD_PAT = re.compile(
    r"sed -i|> *[A-Za-z0-9_]+\.(tex|py)|python +\S*\.py|mv |cp |rename",
    re.I)

con = sqlite3.connect('file:%s?mode=ro' % DB.replace('\\', '/'), uri=True)
cur = con.cursor()
cur.execute("select p.id, p.session_id, p.time_created, p.data from part p "
            "order by p.rowid")

seen = set()
for pid, sess, t, data in cur.fetchall():
    if not data:
        continue
    try:
        d = json.loads(data)
    except Exception:
        continue
    if d.get('type') != 'tool' or d.get('tool') != 'Bash':
        continue
    inp = (d.get('state', {}) or {}).get('input', {}) or {}
    cmd = inp.get('command', '')
    if not MOD_PAT.search(cmd):
        continue
    for fn in FILES:
        if fn in cmd and (pid, fn) not in seen:
            seen.add((pid, fn))
            print('@%d [%s] %s' % (t, fn, cmd[:400].replace('\n', ' ⏎ ')))
            break
