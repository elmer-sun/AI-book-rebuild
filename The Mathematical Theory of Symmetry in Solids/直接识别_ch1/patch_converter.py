# -*- coding: utf-8 -*-
import io

p = 'convert_ch1.py'
s = io.open(p, encoding='utf-8').read()
BS = chr(92)

# 1. signature + ctx init
if 'def process_block(text, out, ctx=None)' not in s:
    s = s.replace(
        'def process_block(text, out):\n    lines = text.split',
        'def process_block(text, out, ctx=None):\n    if ctx is None:\n        ctx = {}\n    lines = text.split',
    )

# 2. replace fragile reversed-scan detection with explicit ctx state
old_detect = (
    "            opened_minipage = False\n"
    "            for l in reversed(out[-4:]):\n"
    "                if l.startswith('" + BS + "begin{minipage}'):\n"
    "                    opened_minipage = True\n"
    "                    break\n"
    "                if l.strip():\n"
    "                    break\n"
)
new_detect = "            opened_minipage = ctx.get('table', False)\n"
assert old_detect in s, 'detect block not found'
s = s.replace(old_detect, new_detect)

# 3. close minipage and reset state
old_close = (
    "            if opened_minipage:\n"
    "                out.append('" + BS + "end{minipage}')\n"
    "            out.append('" + BS + "medskip')\n"
)
new_close = (
    "            if opened_minipage:\n"
    "                out.append('" + BS + "end{minipage}')\n"
    "                ctx['table'] = False\n"
    "            out.append('" + BS + "medskip')\n"
)
assert old_close in s, 'close block not found'
s = s.replace(old_close, new_close)

# 4. TABLE label branch: set ctx, skip blanks before subtitle
old_label = (
    "            out.append('" + BS + "centering" + BS + "textbf{TABLE ' + m.group(1) + '}')\n"
    "            i += 1\n"
    "            if i < len(lines) and lines[i].strip():\n"
)
new_label = (
    "            out.append('" + BS + "centering" + BS + "textbf{TABLE ' + m.group(1) + '}')\n"
    "            ctx['table'] = True\n"
    "            i += 1\n"
    "            while i < len(lines) and not lines[i].strip():\n"
    "                i += 1\n"
    "            if i < len(lines) and lines[i].strip() and not lines[i].startswith('|'):\n"
)
assert old_label in s, 'label block not found'
s = s.replace(old_label, new_label)

# 5. top-level call passes ctx
s = s.replace('process_block(md, out)', "process_block(md, out, {'table': False})")

io.open(p, 'w', encoding='utf-8', newline='\n').write(s)
print('all patches applied')
