# -*- coding: utf-8 -*-
"""从 zcode 会话数据库提取被损坏 tex 文件的完整操作时间线与内容快照"""
import json
import os
import sqlite3

DB = os.path.expandvars(r'E:\AI整理书籍\磁学\recovery\db.sqlite')
OUT = r'E:\AI整理书籍\磁学\recovery'
FILES = ['ch1.tex', 'ch2.tex', 'ch3.tex', 'ch4.tex', 'ch5.tex', 'ch6.tex',
         'ch7.tex', 'ch8.tex', 'appB.tex', 'appC.tex', 'appD.tex']

con = sqlite3.connect('file:%s?mode=ro' % DB.replace('\\', '/'), uri=True)
cur = con.cursor()
cur.execute("select p.id, p.session_id, p.time_created, p.data from part p "
            "order by p.rowid")
rows = cur.fetchall()

calls = {}   # callID -> dict(use=..., result=...)
for pid, sess, t, data in rows:
    if not data:
        continue
    try:
        d = json.loads(data)
    except Exception:
        continue
    tt = d.get('type')
    if tt == 'tool':
        cid = d.get('callID')
        c = calls.setdefault(cid, {})
        c['use'] = d
        c['time'] = t
        c['sess'] = sess
    elif tt == 'tool_result':
        cid = d.get('callID')
        c = calls.setdefault(cid, {})
        c['result'] = d
        c.setdefault('time', t)

summary = {}
for cid, c in calls.items():
    use = c.get('use', {})
    tool = use.get('tool', '')
    inp = use.get('state', {}).get('input', {}) or {}
    res = c.get('result', {})
    rout = res.get('state', {}).get('output', '') or ''
    if isinstance(rout, dict):
        rout = str(rout)
    # 目标文件
    fp = inp.get('file_path') or inp.get('notebook_path') or ''
    base = os.path.basename(fp) if fp else ''
    cmd = inp.get('command', '') if tool == 'Bash' else ''
    for fn in FILES:
        hit = None
        if base == fn:
            hit = 'file'
        elif tool == 'Bash' and fn in cmd:
            hit = 'cmd'
        elif tool in ('Write', 'Edit') and fn in json.dumps(inp, ensure_ascii=False):
            hit = 'file'
        if not hit:
            continue
        entry = {
            'time': c.get('time', 0),
            'sess': c.get('sess', '')[:40],
            'tool': tool,
            'kind': hit,
            'size_use': len(json.dumps(inp, ensure_ascii=False)),
            'size_out': len(rout) if hit == 'file' and base == fn and tool == 'Read' else 0,
        }
        if tool == 'Write':
            content = inp.get('content', '')
            entry['content_len'] = len(content)
            entry['head'] = content[:50].replace('\n', ' ')
        if tool == 'Edit':
            entry['old_len'] = len(inp.get('old_string', ''))
            entry['new_len'] = len(inp.get('new_string', ''))
        if tool == 'Read':
            entry['out_len'] = len(rout)
            entry['out_head'] = rout[:50].replace('\n', ' ')
        summary.setdefault(fn, []).append(entry)

for fn in FILES:
    evs = sorted(summary.get(fn, []), key=lambda x: x['time'])
    print('=' * 20, fn, len(evs), 'events')
    for e in evs:
        extra = ''
        if 'content_len' in e:
            extra = ' WRITE %d chars | %s' % (e['content_len'], e['head'])
        elif 'old_len' in e:
            extra = ' EDIT old=%d new=%d' % (e['old_len'], e['new_len'])
        elif e['tool'] == 'Read':
            extra = ' READ out=%d | %s' % (e.get('out_len', 0),
                                           e.get('out_head', ''))
        elif e['kind'] == 'cmd':
            extra = ' (bash mentions)'
        print('  %s %-8s %-6s%s' % (e['time'], e['tool'], e['kind'], extra))

# 把两个今天的大 Read 结果完整导出
print('\n==== 导出大 Read 结果 ====')
for cid, c in calls.items():
    use = c.get('use', {})
    if use.get('tool') != 'Read':
        continue
    rout = c.get('result', {}).get('state', {}).get('output', '') or ''
    if len(rout) > 40000:
        fp = use.get('state', {}).get('input', {}).get('file_path', '?')
        safe = os.path.basename(fp).replace('.', '_')
        outp = os.path.join(OUT, 'read_result_%s.txt' % safe)
        with open(outp, 'w', encoding='utf-8') as f:
            f.write(rout)
        print('%s -> %s (%d chars)' % (fp, outp, len(rout)))
