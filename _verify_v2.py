import os, re, subprocess, sys, json

base = r"C:\AI_산출물\개발\tax-labor-manager"
f = os.path.join(base, "prototype_20261013", "index.html")
html = open(f, encoding="utf-8").read()
size = os.path.getsize(f)

SENT = "본 도구는 세무 대리 및 신고 대행 서비스를 제공하지 않으며, 이용자의 편의를 위한 단순 일정 관리 및 세액 계산 참고용 보조 프로그램입니다"
n_sent = html.count(SENT)

# extract the <script>...</script> content
m = re.search(r"<script>(.*)</script>", html, re.S)
js = m.group(1) if m else ""
jf = os.path.join(base, "_tmp_check.js")
open(jf, "w", encoding="utf-8").write(js)

# node --check the extracted JS (strip nothing; it's standalone)
r = subprocess.run(["node", "--check", jf], capture_output=True, text=True)
js_ok = (r.returncode == 0)

# external resource scan: any http(s):// or src="http
ext = re.findall(r"https?://[^\s\"'<>)]+", html)

print(json.dumps({
  "file": f,
  "size_bytes": size,
  "disclaimer_exact_sentence_count": n_sent,
  "js_syntax_ok": js_ok,
  "js_check_stderr": (r.stderr or "").strip()[:300],
  "external_urls_found": ext,
  "top_banner": html.count("disclaimer-banner"),
  "footer": html.count("disclaimer-footer"),
  "inline_calc_disclaimer": html.count("disclaimer-inline"),
}, ensure_ascii=False, indent=2))
