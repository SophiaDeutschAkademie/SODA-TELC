#!/usr/bin/env python3
"""telc B2 말하기 시험 대비 가이드(sprechen-guide.html)를 만듭니다.

입력  sprechen-data.json   가이드의 모든 글과 모범 대화
출력  ../sprechen-guide.html (이 앱 폴더)

빌드할 때 모범 대화의 단어 수가 Teil별 범위 안에 드는지, A와 B가 번갈아 말하는지 검사하고 어긋나면 멈춥니다.
공통 헬퍼와 기본 CSS는 guidelib.py 에 있습니다(schreiben-guide.html과 공유).

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


def dialogs(part, offset=0):
    lo, hi = part["range"]
    out = []
    for i, dg in enumerate(part["dialogs"]):
        n = sum(words(ln.split(": ", 1)[1]) for ln in dg["lines"])
        if not (lo <= n <= hi):
            sys.exit(f'{part["no"]} 대화 {i + 1} "{dg["title"]}": {n}단어, 범위 {lo}~{hi}를 벗어났습니다')
        who = [ln.split(": ", 1)[0] for ln in dg["lines"]]
        if any(a == b for a, b in zip(who, who[1:])) or who[0] != "A":
            sys.exit(f'{part["no"]} 대화 {i + 1} "{dg["title"]}": A와 B가 번갈아 말하지 않습니다')
        head = (f'<header class="lt-h"><span class="lt-n" aria-hidden="true">{NUMS[i + offset]}</span>'
                f'<div><h3 lang="de">{e(dg["title"])}</h3><p class="lt-p">{len(dg["lines"])}턴 · 약 {n}단어</p></div></header>')
        ctx = ""
        if dg.get("kontext"):
            ctx += f'<p class="dg-t"><b>상황</b><span>{e(dg["kontext"])}</span></p>'
        if dg.get("aufgabe"):
            ctx += f'<p class="dg-t"><b>Aufgabe</b><span lang="de">{e(dg["aufgabe"])}</span></p>'
        if dg.get("text"):
            ctx += f'<p class="dg-t"><b>Text</b><span lang="de">{e(dg["text"])}</span></p>'
        if dg.get("hint"):
            ctx += f'<p class="dg-t"><b>연습 힌트</b><span lang="de">{e(dg["hint"])}</span></p>'
        lines = []
        for ln in dg["lines"]:
            w, txt = ln.split(": ", 1)
            lines.append(f'<p class="dl"><b aria-label="{w}">{w}</b><span lang="de">{e(txt)}</span></p>')
        out.append(f'<article class="dg">{head}{ctx}<div class="dg-b">{"".join(lines)}</div></article>')
    return f'<div class="dgs">{"".join(out)}</div>'


def lst(items):
    return '<ul class="bul" lang="de">' + "".join(f"<li>{e(t)}</li>" for t in items) + "</ul>"


def build(d):
    secs = []
    ov = d["overview"]
    secs.append(section(ov["id"], "Überblick", ov["title"],
                        '<dl class="kv">' + "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in ov["rows"]) + "</dl>" +
                        f'<h3 class="sub">{e(d["diff"]["title"])}</h3><p class="note">{e(d["diff"]["text"])}</p>'))

    sc = d["scoring"]
    inner = (table(sc["head"], sc["criteria"], "crit4", A) + f'<p class="note">{e(sc["sum_note"])}</p>' +
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

    t1 = d["teil1"]
    inner = (f'<h3 class="sub">{e(t1["topics_title"])}</h3>' + table(t1["topics_head"], t1["topics"], "tp", A) +
             f'<h3 class="sub">{e(t1["tips_title"])}</h3><ul class="bul">' + "".join(f"<li>{e(t)}</li>" for t in t1["tips"]) + "</ul>" +
             f'<h3 class="sub">{e(t1["phrases_title"])}</h3>' + table(t1["phrases_head"], t1["phrases"], "phr2", A) +
             f'<h3 class="sub">{e(t1["dialogs_title"])}</h3><p class="note">{e(t1["dialogs_note"])}</p>' + dialogs(t1, 0))
    secs.append(section(t1["id"], t1["no"], t1["title"], inner, e(t1["lead"])))

    t2 = d["teil2"]
    inner = (f'<p class="warn"><b>요약으로 끝내지 마세요</b>{e(t2["warn"])}</p>' +
             f'<h3 class="sub">{e(t2["steps_title"])}</h3>' + table(t2["steps_head"], t2["steps"], "flow3", A) + f'<p class="note">{e(t2["steps_note"])}</p>' +
             f'<h3 class="sub">{e(t2["phrases_title"])}</h3>' + table(t2["phrases_head"], t2["phrases"], "phr2", A) +
             f'<h3 class="sub">{e(t2["dialogs_title"])}</h3><p class="note">{e(t2["dialogs_note"])}</p>' + dialogs(t2, 7) +
             f'<h3 class="sub">{e(t2["practice_title"])}</h3>' + lst(t2["practice"]))
    secs.append(section(t2["id"], t2["no"], t2["title"], inner, e(t2["lead"])))

    t3 = d["teil3"]
    inner = (f'<h3 class="sub">{e(t3["steps_title"])}</h3>' + table(t3["steps_head"], t3["steps"], "flow3", A) +
             f'<p class="warn"><b>한 번은 반대하세요</b>{e(t3["warn"])}</p>' +
             f'<h3 class="sub">{e(t3["phrases_title"])}</h3>' + table(t3["phrases_head"], t3["phrases"], "phr2", A) +
             f'<h3 class="sub">{e(t3["dialogs_title"])}</h3><p class="note">{e(t3["dialogs_note"])}</p>' + dialogs(t3, 11) +
             f'<h3 class="sub">{e(t3["practice_title"])}</h3>' + lst(t3["practice"]))
    secs.append(section(t3["id"], t3["no"], t3["title"], inner, e(t3["lead"])))

    so = d["sos"]
    secs.append(section(so["id"], "Hilfe", so["title"], table(so["head"], so["rows"], "phr2", A), e(so["intro"])))

    ms = d["mistakes"]
    secs.append(section(ms["id"], "Fehler", ms["title"], table(ms["head"], ms["rows"], "mis", A)))

    g = d["grammar"]
    secs.append(section(g["id"], "Grammatik", g["title"], table(g["head"], g["rows"], "gr", A), e(g["intro"])))

    ck = d["checklist"]
    secs.append(section(ck["id"], "Checkliste", ck["title"], '<ul class="chk">' + "".join(
        f'<li><span class="bx" aria-hidden="true"></span><span><b>{i + 1}</b>{e(t)}</span></li>' for i, t in enumerate(ck["items"])) + "</ul>" +
        f'<p class="note adv">{e(d["advice"])}</p>'))

    nav = [("uebersicht", "시험 구조"), ("bewertung", "채점"), ("strategie", "점수 전략"), ("vorbereitung", "20분 준비"),
           ("plan", "준비 4단계"), ("teil1", "Teil 1 경험 발표"), ("teil2", "Teil 2 토론"), ("teil3", "Teil 3 함께 계획"),
           ("sos", "막힐 때"), ("fehler", "자주 하는 실수"), ("grammatik", "문법"), ("checkliste", "체크리스트")]
    return page("Sprechen", d, nav, secs, CSS_EXTRA)


CSS_EXTRA = """.tbl.crit4 td:first-child,.tbl.sim td:first-child,.tbl.prep td:first-child,.tbl.plan td:first-child,.tbl.tp td:first-child,.tbl.phr2 td:first-child,.tbl.flow3 td:first-child,.tbl.gr td:first-child{font-weight:700}
.tbl.crit4 td:nth-child(3),.tbl.crit4 td:nth-child(4){white-space:nowrap;font-weight:700;color:var(--ochre-ink)}
.tbl.sim td:nth-child(n+2):nth-child(-n+5){white-space:nowrap;text-align:center}
.tbl.sim th:nth-child(n+2):nth-child(-n+5){text-align:center}
.tbl.sim td:nth-child(5){font-weight:700;color:var(--ochre-ink)}
.tbl.prep td:first-child,.tbl.plan td:first-child{color:var(--ochre-ink);white-space:nowrap}
.tbl.tp td:first-child,.tbl.flow3 td:first-child{color:var(--ochre-ink);white-space:nowrap}
.tbl.tp td:nth-child(2){color:var(--ink-3)}
.tbl.tp td:nth-child(3),.tbl.phr2 td:nth-child(2),.tbl.flow3 td:nth-child(3),.tbl.gr td:nth-child(2){font-weight:600}
.tbl.mis td:nth-child(2){font-weight:600}
.tbl.mis td:nth-child(3){color:var(--ink-3);font-size:14px}
.tbl.gr td:nth-child(3){color:var(--ink-3)}
.dgs{display:grid;gap:16px;margin-top:6px}
.dg{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 20px 16px}
.dg-t{margin-top:12px;font-size:14px;line-height:1.6;color:var(--ink-2)}
.dg-t b{display:inline-block;margin-right:8px;font-size:11.5px;letter-spacing:.12em;color:var(--ochre-ink)}
.dg-b{margin-top:12px;padding:12px 14px;background:var(--mist);border-radius:10px}
.dl{display:grid;grid-template-columns:26px minmax(0,1fr);column-gap:8px;margin:0 0 7px;font-size:14.5px;line-height:1.65;word-break:normal}
.dl:last-child{margin-bottom:0}
.dl b{width:22px;height:22px;margin-top:2px;border-radius:50%;background:var(--navy);color:var(--ivory);font-size:12px;line-height:22px;text-align:center}
.adv{margin-top:22px;font-size:15px}
@media print{.dg{break-inside:avoid}}
"""


def main():
    d = json.load(open(os.path.join(HERE, "sprechen-data.json"), encoding="utf-8"))
    html = build(d)
    open(OUT, "w", encoding="utf-8").write(html)
    finish(OUT, APP)
    c = [len(d[k]["dialogs"]) for k in ("teil1", "teil2", "teil3")]
    print(f"geschrieben: {OUT} ({os.path.getsize(OUT) / 1024:.0f} KB), 모범 대화 {c[0]}+{c[1]}+{c[2]}편")


if __name__ == "__main__":
    main()
