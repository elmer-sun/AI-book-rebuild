# -*- coding: utf-8 -*-
"""重放 v2：只接受 file_path / 命令中带 磁学 的操作，重建各损坏文件"""
import json
import os
import sqlite3
import sys

DB = os.path.expandvars(r'E:\AI整理书籍\磁学\recovery\db.sqlite')
OUT = r'E:\AI整理书籍\磁学\recovery\restored'
os.makedirs(OUT, exist_ok=True)

FILES = sys.argv[1:] or ['ch1.tex', 'ch2.tex', 'ch3.tex', 'ch4.tex',
                         'ch5.tex', 'ch6.tex', 'ch7.tex', 'ch8.tex',
                         'appB.tex', 'appC.tex', 'appD.tex']

con = sqlite3.connect('file:%s?mode=ro' % DB.replace('\\', '/'), uri=True)
cur = con.cursor()
cur.execute("select p.id, p.session_id, p.time_created, p.data from part p "
            "order by p.rowid")
rows = cur.fetchall()

calls = {}
for pid, sess, t, data in rows:
    if not data:
        continue
    try:
        d = json.loads(data)
    except Exception:
        continue
    if d.get('type') == 'tool':
        c = calls.setdefault(d.get('callID'), {})
        c['use'] = d
        c['time'] = t
        c['sess'] = sess
    elif d.get('type') == 'tool_result':
        c = calls.setdefault(d.get('callID'), {})
        c['result'] = d
        c.setdefault('time', t)

events = []
bash_mods = []
for cid, c in calls.items():
    use = c.get('use') or {}
    tool = use.get('tool', '')
    st = use.get('state', {}) or {}
    inp = st.get('input', {}) or {}
    out = st.get('output', '')
    if not isinstance(out, str):
        out = ''
    fp = str(inp.get('file_path', ''))
    if tool in ('Write', 'Edit', 'Read') and '磁学' in fp:
        base = os.path.basename(fp)
        if base in FILES:
            if tool == 'Write':
                events.append((c.get('time', 0), 'Write', base,
                               inp.get('content', '')))
            elif tool == 'Edit':
                events.append((c.get('time', 0), 'Edit', base, inp))
            elif tool == 'Read' and len(out) > 20000:
                events.append((c.get('time', 0), 'Read', base,
                               {'content': out}))
    elif tool == 'Bash':
        cmd = str(inp.get('command', ''))
        if '磁学' in cmd:
            for fn in FILES:
                if fn in cmd and any(
                        k in cmd for k in ('sed -i', '.write(', "open('w'",
                                           '> ' + fn, 'shutil.copy', 'cp ')):
                    bash_mods.append((c.get('time', 0), fn, cmd))
                    break

events.sort(key=lambda x: x[0])
bash_mods.sort(key=lambda x: x[0])

with open(os.path.join(OUT, '..', 'bash_mods_cidian.txt'), 'w',
          encoding='utf-8') as bf:
    for t, fn, cmd in bash_mods:
        bf.write('@%d [%s]\n%s\n\n' % (t, fn, cmd))

for fn in FILES:
    evs = [e for e in events if e[2] == fn]
    base = None
    base_t = 0
    base_kind = None
    for t, tool, f, payload in evs:
        if tool == 'Write':
            if base is None or t > base_t:
                pass
        # 选内容最长的 Write/Read（Write 时间新者优先；Read 视为最终快照）
        if tool == 'Write':
            content = payload if isinstance(payload, str) else ''
            if base is None or len(content) >= len(base):
                if base is None or base_kind == 'Write' or \
                        len(content) > len(base):
                    base, base_t, base_kind = content, t, 'Write'
        elif tool == 'Read':
            content = payload.get('content', '')
            if base is None or t > base_t:
                base, base_t, base_kind = content, t, 'Read'
    if base is None:
        print('%-9s 无基底!' % fn)
        continue
    if base_kind == 'Read':
        lines = []
        for ln in base.split('\n'):
            i = ln.find('\t')
            if 0 < i <= 8 and ln[:i].strip().isdigit():
                lines.append(ln[i + 1:])
            else:
                lines.append(ln)
        base = '\n'.join(lines)
    n_ok = n_fail = 0
    for t, tool, f, payload in evs:
        if tool != 'Edit' or t <= base_t:
            continue
        old = payload.get('old_string', '')
        new = payload.get('new_string', '')
        if old and old in base:
            base = base.replace(old, new, 1)
            n_ok += 1
        else:
            n_fail += 1
            print('   !! %s Edit未命中 @%d old[:50]=%r' % (fn, t, old[:50]))
    print('%-9s 基底=%s@%d(%d) Edit:%d成功/%d未命中 -> %d chars' % (
        fn, base_kind, base_t, len(base), n_ok, n_fail, len(base)))
    with open(os.path.join(OUT, fn), 'w', encoding='utf-8',
              newline='\n') as fh:
        fh.write(base)
