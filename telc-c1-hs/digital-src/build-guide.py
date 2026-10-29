#!/usr/bin/env python3
"""telc C1 Hochschule 쓰기 시험 대비 가이드(schreiben-guide.html)를 만듭니다.

입력  guide-data.json   가이드의 모든 글과 모범 답안
출력  ../schreiben-guide.html (이 앱 폴더)

모범 답안의 단어 수(공백으로 센 값)는 이 스크립트가 직접 세고, 350~420 범위를 벗어나면 멈춥니다.
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
RANGE = (350, 420)


def essays(part):
    lo, hi = RANGE
    cards = []
    for i, a in enumerate(part["items"]):
        total = sum(words(t) for _, t in a["paras"])
        if not (lo <= total <= hi):
            sys.exit(f'모범 답안 {i + 1} "{a["title"]}": {total}단어, 범위 {lo}~{hi}를 벗어났습니다')
        if len(a["paras"]) != 5:
            sys.exit(f'모범 답안 {i + 1} "{a["title"]}": 문단이 5개가 아닙니다')
        q = "".join(f'<blockquote class="zq"><p lang="de">{e(t)}</p><footer lang="de">{e(s)}</footer></blockquote>' for t, s in a["quotes"])
        ps = "".join(f'<div class="pa"><p class="pl" lang="de">{e(lb)} <span>{words(t)}</span></p><p lang="de" class="lt-t">{e(t)}</p></div>' for lb, t in a["paras"])
        cards.append(
            f'<details class="lt ess"><summary><span class="lt-n" aria-hidden="true">{NUMS[i]}</span>'
            f'<span class="sm"><b lang="de">{e(a["title"])}</b><span class="lt-p"><span lang="de">{e(a["textsorte"])}</span> · {total}단어</span></span></summary>'
            f'<div class="eb"><p class="sit" lang="de">{e(a["situation"])}</p><p class="tk" lang="de">{e(a["task"])}</p>{q}'
            f'<div class="lt-b">{ps}</div>'
            f'<p class="lt-c"><b>{total}</b> Wörter <span>최소 350</span></p></div></details>')
    return f'<div class="lts">{"".join(cards)}</div>'


def build(d):
    secs = []
    ov = d["overview"]
    secs.append(section(ov["id"], "Überblick", ov["title"],
                        '<dl class="kv">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in ov["rows"]) + "</dl>" +
                        f'<h3 class="sub">{e(d["diff"]["title"])}</h3><p class="note">{e(d["diff"]["text"])}</p>'))

    sc = d["scoring"]
    inner = (table(["기준", "보는 것"], sc["criteria"], "crit2", A) +
             '<h3 class="sub">등급과 점수 (기준마다)</h3>' + table(sc["levels_head"], sc["levels"], "lv5", A) +
             f'<p class="note">{e(sc["levels_note"])}</p>'
             f'<p class="warn"><b>감점 사례</b>{e(sc["zero"])}</p>'
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
             f'<h3 class="sub">{e(st["type_title"])}</h3>' + table(st["type_head"], st["types"], "typ", A) +
             f'<p class="note">{e(st["type_note"])}</p>'
             f'<h3 class="sub">{e(st["zitat_title"])}</h3>' + table(st["zitat_head"], st["zitat"], "zt", A) +
             f'<p class="note">{e(st["zitat_note"])}</p>')
    secs.append(section(st["id"], "Aufbau", st["title"], inner, e(st["lead"])))

    of = d["official"]
    secs.append(section(of["id"], "Musterlösung", of["title"],
                        '<ul class="bul">' + "".join(f"<li>{e(t)}</li>" for t in of["items"]) + "</ul>", e(of["intro"])))

    ph = d["phrases"]
    inner = "".join(f'<h3 class="sub">{e(g["title"])}</h3>' + table(ph["head"], g["rows"], "phr3", A) for g in ph["groups"])
    inner += f'<p class="note">{e(ph["closing_note"])}</p>'
    secs.append(section(ph["id"], "Redemittel", ph["title"], inner, e(ph["intro"])))

    an = d["answers"]
    secs.append(section(an["id"], "Beispiele", an["title"], f'<p class="note">{e(an["note"])}</p>' + essays(an), e(an["lead"])))

    ms = d["mistakes"]
    secs.append(section(ms["id"], "Fehler", ms["title"], table(ms["head"], ms["rows"], "mis", A)))

    gr = d["grammar"]
    secs.append(section(gr["id"], "Grammatik", gr["title"], table(gr["head"], gr["rows"], "gram", A), e(gr["intro"])))

    ck = d["checklist"]
    secs.append(section(ck["id"], "Checkliste", ck["title"], '<ul class="chk">' + "".join(
        f'<li><span class="bx" aria-hidden="true"></span><span><b>{i + 1}</b>{e(t)}</span></li>' for i, t in enumerate(ck["items"])) + "</ul>" +
        f'<p class="note adv">{e(d["advice"])}</p>'))

    nav = [("uebersicht", "시험 구조"), ("bewertung", "채점"), ("strategie", "70분 전략"), ("plan", "준비 4단계"),
           ("aufbau", "글의 구조"), ("ausdruecke", "표현"), ("beispiele", "모범 답안 10"), ("fehler", "자주 하는 실수"),
           ("grammatik", "문법"), ("checkliste", "체크리스트")]
    return page("Schreiben", d, nav, secs, CSS_EXTRA)


CSS_EXTRA = """.tbl.crit2 td:first-child,.tbl.tm td:first-child,.tbl.plan td:first-child,.tbl.struct td:first-child,.tbl.gram td:first-child,.tbl.lv5 td:first-child,.tbl.sim td:first-child,.tbl.phr3 td:first-child,.tbl.typ td:first-child,.tbl.zt td:first-child{font-weight:700}
.tbl.lv5 td:first-child{font-size:18px;color:var(--ochre-ink)}
.tbl.lv5 td:nth-child(2){font-weight:700;white-space:nowrap}
.tbl.sim td:first-child,.tbl.sim td:nth-child(2){white-space:nowrap}
.tbl.sim td:nth-child(2){font-weight:700;color:var(--ochre-ink)}
.tbl.tm td:nth-child(2){font-weight:700;color:var(--ochre-ink);white-space:nowrap}
.tbl.plan td:first-child,.tbl.struct td:first-child{color:var(--ochre-ink);white-space:nowrap}
.tbl.struct td:nth-child(2){white-space:nowrap}
.tbl.struct td:nth-child(4){font-size:14px}
.tbl.phr3 td:nth-child(3){font-weight:600}
.tbl.gram td:nth-child(2),.tbl.mis td:nth-child(2){font-weight:600}
.tbl.gram td:nth-child(3),.tbl.mis td:nth-child(3){color:var(--ink-3)}
.tbl.mis td:nth-child(3){font-size:14px}
.lts{grid-template-columns:1fr}
details.ess{padding:0}
details.ess>summary{display:grid;grid-template-columns:34px minmax(0,1fr);column-gap:8px;align-items:start;padding:16px 20px;cursor:pointer;list-style:none}
details.ess>summary::-webkit-details-marker{display:none}
details.ess>summary::after{content:"펼치기";position:absolute;right:20px;margin-top:2px;font-size:12px;color:var(--ink-3)}
details.ess{position:relative}
details.ess[open]>summary::after{content:"접기"}
.sm b{display:block;font-size:17px;font-weight:800;line-height:1.35;padding-right:48px}
.eb{padding:0 20px 16px}
.sit{font-size:14.5px;font-weight:600;line-height:1.6}
.tk{margin-top:6px;font-size:14px;line-height:1.6;color:var(--ink-2)}
.zq{margin:10px 0 0;padding:10px 14px;border-left:3px solid var(--ochre);background:var(--mist);border-radius:0 10px 10px 0;font-size:14.5px;line-height:1.6}
.zq p{margin:0}
.zq footer{margin-top:4px;font-size:12.5px;color:var(--ink-3)}
.pa{margin:0 0 12px}
.pa:last-child{margin-bottom:0}
.pl{margin:0 0 2px !important;font-size:11.5px;letter-spacing:.1em;font-weight:700;color:var(--ochre-ink)}
.pl span{margin-left:6px;font-weight:600;letter-spacing:0;color:var(--ink-3)}
.lt-t{margin-top:0 !important}
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
