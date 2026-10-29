#!/usr/bin/env python3
"""telc C1 Hochschule 말하기 시험 대비 가이드(sprechen-guide.html)를 만듭니다.

입력  sprechen-data.json   가이드의 모든 글과 모범 발표·요약·토론
출력  ../sprechen-guide.html (이 앱 폴더)

빌드할 때 모범 예시의 단어 수가 Teil별 범위 안에 드는지, 요약·토론에서 화자가 번갈아 말하는지 검사하고
어긋나면 멈춥니다. 공통 헬퍼와 기본 CSS는 guidelib.py 에 있습니다(schreiben-guide.html과 공유).

사용법 (앱 폴더에서)
  python3 -I digital-src/build-sprechen.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # python3 -I 로 돌려도 guidelib를 찾도록
from guidelib import NUMS, e, finish, page, section, table, words  # noqa: E402

APP = os.path.dirname(HERE)
OUT = os.path.join(APP, "sprechen-guide.html")
A = "auto"


def check(part, name, counts):
    lo, hi = part["range"]
    for i, n in enumerate(counts):
        if not (lo <= n <= hi):
            sys.exit(f'{name} {i + 1}: {n}단어, 범위 {lo}~{hi}를 벗어났습니다')


def det(num, title, sub, body, open_=False):
    return (f'<details class="dg ess"><summary><span class="lt-n" aria-hidden="true">{num}</span>'
            f'<span class="sm"><b lang="de">{e(title)}</b><span class="lt-p">{sub}</span></span></summary>'
            f'<div class="eb">{body}</div></details>')


def presentations(part, offset=0):
    counts = [sum(words(t) for _, t in m["paras"]) for m in part["models"]]
    check(part, "모범 발표", counts)
    out = []
    for i, (m, n) in enumerate(zip(part["models"], counts)):
        if len(m["paras"]) != 5:
            sys.exit(f'모범 발표 {i + 1}: 문단이 5개가 아닙니다')
        ps = "".join(f'<div class="pa"><p class="pl" lang="de">{e(lb)} <span>{words(t)}</span></p><p lang="de" class="lt-t">{e(t)}</p></div>' for lb, t in m["paras"])
        body = (f'<p class="dg-t"><b>Aufgabe</b><span lang="de">{e(m["aufgabe"])}</span></p><div class="dg-b">{ps}</div>'
                f'<p class="lt-c"><b>{n}</b> Wörter <span>약 3분</span></p>')
        out.append(det(NUMS[i + offset], m["title"], f'Präsentation · {n}단어', body))
    return f'<div class="dgs">{"".join(out)}</div>'


def turns_html(turns):
    return "".join(f'<p class="dl"><b aria-label="{w}">{w}</b><span lang="de">{e(t)}</span></p>' for w, t in turns)


def summaries(part, offset):
    counts = [sum(words(t) for _, t in m) for m in part["models"]]
    check(part, "모범 요약·문답", counts)
    out = []
    for i, (m, n) in enumerate(zip(part["models"], counts)):
        who = [w for w, _ in m]
        if any(a == b for a, b in zip(who, who[1:])):
            sys.exit(f'모범 요약·문답 {i + 1}: 화자가 번갈아 말하지 않습니다')
        body = f'<div class="dg-b">{turns_html(m)}</div><p class="lt-c"><b>{n}</b> Wörter <span>약 2분</span></p>'
        out.append(det(NUMS[i + offset], f"Zusammenfassung und Anschlussfragen {NUMS[i + offset]}", f'{len(m)}턴 · {n}단어', body))
    return f'<div class="dgs">{"".join(out)}</div>'


def discussions(part, offset, question):
    counts = [sum(words(t) for _, t in m["turns"]) for m in part["models"]]
    check(part, "모범 토론", counts)
    out = []
    for i, (m, n) in enumerate(zip(part["models"], counts)):
        who = [w for w, _ in m["turns"]]
        if any(a == b for a, b in zip(who, who[1:])) or who[0] != "A":
            sys.exit(f'모범 토론 {i + 1}: 화자가 번갈아 말하지 않습니다')
        z = f'<blockquote class="zq"><p lang="de">{e(m["zitat"])}</p><footer lang="de">{e(m["by"])}</footer></blockquote>'
        body = (z + f'<p class="dg-t"><b>Aufgabe</b><span lang="de">{e(question)}</span></p>'
                f'<div class="dg-b">{turns_html(m["turns"])}</div><p class="lt-c"><b>{n}</b> Wörter <span>약 5~6분</span></p>')
        out.append(det(NUMS[i + offset], m["zitat"].strip("„“"), f'Diskussion · {len(m["turns"])}턴 · {n}단어', body))
    return f'<div class="dgs">{"".join(out)}</div>'


def phrases(p):
    return f'<h3 class="sub">{e(p["phrases_title"])}</h3>' + table(p["phrases_head"], p["phrases"], "phr3", A)


def stepsblock(p, cls):
    return f'<h3 class="sub">{e(p["steps_title"])}</h3>' + table(p["steps_head"], p["steps"], cls, A) + f'<p class="note">{e(p["steps_note"])}</p>'


def build(d):
    secs = []
    ov = d["overview"]
    secs.append(section(ov["id"], "Überblick", ov["title"],
                        '<dl class="kv">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in ov["rows"]) + "</dl>" +
                        f'<h3 class="sub">{e(d["diff"]["title"])}</h3><p class="note">{e(d["diff"]["text"])}</p>'))

    sc = d["scoring"]
    inner = (table(sc["head"], sc["criteria"], "crit3", A) + f'<p class="note">{e(sc["sum_note"])}</p>' +
             f'<h3 class="sub">{e(sc["rules_title"])}</h3><ul class="bul">' + "".join(f"<li>{e(r)}</li>" for r in sc["rules"]) + "</ul>")
    secs.append(section(sc["id"], "Bewertung", sc["title"], inner, e(sc["intro"])))

    sg = d["strategy"]
    inner = ('<ol class="num circ">' + "".join(f'<li><span class="n">{e(n)}</span><span>{e(t)}</span></li>' for n, t in sg["tips"]) + "</ol>" +
             '<h3 class="sub">점수 시뮬레이션</h3>' + table(sg["sim_head"], sg["sim"], "sim", A) + f'<p class="note">{e(sg["sim_note"])}</p>')
    secs.append(section(sg["id"], "Strategie", sg["title"], inner, e(sg["intro"])))

    st = d["steps"]
    secs.append(section(st["id"], "Vorbereitung", st["title"], table(st["head"], st["rows"], "prep", A) +
                        f'<p class="warn"><b>문장을 적지 마세요</b>{e(st["warn"])}</p>', e(st["intro"])))

    pl = d["plan"]
    secs.append(section(pl["id"], "Lernplan", pl["title"], table(pl["head"], pl["rows"], "plan", A), e(pl["intro"])))

    t = d["teil1a"]
    inner = (f'<h3 class="sub">{e(t["aufgabe_title"])}</h3><p class="dg-t" lang="de">{e(t["aufgabe"])}</p>'
             f'<h3 class="sub">{e(t["topics_title"])}</h3><ul class="bul" lang="de">' + "".join(f"<li>{e(x)}</li>" for x in t["topics"]) + "</ul>" +
             f'<p class="note">{e(t["topics_note"])}</p>' + stepsblock(t, "flow4") + phrases(t) +
             f'<h3 class="sub">{e(t["models_title"])}</h3><p class="note">{e(t["models_note"])}</p>' + presentations(t, 0))
    secs.append(section(t["id"], t["no"], t["title"], inner, e(t["lead"])))

    t = d["teil1b"]
    inner = (f'<h3 class="sub">{e(t["aufgabe_title"])}</h3><p class="dg-t" lang="de">{e(t["aufgabe"])}</p>' + stepsblock(t, "flow4") +
             f'<h3 class="sub">{e(t["notes_title"])}</h3><p class="note">{e(t["notes"])}</p>' + phrases(t) +
             f'<h3 class="sub">{e(t["models_title"])}</h3><p class="note">{e(t["models_note"])}</p>' + summaries(t, 4))
    secs.append(section(t["id"], t["no"], t["title"], inner, e(t["lead"])))

    t = d["teil2"]
    inner = (f'<p class="warn"><b>반응 없는 발언은 독백입니다</b>{e(t["warn"])}</p>' +
             f'<h3 class="sub">{e(t["aufgabe_title"])}</h3><p class="dg-t" lang="de">{e(t["aufgabe"])}</p>' + stepsblock(t, "flow3") + phrases(t) +
             f'<h3 class="sub">{e(t["models_title"])}</h3><p class="note">{e(t["models_note"])}</p>' + discussions(t, 6, t["aufgabe"]))
    secs.append(section(t["id"], t["no"], t["title"], inner, e(t["lead"])))

    ms = d["mistakes"]
    secs.append(section(ms["id"], "Fehler", ms["title"], table(ms["head"], ms["rows"], "mis", A)))

    g = d["grammar"]
    secs.append(section(g["id"], "Grammatik", g["title"], table(g["head"], g["rows"], "gr", A), e(g["intro"])))

    ck = d["checklist"]
    secs.append(section(ck["id"], "Checkliste", ck["title"], '<ul class="chk">' + "".join(
        f'<li><span class="bx" aria-hidden="true"></span><span><b>{i + 1}</b>{e(x)}</span></li>' for i, x in enumerate(ck["items"])) + "</ul>" +
        f'<p class="note adv">{e(d["advice"])}</p>'))

    nav = [("uebersicht", "시험 구조"), ("bewertung", "채점"), ("strategie", "점수 전략"), ("vorbereitung", "20분 준비"),
           ("plan", "준비 4단계"), ("teil1a", "Teil 1A 발표"), ("teil1b", "Teil 1B 요약·질문"), ("teil2", "Teil 2 토론"),
           ("fehler", "자주 하는 실수"), ("grammatik", "문법"), ("checkliste", "체크리스트")]
    return page("Sprechen", d, nav, secs, CSS_EXTRA)


CSS_EXTRA = """.tbl.crit3 td:first-child,.tbl.sim td:first-child,.tbl.prep td:first-child,.tbl.plan td:first-child,.tbl.phr3 td:first-child,.tbl.flow3 td:first-child,.tbl.flow4 td:first-child,.tbl.gr td:first-child{font-weight:700}
.tbl.crit3 td:nth-child(3){white-space:nowrap;font-weight:700;color:var(--ochre-ink)}
.tbl.sim td:nth-child(n+2){white-space:nowrap;text-align:center}
.tbl.sim th:nth-child(n+2){text-align:center}
.tbl.sim td:nth-child(4){font-weight:700;color:var(--ochre-ink)}
.tbl.prep td:first-child,.tbl.plan td:first-child{color:var(--ochre-ink);white-space:nowrap}
.tbl.flow3 td:first-child,.tbl.flow4 td:first-child{color:var(--ochre-ink);white-space:nowrap}
.tbl.flow4 td:nth-child(2){white-space:nowrap}
.tbl.flow4 td:nth-child(4),.tbl.flow3 td:nth-child(3),.tbl.phr3 td:nth-child(3),.tbl.gr td:nth-child(2){font-weight:600}
.tbl.flow4 td:nth-child(4),.tbl.flow3 td:nth-child(3){font-size:14px}
.tbl.mis td:nth-child(2){font-weight:600}
.tbl.mis td:nth-child(3),.tbl.gr td:nth-child(3){color:var(--ink-3)}
.tbl.mis td:nth-child(3){font-size:14px}
.dgs{display:grid;gap:12px;margin-top:6px}
.dg{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:0;position:relative}
details.ess>summary{display:grid;grid-template-columns:34px minmax(0,1fr);column-gap:8px;align-items:start;padding:16px 20px;cursor:pointer;list-style:none}
details.ess>summary::-webkit-details-marker{display:none}
details.ess>summary::after{content:"펼치기";position:absolute;right:20px;top:18px;font-size:12px;color:var(--ink-3)}
details.ess[open]>summary::after{content:"접기"}
.sm b{display:block;font-size:16px;font-weight:800;line-height:1.4;padding-right:48px}
.eb{padding:0 20px 16px}
.dg-t{margin-top:12px;font-size:14px;line-height:1.6;color:var(--ink-2)}
.dg-t b{display:inline-block;margin-right:8px;font-size:11.5px;letter-spacing:.12em;color:var(--ochre-ink)}
.dg-b{margin-top:12px;padding:12px 14px;background:var(--mist);border-radius:10px}
.dl{display:grid;grid-template-columns:26px minmax(0,1fr);column-gap:8px;margin:0 0 7px;font-size:14.5px;line-height:1.65;word-break:normal}
.dl:last-child{margin-bottom:0}
.dl b{width:22px;height:22px;margin-top:2px;border-radius:50%;background:var(--navy);color:var(--ivory);font-size:12px;line-height:22px;text-align:center}
.zq{margin:10px 0 0;padding:10px 14px;border-left:3px solid var(--ochre);background:var(--mist);border-radius:0 10px 10px 0;font-size:14.5px;line-height:1.6}
.zq p{margin:0}
.zq footer{margin-top:4px;font-size:12.5px;color:var(--ink-3)}
.pa{margin:0 0 12px;font-size:14.5px;line-height:1.65;word-break:normal}
.pa:last-child{margin-bottom:0}
.pa p{margin:0}
.pl{margin:0 0 2px !important;font-size:11.5px;letter-spacing:.1em;font-weight:700;color:var(--ochre-ink)}
.pl span{margin-left:6px;font-weight:600;letter-spacing:0;color:var(--ink-3)}
.adv{margin-top:22px;font-size:15px}
@media print{.dg{break-inside:avoid}}
"""


def main():
    d = json.load(open(os.path.join(HERE, "sprechen-data.json"), encoding="utf-8"))
    html_out = build(d)
    open(OUT, "w", encoding="utf-8").write(html_out)
    finish(OUT, APP)
    c = [len(d[k]["models"]) for k in ("teil1a", "teil1b", "teil2")]
    print(f"geschrieben: {OUT} ({os.path.getsize(OUT) / 1024:.0f} KB), 모범 예시 {c[0]}+{c[1]}+{c[2]}편")


if __name__ == "__main__":
    main()
