# -*- coding: utf-8 -*-
"""从冻结数据库重放文件历史，恢复被 strip_en_captions.py 破坏的章节文件。

策略：取该文件最后一次完整 Write（或今天的全文件 Read 输出）作为基底，
按时间顺序重放其后的 Edit（old->new，需命中验证），列出其后 Bash 中
涉及文件修改的脚本调用（单独人工处理）。
"""
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

calls = {}
rows_iter = cur.fetchall()
for pid, sess, t, data in rows_iter:
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

events = []   # (time, tool, file, payload)
for cid, c in calls.items():
    use = c.get('use') or {}
    tool = use.get('tool', '')
    st = use.get('state', {}) or {}
    inp = st.get('input', {}) or {}
    out = st.get('output', '')
    if not isinstance(out, str):
        out = json.dumps(out, ensure_ascii=False)
    fp = inp.get('file_path', '')
    base = os.path.basename(fp)
    if tool in ('Write', 'Edit') and base in FILES:
        events.append((c.get('time', 0), tool, base, inp, c.get('sess', '')))
    elif tool == 'Read' and base in FILES and len(out) > 20000:
        events.append((c.get('time', 0), 'Read', base,
                       {'content': out}, c.get('sess', '')))

events.sort(key=lambda x: x[0])

for fn in FILES:
    evs = [e for e in events if e[2] == fn]
    if not evs:
        print('%-9s 无事件' % fn)
        continue
    # 基底：最后一次 Write 或 Read（取内容更大的）
    base = None
    base_t = None
    base_kind = None
    for t, tool, f, inp, sess in evs:
        if tool in ('Write', 'Read'):
            content = inp.get('content', '')
            if base is None or (tool == 'Write') or len(content) > len(base):
                # Write 优先于 Read（Read 可能带行号），同为 Write 取最后
                if tool == 'Write' or base is None:
                    base, base_t, base_kind = content, t, tool
                elif len(content) > len(base):
                    base, base_t, base_kind = content, t, tool
    print('== %s 基底: %s @%d (%d chars)' % (fn, base_kind, base_t,
                                             len(base)))
    if base_kind == 'Read':
        # Read 输出带 "cat -n" 行号前缀，需要剥掉
        lines = []
        for ln in base.split('\n'):
            if ln[:1] == ' ' and '→' not in ln[:20]:
                pass
            # Read 输出格式: "   12\t内容"
            i = ln.find('\t')
            if 0 < i <= 8 and ln[:i].strip().isdigit():
                lines.append(ln[i + 1:])
            else:
                lines.append(ln)
        base = '\n'.join(lines)
    # 重放其后的 Edit
    n_ok = n_fail = 0
    for t, tool, f, inp, sess in evs:
        if t <= base_t:
            continue
        if tool == 'Edit':
            old = inp.get('old_string', '')
            new = inp.get('new_string', '')
            if old and old in base:
                base = base.replace(old, new, 1)
                n_ok += 1
            else:
                n_fail += 1
                print('   !! Edit 未命中 @%d old[:60]=%r' % (t, old[:60]))
    print('   重放 Edit: 成功 %d, 未命中 %d, 最终 %d chars' %
          (n_ok, n_fail, len(base)))
    outp = os.path.join(OUT, fn)
    with open(outp, 'w', encoding='utf-8', newline='\n') as fh:
        fh.write(base)
    # 列出基底之后涉及该文件的 Bash 脚本事件（可能未被重放）
    print('   （其后的脚本调用需人工核对，见 recover_extract 时间线）')
