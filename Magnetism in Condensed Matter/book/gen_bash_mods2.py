# -*- coding: utf-8 -*-
"""生成修改类 Bash 命令清单（含 python 脚本调用），排除事故后命令"""
import json
import os
import sqlite3

DB = os.path.expandvars(r'E:\AI整理书籍\磁学\recovery\db.sqlite')
FILES = ['ch1.tex', 'ch2.tex', 'ch3.tex', 'ch4.tex', 'ch5.tex', 'ch6.tex',
         'ch7.tex', 'ch8.tex', 'appB.tex', 'appC.tex', 'appD.tex']
CUT = 1789232700000  # strip 事故时刻，之后的命令一律排除
EXCLUDE = ('extract_inventory', 'probe_', 'recover_', 'strip_en_captions',
           'render_all', 'build_figs', 'fig_src')

con = sqlite3.connect('file:%s?mode=ro' % DB.replace('\\', '/'), uri=True)
cur = con.cursor()
cur.execute("select p.time_created, p.data from part p order by p.rowid")
out = []
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
    hit = [fn for fn in FILES if fn in cmd]
    if not hit:
        continue
    if 'xelatex' in cmd and 'python' not in cmd and 'sed -i' not in cmd:
        continue
    if any(k in cmd for k in EXCLUDE) and 'swap_ch1_figs' not in cmd:
        continue
    out.append((t, hit[0], cmd))
out.sort()
with open(r'..\recovery\bash_mods2.txt', 'w', encoding='utf-8') as f:
    for t, fn, cmd in out:
        f.write('@%d [%s]\n%s\n----\n' % (t, fn, cmd))
print('commands:', len(out))
