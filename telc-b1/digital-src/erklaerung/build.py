#!/usr/bin/env python3
"""telc B1 Modelltest I 해설 — 오프라인 단일 HTML 빌드.

python3 -I build.py <repo>/telc-b1 <font.ttf> <out.html>
"""
import base64
import html
import importlib.util
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from erk1_lesen import LESEN1, LESEN2, LESEN3, SB1, SB2  # noqa: E402
from erk1_hoeren import HOEREN1, HOEREN2, HOEREN3, SCHREIBEN, SPRECHEN  # noqa: E402

APP, FONT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
WEB = len(sys.argv) > 4 and sys.argv[4] == "web"  # 저장소용: Modelltest 페이지로 돌아가는 버튼 + 접속 집계 태그
D = json.load(open(os.path.join(APP, "digital-src", "data", "mt1.json"), encoding="utf-8"))
L, H, S = D["lesen"], D["hoeren"], D["schreiben"]["task"]

spec = importlib.util.spec_from_file_location("sodatheme", os.path.join(APP, "..", "tools", "soda-theme.py"))
st = importlib.util.module_from_spec(spec)
spec.loader.exec_module(st)

e = html.escape


def de(s):
    return f'<span lang="de">{e(s)}</span>'


# ---------- 정답 검증: 해설의 정답 = mt1.json 정답 ----------
def key(part):
    return {i["no"]: i["answer"] for i in part["items"]}

checks = [(LESEN1, key(L["t1"])), (LESEN2, key(L["t2"])), (LESEN3, key(L["t3"])), (SB1, key(L["sb1"])),
          (SB2, key(L["sb2"])), (HOEREN1, key(H["t1"])), (HOEREN2, key(H["t2"])), (HOEREN3, key(H["t3"]))]
for mine, ref in checks:
    got = {i["no"]: i["ans"] for i in mine["items"]}
    if got != ref:
        sys.exit(f"정답 불일치: {got} != {ref}")
# Hören 문장도 문제지와 같은지
for mine, part in ((HOEREN1, H["t1"]), (HOEREN2, H["t2"]), (HOEREN3, H["t3"])):
    for a, b in zip(mine["items"], part["items"]):
        if a["st"] != b["text"]:
            sys.exit(f"Hören {a['no']} 문장이 다릅니다")
# 근거 인용이 Lesen 본문에 그대로 있는지
lesen_text = " ".join(" ".join(t["paragraphs"]) for t in L["t1"]["texts"]) + " " + " ".join(L["t2"]["paragraphs"])
for it in LESEN1["items"] + LESEN2["items"]:
    for q, _ in it["basis"]:
        if q not in lesen_text:
            sys.exit(f"Lesen {it['no']}: 본문에 없는 인용: {q[:60]}")
ads_text = json.dumps(L["t3"]["infos"], ensure_ascii=False)
for it in LESEN3["items"]:
    for q, _ in it["basis"]:
        if q not in ads_text:
            sys.exit(f"Lesen {it['no']}: 광고에 없는 인용: {q[:60]}")
# Sprachbausteine 문장에 정답 단어가 들어 있는지
for it in SB1["items"]:
    w = next(x for x in L["sb1"]["items"] if x["no"] == it["no"])["options"][it["ans"]]
    if w not in it["sent"]:
        sys.exit(f"SB {it['no']}: 문장에 정답 {w} 없음")
for it in SB2["items"]:
    w = L["sb2"]["words"][it["ans"]].lower()
    if w not in it["sent"].lower():
        sys.exit(f"SB {it['no']}: 문장에 정답 {w} 없음")


# ---------- 조각 ----------
def quotes(basis):
    out = []
    for q, ko in basis:
        out.append(f'<blockquote><p class="q">{de(q)}</p><p class="tr">{e(ko)}</p></blockquote>')
    return "".join(out)


def vocab(v):
    if not v:
        return ""
    lis = "".join(f'<li><b lang="de">{e(a)}</b><span>{e(b)}</span></li>' for a, b in v)
    return f'<div class="voc"><h5>어휘</h5><ul>{lis}</ul></div>'


def card(no, ans_html, head, body):
    return (f'<article class="card" id="a{no}"><header><span class="no">{no}</span>'
            f'<span class="ans">{ans_html}</span><div class="hd">{head}</div></header>'
            f'<div class="exp">{body}</div></article>')


def tip(t):
    return f'<p class="tip"><b>푸는 요령</b>{e(t)}</p>'


def rf(a):
    return "richtig" if a == "R" else "falsch"


def rfbadge(a):
    return f'<b class="rf {a}">{"+" if a == "R" else "–"}</b><i>{rf(a)}</i>'


# ---------- Lesen Teil 1 ----------
hl = {h["letter"]: h["text"] for h in L["t1"]["headlines"]}
p = [f'<section id="l1"><h2><small>Leseverstehen</small>Teil 1 · 제목 고르기</h2>', tip(LESEN1["tip"])]
for it in LESEN1["items"]:
    head = f'<p class="topic">{e(it["topic"])}</p><p class="pick rv">{de(it["ans"] + " · " + hl[it["ans"]])}</p>'
    body = quotes(it["basis"]) + f'<p>{e(it["why"])}</p><p class="trap"><b>함정</b>{e(it["trap"])}</p>' + vocab(it["vocab"])
    p.append(card(it["no"], f'<b>{it["ans"]}</b>', head, body))
p.append("</section>")
SEC_L1 = "".join(p)

# ---------- Lesen Teil 2 ----------
t2items = {i["no"]: i for i in L["t2"]["items"]}
p = [f'<section id="l2"><h2><small>Leseverstehen</small>Teil 2 · 기사 읽기 <span lang="de">„{e(L["t2"]["title"])}“</span></h2>',
     '<p class="intro">Lindenbach 마을의 마지막 슈퍼마켓이 문을 닫은 뒤, 주민들이 직접 가게를 운영하는 이야기입니다.</p>', tip(LESEN2["tip"])]
for it in LESEN2["items"]:
    q = t2items[it["no"]]
    opts = "".join(
        f'<li class="{"ok" if k == it["ans"] else ""}"><b>{k}</b><span lang="de">{e(v)}</span>'
        + (f'<em>{e(it["wrong"][k])}</em>' if k in it["wrong"] else "") + "</li>"
        for k, v in q["options"].items())
    head = f'<p class="pick">{de(q["stem"] + " …")}</p>'
    body = quotes(it["basis"]) + f'<p>{e(it["why"])}</p><ol class="opts">{opts}</ol>' + vocab(it["vocab"])
    p.append(card(it["no"], f'<b>{it["ans"]}</b>', head, body))
p.append("</section>")
SEC_L2 = "".join(p)

# ---------- Lesen Teil 3 ----------
ad = {i["letter"]: (i["header"] or i["title"]) for i in L["t3"]["infos"]}
t3items = {i["no"]: i for i in L["t3"]["items"]}
p = [f'<section id="l3"><h2><small>Leseverstehen</small>Teil 3 · 광고 고르기</h2>', tip(LESEN3["tip"])]
for it in LESEN3["items"]:
    q = t3items[it["no"]]
    who = "해당 광고 없음" if it["ans"] == "x" else ad[it["ans"]]
    head = (f'<p class="pick">{de(q["text"])}</p><p class="cond"><b>조건</b>{e(it["cond"])}</p>'
            f'<p class="topic">→ {e(it["ans"])} · <span lang="de">{e(who)}</span></p>')
    body = quotes(it["basis"]) + f'<p>{e(it["why"])}</p>' + (f'<p class="trap"><b>함정</b>{e(it["trap"])}</p>' if it["trap"] else "")
    p.append(card(it["no"], f'<b>{it["ans"]}</b>', head, body))
p.append("</section>")
SEC_L3 = "".join(p)


# ---------- Sprachbausteine ----------
def gap_text(paragraphs, fill):
    out = []
    for para in paragraphs:
        t = e(para)
        t = re.sub(r"\{\{(\d+)\}\}", lambda m: f'<mark><sup>{m.group(1)}</sup>{e(fill(m.group(1)))}</mark>', t)
        out.append("<p>" + t.replace("\n", "<br>") + "</p>")
    return '<div class="letter" lang="de">' + "".join(out) + "</div>"


sb1opt = {i["no"]: i for i in L["sb1"]["items"]}
p = ['<section id="s1"><h2><small>Sprachbausteine</small>Teil 1 · 항의 메일 (Kinderwagen)</h2>', tip(SB1["tip"]),
     '<details class="full"><summary>정답을 채운 전체 글 보기</summary>',
     gap_text(L["sb1"]["paragraphs"], lambda n: sb1opt[n]["options"][sb1opt[n]["answer"]]), "</details>"]
for it in SB1["items"]:
    q = sb1opt[it["no"]]
    opts = "".join(
        f'<li class="{"ok" if k == it["ans"] else ""}"><b>{k}</b><span lang="de">{e(v)}</span>'
        + (f'<em>{e(it["wrong"][k])}</em>' if k in it["wrong"] else "") + "</li>"
        for k, v in q["options"].items())
    head = f'<p class="pick rv">{de(it["sent"])}</p><p class="tr rv">{e(it["ko"])}</p>'
    body = f'<p>{e(it["why"])}</p><ol class="opts">{opts}</ol>'
    p.append(card(it["no"], f'<b>{it["ans"]}</b><i lang="de">{e(q["options"][it["ans"]])}</i>', head, body))
p.append("</section>")
SEC_S1 = "".join(p)

W = L["sb2"]["words"]
sb2ans = {i["no"]: i["answer"] for i in L["sb2"]["items"]}
used = set(sb2ans.values())
wbox = "".join(f'<li class="{"u" if k in used else "n"}"><b>{k}</b><span lang="de">{e(v)}</span></li>' for k, v in W.items())
p = ['<section id="s2"><h2><small>Sprachbausteine</small>Teil 2 · 친구에게 보내는 메일 (Neu in Wien)</h2>', tip(SB2["tip"]),
     f'<div class="words"><h5>단어 상자 <small>진하게 = 정답으로 쓰인 단어</small></h5><ul>{wbox}</ul></div>',
     '<details class="full"><summary>정답을 채운 전체 글 보기</summary>',
     gap_text(L["sb2"]["paragraphs"], lambda n: W[sb2ans[n]].lower()), "</details>"]
for it in SB2["items"]:
    head = f'<p class="pick rv">{de(it["sent"])}</p><p class="tr rv">{e(it["ko"])}</p>'
    body = f'<p>{e(it["why"])}</p>' + (f'<p class="trap"><b>헷갈리는 단어</b>{e(it["wrong"])}</p>' if it["wrong"] else "")
    p.append(card(it["no"], f'<b>{it["ans"]}</b><i lang="de">{e(W[it["ans"]])}</i>', head, body))
p.append(f'<p class="note">{e(SB2["unused"])}</p></section>')
SEC_S2 = "".join(p)


# ---------- Hören ----------
def hoeren(sec_id, title, data):
    p = [f'<section id="{sec_id}"><h2><small>Hörverstehen</small>{title}</h2>', f'<p class="intro">{e(data["intro"])}</p>', tip(data["tip"])]
    for it in data["items"]:
        head = f'<p class="pick">{de(it["st"])}</p><p class="tr">{e(it["stko"])}</p>'
        body = '<h6>들은 내용</h6>' + quotes(it["basis"]) + f'<p>{e(it["why"])}</p>'
        p.append(card(it["no"], rfbadge(it["ans"]), head, body))
    p.append("</section>")
    return "".join(p)


SEC_H1 = hoeren("h1", "Teil 1 · 다섯 사람의 의견 (1회)", HOEREN1)
SEC_H2 = hoeren("h2", "Teil 2 · 인터뷰 (2회)", HOEREN2)
SEC_H3 = hoeren("h3", "Teil 3 · 안내 방송 (각 2회)", HOEREN3)

# ---------- Schreiben ----------
mail = "".join("<p>" + e(x).replace("\n", "<br>") + "</p>" for x in S["mail"])
pts = "".join(f'<li><span class="n">{i}</span><div><p lang="de">{e(a)}</p><p class="tr">{e(b)}</p><p class="ex" lang="de">{e(c)}</p></div></li>'
              for i, (a, b, c) in enumerate(SCHREIBEN["points"], 1))
paras = S["model"]["text"].split("\n\n")
marks = S["model"]["marks"]
assert len(paras) == len(marks) == len(SCHREIBEN["model_ko"])
model = "".join(
    f'<div class="mrow"><span class="lp">{("LP " + m) if m else ""}</span><p lang="de">{e(t).replace(chr(10), "<br>")}</p><p class="tr">{e(k)}</p></div>'
    for t, m, k in zip(paras, marks, SCHREIBEN["model_ko"]))
wc = len(re.findall(r"\S+", S["model"]["text"]))
SEC_W = f"""<section id="w"><h2><small>Schriftlicher Ausdruck</small>쓰기 · Julia에게 답장</h2>
<p class="intro">{e(SCHREIBEN["situation"])}</p>
<div class="box mail" lang="de"><h5>Julia의 메일</h5>{mail}</div>
<h3>Leitpunkte 네 개와 쓸 수 있는 문장</h3><ol class="lps">{pts}</ol>
<h3>자주 하는 실수</h3><ul class="dots">{"".join(f"<li>{e(t)}</li>" for t in SCHREIBEN["traps"])}</ul>
<h3>편지 구성</h3><table class="tbl"><tbody>{"".join(f'<tr><th lang="de">{e(a)}</th><td lang="de">{e(b)}</td></tr>' for a, b in SCHREIBEN["structure"])}</tbody></table>
<h3>모범 답안 <small>약 {wc}단어 · LP = Leitpunkt</small></h3><div class="model">{model}</div>
<h3>쓸 수 있는 표현</h3><table class="tbl"><tbody>{"".join(f'<tr><td lang="de">{e(a)}</td><td>{e(b)}</td></tr>' for a, b in SCHREIBEN["redemittel"])}</tbody></table>
<h3>채점 기준</h3><table class="tbl crit"><tbody>{"".join(f'<tr><th>{a}</th><td><span lang="de">{e(b)}</span><br>{e(c)}</td></tr>' for a, b, c in SCHREIBEN["criteria"])}</tbody></table>
<p class="note">각 기준은 A~D로 평가하고 합계에 3을 곱해 최대 45점입니다. I(내용) 또는 III(정확성)에서 D를 받으면 쓰기는 0점입니다.</p>
</section>"""


# ---------- Sprechen ----------
def rm(rows):
    return '<table class="tbl"><tbody>' + "".join(f'<tr><td lang="de">{e(a)}</td><td>{e(b)}</td></tr>' for a, b in rows) + "</tbody></table>"


sp = SPRECHEN
SEC_M = f"""<section id="m"><h2><small>Mündlicher Ausdruck</small>말하기 · 약 15분, 두 사람이 함께</h2>
<h3>Teil 1 · <span lang="de">Einander kennenlernen</span></h3><p class="lead2">{e(sp["t1"]["task"])}</p>
<ul class="dots">{"".join(f"<li>{e(t)}</li>" for t in sp["t1"]["points"])}</ul>{rm(sp["t1"]["redemittel"])}
<h3>Teil 2 · <span lang="de">Über ein Thema sprechen</span></h3><p class="lead2">{e(sp["t2"]["task"])}</p>
<div class="two"><div class="box"><h5>A의 종이</h5><p>{e(sp["t2"]["a"])}</p></div><div class="box"><h5>B의 종이</h5><p>{e(sp["t2"]["b"])}</p></div></div>
<ol class="steps">{"".join(f'<li><b lang="de">{e(a)}</b><span>{e(b)}</span></li>' for a, b in sp["t2"]["steps"])}</ol>{rm(sp["t2"]["redemittel"])}
<h3>Teil 3 · <span lang="de">Gemeinsam etwas planen</span></h3><p class="lead2">{e(sp["t3"]["task"])}</p>
<ul class="dots">{"".join(f"<li>{e(t)}</li>" for t in sp["t3"]["points"])}</ul>{rm(sp["t3"]["redemittel"])}
<p class="note">말하기 모범 대화는 PDF 21쪽에 있습니다.</p>
</section>"""


# ---------- 정답표 ----------
def krow(label, href, items, fmt):
    cells = "".join(f'<a href="#a{n}"><span>{n}</span><b>{fmt(a)}</b></a>' for n, a in items)
    return f'<div class="krow"><h4><a href="{href}">{label}</a></h4><div class="kc">{cells}</div></div>'


def ks(part):
    return [(i["no"], i["answer"]) for i in part["items"]]


KEY = ('<section id="key"><h2><small>Lösungsschlüssel</small>정답표</h2><p class="intro">번호를 누르면 해설로 이동합니다. Hören은 + = richtig, – = falsch.</p>'
       + krow("Lesen Teil 1", "#l1", ks(L["t1"]), str) + krow("Lesen Teil 2", "#l2", ks(L["t2"]), str)
       + krow("Lesen Teil 3", "#l3", ks(L["t3"]), str) + krow("Sprachbausteine 1", "#s1", ks(L["sb1"]), str)
       + krow("Sprachbausteine 2", "#s2", ks(L["sb2"]), str)
       + krow("Hören Teil 1", "#h1", ks(H["t1"]), lambda a: "+" if a == "R" else "–")
       + krow("Hören Teil 2", "#h2", ks(H["t2"]), lambda a: "+" if a == "R" else "–")
       + krow("Hören Teil 3", "#h3", ks(H["t3"]), lambda a: "+" if a == "R" else "–")
       + """<table class="tbl pts"><thead><tr><th>모듈</th><th>배점</th><th>최대</th></tr></thead><tbody>
<tr><td>Lesen Teil 1·2</td><td>문항당 5점</td><td rowspan="3">105점</td></tr>
<tr><td>Lesen Teil 3</td><td>문항당 2,5점</td></tr>
<tr><td>Sprachbausteine 1·2</td><td>문항당 1,5점</td></tr>
<tr><td>Hören Teil 1·3</td><td>문항당 5점</td><td rowspan="2">75점</td></tr>
<tr><td>Hören Teil 2</td><td>문항당 2,5점</td></tr>
<tr><td>Schreiben</td><td>선생님 채점</td><td>45점</td></tr>
<tr><td>Sprechen</td><td>선생님 채점</td><td>75점</td></tr>
</tbody></table><p class="note">필기(Lesen·Sprachbausteine·Hören·Schreiben) 225점 중 135점(60 %), 말하기 75점 중 45점(60 %)을 각각 넘어야 합격입니다.</p></section>""")

# ---------- 글꼴과 로고 ----------
body_html = KEY + SEC_L1 + SEC_L2 + SEC_L3 + SEC_S1 + SEC_S2 + SEC_H1 + SEC_H2 + SEC_H3 + SEC_W + SEC_M
chars = set(body_html) | set("telc B1 Modelltest I 해설 SODA LEHRWERK 소피아 독일어학원 Sophia Deutsch Akademie 정답 가리기 보기 목차 정답표 위로 다크 모드 켜기 끄기 켜짐 꺼짐 누르면 라이트로 바뀌어요 카드를 눌러 확인하세요")
from fontTools import subset  # noqa: E402
from fontTools.ttLib import TTFont  # noqa: E402
cps = set(range(0x20, 0x7F)) | {ord(c) for c in chars if ord(c) >= 0x20}
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
FONT64 = base64.b64encode(buf.getvalue()).decode()
LOGO64 = base64.b64encode(open(os.path.join(APP, "digital-src", "logo-small.png"), "rb").read()).decode()

CSS = open(os.path.join(HERE, "style.css"), encoding="utf-8").read().replace("__FONT__", FONT64)
NAV = [("key", "정답표"), ("l1", "Lesen 1"), ("l2", "Lesen 2"), ("l3", "Lesen 3"), ("s1", "SB 1"), ("s2", "SB 2"),
       ("h1", "Hören 1"), ("h2", "Hören 2"), ("h3", "Hören 3"), ("w", "Schreiben"), ("m", "Sprechen")]
nav = "".join(f'<a href="#{a}">{b}</a>' for a, b in NAV)
if WEB:
    back = (st.TOC_JS.replace("__HREF__", "index.html#1").replace("목차로 돌아가기", "Modelltest I 페이지로 돌아가기")
            .replace("</svg>목차", "</svg>Modelltest I"))
    theme_js = st.THEME_JS.replace("__TOC__", back)
    EXTRA_HEAD = st.ANALYTICS_TAG
else:
    theme_js = st.THEME_JS.replace("__TOC__", "")
    EXTRA_HEAD = ""

page = f"""<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
{theme_js}
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#14181E">
<title>telc B1 Modelltest I 해설</title>
<style>{CSS}</style>
{EXTRA_HEAD}<style id="soda-dark">{st.BUTTON_CSS}</style>
</head>
<body>
<header class="cover">
<div class="brand"><img src="data:image/png;base64,{LOGO64}" alt=""><b>Sophia Deutsch Akademie</b></div>
<p class="eyebrow">SODA Lehrwerk · telc Deutsch B1</p>
<h1>Modelltest I</h1>
<p class="sub">해설</p>
<p class="lead">Lesen · Sprachbausteine · Hören 60문항의 근거와 함정, Schreiben 모범 답안, Sprechen 진행 요령</p>
</header>
<nav class="nav" aria-label="목차"><div class="navin">{nav}<button type="button" id="hide" aria-pressed="false">정답 가리기</button></div></nav>
<main>{body_html}</main>
<footer class="foot"><span>© Sophia Deutsch Akademie · telc B1 Modelltest I 해설</span><a href="#top" onclick="scrollTo(0,0);return false">위로</a></footer>
<script>
(function(){{
  var b=document.getElementById('hide'), d=document.body;
  b.addEventListener('click',function(){{
    var on=!d.classList.contains('hide'); d.classList.toggle('hide',on); b.setAttribute('aria-pressed',on?'true':'false');
    b.textContent=on?'정답 보기':'정답 가리기';
    document.querySelectorAll('.card.open').forEach(function(c){{c.classList.remove('open');}});
  }});
  document.addEventListener('click',function(ev){{
    if(!d.classList.contains('hide')) return;
    var c=ev.target.closest('.card'); if(c && !ev.target.closest('a')) c.classList.add('open');
  }});
}})();
</script>
</body>
</html>
"""
open(OUT, "w", encoding="utf-8").write(page)
print(OUT, os.path.getsize(OUT), "bytes,", len(cps), "glyphs, model words", wc)
