# 渲染全书页面 PNG 供视觉验收 (130dpi 灰度)
import pymupdf, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..'))
OUT = os.path.join(ROOT, 'render')
os.makedirs(OUT, exist_ok=True)
doc = pymupdf.open(os.path.join(ROOT, 'main.pdf'))
for i, page in enumerate(doc):
    pix = page.get_pixmap(dpi=130, colorspace=pymupdf.csGRAY)
    pix.save(os.path.join(OUT, 'p%03d.png' % (i + 1)))
doc.close()
print('rendered', len(os.listdir(OUT)), 'pages ->', OUT)
