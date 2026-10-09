#!/usr/bin/env python3
"""convert_pdf.py 的本地副本，增加 --insecure 选项。

背景：MinerU Agent API 的解析结果托管在 cdn-mineru.openxlab.org.cn，
该 CDN 的 TLS 证书于 2026-10 前后过期（schannel/requests 均报
CERTIFICATE_VERIFY_FAILED: certificate has expired），导致解析完成后
无法下载 full.md。--insecure 仅对下载已解析结果这一步关闭证书校验
（上传与轮询走 mineru.net 主站，证书正常）。本工作区约定俗成的
MinerU 提取管线因此得以继续；上游修好证书后可去掉 --insecure。

除此之外与官方脚本 convert_pdf.py（C:\\Users\\elmer\\.agents\\skills\\
pdf-to-markdown\\scripts\\）完全一致。
"""

import argparse
import os
import re
import shutil
import sys
import tempfile
import time
from urllib.parse import urlparse

try:
    import requests
    import urllib3
except ImportError:
    print("requests required. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

AGENT_BASE = "https://mineru.net/api/v1/agent"
MAX_PAGES = 20
MAX_MB = 9
POLL_INTERVAL = 3
DEFAULT_TIMEOUT = 600

INSECURE = False  # set by --insecure


def _http_request(method, url, *, desc, timeout=60, json_body=None,
                  data_path=None, attempts=4):
    last_err = None
    for attempt in range(1, attempts + 1):
        try:
            if data_path is not None:
                with open(data_path, "rb") as f:
                    resp = requests.request(method, url, data=f, timeout=timeout,
                                            verify=INSECURE)
            else:
                resp = requests.request(method, url, json=json_body, timeout=timeout,
                                        verify=INSECURE)

            if resp.status_code == 429:
                last_err = RuntimeError("HTTP 429 rate-limited")
                if attempt < attempts:
                    wait = 15 * attempt
                    print(f"    {desc}: rate-limited, retry {attempt}/{attempts - 1} "
                          f"in {wait}s", file=sys.stderr)
                    time.sleep(wait)
                    continue
                break
            if 200 <= resp.status_code < 300:
                return resp
            last_err = RuntimeError(f"HTTP {resp.status_code}: {resp.text[:200]}")
        except (requests.ConnectionError, requests.Timeout) as exc:
            last_err = exc

        if attempt < attempts:
            wait = 5 * attempt
            print(f"    {desc}: attempt {attempt} failed ({last_err}); "
                  f"retrying in {wait}s", file=sys.stderr)
            time.sleep(wait)

    raise RuntimeError(f"{desc} failed after {attempts} attempts: {last_err}")


def _api_json(resp):
    try:
        payload = resp.json()
    except ValueError:
        raise RuntimeError(
            f"non-JSON response (HTTP {resp.status_code}): {resp.text[:200]!r}")
    if isinstance(payload, dict) and payload.get("code") not in (None, 0):
        raise RuntimeError(f"API error {payload.get('code')}: {payload.get('msg')}")
    return payload.get("data", {}) if isinstance(payload, dict) else payload


def _pypdf():
    try:
        from pypdf import PdfReader, PdfWriter
        return PdfReader, PdfWriter
    except ImportError:
        print("pypdf required. Run: pip install pypdf", file=sys.stderr)
        sys.exit(1)


def _write_and_measure(writer, path):
    with open(path, "wb") as out:
        writer.write(out)
    mb = os.path.getsize(path) / (1024 * 1024)
    os.remove(path)
    return mb


def split_pdf(file_path, temp_dir, span=None):
    PdfReader, PdfWriter = _pypdf()
    base = os.path.splitext(os.path.basename(file_path))[0]

    with open(file_path, "rb") as f:
        reader = PdfReader(f)
        total = len(reader.pages)
        first, last = (1, total) if span is None else span
        if last > total:
            raise ValueError(f"page range {first}-{last} exceeds document "
                             f"({total} pages)")
        chunks = []
        start = first
        tmp = os.path.join(temp_dir, "_measure.pdf")

        while start <= last:
            writer = PdfWriter()
            count = 0

            for i in range(start, last + 1):
                test = PdfWriter()
                for p in writer.pages:
                    test.add_page(p)
                test.add_page(reader.pages[i - 1])

                test_mb = _write_and_measure(test, tmp)

                if count + 1 > MAX_PAGES or test_mb > MAX_MB:
                    if count == 0:
                        count = 1
                        writer = test
                        print(f"  Warning: page {i} alone is {test_mb:.1f}MB "
                              f"(API limit is 10MB)", file=sys.stderr)
                    break

                writer = test
                count += 1

            end = start + count - 1
            out_path = os.path.join(temp_dir, f"{base}_p{start}-{end}.pdf")

            with open(out_path, "wb") as out:
                writer.write(out)
            final_mb = os.path.getsize(out_path) / (1024 * 1024)

            chunks.append((out_path, start, end))
            print(f"  chunk: pages {start:>3}-{end:<3}  {count:>2}p  "
                  f"{final_mb:5.1f} MB")
            start = end + 1

    return chunks, total


def _parse_options(opts):
    body = {"language": opts.language}
    if opts.ocr:
        body["is_ocr"] = True
    return body


def _submit_file(file_path, opts):
    body = _parse_options(opts)
    body["file_name"] = os.path.basename(file_path)
    data = _api_json(_http_request("POST", f"{AGENT_BASE}/parse/file",
                                   json_body=body, timeout=30, desc="submit"))
    task_id = data.get("task_id")
    file_url = data.get("file_url")
    if not task_id or not file_url:
        raise RuntimeError(f"submit response missing task_id/file_url: {data}")
    _http_request("PUT", file_url, data_path=file_path,
                  timeout=(30, 600), desc="upload")
    return task_id


def _poll(task_id, timeout_s):
    start = time.time()
    last_state = None
    while time.time() - start < timeout_s:
        data = _api_json(_http_request("GET", f"{AGENT_BASE}/parse/{task_id}",
                                       timeout=30, desc="poll"))
        state = data.get("state", "unknown")
        if state != last_state:
            print(f"    [{int(time.time() - start)}s] {state}")
            last_state = state
        if state == "done":
            md_url = data.get("markdown_url")
            if not md_url:
                raise RuntimeError(f"state=done but markdown_url missing: {data}")
            return _http_request("GET", md_url, timeout=120,
                                 desc="download markdown").text
        if state == "failed":
            raise RuntimeError(
                f"parse failed [{data.get('err_code')}]: {data.get('err_msg')}")
        time.sleep(POLL_INTERVAL)
    raise TimeoutError(f"parse not done after {timeout_s}s "
                       f"(last state: {last_state})")


def convert_chunk(file_path, index, total, opts, timeout_s):
    label = f"[{index}/{total}]" if total > 1 else ""
    name = os.path.basename(file_path)
    try:
        task_id = _submit_file(file_path, opts)
        print(f"  {label} {name} - uploading, parsing...")
        md = _poll(task_id, timeout_s)
        print(f"  {label} {name} - done ({len(md)} chars)")
        return True, md
    except Exception as e:
        print(f"  {label} {name} - FAILED: {e}", file=sys.stderr)
        return False, (f"\n\n> [Chunk {index} (pages shown in marker above): "
                       f"{name} failed - {e}]\n\n")


def _download_pdf(url, dest_dir, attempts=4):
    name = os.path.basename(urlparse(url).path) or "download.pdf"
    if not name.lower().endswith(".pdf"):
        name += ".pdf"
    dest = os.path.join(dest_dir, name)
    last_err = None
    for attempt in range(1, attempts + 1):
        try:
            with requests.get(url, stream=True, timeout=(15, 120),
                              verify=INSECURE) as resp:
                resp.raise_for_status()
                with open(dest, "wb") as f:
                    for block in resp.iter_content(1 << 16):
                        f.write(block)
            return dest
        except (requests.RequestException, OSError) as exc:
            last_err = exc
            if attempt < attempts:
                wait = 5 * attempt
                print(f"    download: attempt {attempt} failed ({exc}); "
                      f"retrying in {wait}s", file=sys.stderr)
                time.sleep(wait)
    raise RuntimeError(f"download failed after {attempts} attempts: {last_err}")


def _parse_pages(text):
    if not text:
        return None
    m = re.fullmatch(r"(\d+)(?:-(\d+))?", text.strip())
    if not m:
        raise ValueError(f"bad --pages value {text!r}: use 'N' or 'A-B'")
    first = int(m.group(1))
    last = int(m.group(2) or first)
    if first < 1 or last < first:
        raise ValueError(f"bad --pages value {text!r}")
    return (first, last)


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="PDF to Markdown via MinerU Agent API (local copy, --insecure)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("input", nargs="?", help="PDF file path")
    group.add_argument("--url", help="PDF URL (downloaded, then converted)")
    parser.add_argument("--output", "-o", help="Output .md path "
                        "(default: <input>.md next to the PDF)")
    parser.add_argument("--pages", help="Page range to convert, e.g. 7 or 3-14")
    parser.add_argument("--language", default="en",
                        help="Document language hint (default: en; use ch for Chinese)")
    parser.add_argument("--ocr", action="store_true",
                        help="Enable OCR for scanned/image-only PDFs")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT,
                        help=f"Per-chunk parse timeout in seconds "
                             f"(default: {DEFAULT_TIMEOUT})")
    parser.add_argument("--keep-temp", action="store_true",
                        help="Keep temp chunk files for debugging")
    parser.add_argument("--insecure", action="store_true",
                        help="Disable TLS verification (for expired-cert CDN)")
    args = parser.parse_args()

    global INSECURE
    INSECURE = args.insecure
    if INSECURE:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        span = _parse_pages(args.pages)
    except ValueError as e:
        print(str(e), file=sys.stderr)
        sys.exit(1)

    temp_dir = tempfile.mkdtemp(prefix="pdf2md_")
    try:
        if args.input:
            pdf_path = args.input
            if not os.path.isfile(pdf_path):
                print(f"File not found: {pdf_path}", file=sys.stderr)
                sys.exit(1)
            output_path = args.output or (os.path.splitext(pdf_path)[0] + ".md")
        else:
            print(f"Downloading {args.url} ...")
            pdf_path = _download_pdf(args.url, temp_dir)
            default_name = os.path.splitext(os.path.basename(pdf_path))[0] + ".md"
            output_path = args.output or default_name

        out_dir = os.path.dirname(os.path.abspath(output_path))
        os.makedirs(out_dir, exist_ok=True)

        total_mb = os.path.getsize(pdf_path) / (1024 * 1024)
        print(f"PDF: {total_mb:.1f}MB")

        print("Splitting...")
        chunks, _ = split_pdf(pdf_path, temp_dir, span)
        print(f"{len(chunks)} chunks total\n")

        results = []
        for i, (chunk_path, p_start, p_end) in enumerate(chunks, 1):
            print(f"-- Chunk {i}/{len(chunks)}  pages {p_start}-{p_end} --")
            ok, text = convert_chunk(chunk_path, i, len(chunks),
                                     args, args.timeout)
            results.append((ok, text, p_start, p_end))

        parts = []
        for ok, text, p_start, p_end in results:
            if len(results) > 1:
                parts.append(f"<!-- pages {p_start}-{p_end} -->")
            parts.append(text)
        merged = "\n\n".join(parts)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(merged)

        failed = [r for r in results if not r[0]]
        print(f"\nSaved: {output_path}  ({len(merged)} chars)")
        print(f"Summary: {len(results) - len(failed)} chunk(s) OK, "
              f"{len(failed)} failed")
        if failed:
            ranges = ", ".join(f"{s}-{e}" for _, _, s, e in failed)
            print(f"Failed page ranges: {ranges}", file=sys.stderr)
            sys.exit(2)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if args.keep_temp:
            print(f"Temp files kept: {temp_dir}")
        else:
            shutil.rmtree(temp_dir, ignore_errors=True)
            if os.path.exists(temp_dir):
                print(f"Warning: could not fully remove temp dir {temp_dir} "
                      f"- delete it manually", file=sys.stderr)


if __name__ == "__main__":
    main()
