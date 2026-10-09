# -*- coding: utf-8 -*-
"""Assemble ch1.md from per-page files, with cross-page paragraph stitching.
Stitch rule: if the last non-empty line of page N ends mid-sentence (no sentence-
final punctuation) and the first non-empty line of page N+1 starts lowercase,
join them into one paragraph (original page breaks are not paragraph breaks)."""
import io, glob, re

files = sorted(glob.glob('md/p0[1-6]*.md'))
assert len(files) == 50, files

pages = [io.open(f, encoding='utf-8').read().strip() for f in files]
pages = [re.sub(r'<!--.*?-->', '', p, flags=re.S).strip() for p in pages]

SENT_END = tuple('.!?;:)”’*')  # allow closing quotes/italics right after punctuation

stitched = 0
for i in range(len(pages) - 1):
    a = pages[i].rstrip()
    b = pages[i + 1].lstrip()
    la = a.split('\n')[-1].strip()
    lb = b.split('\n')[0].strip()
    if not la or not lb:
        continue
    # only plain text paragraph lines
    if la.startswith(('|', '>', '#', '!', '-', '‡', '§', '脚注', '---', 'FIG.', '**TABLE', '\x02')):
        continue
    if lb.startswith(('|', '>', '#', '!', '-', '‡', '§', '脚注', '---', 'FIG.', '**TABLE')):
        continue
    ends_open = not la.endswith(SENT_END) and not la.endswith('.')
    starts_lower = lb[:1].islower() or lb[:1].isdigit()
    if ends_open and starts_lower:
        print('stitch:', repr(la[-40:]), '+', repr(lb[:40]))
        a = a[: a.rfind(la)] + la  # keep trailing newlines stripped
        pages[i] = a
        pages[i + 1] = b[b.index(lb) + len(lb):].lstrip('\n')
        pages[i + 1] = (pages[i + 1] if pages[i + 1] else '')
        # join: append first line of next page to last line of this page
        pages[i] = a + ' ' + lb
        stitched += 1

doc = '\n\n'.join(p for p in pages if p) + '\n'
# global notation fixes
doc = doc.replace('\\mathbf{\\Gamma}', '\\boldsymbol{\\Gamma}')
io.open('ch1.md', 'w', encoding='utf-8', newline='\n').write(doc)
print('ch1.md rebuilt; paragraphs stitched across pages:', stitched)
print('chars:', len(doc))
