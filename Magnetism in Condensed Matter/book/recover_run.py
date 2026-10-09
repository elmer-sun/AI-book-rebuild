# -*- coding: utf-8 -*-
"""在隔离副本 recovery/build 中重放全部修改命令，然后编译并与事故前 PDF 逐页比对"""
import json
import os
import shutil
import sqlite3
import subprocess
import sys

REC = r'E:\AI整理书籍\磁学\recovery'
BOOK = r'E:\AI整理书籍\磁学\book'
BUILD = os.path.join(REC, 'build')
DB = os.path.join(REC, 'db.sqlite')
FILES = ['ch1.tex', 'ch2.tex', 'ch3.tex', 'ch4.tex', 'ch5.tex', 'ch6.tex',
         'ch7.tex', 'ch8.tex', 'appB.tex', 'appC.tex', 'appD.tex']
CUT = 1789232700000

# ---- 1. 搭建隔离副本
if os.path.exists(BUILD):
    print('删除旧 build ...')
    shutil.rmtree(BUILD)
print('复制 book -> build ...')
shutil.copytree(BOOK, BUILD)

# ---- 2. 用恢复的 tex 覆盖
for fn in FILES:
    src = os.path.join(REC, 'restored', fn)
    if os.path.exists(src):
        shutil.copy(src, os.path.join(BUILD, fn))
        print('restored ->', fn)

# ---- 3. 提取并重放修改命令
con = sqlite3.connect('file:%s?mode=ro' % DB.replace('\\', '/'), uri=True)
cur = con.cursor()
cur.execute("select p.time_created, p.data from part p order by p.rowid")
cmds = []
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
    if not any(fn in cmd for fn in FILES):
        # swap_ch1_figs / fix 脚本调用可能不带文件名，但带脚本名
        if not any(k in cmd for k in ('swap_ch1_figs', 'fix_phantoms',
                                      'fix_fig313', 'fix_ch7_tags',
                                      'fix_ch8.py', 'log_ch7', 'fix_c24',
                                      'fix_F_tags')):
            continue
    if 'xelatex' in cmd and 'python' not in cmd and 'sed -i' not in cmd:
        continue
    if any(k in cmd for k in ('extract_inventory', 'probe_', 'recover_',
                              'strip_en_captions', 'render_all')):
        continue
    cmds.append((t, cmd))
cmds.sort()
print('待重放命令:', len(cmds))

log = open(os.path.join(REC, 'replay_log.txt'), 'w', encoding='utf-8')
for i, (t, cmd) in enumerate(cmds):
    r = subprocess.run(['bash', '-c', cmd], cwd=BUILD,
                       capture_output=True, text=True, errors='replace',
                       timeout=180)
    log.write('#### %d @%d exit=%d\n%s\n' % (i, t, r.returncode, cmd))
    if r.stdout:
        log.write('OUT: ' + r.stdout[:500] + '\n')
    if r.returncode != 0 and r.stderr:
        log.write('ERR: ' + r.stderr[:300] + '\n')
log.close()
print('重放完成，日志 recovery/replay_log.txt')

# ---- 4. 编译
r = subprocess.run('xelatex -interaction=nonstopmode main.tex >/dev/null '
                   '2>&1; xelatex -interaction=nonstopmode main.tex 2>&1 '
                   '| tail -2', cwd=BUILD, shell=True,
                   capture_output=True, text=True, errors='replace',
                   timeout=1200)
print(r.stdout)
