#!/usr/bin/env python3
"""index.html(표지 · 응시 방식 · 페이퍼 목록 · 디지털 목록 · 시험별 페이지)을 data/mtN.json과 이 폴더의 PDF·MP3에서 만듭니다.

python3 digital-src/build-index.py        # 이 앱 폴더의 index.html을 다시 씁니다

필요한 것: 이 앱 폴더의 `telc B1 Modelltest N.pdf`, `telc B1 Modelltest N.1.mp3` ~ `N.3.mp3`, digital-src/data/mtN.json
(`index` 블록: 목록용 제목·주제), ffprobe(음원 길이)
"""
import argparse
import base64
import glob
import html
import json
import os
import re
import subprocess
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
LEVEL = "B1"
PREFIX = "sodaTelcB1.v1."
PDF_PAGES = {"lesen": [2, 4, 6, 9, 10], "hoeren": [11, 12, 13], "schreiben": 14, "sprechen": [15, 16, 18],
             "loesung": 19, "muster": 20, "dialoge": 21, "hoertexte": 22, "kommentar": 24}
PDF_PAGE_COUNT = 24
ARROW = ('<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M5.5 2.5 11 8l-5.5 5.5" fill="none" '
         'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ARROW_R = ('<svg width="16" height="16" viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 8h11M9 3.5 13.5 8 9 12.5" fill="none" '
           'stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def e(s):
    return html.escape(str(s), quote=True)


def check_glyphs(font_path, text):
    """Warnt, wenn Zeichen in fonts/pretendard-index.woff fehlen (sie erscheinen dann in der Systemschrift)."""
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        return
    cmap = TTFont(font_path).getBestCmap()
    missing = sorted({c for c in text if ord(c) >= 0x20 and ord(c) not in cmap and not c.isspace()})
    if missing:
        print("Hinweis: Diese Zeichen fehlen in fonts/pretendard-index.woff und erscheinen in der Systemschrift:", "".join(missing))


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                         capture_output=True, text=True, check=True).stdout.strip()
    return float(out)


def mmss(sec):
    s = int(round(sec))
    return f"{s // 60}:{s % 60:02d}"


def roman_no(n):
    return f"{n:02d}"


class Test:
    def __init__(self, n, repo):
        self.n = n
        self.d = json.load(open(os.path.join(HERE, "data", f"mt{n}.json"), encoding="utf-8"))
        self.roman = self.d["roman"]
        self.pdf = quote(f"telc {LEVEL} Modelltest {n}.pdf")
        self.dur = []
        for k in range(1, 4):
            fp = os.path.join(repo, f"telc {LEVEL} Modelltest {n}.{k}.mp3")
            if not os.path.exists(fp):
                sys.exit(f"Audio fehlt: {fp}")
            self.dur.append(duration(fp))
        if not os.path.exists(os.path.join(repo, f"telc {LEVEL} Modelltest {n}.pdf")):
            sys.exit(f"PDF fehlt: Modelltest {n}")
        self.hoeren_min = int(-(-sum(self.dur) // 60)) + 2   # wie in build-digital.py

    def mp3(self, k):
        return quote(f"telc {LEVEL} Modelltest {self.n}.{k}.mp3")

    def pg(self, p):
        return f'{self.pdf}#page={p}'

    def short(self):
        return self.d["index"]["short"]


def link(t, p, label=None):
    return f'<a class="p" href="{t.pg(p)}" target="_blank" rel="noopener">{label or "S. " + str(p)}</a>'


def item(tag, title, desc, right):
    return f'<div class="it"><span class="t">{e(tag)}</span><span class="d" lang="de">{e(title)}<span>{e(desc)}</span></span>{right}</div>'


def paper_page(t):
    d, ix, L = t.d, t.d["index"], t.d["lesen"]
    n = t.n
    pl = PDF_PAGES["lesen"]
    out = []
    out.append(f'<section class="page mdt" id="m{n}" aria-labelledby="m{n}-h">')
    out.append('<div class="brand"><img src="__LOGO__" alt=""><b>Sophia Deutsch Akademie</b></div>')
    out.append('<div class="main">')
    out.append(f'<p class="eyebrow">telc Deutsch {LEVEL}</p>')
    out.append(f'<h2 id="m{n}-h" lang="de">Modelltest {e(t.roman)}</h2>')
    out.append(f'<p class="lead">Lesen · Sprachbausteine · Hören · Schreiben · Sprechen — {PDF_PAGE_COUNT} Seiten, Hörtexte 3 Dateien</p>')
    out.append('<div class="actions">'
               f'<a class="btn" href="{t.pdf}" target="_blank" rel="noopener">PDF 열기</a>'
               f'<a class="btn ghost" href="{t.pdf}" download>PDF 다운로드</a>'
               f'<a class="btn ghost" href="#d{n}">디지털로 풀기</a>'
               f'<a class="btn ghost" href="{t.pg(PDF_PAGES["loesung"])}" target="_blank" rel="noopener">Lösungsschlüssel</a></div>')
    # Lesen + Sprachbausteine
    out.append('<div class="mod"><h3 lang="de">Leseverstehen und Sprachbausteine<small>90 Min.</small></h3>')
    out.append(item("Lesen 1", "Fünf kurze Texte", "Überschriften a–j · Zuordnung · 1–5 · Seite 2–3", link(t, pl[0])))
    out.append(item("Lesen 2", L["t2"]["title"], "Zeitungsartikel · a / b / c · 6–10 · Seite 4–5", link(t, pl[1])))
    out.append(item("Lesen 3", "Situationen und Anzeigen", "Situationen 11–20 · Anzeigen a–l · eine Situation ohne Lösung (x) · Seite 6–8", link(t, pl[2])))
    out.append(item("Sprache 1", ix["sb1"], "Grammatik · a / b / c · 21–30", link(t, pl[3])))
    out.append(item("Sprache 2", ix["sb2"], "Wortschatz · Wortkasten a–o · 31–40", link(t, pl[4])))
    out.append('</div>')
    # Hören
    out.append(f'<div class="mod"><h3 lang="de">Hörverstehen<small>ca. {t.hoeren_min} Min.</small></h3>')
    kinds = [("Kurze Texte", "einmal", "Richtig / Falsch · 41–45"), ("Gespräch", "zweimal", "Richtig / Falsch · 46–55"),
             ("Ansagen und Mitteilungen", "zweimal", "Richtig / Falsch · 56–60")]
    for k in range(3):
        kind, times, what = kinds[k]
        desc = f'{kind} · {times} · {what} · {mmss(t.dur[k])}'
        right = (link(t, PDF_PAGES["hoeren"][k]) +
                 f'<audio controls preload="none" src="{t.mp3(k + 1)}" aria-label="Hören Teil {k + 1}"></audio>'
                 f'<a class="dl" href="{t.mp3(k + 1)}" download>MP3 다운로드</a>')
        out.append(item(f"Hören {k + 1}", ix["hoeren"][f"t{k + 1}"], desc, right))
    out.append('</div>')
    # Schreiben
    out.append('<div class="mod"><h3 lang="de">Schriftlicher Ausdruck<small>30 Min.</small></h3>')
    out.append(item("Aufgabe", ix["schreiben"], "E-Mail beantworten · 4 Leitpunkte · Betreff, Anrede, Schluss", link(t, PDF_PAGES["schreiben"])))
    out.append('</div>')
    # Sprechen
    sp = ix["sprechen"]
    out.append('<div class="mod"><h3 lang="de">Mündlicher Ausdruck<small>ca. 15 Min. · zu zweit</small></h3>')
    out.append(item("Teil 1", "Einander kennenlernen", "Fragen zur Person · Partner/in befragen", link(t, PDF_PAGES["sprechen"][0])))
    out.append(item("Teil 2", sp["t2"], "Über ein Thema sprechen · zwei Meinungen · Teilnehmer/in A und B", link(t, PDF_PAGES["sprechen"][1], "S. 16–17")))
    out.append(item("Teil 3", sp["t3"], "Gemeinsam etwas planen · Vorschläge und Reaktion", link(t, PDF_PAGES["sprechen"][2])))
    out.append('</div>')
    # Materialien
    out.append('<div class="mod"><h3 lang="de">Lösungen und Materialien</h3>')
    out.append(item("Lösungen", "Lösungsschlüssel", "Lesen · Sprachbausteine · Hören · Punkte · Seite 19", link(t, PDF_PAGES["loesung"])))
    out.append(item("Schreiben", "Musterlösung", "Beispiel-E-Mail mit Leitpunkten und Bewertung · Seite 20", link(t, PDF_PAGES["muster"])))
    out.append(item("Sprechen", "Musterdialoge", "Mündlicher Ausdruck Teil 1–3 · Seite 21", link(t, PDF_PAGES["dialoge"])))
    out.append(item("Hörtexte", "Transkripte", "Hören Teil 1–3 · Seite 22–23", link(t, PDF_PAGES["hoertexte"])))
    out.append(item("Lehrende", "Kommentar", "Fallen und Distraktoren · Seite 24", link(t, PDF_PAGES["kommentar"])))
    out.append('</div></div>')
    out.append(f'<div class="foot"><a href="#list">← Modelltest</a><span>telc {LEVEL} · Modelltest {e(t.roman)}</span></div></section>')
    return "\n".join(out)


def digital_page(t):
    n = t.n
    out = []
    out.append(f'<section class="page mdt" id="d{n}" aria-labelledby="d{n}-h">')
    out.append('<div class="brand"><img src="__LOGO__" alt=""><b>Sophia Deutsch Akademie</b></div>')
    out.append('<div class="main">')
    out.append(f'<p class="eyebrow">telc Deutsch {LEVEL} · Digital</p>')
    out.append(f'<h2 id="d{n}-h" lang="de">Modelltest {e(t.roman)}</h2>')
    out.append('<p class="lead">모듈을 고르면 디지털 시험 화면이 열립니다. 시작 전에 화면 사용법(튜토리얼)을 볼 수 있고, 제출하면 바로 채점됩니다.</p>')
    out.append('<div class="mod"><h3 lang="de">Am Computer<small>Lesen · Hören · Schreiben</small></h3>')
    rows = [("Lesen", "Leseverstehen + Sprachbausteine · 40 Aufgaben", "90 Minuten · Lesen 1–3 · Sprachbausteine 1–2 · Markieren", "lesen"),
            ("Hören", "3 Teile · 20 Aufgaben", f"ca. {t.hoeren_min} Minuten · automatische Wiedergabe · Teil 1 einmal, Teil 2 und 3 zweimal · Kopfhörer empfohlen", "hoeren"),
            ("Schreiben", "E-Mail beantworten · 4 Leitpunkte", "30 Minuten · Wörterzähler · Musterlösung zum Vergleich", "schreiben")]
    for tag, title, desc, m in rows:
        out.append(f'<div class="it"><span class="t">{tag}</span><span class="d" lang="de">{title}<span>{desc}</span></span>'
                   f'<a class="go" href="digital.html#{n}-{m}">시작</a><span class="stt" data-m="{m}"></span></div>')
    out.append('</div>')
    out.append('<div class="mod"><h3 lang="de">Mündlicher Ausdruck<small>vor Ort oder per Videokonferenz · zu zweit</small></h3>')
    out.append('<p class="note">Der mündliche Teil ist auch bei der digitalen Prüfung ein Gespräch mit Prüfenden; die Aufgaben stehen im PDF. · '
               '말하기는 디지털 시험에서도 시험관과 대면(또는 화상)으로 봅니다. 과제는 PDF에 있습니다.</p>')
    out.append(item("Sprechen", "Aufgabenblätter", "Teil 1–3", link(t, PDF_PAGES["sprechen"][0])))
    out.append('</div></div>')
    out.append(f'<div class="foot"><a href="#digital">← Modelltest digital</a><a href="#{n}">페이퍼 자료 (PDF · MP3) →</a></div></section>')
    return "\n".join(out)


def toc(tests, prefix, label):
    lis = []
    for t in tests:
        lis.append(f'<li><a class="tocl" href="#{prefix}{t.n}"><span class="no">{roman_no(t.n)}</span><span>'
                   f'<span class="nm" lang="de">Modelltest {e(t.roman)}</span><span class="ds" lang="de">{e(t.short())}</span></span>'
                   f'<span class="lk">{ARROW}</span></a></li>')
    return f'<ol class="toc" aria-label="{label}">\n' + "\n".join(lis) + '\n    </ol>'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=os.path.dirname(HERE))
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    nums = sorted(int(re.search(r"mt(\d+)\.json$", f).group(1)) for f in glob.glob(os.path.join(HERE, "data", "mt*.json")))
    tests = [Test(n, a.repo) for n in nums]
    ids = ["cover", "mode", "list", "digital"] + [f"m{n}" for n in nums] + [f"d{n}" for n in nums]
    hide = ",".join(f'html:not([data-page="{i}"]) #{i}' for i in ids) + "{display:none}"
    anim = ",".join(f"#{i}" for i in ids) + "{animation:pgIn .35s ease both}"
    reduced = "@media (prefers-reduced-motion:reduce){" + ",".join(f"#{i}" for i in ids) + "{animation:none}}"
    css = open(os.path.join(HERE, "index-style.css"), encoding="utf-8").read()
    css = css.replace("/*HIDE*/", hide).replace("/*ANIM*/", anim).replace("/*REDUCED*/", reduced)
    font = base64.b64encode(open(os.path.join(HERE, "fonts", "pretendard-index.woff"), "rb").read()).decode()
    logo = "data:image/png;base64," + base64.b64encode(open(os.path.join(HERE, "logo-index.png"), "rb").read()).decode()
    lo, hi = nums[0], nums[-1]
    rng = f"{lo}–{hi}"
    pre = ('<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           '<meta name="color-scheme" content="light">\n<meta name="robots" content="noindex,nofollow">\n'
           "<script>(function(){var h=location.hash.replace('#','');var p='cover';if(h==='mode'||h==='list'||h==='digital')p=h;"
           f"else if(/^[{lo}-{hi}]$/.test(h))p='m'+h;else if(/^d[{lo}-{hi}]$/.test(h))p=h;"
           "document.documentElement.setAttribute('data-page',p);})();</script>\n"
           f'<title>telc {LEVEL} Modelltest — Sophia Deutsch Akademie</title>\n'
           '<style>/* Pretendard (SIL Open Font License 1.1, digital-src/fonts/Pretendard-OFL.txt), Teilmenge mit den hier verwendeten Zeichen */'
           f'@font-face{{font-family:"Pretendard SODA";src:url(data:font/woff;base64,{font}) format("woff");font-weight:45 930;font-style:normal;font-display:swap}}</style>\n'
           f'<style>\n{css}</style>\n</head>\n<body>\n')
    brand = '<div class="brand"><img src="__LOGO__" alt=""><b>Sophia Deutsch Akademie</b></div>'
    body = f'''<header class="page" id="cover">
  <div class="brand"><img src="__LOGO__" alt="Sophia Deutsch Akademie 로고"><b>Sophia Deutsch Akademie</b></div>
  <div class="main">
    <p class="eyebrow">Prüfungsvorbereitung</p>
    <h1 lang="de">telc {LEVEL}</h1>
    <p class="lead">Modelltest {rng} · Papier und digital</p>
    <div class="rule" aria-hidden="true"></div>
    <a class="start" href="#mode" id="start" style="text-decoration:none">시작하기 {ARROW_R}</a>
  </div>
  <div class="foot"><span>© 2026 Sophia Deutsch Akademie</span></div>
</header>

<section class="page" id="mode" aria-labelledby="mode-h">
  {brand}
  <div class="main">
    <p class="eyebrow">telc {LEVEL}</p>
    <h2 id="mode-h">응시 방식</h2>
    <p class="lead" style="margin:0 0 28px;font-size:15px">보실 시험 방식을 고르세요.</p>
    <div class="modes">
      <a class="mode" href="#list"><span class="mk" lang="de">Papier</span><b>페이퍼 시험</b><span class="ds">PDF 문제지와 듣기 음원(MP3)을 열거나 내려받아 종이에 풉니다. 해답·듣기 대본·모범 답안이 PDF에 함께 있습니다.</span><span class="go2">PDF · 음원 받기 {ARROW}</span></a>
      <a class="mode" href="#digital"><span class="mk" lang="de">Digital</span><b>디지털 시험</b><span class="ds">Lesen · Sprachbausteine · Hören · Schreiben을 컴퓨터 시험 화면에서 풉니다. 남은 시간 표시, 음원 자동 재생, 단어 수 자동 계산, 제출 후 바로 채점됩니다.</span><span class="go2">컴퓨터에서 풀기 {ARROW}</span></a>
      <a class="mode" href="schreiben-guide.html"><span class="mk" lang="de">Leitfaden</span><b lang="de">Schreiben <span lang="ko">시험 가이드</span></b><span class="ds">시험 방식과 채점, 모범 답안</span><span class="go2">가이드 보기 {ARROW}</span></a>
      <a class="mode" href="sprechen-guide.html"><span class="mk" lang="de">Leitfaden</span><b lang="de">Sprechen <span lang="ko">시험 가이드</span></b><span class="ds">시험 방식과 채점, 모범 대화</span><span class="go2">가이드 보기 {ARROW}</span></a>
    </div>
    <p class="note">telc 필기시험은 대부분 컴퓨터(DIGItelc)로 치러집니다. 이 화면은 그 방식에 맞춘 연습용입니다(공식 화면의 복제는 아닙니다). 듣기는 헤드폰을 권합니다. Sprechen은 두 방식 모두 시험관과 함께 봅니다.</p>
  </div>
  <div class="foot"><a href="#">← 표지</a><span>telc {LEVEL}</span></div>
</section>

<section class="page" id="list" aria-labelledby="list-h">
  {brand}
  <div class="main">
    <p class="eyebrow">telc Deutsch {LEVEL} · Papier</p>
    <h2 id="list-h" lang="de">Modelltest</h2>
    <p class="lead">페이퍼 시험 · 모의고사를 선택하면 PDF 문제지와 듣기 음원을 열거나 내려받을 수 있습니다.</p>
    {toc(tests, "", "Modelltest 목록")}
  </div>
  <div class="foot"><a href="#mode">← 응시 방식</a><span>telc {LEVEL} · Papier</span></div>
</section>

<section class="page" id="digital" aria-labelledby="dg-h">
  {brand}
  <div class="main">
    <p class="eyebrow">telc {LEVEL} · Digital</p>
    <h2 id="dg-h" lang="de">Modelltest digital</h2>
    <p class="lead">디지털 시험 · 모의고사를 고른 뒤 Lesen · Hören · Schreiben 모듈을 컴퓨터에서 풉니다.</p>
    {toc(tests, "d", "디지털 Modelltest 목록")}
  </div>
  <div class="foot"><a href="#mode">← 응시 방식</a><span>telc {LEVEL} · Digital</span></div>
</section>

'''
    pages = "\n".join(paper_page(t) for t in tests) + "\n" + "\n".join(digital_page(t) for t in tests) + "\n"
    script = f'''<script>
(function(){{
  var root=document.documentElement;
  function fmt(s){{s=Math.max(0,Math.ceil(s));var m=Math.floor(s/60),x=s%60;return(m<10?'0':'')+m+':'+(x<10?'0':'')+x;}}
  function get(k){{try{{var v=localStorage.getItem('{PREFIX}'+k);return v?JSON.parse(v):null;}}catch(e){{return null;}}}}
  function status(n){{
    var els=document.querySelectorAll('#d'+n+' .stt');
    for(var i=0;i<els.length;i++){{
      var k='mt'+n+'.'+els[i].getAttribute('data-m'),st=get(k+'.state'),rs=get(k+'.result'),t='';
      if(st&&st.remaining>1)t='진행 중 · 남은 시간 '+fmt(st.remaining)+' (이어서 풀기 가능)';
      else if(rs&&rs.score)t='최근 결과 '+rs.score.correct+'/'+rs.score.total+' · '+String(rs.score.points).replace('.',',')+'/'+rs.score.max+'점 ('+rs.finished+')';
      else if(rs)t='최근 제출 '+rs.finished;
      els[i].textContent=t;
    }}
  }}
  function route(){{var h=location.hash.replace('#','');var p='cover';if(h==='mode'||h==='list'||h==='digital')p=h;else if(/^[{lo}-{hi}]$/.test(h))p='m'+h;else if(/^d[{lo}-{hi}]$/.test(h))p=h;root.setAttribute('data-page',p);window.scrollTo(0,0);if(p.charAt(0)==='d'&&p!=='digital')status(p.slice(1));}}
  window.addEventListener('hashchange',route);
  route();
}})();
</script>
</body>
</html>
'''
    doc = (pre + body + pages + script).replace("__LOGO__", logo)
    check_glyphs(os.path.join(HERE, "fonts", "pretendard-index.woff"), re.sub(r"data:[^\"')]+", "", doc))
    out = a.out or os.path.join(a.repo, "index.html")
    open(out, "w", encoding="utf-8").write(doc)
    # Lehrwerk 공통 다크 모드 스위치(tools/soda-theme.py)를 넣습니다
    theme = os.path.join(HERE, "..", "..", "tools", "soda-theme.py")
    if os.path.exists(theme):
        subprocess.run([sys.executable, theme, out, "--kind", "index"], check=True)
    print(f"geschrieben: {out} ({len(doc.encode('utf-8')) / 1024:.0f} KB), Modelltests: {', '.join(str(n) for n in nums)}")


if __name__ == "__main__":
    main()
