#!/usr/bin/env python3
"""telc Deutsch B2 Modelltest N 작문 연습 — 단일 HTML 빌드.

python3 -I build.py <app-folder> <N> <font.ttf> <out.html> [web]
작문 연습 데이터: swN.py (형식은 FORMAT.md), 모든 회차가 함께 쓰는 글: gemeinsam.py
과제 원문(광고, 상황, Leitpunkte)은 ../data/mtN.json, 과제 제목과 Leitpunkt 번역은 ../erklaerung/erkN_hoeren.py,
시험지 쪽수는 앱 폴더의 index.html에서 가져옵니다.
web: 저장소용 — 시험 페이지로 돌아가는 버튼, 접속 집계 태그, 학습 포탈 학습 저장(sync.js)을 넣습니다.
     없으면 학생에게 파일로 주는 오프라인판입니다(제출하기는 그대로 됩니다).

빌드 전에 검사합니다(어긋나면 멈춤): 과제 수(A·B), 번호마다 필요한 칸, 편지의 짜임(Betreff, 호칭, 도입,
Leitpunkt 셋, 마무리, 끝인사), {…} 짝, B2 예시의 본문 단어 수(쓰기 가이드 기준), 호칭 다음 줄의 소문자,
한국어 글의 어조(‘~다’ 체·반말).
"""
import base64
import html
import importlib
import importlib.util
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

APP, N, FONT, OUT = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
WEB = len(sys.argv) > 5 and sys.argv[5] == "web"
D = json.load(open(os.path.join(APP, "digital-src", "data", f"mt{N}.json"), encoding="utf-8"))
ROMAN = D["roman"]
S = D["schreiben"]["tasks"]
G = importlib.import_module("gemeinsam")
AUF = importlib.import_module(f"sw{N}").AUFGABEN


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ERK = _load(os.path.join(APP, "digital-src", "erklaerung", f"erk{N}_hoeren.py"), f"erk{N}_hoeren").SCHREIBEN["tasks"]
st = _load(os.path.join(APP, "..", "tools", "soda-theme.py"), "sodatheme")

e = html.escape
CIRC = "①②③④⑤⑥⑦⑧⑨⑩"
TITLE = f"telc B2 Modelltest {ROMAN} 작문 연습"
LO, HI = G.RANGE


def plain(t):
    return t.replace("{", "").replace("}", "")


def words(t):
    return len(t.split())


def ko(t):
    """한국어 글 속의 «…»를 독일어 조각으로 표시합니다."""
    return re.sub(r"«(.+?)»", lambda m: f'<b class="de" lang="de">{m.group(1)}</b>', e(t))


def marked(t):
    """B2 예시의 {…}를 강조로 바꿉니다."""
    return re.sub(r"\{(.+?)\}", lambda m: f"<mark>{m.group(1)}</mark>", e(t))


def lp_no(role):
    m = re.fullmatch(r"Leitpunkt ([1-4])", role)
    return int(m.group(1)) if m else None


# ---------- 검사 ----------
CAP_OK = {"Sie", "Ihnen", "Ihr", "Ihre", "Ihren", "Ihrem", "Ihrer", "Ihres", "Entschuldigung"}
BAD_END = re.compile(r"(?<![니까])다[.!]?$")
BANMAL = re.compile(r"(?:한다|했다|이다|있다|없다|된다|않는다|하자|해라|이야|거야)[.!]?$")
SKIP_NEED = {"sein", "sich", "etwas", "jemandem", "jemanden"}


def tone(text, where):
    for s in re.split(r"(?<=[.!?])\s+", text.strip()):
        s = re.sub(r"«.+?»", "", s).strip()
        if s and (BAD_END.search(s) or BANMAL.search(s)):
            sys.exit(f"{where}: ‘~다’ 체나 반말로 끝나는 문장: {s}")


def found(w, bag):
    """주어진 표현의 낱말이 예시에 있는지(어미 변화와 합성어는 느슨하게 봅니다)."""
    if w in bag or (w == "zu" and any("zu" in x for x in bag)):
        return True
    if len(w) >= 5 and any(w in x for x in bag):  # Vertrag → Mitgliedsvertrag
        return True
    stem = re.sub(r"(?:en|n)$", "", w)
    return len(stem) >= 4 and any(stem in x for x in bag)  # erwecken → erweckt


def body_words(parts, key):
    """호칭부터 맺음 문장까지: Betreff와 마지막 번호 뒤의 줄(끝인사, 이름)은 세지 않습니다."""
    last = max(i for i, p in enumerate(parts) if "fix" not in p)
    tot = 0
    for i, p in enumerate(parts):
        if p.get("role") == "Betreff" or ("fix" in p and i > last):
            continue
        tot += words(p["fix"] if "fix" in p else plain(p[key]))
    return tot


if len(AUF) != 2 or len(S) != 2 or len(ERK) != 2:
    sys.exit("과제는 Aufgabe A·B, 두 개여야 합니다")
COVER = {}
for a, t, erk in zip(AUF, S, ERK):
    L = t["letter"]
    where = f"Modelltest {N} Aufgabe {L}"
    if erk["letter"] != L:
        sys.exit(f"{where}: 해설 데이터의 과제 순서가 다릅니다")
    tone(a["ko"], where + " ko")
    for s in a["sum"]:
        tone(s, where + " sum")
    seq = a["parts"]
    parts = [p for p in seq if "fix" not in p]
    if not 5 <= len(parts) <= len(CIRC):
        sys.exit(f"{where}: 고쳐 쓸 번호가 {len(parts)}개입니다")
    # 편지의 짜임: Betreff, 호칭, 도입, Leitpunkt …, 마무리, 끝인사와 이름
    if not (seq[0].get("role") == "Betreff" and seq[0].get("short")):
        sys.exit(f"{where}: 첫 칸은 Betreff(short)입니다")
    if not seq[1].get("fix", "").startswith("Sehr geehrte"):
        sys.exit(f"{where}: Betreff 다음은 격식 있는 호칭(fix)입니다")
    if not seq[-1].get("fix", "").startswith("Mit freundlichen Grüßen\n"):
        sys.exit(f"{where}: 마지막 칸은 «Mit freundlichen Grüßen» + 이름(fix)입니다")
    roles = [p["role"] for p in parts]
    if roles[1] != "도입" or roles[-1] != "마무리" or any(lp_no(r) is None for r in roles[2:-1]):
        sys.exit(f"{where}: 번호의 차례는 Betreff, 도입, Leitpunkt …, 마무리입니다: {roles}")
    lps = [lp_no(r) for r in roles[2:-1]]
    if lps != sorted(lps) or len(set(lps)) != 3:
        sys.exit(f"{where}: Leitpunkt 세 개를 차례대로 씁니다: {lps}")
    COVER[L] = sorted(set(lps))
    for i, p in enumerate(parts, 1):
        for key in ("role", "b1", "use", "use_ko", "tip", "b2"):
            if not p.get(key):
                sys.exit(f"{where} {CIRC[i - 1]}: {key}가 없습니다")
        if p["b2"].count("{") != p["b2"].count("}") or "{" not in p["b2"] or re.search(r"\{[^}]*\{", p["b2"]):
            sys.exit(f"{where} {CIRC[i - 1]}: b2의 {{…}} 짝이 맞지 않습니다: {p['b2']}")
        if "{" in p["b1"]:
            sys.exit(f"{where} {CIRC[i - 1]}: b1에는 {{…}}를 쓰지 않습니다")
        tone(p["tip"], f"{where} {CIRC[i - 1]} tip")
        tone(p["use_ko"], f"{where} {CIRC[i - 1]} use_ko")
        if p["role"] == "Betreff" and not (p["b1"].startswith("Betreff: ") and plain(p["b2"]).startswith("Betreff: ")):
            sys.exit(f"{where} {CIRC[i - 1]}: Betreff 칸은 «Betreff: »로 시작합니다")
        bag = set(re.findall(r"[a-zäöüß]+", plain(p["b2"]).lower()))
        need = [w for w in re.findall(r"[a-zäöüß]+", p["use"].lower()) if w not in SKIP_NEED and w != "betreff"]
        miss = [w for w in need if not found(w, bag)]
        if miss:
            print(f"  알림 {where} {CIRC[i - 1]}: 표현의 낱말이 예시에 없습니다: {miss}", file=sys.stderr)
    for x, p in enumerate(seq[:-1]):
        if p.get("fix", "").rstrip().endswith(","):
            nxt = seq[x + 1]
            for key in ("b1", "b2"):
                tt = plain(nxt.get(key, ""))
                # 명사와 존칭(Sie, Ihr …)은 호칭 다음 줄에서도 대문자입니다
                if tt and not tt[0].islower() and tt.split()[0].strip(",.!?:") not in CAP_OK:
                    sys.exit(f"{where}: 호칭 다음 줄은 소문자로 시작합니다: {tt[:30]}")
    total = body_words(seq, "b2")
    if not LO <= total <= HI:
        sys.exit(f"{where}: B2 예시 본문 {total}단어, 범위 {LO}~{HI}를 벗어났습니다")
    if body_words(seq, "b1") >= total:
        sys.exit(f"{where}: B1 답안이 B2 예시보다 깁니다")


# ---------- 글의 짜임(줄·문단) ----------
def layout(L, seq):
    """파트를 줄과 문단으로 묶습니다. 같은 role(Leitpunkt 1 …)이 이어지면 한 문단입니다.
    nc: 단어 수에 넣지 않는 줄(Betreff, 끝인사와 이름)."""
    last = max(i for i, p in enumerate(seq) if "fix" not in p)
    out, cur, n = [], None, 0
    for i, p in enumerate(seq):
        if "fix" in p:
            out.append({"line": True, "nc": i > last, "items": [{"fix": p["fix"]}]})
            cur = None
            continue
        n += 1
        item = {"k": f"{L}-{n}", "n": CIRC[n - 1]}
        if p.get("short"):
            out.append({"line": True, "nc": p["role"] == "Betreff", "items": [item]})
            cur = None
            continue
        if cur is None or cur["g"] != p["role"]:
            cur = {"g": p["role"], "items": []}
            out.append(cur)
        cur["items"].append(item)
    return out


def render(lay, seq, kind):
    """kind: b1(번호 붙은 B1 답안) 또는 b2(강조 붙은 B2 예시)."""
    by, n = {}, 0
    for p in seq:
        if "fix" not in p:
            n += 1
            by[CIRC[n - 1]] = p
    html_out, text_out = [], []
    for b in lay:
        hs, ts = [], []
        for it in b["items"]:
            if "fix" in it:
                hs.append(e(it["fix"]))
                ts.append(it["fix"])
                continue
            p = by[it["n"]]
            if kind == "b1":
                hs.append(f'<span class="pn">{CIRC.index(it["n"]) + 1}</span>{e(p["b1"])}')
                ts.append(p["b1"])
            else:
                hs.append(marked(p["b2"]))
                ts.append(plain(p["b2"]))
        cls = ' class="gr"' if b.get("line") else ""
        html_out.append(f"<p{cls}>{' '.join(hs)}</p>")
        text_out.append(" ".join(ts))
    return "".join(html_out), "\n\n".join(text_out)


# ---------- 조각 ----------
def _ad(a):
    """광고(해설 페이지와 같은 모양)."""
    out = []
    for k in ("header", "tag", "title", "subtitle"):
        if a.get(k):
            out.append(f'<p class="ad-{k}">{e(a[k])}</p>')
    if a.get("facts"):
        out.append('<ul class="dots">' + "".join(f"<li>{e(x)}</li>" for x in a["facts"]) + "</ul>")
    out += [f"<p>{e(x)}</p>" for x in a.get("body", [])]
    if a.get("footer"):
        out.append(f'<p class="ad-footer">{e(a["footer"])}</p>')
    return "".join(out)


def task_pages():
    """index.html의 페이퍼 시험 페이지에서 Aufgabe A·B의 시험지 쪽수를 찾습니다."""
    try:
        idx = open(os.path.join(APP, "index.html"), encoding="utf-8").read()
        i = idx.index(f'<section class="page mdt" id="m{N}"')
        blk = idx[i:idx.index("</section>", i)]
    except (OSError, ValueError):
        return {}
    out = {}
    for L in "AB":
        m = re.search(r'<span class="t">Aufgabe ' + L + r'</span>[^\n]*?#page=(\d+)', blk)
        if m:
            out[L] = int(m.group(1))
    return out


PAGES = task_pages()


def lp_ko(erk, i):
    return erk["points"][i - 1][1].rstrip(".")


def task_box(L, t, erk):
    page = f" <small>시험지 {PAGES[L]}쪽</small>" if L in PAGES else ""
    ad = f'<div class="box mail" lang="de"><h5>{e(t["lead"])}</h5>{_ad(t["ad"])}</div>'
    task = "".join(f"<p>{e(x)}</p>" for x in t["situation"] + t["choice"])
    task += '<ul class="dots">' + "".join(f"<li>{e(x)}</li>" for x in t["points"]) + "</ul>"
    task += f"<p>{e(t['closing'])}</p>"
    box = f'<div class="box" lang="de"><h5 lang="ko">과제{page}</h5>{task}</div>'
    cov = COVER[L]
    lis = []
    for i in range(1, len(erk["points"]) + 1):
        on = i in cov
        cls = ' class="on"' if on else ""
        tag = "<em>이 답안</em>" if on else ""
        lis.append(f"<li{cls}><b>{i}</b><span>{e(lp_ko(erk, i))}</span>{tag}</li>")
    nums = "·".join(map(str, cov))
    note = f'<p class="lpn">이 연습의 답안은 a) 방식으로, Leitpunkt {nums} 세 가지를 씁니다.</p>'
    lis = "".join(lis)
    return ad + box + f'<ol class="lpko">{lis}</ol>' + note


def part_card(L, i, p, erk):
    k = f"{L}-{i}"
    short = bool(p.get("short"))
    lines = 1 if short else max(2, -(-len(plain(p["b2"])) // 52) + 1)
    ta_cls = "ans short" if short else "ans"
    rows = 1 if short else 3
    n = lp_no(p["role"])
    lpk = f'<span class="lpk">{e(lp_ko(erk, n))}</span>' if n else ""
    return f"""<li class="part" id="p{k}">
<div class="ph"><span class="pn">{i}</span><span class="role">{e(p["role"])}</span>{lpk}<span class="ok">✓ 작성</span></div>
<div class="b1s"><span class="lab">B1</span><p lang="de">{e(p["b1"])}</p></div>
<div class="use"><span class="lab">쓸 표현</span><span class="ux" lang="de">{e(p["use"])}</span><em>{e(p["use_ko"])}</em></div>
<p class="hint">{ko(p["tip"])}</p>
<textarea class="{ta_cls}" data-k="{k}" rows="{rows}" lang="de" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off" aria-label="{i}번 B2 문장" placeholder="B2 문장으로 고쳐 쓰십시오"></textarea>
<div class="pv" lang="de"></div><div class="pl" aria-hidden="true">{"<i></i>" * lines}</div>
<div class="pbar"><button class="sbtn exb" type="button" aria-expanded="false" aria-controls="x{k}">예시 보기</button></div>
<div class="ex" id="x{k}" hidden><span class="lab">B2 예시</span><p lang="de">{marked(p["b2"])}</p></div>
</li>"""


sections, data_aufg = [], []
for a, t, erk in zip(AUF, S, ERK):
    L = t["letter"]
    seq = a["parts"]
    parts = [p for p in seq if "fix" not in p]
    lay = layout(L, seq)
    b1_html, _ = render(lay, seq, "b1")
    b2_html, _ = render(lay, seq, "b2")
    n1, n2 = body_words(seq, "b1"), body_words(seq, "b2")
    frame = "Betreff와 번호가 붙은 부분을 고쳐 씁니다. 호칭과 끝인사, 이름은 그대로 둡니다."
    cards = "".join(part_card(L, i, p, erk) for i, p in enumerate(parts, 1))
    chk = "".join(f"<li><span>{ko(x)}</span></li>" for x in G.CHECK[t["kind"]])
    summ = "".join(f"<li>{ko(x)}</li>" for x in a["sum"])
    sections.append(f"""<section id="w{L}" class="aufg" data-a="{L}">
<h2><small>Aufgabe {L} · <span lang="de">{e(t["kind"])}</span> · 최소 {t["words"]}단어</small>{e(erk["title"])}</h2>
<p class="kind">{e(G.KIND)}</p>
<p class="intro">{e(a["ko"])}</p>
{task_box(L, t, erk)}
<h3 class="sub3">B1 답안 <span class="cnt">본문 {n1}단어</span></h3>
<div class="b1l" lang="de">{b1_html}</div>
<h3 class="sub3">B2로 고쳐 쓰기 <span class="prog" id="prog{L}">작성 0 / {len(parts)}</span></h3>
<p class="frame">{ko(frame)}</p>
<ol class="parts">{cards}</ol>
<details class="mine" id="mine{L}"><summary>내 글 전체 <span class="wc">0단어</span><small>목표 {LO}–{HI}단어 · {e(G.COUNT_NOTE)}</small></summary>
<div class="ml" lang="de"></div>
<div class="acts"><button class="sbtn cp" type="button" data-a="{L}">이 글 복사</button></div>
<h5>제출 전 확인</h5><ul class="chk">{chk}</ul></details>
<details class="b2f"><summary>B2 예시 답안 전체 <span class="wc ok">{n2}단어</span><small>B1 답안 {n1}단어 · 본문 기준</small></summary>
<div class="ml" lang="de">{b2_html}</div></details>
<h4 class="sub3 sumh">B1 → B2, 이렇게 바뀌었습니다</h4>
<ul class="dots sum">{summ}</ul>
</section>""")
    data_aufg.append({
        "no": L, "title": erk["title"], "lo": LO, "hi": HI,
        "layout": [{"line": bool(b.get("line")), "nc": bool(b.get("nc")),
                    "items": [({"fix": it["fix"]} if "fix" in it else {"k": it["k"], "n": it["n"]}) for it in b["items"]]}
                   for b in lay],
        "parts": [{"k": f"{L}-{i}", "n": CIRC[i - 1], "role": p["role"], "b1": p["b1"], "use": p["use"]}
                  for i, p in enumerate(parts, 1)],
    })

steps = "".join(f"<li><b>{e(x)}</b>{e(y)}</li>" for x, y in G.STEPS)
diff = "".join(f'<li><b>{e(x)}</b><div class="d2"><small>B1</small>{ko(y)}</div><div class="d1"><small>B2</small>{ko(z)}</div></li>'
               for x, y, z in G.DIFF)
save_note = ("쓴 내용은 이 브라우저에 저절로 저장됩니다. 학습 포탈에 로그인한 상태라면 다른 기기에서도 이어서 쓸 수 있습니다."
             if WEB else "쓴 내용은 이 브라우저에 저절로 저장됩니다. 파일을 다른 곳으로 옮기면 저장한 내용이 이어지지 않을 수 있습니다.")
HOW = f"""<section id="how"><h2><small>Schreibübung</small>이렇게 연습합니다</h2>
<ol class="steps">{steps}</ol>
<p class="note">시험에서는 Aufgabe A와 B 가운데 하나만 골라 씁니다. 이 연습에서는 두 과제를 모두 고쳐 쓰면서 정보 요청과 항의에 쓰는 표현을 함께 익힙니다.</p>
<h3>{e(G.DIFF_TITLE)}</h3>
<ul class="diff">{diff}</ul>
<p class="note">{e(G.DIFF_NOTE)}</p>
<p class="save">{e(save_note)}</p></section>"""

SUB = f"""<section id="sub"><h2><small>Abgabe</small>제출과 보관</h2>
<div class="subbox"><h3>{e(G.SUBMIT_TITLE)}<em>{e(G.SUBMIT_TAG)}</em></h3>
{"".join(f"<p>{x}</p>" for x in G.SUBMIT_TEXT)}
<p class="sc">작성: <span id="subcnt"></span></p>
<label>이름 <input id="subName" type="text" maxlength="60" autocomplete="name"></label>
<div class="acts"><button class="btn" id="sb" type="button">선생님께 제출하기</button><span class="st" id="subSt" role="status"></span></div></div>
<div class="acts keep"><button class="sbtn" id="cpall" type="button">전체 복사</button><button class="sbtn" id="dl" type="button">txt 저장</button><button class="sbtn" id="reset" type="button">쓴 내용 모두 지우기</button></div>
</section>"""

# 제출 주소: 디지털 시험 화면(template.html)과 같은 주소를 씁니다. tools/set-submit-url.py가 이 파일들도 함께 바꿉니다.
tpl = open(os.path.join(APP, "digital-src", "template.html"), encoding="utf-8").read()
m = re.search(r"var SUBMIT_URL = '([^']*)';", tpl)
SUBMIT_URL = m.group(1) if m else ""

APPJS = open(os.path.join(HERE, "app.js"), encoding="utf-8").read().replace("var SUBMIT_URL = '__SUBMIT_URL__';", f"var SUBMIT_URL = '{SUBMIT_URL}';")
if f"var SUBMIT_URL = '{SUBMIT_URL}';" not in APPJS:
    sys.exit("app.js에서 SUBMIT_URL 줄을 찾지 못했습니다")
DATA = json.dumps({"mt": str(N), "roman": ROMAN, "title": TITLE, "aufg": data_aufg}, ensure_ascii=False).replace("</", "<\\/")

NAV = [("how", "사용법"), ("wA", "Aufgabe A"), ("wB", "Aufgabe B"), ("sub", "제출")]
nav = "".join(f'<a href="#{x}">{y}</a>' for x, y in NAV)
body_html = HOW + "".join(sections) + SUB

if WEB:
    back = (st.TOC_JS.replace("__HREF__", f"index.html#{N}").replace("목차로 돌아가기", f"Modelltest {ROMAN} 페이지로 돌아가기")
            .replace("</svg>목차", f"</svg>Modelltest {ROMAN}"))
    theme_js = st.SYNC_TAG + "\n" + st.THEME_JS.replace("__TOC__", back)
    EXTRA_HEAD = st.ANALYTICS_TAG
else:
    theme_js = st.THEME_JS.replace("__TOC__", "")
    EXTRA_HEAD = ""

CSS = (open(os.path.join(HERE, "..", "erklaerung", "style.css"), encoding="utf-8").read()
       + open(os.path.join(HERE, "style.css"), encoding="utf-8").read())
LOGO64 = base64.b64encode(open(os.path.join(APP, "digital-src", "logo-small.png"), "rb").read()).decode()


def page(font64):
    return f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
{theme_js}
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#14181E">
<title>{TITLE}</title>
<style>{CSS.replace("__FONT__", font64)}</style>
{EXTRA_HEAD}<style id="soda-dark">{st.BUTTON_CSS}</style>
</head>
<body>
<header class="cover">
<div class="brand"><img src="data:image/png;base64,{LOGO64}" alt=""><b>Sophia Deutsch Akademie</b></div>
<p class="eyebrow">SODA Lehrwerk · telc Deutsch B2</p>
<h1>Modelltest {ROMAN}</h1>
<p class="sub">작문 연습</p>
<p class="lead">{e(G.LEAD)}</p>
</header>
<nav class="nav" aria-label="목차"><div class="navin">{nav}<button type="button" id="exall" aria-pressed="false">예시 모두 보기</button></div></nav>
<main>{body_html}</main>
<footer class="foot"><span>© Sophia Deutsch Akademie · {TITLE}</span><a href="#top" onclick="scrollTo(0,0);return false">위로</a></footer>
<div class="toast" id="toast" role="status" hidden></div>
<script type="application/json" id="sw-data">{DATA}</script>
<script>{APPJS}</script>
</body>
</html>
"""


draft = page("")
# 글꼴: 화면에 쓰는 글자, 스크립트 안내 문구, 학생이 칠 독일어 글자(라틴 문자와 문장 부호)
chars = set(draft)
from fontTools import subset  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
cps = set(range(0x20, 0x7F)) | set(range(0xA0, 0x180)) | {0x2013, 0x2014, 0x2018, 0x2019, 0x201A, 0x201C, 0x201D, 0x201E,
                                                          0x2026, 0x20AC, 0x2022, 0x2192, 0x25B8, 0x25BE, 0x25A1, 0x2713}
cps |= {ord(c) for c in chars if ord(c) >= 0x20}
f = TTFont(FONT)
o = subset.Options()
o.flavor = "woff"
o.layout_features = ["kern", "liga", "calt", "locl", "tnum", "ccmp", "mark", "mkmk"]
o.notdef_outline = True
ss = subset.Subsetter(o)
ss.populate(unicodes=sorted(cps))
ss.subset(f)
f.flavor = "woff"
buf = io.BytesIO()
f.save(buf)
out = page(base64.b64encode(buf.getvalue()).decode())
if "_" in os.path.basename(OUT):
    sys.exit("파일 이름에 밑줄(_)을 쓰지 않습니다")
open(OUT, "w", encoding="utf-8").write(out)
print(OUT, os.path.getsize(OUT), "bytes,", len(cps), "glyphs")
