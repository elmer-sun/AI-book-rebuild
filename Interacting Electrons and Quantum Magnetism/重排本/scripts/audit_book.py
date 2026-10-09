# -*- coding: utf-8 -*-
"""全书程序审计：
1) 各章 tex 的 \\tag 计数 vs 源 md 的 tag 计数
2) tag 唯一性
3) 残留 markdown/英文占位检查
"""
import re, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CH = os.path.join(ROOT, 'chapters')
MD = os.path.join(ROOT, 'md')

# (tex文件, 源md文件列表)
UNITS = [
    ('ch01', ['ch01']), ('ch02', ['ch02']), ('ch03', ['ch03']),
    ('ch04', ['ch04']), ('ch05', ['ch05']), ('ch06', ['ch06']),
    ('ch07', ['ch07']), ('ch08', ['ch08']), ('ch09', ['ch09']),
    ('ch10', ['ch10']), ('ch11', ['ch11']), ('ch12', ['ch12']),
    ('ch13', ['ch13']), ('ch14', ['ch14']), ('ch15', ['ch15']),
    ('ch16', ['ch16']), ('ch17', ['ch17']), ('ch18', ['ch18_f1', 'ch18_f2']),
    ('ch19', ['ch19']),
    ('appA', ['appA']), ('appB', ['appB']), ('appC', ['appC']),
    ('appD', ['appD']), ('appE', ['appE']),
]

def tags_in(text):
    out = []
    for m in re.finditer(r'\\tag\s*\{([^}]*)\}', text):
        out.append(m.group(1).strip())
    return out

all_tags = {}
problems = []
for tex, mds in UNITS:
    t = open(os.path.join(CH, tex + '.tex'), encoding='utf-8').read()
    tt = tags_in(t)
    src_tags = []
    for m in mds:
        s = open(os.path.join(MD, m + '.md'), encoding='utf-8').read()
        src_tags += tags_in(s)
    # 源里损坏的 tag（如 \tag {5.} 或 \tag {1}\tag{5.52}）先清理出合法编号
    valid = []
    for tg in src_tags:
        for part in tg.split('}'):
            part = part.strip()
            if re.match(r'^\d+\.\d+$', part) or re.match(r'^[A-E]\.\d+$', part):
                valid.append(part)
    # tex 侧同样只留合法编号
    tt_valid = [x for x in tt if re.match(r'^\d+\.\d+$', x) or re.match(r'^[A-E]\.\d+$', x)]
    dup = [x for x in set(tt_valid) if tt_valid.count(x) > 1]
    missing = sorted(set(valid) - set(tt_valid))
    extra = sorted(set(tt_valid) - set(valid))
    status = 'OK'
    if dup or missing or extra:
        status = 'CHECK'
        problems.append((tex, dup, missing, extra))
    print('%-6s tex=%3d valid_src=%3d  %s' % (tex, len(tt_valid), len(set(valid)), status))

print()
if problems:
    for tex, dup, missing, extra in problems:
        print('==', tex)
        if dup: print('  重复:', dup)
        if missing: print('  缺失:', missing)
        if extra: print('  多出:', extra)
else:
    print('全部编号一一对应')

# 残留检查
print()
BAD = ['\\begin{array}{r c l}', '<table', '](', '```', '\\tag {', '\\quad , \\quad']
for tex, _ in UNITS:
    t = open(os.path.join(CH, tex + '.tex'), encoding='utf-8').read()
    for b in BAD:
        if b in t:
            print('残留 %-6s: %r' % (tex, b))
# 疑似漏译英文段落（长英文句子）
print()
for tex, _ in UNITS:
    t = open(os.path.join(CH, tex + '.tex'), encoding='utf-8').read()
    for line in t.split('\n'):
        ln = re.sub(r'\\[a-zA-Z]+', '', line)
        ln = re.sub(r'\$[^$]*\$', '', ln)
        words = re.findall(r'[A-Za-z]{4,}', ln)
        if len(words) >= 6 and not re.match(r'^\s*%', line) and 'item' not in line:
            print('疑似英文 %-6s: %s' % (tex, line.strip()[:90]))
