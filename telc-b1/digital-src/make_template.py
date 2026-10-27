#!/usr/bin/env python3
"""telc-B1-Vorlage aus der telc-B2-Vorlage ableiten.

python3 digital-src/make_template.py      # b2.template.html  ->  template.html

b2.template.html ist eine unveränderte Kopie von ../telc-b2/digital-src/template.html.
Unterschiede zu B2 (telc Deutsch B1):
- Schriftlicher Ausdruck: genau eine Aufgabe (E-Mail beantworten, vier Leitpunkte), kein Mindestumfang;
  Musterlösung mit Leitpunkt-Markierungen und Randnotizen.
- Hören: Dauer je Modelltest aus den Audiodateien; Teil 1 einmal, Teil 2 und 3 zweimal.
- Lesen Teil 3 heißt »Anzeigen a–l«; Anzeigen-Designs wie bei B2 (logo mit Anfangsbuchstabe).
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "b2.template.html"), encoding="utf-8").read()
out = src


def sub1(old, new, count=1):
    global out
    n = out.count(old)
    assert n == count, f"{n}x statt {count}x: {old[:90]!r}"
    out = out.replace(old, new)


def repline(prefix, new):
    """die eine Zeile ersetzen, die (ohne Einrückung) mit prefix beginnt"""
    global out
    lines = out.split("\n")
    idx = [i for i, ln in enumerate(lines) if ln.lstrip().startswith(prefix)]
    assert len(idx) == 1, f"{len(idx)} Zeilen mit {prefix[:70]!r}"
    ind = lines[idx[0]][: len(lines[idx[0]]) - len(lines[idx[0]].lstrip())]
    lines[idx[0]] = ind + new
    out = "\n".join(lines)


def block(start, end, new):
    """alles von start (einschließlich) bis end (ausschließlich) ersetzen"""
    global out
    assert out.count(start) == 1, f"{out.count(start)}x: {start[:80]!r}"
    i = out.index(start)
    j = out.index(end, i)
    out = out[:i] + new + out[j:]


# ------------------------------------------------------------------ Titel, Schlüssel, Konstanten
sub1("<title>telc Deutsch B2 digital — Sophia Deutsch Akademie</title>", "<title>telc Deutsch B1 digital — Sophia Deutsch Akademie</title>")
sub1("var PREFIX = 'sodaTelcB2.v1.';", "var PREFIX = 'sodaTelcB1.v1.';")
sub1("hoeren: { name: 'Hören', full: 'Hörverstehen', minutes: 20, ko: '듣기' },", "hoeren: { name: 'Hören', full: 'Hörverstehen', minutes: 30, ko: '듣기' },")
sub1("var WORDS_MIN = 150;", "var WORDS_MIN = 0;   /* telc B1 nennt im Aufgabentext keinen Mindestumfang: nur Wörterzähler */")
sub1("  var T = D.tests[R.mt];\n", "  var T = D.tests[R.mt];\n  if (T.minutes && T.minutes.hoeren) MOD.hoeren.minutes = T.minutes.hoeren;   /* Dauer der Audiodateien + Zeit zum Antworten */\n")
sub1("' — telc B2 digital';", "' — telc B1 digital';")
sub1("<span class=\"gz\">telc Deutsch </span>B2 · ", "<span class=\"gz\">telc Deutsch </span>B1 · ")
sub1("'<h1>telc Deutsch B2 · ' + info.full + '</h1>'", "'<h1>telc Deutsch B1 · ' + info.full + '</h1>'")
sub1("var lines = ['telc Deutsch B2 · Modelltest '", "var lines = ['telc Deutsch B1 · Modelltest '")
sub1("var fname = 'telc B2 Modelltest '", "var fname = 'telc B1 Modelltest '")
sub1("var subj = 'telc B2 Modelltest '", "var subj = 'telc B1 Modelltest '")

# ------------------------------------------------------------------ Zusatz-CSS (Mail im Aufgabentext, Musterlösung)
sub1(".wc.low b{color:var(--warn)}", """.wc.low b{color:var(--warn)}
.mailbox{border:1px solid var(--line);border-left:4px solid var(--acc);border-radius:6px;background:#f8f9fb;padding:12px 16px 4px;margin:4px 0 14px}
.mailbox p{margin:0 0 .7em}
.mdl.pp{white-space:normal}
.mdl.pp p{position:relative;margin:0 0 .75em;padding-left:30px}
.mdl.pp p.nolp{padding-left:0}
.mdl.pp .lp{position:absolute;left:0;top:.15em;display:inline-flex;align-items:center;justify-content:center;width:21px;height:21px;border-radius:50%;background:var(--acc);color:#fff;font-size:12.5px;font-weight:700}
.mnotes{white-space:pre-wrap;font-family:var(--font);font-size:14px;line-height:1.55;color:var(--ink-2);background:#fff;border:1px solid var(--line);border-radius:6px;padding:10px 14px;margin:10px 0 0}
html[data-theme="dark"] .mailbox{background:var(--soft)}
html[data-theme="dark"] .mnotes{background:var(--panel)}""")

# ------------------------------------------------------------------ Anzeigen (Lesen Teil 3)
sub1("leftTitle: 'Info-Texte a–l', rightTitle: 'Situationen 11–20',", "leftTitle: 'Anzeigen a–l', rightTitle: 'Situationen 11–20',")
sub1("return selItem(it, 'Info-Text:', L12.concat(['x']));", "return selItem(it, 'Anzeige:', L12.concat(['x']));")
sub1("var m = /^(.{3,70}?[.:])(\\s+)([\\s\\S]*)$/.exec(arr[0]);", "var m = /^([^,]{3,60}?[.:])(\\s+)([\\s\\S]*)$/.exec(arr[0]);")
sub1("var ini = String(n.main || '?').trim().charAt(0);", "var ini = dc.ini || String(n.main || '?').trim().charAt(0);")
sub1("right: '<p class=\"inst\">' + esc(L.t2.taskInstruction) + '</p>' + L.t2.items.map(abcItem).join('') });",
     "right: (L.t2.taskInstruction ? '<p class=\"inst\">' + esc(L.t2.taskInstruction) + '</p>' : '') + L.t2.items.map(abcItem).join('') });")


# Gruss und Name in einem Absatz (Zeilenumbruch) · Sprachbausteine Teil 2 ohne Überschrift
sub1("      return '<p>' + esc(p).replace(/\\{\\{(\\d+)\\}\\}/g, function (m, n) {",
     "      return '<p>' + esc(p).replace(/\\n/g, '<br>').replace(/\\{\\{(\\d+)\\}\\}/g, function (m, n) {")
sub1("left: '<article class=\"card doc\"><h3 class=\"h1t\">' + esc(L.sb2.title) + '</h3>' + gapParas(L.sb2.paragraphs) + '</article>',",
     "left: '<article class=\"card doc\">' + (L.sb2.title ? '<h3 class=\"h1t\">' + esc(L.sb2.title) + '</h3>' : '') + gapParas(L.sb2.paragraphs) + '</article>',")

# ------------------------------------------------------------------ Schreiben: eine E-Mail-Aufgabe
block("  function taskHTML(tk) {", "  var M = R.mod === 'lesen'", """  function taskHTML(tk) {
    var h = '<div class="task"><p class="ctxl">' + esc(tk.lead) + '</p>';
    h += '<div class="mailbox">' + (tk.mail || []).map(function (p) { return '<p>' + esc(p).replace(/\\n/g, '<br>') + '</p>'; }).join('') + '</div>';
    h += '<p>' + esc(tk.instruction) + '</p>';
    h += '<ul class="pts">' + (tk.points || []).map(function (p) { return '<li>' + esc(p) + '</li>'; }).join('') + '</ul>';
    return h + '<p>' + esc(tk.closing) + '</p></div>';
  }
  function buildSchreiben() {
    var tk = T.schreiben.task;
    T.schreiben.tasks = [tk];   /* gemeinsame Ergebnis-/Textausgabe wie bei mehreren Aufgaben */
    var pages = [{ key: 'S1', teil: 1, title: 'Schriftlicher Ausdruck', leftTitle: 'E-Mail beantworten',
      left: (T.schreiben.intro ? '<p class="inst">' + esc(T.schreiben.intro) + '</p>' : '') + taskHTML(tk), task: tk }];
    return { pages: pages, items: [], teile: [1], two: true, writing: true, labels: { 1: 'E-Mail' } };
  }

""")

# Reiter: nur ein Teil; »fertig«, sobald ein Text da ist
sub1("        done = wc >= WORDS_MIN;", "        done = wc > 0;")
sub1("$('#wc').classList.toggle('low', n > 0 && n < WORDS_MIN);", "$('#wc').classList.toggle('low', WORDS_MIN > 0 && n > 0 && n < WORDS_MIN);")
sub1("'<div class=\"wc\" id=\"wc\"><span>mindestens ' + WORDS_MIN + ' Wörter</span><span>Wörter: <b id=\"wcn\">0</b></span></div>",
     "'<div class=\"wc\" id=\"wc\"><span>' + (WORDS_MIN ? 'mindestens ' + WORDS_MIN + ' Wörter' : 'Wörterzähler (zur Orientierung)') + '</span><span>Wörter: <b id=\"wcn\">0</b></span></div>")
sub1("aria-label=\"Text für Aufgabe ' + p.teil + '\"></textarea>'", "aria-label=\"Ihre E-Mail\"></textarea>'")

# Abgabe-Dialog / Zählung
sub1("if (M.writing) return [1, 2].some(function (n) { return String(S.texts[n] || '').trim(); }) ? 0 : 1;",
     "if (M.writing) return String(S.texts[1] || '').trim() ? 0 : 1;")
block("      var both = [1, 2].every(", "    } else {\n      de = open ? 'Sie haben noch ' + open", """      de = open ? 'Sie haben noch keinen Text geschrieben. Möchten Sie das Modul trotzdem abgeben?' : 'Möchten Sie das Modul jetzt abgeben? Danach können Sie Ihren Text nicht mehr ändern.';
      ko = open ? '아직 아무 글도 쓰지 않았습니다. 그래도 제출할까요?' : '지금 제출할까요? 제출하면 더 이상 고칠 수 없습니다.';
""")
sub1("if (M.writing) res.texts = { 1: S.texts[1] || '', 2: S.texts[2] || '' };", "if (M.writing) res.texts = { 1: S.texts[1] || '' };")
sub1("var ans = M.writing ? ([1, 2].filter(function (n) { return String(res.texts[n] || '').trim(); }).length ? 'Text abgegeben' : 'kein Text geschrieben')",
     "var ans = M.writing ? (String(res.texts[1] || '').trim() ? 'Text abgegeben' : 'kein Text geschrieben')")

# Text-Export
block("      [1, 2].forEach(function (n) {\n        var tk = T.schreiben.tasks[n - 1]", "    return lines.join('\\n');", """      var tx1 = res.texts[1] || '';
      if (tx1.trim()) lines.push('', '— E-Mail · ' + wordCount(tx1) + ' Wörter —', tx1.trim());
      else lines.push('', '(kein Text)');
    }
""")

# Ergebnisansicht Schreiben
block("      var any = false;\n      T.schreiben.tasks.forEach(", "      h += '<p class=\"note\">Schriftlicher Ausdruck wird", """      var tk = T.schreiben.task, tx = res.texts[1] || '', wc = wordCount(tx);
      h += '<div class="wtask"><h3>E-Mail beantworten<small>' + (tx.trim() ? wc + ' Wörter' : 'nicht bearbeitet') + '</small></h3>';
      if (tx.trim()) h += '<pre>' + esc(tx) + '</pre>';
      if (tk.model && tk.model.text) {
        var mps = tk.model.text.split('\\n\\n'), mk = tk.model.marks || [];
        h += '<details><summary>Musterlösung' + (tk.model.label ? ' · ' + esc(tk.model.label) : '') + '</summary><div class="mdl pp">' +
          mps.map(function (p, i) {
            return '<p' + (mk[i] ? '' : ' class="nolp"') + '>' + (mk[i] ? '<span class="lp" title="Leitpunkt ' + esc(mk[i]) + '">' + esc(mk[i]) + '</span>' : '') + esc(p).replace(/\\n/g, '<br>') + '</p>';
          }).join('') + '</div>' +
          '<p class="note" style="margin:8px 0 0">Die Zahlen am Rand zeigen, welcher Leitpunkt in dem Absatz beantwortet wird. · 왼쪽 숫자는 그 문단이 답하는 Leitpunkt 번호입니다.</p>' +
          (tk.model.notes ? '<div class="mnotes">' + esc(tk.model.notes) + '</div>' : '') + '</details>';
      }
      h += '</div>';
""")
sub1("(pg.muster ? '<a class=\"btn sm\" href=\"' + pdf + '#page=' + pg.muster + '\" target=\"_blank\" rel=\"noopener\">Musterlösungen (PDF S. ' + pg.muster + '–' + (pg.muster + 1) + ')</a>' : '')",
     "(pg.muster ? '<a class=\"btn sm\" href=\"' + pdf + '#page=' + pg.muster + '\" target=\"_blank\" rel=\"noopener\">Musterlösung (PDF S. ' + pg.muster + ')</a>' : '')")

# ------------------------------------------------------------------ Startseite: Fakten und Hinweise
repline("var facts = R.mod === 'lesen'", "var facts = R.mod === 'lesen' ? ['90 Minuten', 'Lesen 1–3 · Sprachbausteine 1–2', '40 Aufgaben'] : R.mod === 'hoeren' ? ['ca. ' + MOD.hoeren.minutes + ' Minuten', '3 Teile', '20 Aufgaben', 'Teil 1 einmal · Teil 2 und 3 zweimal', 'Kopfhörer empfohlen'] : ['30 Minuten', 'E-Mail mit vier Leitpunkten', 'Wörterzähler'];")
repline("['Die drei Hörtexte werden automatisch nacheinander abgespielt.",
        "['Die drei Hörtexte werden automatisch nacheinander abgespielt. Teil 1 hören Sie einmal, Teil 2 und Teil 3 jeweils zweimal (die Wiederholung steht schon in der Aufnahme). Sie können nicht anhalten oder zurückspulen.', '음원 3개가 자동으로 이어서 재생됩니다. Teil 1은 한 번, Teil 2·3은 두 번 들려주며(다시 들려주는 부분도 음원에 들어 있음), 멈추거나 되감을 수 없습니다.'],")
block("        ['Wählen Sie eine der beiden Aufgaben: A (Bitte um Informationen)", "      ]\n    }[R.mod];", """        ['Sie antworten auf eine E-Mail. Behandeln Sie alle vier Leitpunkte und wählen Sie Betreff, Anrede, Einleitung, Schluss und Grußformel passend zur Situation (Freund/in: du · Firma, Schule, Hausverwaltung: Sie).', '이메일에 답하는 글을 씁니다. 네 가지 Leitpunkte에 모두 답하고, 제목·인사·첫 문장·끝인사를 받는 사람에 맞게 정하세요(du 또는 Sie).'],
        ['Schreiben Sie Ihren Text in das Textfeld. Die Wörter werden automatisch gezählt (nur zur Orientierung). Es gibt keine Rechtschreibkorrektur.', '입력란에 글을 쓰면 단어 수가 자동으로 계산됩니다(참고용). 맞춤법 자동 교정은 없습니다.'],
        ['Umlaute und ß können Sie mit den Sonderzeichen-Tasten einfügen.', 'ä, ö, ü, ß는 특수문자 버튼으로 넣을 수 있습니다.'],
        ['Bewertet wird nur der Text im Textfeld. Nach Ablauf der Zeit wird das Modul automatisch abgegeben.', '입력란의 글만 평가 대상이며, 시간이 끝나면 자동으로 제출됩니다.']
""")

# ------------------------------------------------------------------ Tutorial
repline("['#abar', 'Hier sehen Sie, welcher Hörtext gerade läuft.",
        "['#abar', 'Hier sehen Sie, welcher Hörtext gerade läuft. Die Hörtexte starten automatisch; die Wiederholung (Teil 2 und 3) steht schon in der Aufnahme. Sie können nicht anhalten oder zurückspulen.', '지금 재생 중인 음원이 표시됩니다. 음원은 자동으로 시작되고, Teil 2·3은 다시 들려주는 부분도 음원에 들어 있습니다. 멈추거나 되감을 수 없습니다.'],")
repline("['#tabs', 'Hier wechseln Sie zwischen Aufgabe A und Aufgabe B.", "['#tabs', 'Hier sehen Sie den Teil und die Zahl Ihrer Wörter.', '지금 Teil과 단어 수가 표시됩니다.'],")
repline("['.pane.l', 'Hier steht die Aufgabe mit der Anzeige und den vier Leitpunkten.", "['.pane.l', 'Hier stehen die E-Mail, auf die Sie antworten, und die vier Leitpunkte.', '여기에 답할 이메일과 네 가지 Leitpunkte가 있습니다.'],")
repline("['#wc', 'Die Wörter werden automatisch gezählt. Schreiben Sie mindestens 150 Wörter.'", "['#wc', 'Die Wörter werden automatisch gezählt. Das ist nur eine Orientierung; die Aufgabe nennt keine Mindestzahl.', '단어 수가 자동으로 계산됩니다. 참고용이며 과제에 단어 수 기준은 없습니다.'],")

left = [m.group(0) for m in re.finditer(r".{30}\bB2\b.{30}", re.sub(r"[A-Za-z0-9+/=]{60,}", "", out))]
if left:
    print("Hinweis: »B2« kommt noch vor:", *left, sep="\n  ")
open(os.path.join(HERE, "template.html"), "w", encoding="utf-8").write(out)
print("template.html geschrieben:", len(out.encode("utf-8")) // 1024, "KB")
