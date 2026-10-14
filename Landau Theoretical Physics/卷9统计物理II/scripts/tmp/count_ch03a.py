import io, re, collections
s = io.open(r'E:\AI整理书籍\朗道理论物理教程\卷9统计物理II\重排本\chapters\ch03a.tex', encoding='utf-8').read()
b_eq = len(re.findall(r'\\begin\{equation\}', s))
b_eqs = len(re.findall(r'\\begin\{equation\*\}', s))
labels = re.findall(r'\\label\{([^}]*)\}', s)
secs = re.findall(r'\\section\{', s)
circ = re.findall(r'[\u2460\u2461\u2462]', s)
lines_c = [l for l in s.splitlines() if re.search(r'[\u2460\u2461\u2462]', l)]
dup = [k for k, v in collections.Counter(labels).items() if v > 1]
print('equation (numbered):', b_eq)
print('equation*          :', b_eqs)
print('total displays     :', b_eq + b_eqs)
print('labels             :', len(labels))
print('sections           :', len(secs))
print('circled marks      :', len(circ))
print('lines w/ circles   :', len(lines_c))
print('dup labels         :', dup)
nums = sorted(labels)
print('labels first/last  :', nums[0], nums[-1])
