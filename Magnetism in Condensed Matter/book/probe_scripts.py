# -*- coding: utf-8 -*-
"""找出所有执行修复脚本的 Bash 命令（不带文件名因此之前漏掉）"""
import json
import os
import sqlite3

DB = os.path.expandvars(r'E:\AI整理书籍\磁学\recovery\db.sqlite')
CUT = 1789232700000
MARKS = ['python fix_', 'python swap_', 'python log_', 'python assemble_',
         'python patch_', 'python gen_', 'python convert_',
         'python check_', 'sed -i']

con = sqlite3.connect('file:%s?mode=ro' % DB.replace('\\', '/'), uri=True)
cur = con.cursor()
cur.execute("select p.time_created, p.data from part p order by p.rowid")
for t, data in cur.fetchall():
    if not data or t >= CUT:
        continue
    try:
        d = json.loads(data)
    except Exception:
        continue
    if d.get('type') != 'tool' or d.get('tool') != 'Bash':
        continue
    cmd = str((d.get('state') or {}).get('input', {}).get('command', ''))
    if '磁学' not in cmd:
        continue
    if not any(m in cmd for m in MARKS):
        continue
    if any(k in cmd for k in ('群论', '李政道', 'build_figs', 'probe_',
                              'recover_', 'extract_inventory')):
        continue
    print('@%d  %s' % (t, cmd[:260].replace('\n', ' ⏎ ')))
