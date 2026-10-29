#!/usr/bin/env python3
"""telc B2 쓰기 시험 대비 가이드(schreiben-guide.html)를 만듭니다.

입력  guide-data.json   가이드의 모든 글과 모범 답안
출력  ../schreiben-guide.html (이 앱 폴더)

모범 답안의 본문 단어 수(Anrede부터 Schluss까지)는 이 스크립트가 직접 세고, 범위를 벗어나면 멈춥니다.
공통 헬퍼와 기본 CSS는 guidelib.py 에 있습니다.

사용법 (앱 폴더에서)
  python3 -I digital-src/build-guide.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # python3 -I 로 돌려도 guidelib를 찾도록
from guidelib import NUMS, e, finish, page, section, table, words  # noqa: E402

APP = os.path.dirname(HERE)
OUT = os.path.join(APP, "schreiben-guide.html")
A = "auto"


def texts(part):
    lo, hi = part["range"]
    cards = []
    for i, a in enumerate(part["items"]):
        total = words(a["body"])
        if not (lo <= total <= hi):
            sys.exit(f'모범 답안 {i + 1} "{a["title"]}": {total}단어, 범위 {lo}~{hi}를 벗어났습니다')
        ps = "".join(f'<p lang="de" class="lt-t">{e(p)}</p>' for p in a["body"].split("\n\n"))
        gl = "".join(f'<p lang="de">{e(l)}</p>' for l in a["gruss"].split("\n"))
        box = (f'<div class="lt-b"><p lang="de" class="dt">{e(a["ort"])}</p><p lang="de" class="bt"><b>Betreff</b> {e(a["betreff"])}</p>'
               f'<p lang="de">{e(a["anrede"])}</p>{ps}<div class="lt-g">{gl}</div></div>')
        pts = '<ol class="lp" lang="de">' + "".join(f"<li>{e(p)}</li>" for p in a["points"]) + "</ol>"
        cards.append(
            f'<article class="lt"><header class="lt-h"><span class="lt-n" aria-hidden="true">{NUMS[i]}</span>'
            f'<div><h3>{e(a["title"])}</h3><p class="lt-p" lang="de">{e(a["task"])}</p></div></header>'
            f'{pts}{box}<p class="lt-c"><b>{total}</b> Wörter <span>본문, 최소 150</span></p></article>')
    return f'<div class="lts">{"".join(cards)}</div>'


def build(d):
    secs = []
    ov = d["overview"]
    secs.append(section(ov["id"], "Überblick", ov["title"],
                        '<dl class="kv">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in ov["rows"]) + "</dl>" +
                        f'<h3 class="sub">{e(d["diff"]["title"])}</h3><p class="note">{e(d["diff"]["text"])}</p>'))

    sc = d["scoring"]
    inner = (table(["기준", "보는 것"], sc["criteria"], "crit2", A) +
             f'<h3 class="sub">등급과 점수</h3>' + table(sc["levels_head"], sc["levels"], "lv5", A) +
             f'<p class="note">{e(sc["levels_note"])}</p>'
             f'<p class="warn"><b>0점 규칙</b>{e(sc["zero"])}</p>'
             f'<p class="note">{e(sc["zusatz"])}</p>'
             f'<h3 class="sub">{e(sc["sim_title"])}</h3>' + table(sc["sim_head"], sc["sim"], "sim", A) +
             f'<p class="note">{e(sc["sim_note"])}</p>')
    secs.append(section(sc["id"], "Bewertung", sc["title"], inner, e(sc["intro"])))

    sg = d["strategy"]
    inner = (f'<h3 class="sub">{e(sg["time_title"])}</h3>' + table(sg["time_head"], sg["time"], "tm", A) +
             f'<h3 class="sub">{e(sg["tips_title"])}</h3><ol class="num circ">' + "".join(
                 f'<li><span class="n">{e(n)}</span><span>{e(t)}</span></li>' for n, t in sg["tips"]) + "</ol>")
    secs.append(section(sg["id"], "Strategie", sg["title"], inner, e(sg["intro"])))

    pl = d["plan"]
    secs.append(section(pl["id"], "Lernplan", pl["title"], table(pl["head"], pl["rows"], "plan", A), e(pl["intro"])))

    st = d["structure"]
    inner = (table(st["head"], st["rows"], "struct", A) + f'<p class="note">{e(st["para_note"])}</p>'
             f'<p class="warn"><b>BETREFF · ANREDE</b>{e(st["warn"])}</p>'
             f'<h3 class="sub">{e(st["betreff_title"])}</h3>' + table(st["betreff_head"], st["betreff"], "bt2", A) +
             f'<p class="note">{e(st["betreff_note"])}</p>'
             f'<h3 class="sub">{e(st["rules_title"])}</h3>' + table(st["rules_head"], st["rules"], "rl", A) +
             f'<h3 class="sub">{e(st["ich_title"])}</h3>' + table(st["ich_head"], st["ich"], "ich", A) +
             f'<p class="note">{e(st["ich_note"])}</p>')
    secs.append(section(st["id"], "Aufbau", st["title"], inner, e(st["lead"])))

    of = d["official"]
    secs.append(section(of["id"], "Musterlösung", of["title"],
                        '<ul class="bul">' + "".join(f"<li>{e(t)}</li>" for t in of["items"]) + "</ul>", e(of["intro"])))

    ph = d["phrases"]
    inner = "".join(f'<h3 class="sub">{e(g["title"])}</h3>' + table(ph["head"], g["rows"], "phr2", A) for g in ph["groups"])
    inner += f'<p class="note">{e(ph["closing_note"])}</p>'
    secs.append(section(ph["id"], "Redemittel", ph["title"], inner, e(ph["intro"])))

    an = d["answers"]
    secs.append(section(an["id"], "Beispiele", an["title"], f'<p class="note">{e(an["note"])}</p>' + texts(an), e(an["lead"])))

    ms = d["mistakes"]
    secs.append(section(ms["id"], "Fehler", ms["title"], table(ms["head"], ms["rows"], "mis", A)))

    gr = d["grammar"]
    secs.append(section(gr["id"], "Grammatik", gr["title"], table(gr["head"], gr["rows"], "gram", A), e(gr["intro"])))

    ck = d["checklist"]
    secs.append(section(ck["id"], "Checkliste", ck["title"], '<ul class="chk">' + "".join(
        f'<li><span class="bx" aria-hidden="true"></span><span><b>{i + 1}</b>{e(t)}</span></li>' for i, t in enumerate(ck["items"])) + "</ul>" +
        f'<p class="note adv">{e(d["advice"])}</p>'))

    nav = [("uebersicht", "시험 구조"), ("bewertung", "채점"), ("strategie", "30분 전략"), ("plan", "준비 4단계"),
           ("aufbau", "글의 구조"), ("ausdruecke", "표현"), ("beispiele", "모범 답안 10"), ("fehler", "자주 하는 실수"),
           ("grammatik", "문법"), ("checkliste", "체크리스트")]
    return page("Schreiben", d, nav, secs, CSS_EXTRA)


CSS_EXTRA = """.tbl.crit2 td:first-child,.tbl.tm td:first-child,.tbl.plan td:first-child,.tbl.struct td:first-child,.tbl.gram td:first-child,.tbl.lv5 td:first-child,.tbl.sim td:first-child,.tbl.rl td:first-child,.tbl.phr2 td:first-child,.tbl.bt2 td:first-child{font-weight:700}
.tbl.crit2 td:first-child{white-space:nowrap}
.tbl.lv5 td:first-child{font-size:18px;color:var(--ochre-ink)}
.tbl.lv5 td:nth-child(2){font-weight:700;white-space:nowrap}
.tbl.sim td:nth-child(2),.tbl.sim td:nth-child(3){white-space:nowrap}
.tbl.sim td:nth-child(3){font-weight:700;color:var(--ochre-ink)}
.tbl.tm td:nth-child(2){font-weight:700;color:var(--ochre-ink);white-space:nowrap}
.tbl.plan td:first-child{color:var(--ochre-ink);white-space:nowrap}
.tbl.struct td:first-child{color:var(--ochre-ink);white-space:nowrap}
.tbl.struct td:nth-child(3){font-size:14px}
.tbl.rl td:nth-child(3){color:var(--ink-3);font-size:14px}
.tbl.phr2 td:nth-child(2){font-weight:600}
.tbl.bt2 td:nth-child(2){font-weight:600}
.tbl.ich td:nth-child(2){font-weight:600}
.tbl.gram td:nth-child(2){font-weight:600}
.tbl.gram td:nth-child(3){color:var(--ink-3)}
.tbl.mis td:nth-child(2){font-weight:600}
.tbl.mis td:nth-child(3){color:var(--ink-3);font-size:14px}
.lp{margin:12px 0 0;padding:0;list-style:none;font-size:13.5px;line-height:1.55;color:var(--ink-2)}
.lp li{position:relative;padding-left:16px;margin:0 0 2px}
.lp li::before{content:"·";position:absolute;left:4px;font-weight:700;color:var(--ochre-ink)}
.lt-t{margin-top:0}
.dt{text-align:right;margin:0 0 8px !important;color:var(--ink-3);font-size:13.5px}
.bt{margin:0 0 8px !important}
.bt b{display:inline-block;margin-right:6px;font-size:11.5px;letter-spacing:.1em;color:var(--ochre-ink)}
.adv{margin-top:22px;font-size:15px}
"""


def main():
    d = json.load(open(os.path.join(HERE, "guide-data.json"), encoding="utf-8"))
    html_out = build(d)
    open(OUT, "w", encoding="utf-8").write(html_out)
    finish(OUT, APP)
    print(f"geschrieben: {OUT} ({os.path.getsize(OUT) / 1024:.0f} KB), 모범 답안 {len(d['answers']['items'])}편")


if __name__ == "__main__":
    main()
