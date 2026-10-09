#!/bin/bash
# 批量 MinerU 提取剩余各章（顺序提交，避开 per-IP 限流；已完成的跳过）
cd "E:/AI整理书籍/齐曼/MinerU" || exit 1
PY="C:/Users/elmer/AppData/Local/Programs/Python/Python313/python.exe"
SCRIPT="E:/AI整理书籍/齐曼/scripts/convert_pdf_local.py"

declare -A FILES=(
  [ch02]="../章节拆分/02_格波_p041-090.pdf"
  [ch03]="../章节拆分/03_电子态_p091-132.pdf"
  [ch04]="../章节拆分/04_固体的静态性质_p133-159.pdf"
  [ch05]="../章节拆分/05_电子间相互作用_p160-184.pdf"
  [ch06]="../章节拆分/06_电子动力学_p185-224.pdf"
  [ch07]="../章节拆分/07_输运性质_p225-268.pdf"
  [ch08]="../章节拆分/08_光学性质_p269-305.pdf"
  [ch09]="../章节拆分/09_费米面_p306-342.pdf"
  [ch10]="../章节拆分/10_磁性_p343-388.pdf"
  [ch11]="../章节拆分/11_超导电性_p389-428.pdf"
  [ch12]="../章节拆分/12_文献目录_p429-438.pdf"
  [ch13]="../章节拆分/13_索引_p439-451.pdf"
)

ORDER="ch02 ch03 ch04 ch05 ch06 ch07 ch08 ch09 ch10 ch11 ch12 ch13"

for key in $ORDER; do
  f="${FILES[$key]}"
  if [ -s "$key.md" ]; then
    echo "== $key already done, skip"
    continue
  fi
  echo "== $key start: $(date +%H:%M:%S)"
  "$PY" "$SCRIPT" "$f" --ocr --insecure -o "$key.md" --timeout 900
  echo "== $key exit=$?"
done
echo "== ALL DONE $(date +%H:%M:%S)"
