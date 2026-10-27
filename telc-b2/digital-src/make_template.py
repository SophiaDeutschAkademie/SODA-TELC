#!/usr/bin/env python3
"""telc-B2-Vorlage aus der B1-Vorlage ableiten: python3 make_template.py -> digital.src.html"""
import re, sys

src = open("/home/claude/work/b2/b1.template.html", encoding="utf-8").read()
out = src


def sub1(old, new, text=None, count=1):
    global out
    assert old in out, "nicht gefunden: " + old[:80]
    assert out.count(old) == count, f"{out.count(old)}x statt {count}x: {old[:80]}"
    out = out.replace(old, new)


def block(start, end, new):
    """alles von start (einschliesslich) bis end (ausschliesslich) ersetzen"""
    global out
    i = out.index(start)
    j = out.index(end, i)
    out = out[:i] + new + out[j:]


# ---------------------------------------------------------------- head / theme
sub1("<title>Goethe B1 digital — Sophia Deutsch Akademie</title>", "<title>telc Deutsch B2 digital — Sophia Deutsch Akademie</title>")
sub1("--acc:#1d6a56;--acc-2:#165443;--acc-w:#e3f0eb;--acc-line:#93c4b2;", "--acc:#1f5a9e;--acc-2:#17457a;--acc-w:#e6eef8;--acc-line:#9db9dc;")
sub1(".opt:hover{background:#f3f7f5;border-color:var(--line)}", ".opt:hover{background:#f1f5fa;border-color:var(--line)}")
sub1(".cell:hover{background:#eef3f1}", ".cell:hover{background:#eef2f8}")
sub1(".d-speech .bub{position:relative;display:inline-block;background:#e3efe9;border:1.5px solid #2b5f4d;",
     ".d-speech .bub{position:relative;display:inline-block;background:#e6eef8;border:1.5px solid #2b4f7d;")
sub1(".d-speech .bub::after{content:\"\";position:absolute;left:22px;bottom:-8px;width:13px;height:13px;background:#e3efe9;border-right:1.5px solid #2b5f4d;border-bottom:1.5px solid #2b5f4d;",
     ".d-speech .bub::after{content:\"\";position:absolute;left:22px;bottom:-8px;width:13px;height:13px;background:#e6eef8;border-right:1.5px solid #2b4f7d;border-bottom:1.5px solid #2b4f7d;")

# ---------------------------------------------------------------- extra CSS
EXTRA_CSS = r"""
/* ---------- telc: Texte, Luecken, Hilfslisten ---------- */
.txs .tn{display:flex;align-items:center;gap:10px;font-size:1.05em;margin:0 0 6px}
.txs .tn b{display:inline-flex;width:28px;height:28px;border-radius:4px;background:var(--ink);color:#fff;align-items:center;justify-content:center;font-size:.9em}
.txs .tb{padding:0 0 18px;margin:0 0 18px;border-bottom:1px solid var(--line-2)}
.txs .tb:last-child{border-bottom:0;margin-bottom:0}
.txs p,.doc p{margin:0 0 .75em}
.art .iq{font-weight:700;color:var(--ink-2)}
.rh{font-size:.8em;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin:0 0 8px}
.hlist{list-style:none;padding:0;margin:0 0 18px;border:1px solid var(--line);border-radius:6px;background:#f8f9fb}
.hlist li{display:grid;grid-template-columns:26px minmax(0,1fr);gap:8px;padding:7px 12px;border-bottom:1px solid var(--line-2);line-height:1.4}
.hlist li:last-child{border-bottom:0}
.hlist li b{color:var(--ink-2)}
.hlist li.used{color:#8a929d}
.hlist li.used span{text-decoration:line-through;text-decoration-color:#b4bbc4}
.gapx{display:inline-flex;align-items:baseline;gap:6px;min-width:84px;margin:0 2px;padding:0 6px;border-bottom:2px solid var(--ink-2);background:#f1f4f9;border-radius:3px 3px 0 0;cursor:pointer;font-weight:700;line-height:1.45;vertical-align:baseline}
.gapx b{font-size:.74em;color:var(--muted)}
.gapx i{font-style:normal;color:var(--ink)}
.gapx.filled{background:var(--acc-w);border-bottom-color:var(--acc)}
.gapx.filled b{color:var(--acc-2)}
.gapx:hover{background:#e3eaf4}
.wbox{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:2px 14px;border:1px solid var(--line);border-radius:6px;background:#f8f9fb;padding:10px 14px;margin:0 0 18px;font-size:.92em}
.wbox span{display:flex;gap:8px;padding:3px 0;letter-spacing:.03em}
.wbox span b{color:var(--ink-2);min-width:14px}
.wbox span.used{color:#8a929d;text-decoration:line-through;text-decoration-color:#b4bbc4}
.opts.row.w .opt{min-width:132px}
.ads.one{grid-template-columns:minmax(0,560px);margin:4px 0 16px}
.task .ctxl{font-weight:700}
.task ol,.task ul.pts{margin:.2em 0 .9em;padding-left:1.25em}
.task .chl p{margin:0 0 .25em}
.wc.low b{color:var(--warn)}
@media (max-width:560px){.wbox{grid-template-columns:repeat(2,minmax(0,1fr))}}
"""
sub1("/* ---------- footer ---------- */", EXTRA_CSS + "\n/* ---------- footer ---------- */")

# ---------------------------------------------------------------- JS: header / constants
sub1("var PREFIX = 'sodaGZB1.v1.';", "var PREFIX = 'sodaTelcB2.v1.';")
block("  var MOD = {", "  var FS = [16, 18, 20.5];", """  var MOD = {
    lesen: { name: 'Lesen', full: 'Leseverstehen und Sprachbausteine', minutes: 90, ko: '읽기·어휘문법' },
    hoeren: { name: 'Hören', full: 'Hörverstehen', minutes: 20, ko: '듣기' },
    schreiben: { name: 'Schreiben', full: 'Schriftlicher Ausdruck', minutes: 30, ko: '쓰기' }
  };
  var WORDS_MIN = 150;
""")
sub1("document.title = 'Modelltest ' + T.roman + ' · ' + MOD[R.mod].name + ' — Goethe B1 digital';",
     "document.title = 'Modelltest ' + T.roman + ' · ' + MOD[R.mod].name + ' — telc B2 digital';")

# ---------------------------------------------------------------- item + text renderers
block("  /* ---------- item renderers ---------- */", "  /* ---------- Anzeigen (Lesen Teil 3): Layouts ---------- */", r"""  /* ---------- item renderers ---------- */
  function optRow(no, val, label, letter, checked, dis) {
    return '<label class="opt' + (checked ? ' on' : '') + (dis ? ' dis' : '') + '"><input type="radio" name="a' + esc(no) + '" value="' + esc(val) + '"' +
      (checked ? ' checked' : '') + (dis ? ' disabled' : ' data-no="' + esc(no) + '"') + '><span class="rb"></span>' +
      (letter ? '<span class="lt">' + esc(letter) + '</span>' : '') + '<span>' + esc(label) + '</span></label>';
  }
  function qWrap(no, inner) {
    return '<div class="q" id="q-' + esc(no) + '"><div class="qn">' + esc(no) + '</div><div class="qb">' + inner + '</div></div>';
  }
  function rfItem(it) {
    return qWrap(it.no, '<p class="qt">' + esc(it.text) + '</p><div class="opts row" role="radiogroup" aria-label="Aufgabe ' + esc(it.no) + '">' +
      optRow(it.no, 'R', 'Richtig', '', false, false) + optRow(it.no, 'F', 'Falsch', '', false, false) + '</div>');
  }
  function abcItem(it) {
    var h = '<p class="qt">' + esc(it.stem) + '</p><div class="opts" role="radiogroup" aria-label="Aufgabe ' + esc(it.no) + '">';
    ['a', 'b', 'c'].forEach(function (k) { h += optRow(it.no, k, it.options[k], k, false, false); });
    return qWrap(it.no, h + '</div>');
  }
  function sb1Item(it) {
    var h = '<p class="qt"><b>Lücke ' + esc(it.no) + '</b></p><div class="opts row w" role="radiogroup" aria-label="Lücke ' + esc(it.no) + '">';
    ['a', 'b', 'c'].forEach(function (k) { h += optRow(it.no, k, it.options[k], k, false, false); });
    return qWrap(it.no, h + '</div>');
  }
  function selItem(it, label, keys, fmtOpt) {
    var h = '<p class="qt">' + it.prompt + '</p><div class="selw"><label for="s-' + esc(it.no) + '">' + esc(label) + '</label>' +
      '<select id="s-' + esc(it.no) + '" data-no="' + esc(it.no) + '"><option value="">–</option>';
    keys.forEach(function (k) { h += '<option value="' + k + '">' + esc(fmtOpt ? fmtOpt(k) : k) + '</option>'; });
    return qWrap(it.no, h + '</select></div>');
  }
  var L12 = 'abcdefghijkl'.split(''), L15 = 'abcdefghijklmno'.split(''), L10 = 'abcdefghij'.split('');
  function para(arr) { return (arr || []).map(function (p) { return '<p>' + esc(p) + '</p>'; }).join(''); }
  function clip(s, n) { s = String(s || ''); return s.length > n ? s.slice(0, n).replace(/\s+\S*$/, '') + ' …' : s; }

  /* ---------- text renderers ---------- */
  function textsHTML(t1) {
    return '<div class="txs">' + t1.texts.map(function (x) {
      return '<div class="tb" id="tx-' + esc(x.no) + '"><h3 class="tn"><b>' + esc(x.no) + '</b></h3>' + para(x.paragraphs) + '</div>';
    }).join('') + '</div>';
  }
  function hlistHTML(t1) {
    return '<ol class="hlist" id="hlist">' + t1.headlines.map(function (h) {
      return '<li data-k="' + esc(h.letter) + '"><b>' + esc(h.letter) + '</b><span>' + esc(h.text) + '</span></li>';
    }).join('') + '</ol>';
  }
  function articleHTML(t) {
    var body = (t.paragraphs || []).map(function (p) {
      if (typeof p === 'string') return '<p>' + esc(p) + '</p>';
      return '<p' + (p.q ? ' class="iq"' : '') + '>' + esc(p.text) + '</p>';
    }).join('');
    return '<article class="card art"><h3>' + esc(t.title) + '</h3>' + (t.lead ? '<p class="lead">' + esc(t.lead) + '</p>' : '') + body +
      (t.source ? '<p class="src">' + esc(t.source) + '</p>' : '') + '</article>';
  }
  function gapParas(arr) {
    return (arr || []).map(function (p) {
      return '<p>' + esc(p).replace(/\{\{(\d+)\}\}/g, function (m, n) {
        return '<span class="gapx" id="g-' + n + '" data-gap="' + n + '" role="button" tabindex="0" title="Lücke ' + n + '"><b>' + n + '</b><i></i></span>';
      }) + '</p>';
    }).join('');
  }
  function wboxHTML(words) {
    return '<div class="wbox" id="wbox">' + L15.map(function (k) { return '<span data-k="' + k + '"><b>' + k + '</b>' + esc(words[k]) + '</span>'; }).join('') + '</div>';
  }

""")

# ---------------------------------------------------------------- remove comments/doc renderers, new module models
block("  function commentsHTML(t) {", "  /* ---------- module models ---------- */", "")
block("  /* ---------- module models ---------- */", "  var M = R.mod === 'lesen'", r"""  /* ---------- module models ---------- */
  function buildLesen() {
    var L = T.lesen, pages = [], items = [];
    function reg(list, type, teil, page, w) {
      list.forEach(function (it) { items.push({ no: it.no, type: type, answer: it.answer, teil: teil, page: page, w: w, src: it }); });
    }
    // Teil 1
    L.t1.items.forEach(function (it, i) {
      var tx = L.t1.texts[i];
      it.prompt = '<b>Text ' + esc(it.no) + '</b>';
      it.text = 'Text ' + it.no + ': ' + clip(tx ? tx.paragraphs[0] : '', 56);
    });
    pages.push({ key: 'L1', teil: 1, title: 'Lesen Teil 1', inst: [L.t1.instruction], leftTitle: 'Texte 1–5', rightTitle: 'Aufgaben 1–5', left: textsHTML(L.t1),
      right: '<p class="rh">Überschriften a–j</p>' + hlistHTML(L.t1) + L.t1.items.map(function (it) { return selItem(it, 'Überschrift:', L10); }).join('') });
    reg(L.t1.items, 'sel1', 1, 0, 5);
    // Teil 2
    pages.push({ key: 'L2', teil: 2, title: 'Lesen Teil 2', inst: [L.t2.instruction], leftTitle: L.t2.kind === 'interview' ? 'Interview' : 'Artikel', rightTitle: 'Aufgaben 6–10',
      left: articleHTML(L.t2), right: '<p class="inst">' + esc(L.t2.taskInstruction) + '</p>' + L.t2.items.map(abcItem).join('') });
    reg(L.t2.items, 'abc', 2, 1, 5);
    // Teil 3
    L.t3.items.forEach(function (it) { it.prompt = esc(it.text); });
    pages.push({ key: 'L3', teil: 3, title: 'Lesen Teil 3', inst: [L.t3.instruction], leftTitle: 'Info-Texte a–l', rightTitle: 'Situationen 11–20',
      left: adsHTML(L.t3.infos), right: L.t3.items.map(function (it) { return selItem(it, 'Info-Text:', L12.concat(['x'])); }).join('') });
    reg(L.t3.items, 'sel3', 3, 2, 2.5);
    // Sprachbausteine 1
    pages.push({ key: 'S1', teil: 4, title: 'Sprachbausteine Teil 1', inst: [L.sb1.instruction], leftTitle: 'Text', rightTitle: 'Lücken 21–30',
      left: '<article class="card doc">' + gapParas(L.sb1.paragraphs) + '</article>', right: L.sb1.items.map(sb1Item).join('') });
    reg(L.sb1.items, 'sb1', 4, 3, 1.5);
    // Sprachbausteine 2
    L.sb2.items.forEach(function (it) { it.prompt = '<b>Lücke ' + esc(it.no) + '</b>'; });
    pages.push({ key: 'S2', teil: 5, title: 'Sprachbausteine Teil 2', inst: [L.sb2.instruction], leftTitle: 'Text', rightTitle: 'Lücken 31–40',
      left: '<article class="card doc"><h3 class="h1t">' + esc(L.sb2.title) + '</h3>' + gapParas(L.sb2.paragraphs) + '</article>',
      right: '<p class="rh">Wörter a–o</p>' + wboxHTML(L.sb2.words) + L.sb2.items.map(function (it) { return selItem(it, 'Wort:', L15, function (k) { return k + ' – ' + L.sb2.words[k]; }); }).join('') });
    reg(L.sb2.items, 'sb2', 5, 4, 1.5);
    return { pages: pages, items: items, teile: [1, 2, 3, 4, 5], two: true, max: 105,
      labels: { 1: 'Lesen 1', 2: 'Lesen 2', 3: 'Lesen 3', 4: 'Sprachbausteine 1', 5: 'Sprachbausteine 2' } };
  }

  function buildHoeren() {
    var H = T.hoeren, pages = [], items = [];
    [['t1', 5], ['t2', 2.5], ['t3', 5]].forEach(function (d, i) {
      var t = H[d[0]], n = t.items;
      pages.push({ key: 'H' + (i + 1), teil: i + 1, title: 'Hören Teil ' + (i + 1), inst: [t.instruction, t.readNote], rightTitle: 'Aufgaben ' + n[0].no + '–' + n[n.length - 1].no,
        right: n.map(rfItem).join('') });
      n.forEach(function (it) { items.push({ no: it.no, type: 'rf', answer: it.answer, teil: i + 1, page: i, w: d[1], src: it }); });
    });
    return { pages: pages, items: items, teile: [1, 2, 3], two: false, max: 75, labels: { 1: 'Teil 1', 2: 'Teil 2', 3: 'Teil 3' } };
  }

  function taskHTML(tk) {
    var ad = tk.ad || {};
    var h = '<div class="task"><p class="ctxl">' + esc(tk.lead) + '</p><div class="ads one"><div class="ad d-' + (AD[ad.design] ? ad.design : 'inst') + '">' +
      AD[AD[ad.design] ? ad.design : 'inst'](ad, ad.deco || {}) + '</div></div>';
    h += (tk.situation || []).map(function (s) { return '<p>' + esc(s) + '</p>'; }).join('');
    h += '<div class="chl">' + (tk.choice || []).map(function (s) { return '<p>' + esc(s) + '</p>'; }).join('') + '</div>';
    h += '<ul class="pts">' + (tk.points || []).map(function (p) { return '<li>' + esc(p) + '</li>'; }).join('') + '</ul>';
    return h + '<p>' + esc(tk.closing) + '</p></div>';
  }
  function buildSchreiben() {
    var pages = T.schreiben.tasks.map(function (tk, i) {
      return { key: 'S' + tk.letter, teil: i + 1, title: 'Schreiben Aufgabe ' + tk.letter, leftTitle: 'Aufgabe ' + tk.letter + ' · ' + tk.kind,
        left: (i === 0 ? '<p class="inst">' + esc(T.schreiben.intro) + '</p>' : '') + taskHTML(tk), task: tk };
    });
    return { pages: pages, items: [], teile: [1, 2], two: true, writing: true, labels: { 1: 'Aufgabe A', 2: 'Aufgabe B' } };
  }

""")

# ---------------------------------------------------------------- state
sub1("answers: {}, marks: {}, texts: { 1: '', 2: '', 3: '' },", "answers: {}, marks: {}, texts: { 1: '', 2: '' },")

# ---------------------------------------------------------------- top bar
sub1("""'<div class="id"><b><span class="gz">Goethe-Zertifikat </span>B1 · ' + MOD[R.mod].name + '</b><span>Modelltest '""",
     """'<div class="id"><b><span class="gz">telc Deutsch </span>B2 · ' + MOD[R.mod].name + '</b><span>Modelltest '""")

# ---------------------------------------------------------------- start page
block("    var facts = R.mod === 'lesen'", "    var resumeOK = saved", r"""    var facts = R.mod === 'lesen' ? ['90 Minuten', 'Lesen 1–3 · Sprachbausteine 1–2', '40 Aufgaben'] : R.mod === 'hoeren' ? ['ca. 20 Minuten', '3 Teile', '20 Aufgaben', 'jeder Text nur einmal', 'Kopfhörer empfohlen'] : ['30 Minuten', 'Aufgabe A oder B', 'mindestens 150 Wörter'];
    var rules = {
      lesen: [
        ['Dieses Modul enthält Leseverstehen (Teil 1–3) und Sprachbausteine (Teil 1–2). Alle fünf Teile haben zusammen 90 Minuten Zeit. Die Reihenfolge der Teile können Sie selbst wählen.', '읽기(Teil 1–3)와 어휘·문법(Sprachbausteine 1–2)을 합쳐 90분입니다. Teil 순서는 자유롭게 정할 수 있습니다.'],
        ['Links sehen Sie den Text, rechts die Aufgaben. Wählen Sie die richtige Lösung aus.', '왼쪽은 지문, 오른쪽은 문항입니다. 정답을 고르세요.'],
        ['In den Sprachbausteinen erscheint Ihre Antwort direkt in der Lücke des Textes. Mit einem Klick auf die Lücke springen Sie zur Aufgabe.', '어휘·문법에서는 고른 답이 지문의 빈칸에 바로 들어갑니다. 빈칸을 누르면 해당 문항으로 이동합니다.'],
        ['Mit „Markieren“ können Sie Textstellen farbig hervorheben.', '‘Markieren’을 켜고 드래그하면 지문에 형광펜을 칠할 수 있습니다.'],
        ['Sie können Ihre Antworten bis zum Ende der Prüfungszeit ändern. Danach wird das Modul automatisch abgegeben.', '시간이 끝날 때까지 답을 고칠 수 있고, 시간이 끝나면 자동으로 제출됩니다.']
      ],
      hoeren: [
        ['Die drei Hörtexte werden automatisch nacheinander abgespielt. Jeder Text wird nur einmal gespielt. Sie können ihn nicht anhalten, zurückspulen oder wiederholen.', '음원 3개가 자동으로 이어서 재생되며, 각각 한 번만 들려줍니다. 멈추거나 되감거나 다시 들을 수 없습니다.'],
        ['Der Bildschirm wechselt mit dem Hörtext automatisch zum nächsten Teil. Lesen Sie die Aufgaben schon vor dem Hören. Frühere Teile können Sie wieder öffnen und Antworten ändern.', '음원에 맞춰 화면이 다음 Teil로 넘어갑니다. 듣기 전에 문항을 미리 읽으세요. 지나간 Teil은 다시 열어 답을 고칠 수 있습니다.'],
        ['Entscheiden Sie bei jeder Aussage: richtig (+) oder falsch (–).', '각 문장이 맞으면 Richtig(+), 틀리면 Falsch(–)를 고릅니다.'],
        ['Stellen Sie die Lautstärke vor dem Start ein. Verwenden Sie am besten Kopfhörer.', '시작 전에 음량을 맞추세요. 헤드폰 사용을 권합니다.']
      ],
      schreiben: [
        ['Wählen Sie eine der beiden Aufgaben: A (Bitte um Informationen) oder B (Beschwerde). Sie schreiben eine halbformelle E-Mail mit mindestens 150 Wörtern.', '과제 A(정보 요청) 또는 B(항의) 중 하나를 골라 150단어 이상의 준공식 이메일을 씁니다.'],
        ['Schreiben Sie Ihren Text in das Textfeld. Die Wörter werden automatisch gezählt. Es gibt keine Rechtschreibkorrektur.', '입력란에 글을 쓰면 단어 수가 자동으로 계산됩니다. 맞춤법 자동 교정은 없습니다.'],
        ['Umlaute und ß können Sie mit den Sonderzeichen-Tasten einfügen.', 'ä, ö, ü, ß는 특수문자 버튼으로 넣을 수 있습니다.'],
        ['Bewertet wird nur der Text im Textfeld. Nach Ablauf der Zeit wird das Modul automatisch abgegeben.', '입력란의 글만 평가 대상이며, 시간이 끝나면 자동으로 제출됩니다.']
      ]
    }[R.mod];
""")
sub1("'<h1>Goethe-Zertifikat B1 · ' + info.name + '</h1>' +", "'<h1>telc Deutsch B2 · ' + info.full + '</h1>' +")
sub1("so wie am Computer im Prüfungszentrum.</p>'", "wie am Computer im Prüfungszentrum.</p>'")

# ---------------------------------------------------------------- exam shell
sub1("ctx: H.t2.context, ", "", count=0) if False else None

# tabs
sub1("""      if (M.writing) {
        var wc = wordCount(S.texts[teil]);
        label = 'Aufgabe ' + teil;
        pr = wc + ' Wörter';
        done = wc >= (T.schreiben.tasks[teil - 1].words || 40);
      } else {
        var its = M.items.filter(function (it) { return it.teil === teil; });
        var ans = its.filter(function (it) { return S.answers[it.no] != null; }).length;
        label = 'Teil ' + teil; pr = ans + '/' + its.length; done = ans === its.length;
      }""", """      if (M.writing) {
        var wc = wordCount(S.texts[teil]);
        label = M.labels[teil];
        pr = wc + ' Wörter';
        done = wc >= WORDS_MIN;
      } else {
        var its = M.items.filter(function (it) { return it.teil === teil; });
        var ans = its.filter(function (it) { return S.answers[it.no] != null; }).length;
        label = M.labels[teil]; pr = ans + '/' + its.length; done = ans === its.length;
      }""")

# writing pane word line
sub1("""'<div class="wc" id="wc"><span>circa ' + esc(p.task.words) + ' Wörter</span><span>Wörter: <b id="wcn">0</b></span></div></div></section>';""",
     """'<div class="wc" id="wc"><span>mindestens ' + WORDS_MIN + ' Wörter</span><span>Wörter: <b id="wcn">0</b></span></div></div></section>';""")
sub1("function updateWC() { var ed = $('#ed'); if (ed) $('#wcn').textContent = wordCount(ed.value); }",
     "function updateWC() { var ed = $('#ed'); if (ed) { var n = wordCount(ed.value); $('#wcn').textContent = n; $('#wc').classList.toggle('low', n > 0 && n < WORDS_MIN); } }")
sub1("['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü', '„', '“'].map", "['ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü'].map")

# page render: sync gaps etc.
sub1("""    renderTabs(); renderChips(); renderNav();
    if (R.mod === 'hoeren') renderAudioBar();
  }""", """    syncRefs();
    renderTabs(); renderChips(); renderNav();
    if (R.mod === 'hoeren') renderAudioBar();
  }

  /* Luecken im Text, benutzte Ueberschriften/Woerter */
  function syncRefs() {
    $$('.gapx').forEach(function (g) {
      var no = g.getAttribute('data-gap'), it = ITEM[no], v = S.answers[no], w = '';
      if (it && v != null) w = it.type === 'sb1' ? (it.src.options[v] || '') : (T.lesen.sb2.words[v] || '');
      $('i', g).textContent = w;
      g.classList.toggle('filled', !!w);
    });
    var used = {};
    Object.keys(S.answers).forEach(function (no) {
      var it = ITEM[no]; if (!it) return;
      if (it.type === 'sel1' || it.type === 'sb2') used[it.type + S.answers[no]] = true;
    });
    $$('#hlist li').forEach(function (li) { li.classList.toggle('used', !!used['sel1' + li.getAttribute('data-k')]); });
    $$('#wbox span').forEach(function (sp) { sp.classList.toggle('used', !!used['sb2' + sp.getAttribute('data-k')]); });
  }""")
sub1("""    markAnswered(no); renderTabs(); renderChips(); saveSoon();
  }""", """    markAnswered(no); syncRefs(); renderTabs(); renderChips(); saveSoon();
  }
  function onGapClick(e) {
    var g = e.target.closest && e.target.closest('.gapx');
    if (!g || markMode) return;
    jumpTo(g.getAttribute('data-gap'));
  }""")
sub1("    main.addEventListener('click', onMarkClick);", "    main.addEventListener('click', onMarkClick);\n    main.addEventListener('click', onGapClick);\n    main.addEventListener('keydown', function (e) { if ((e.key === 'Enter' || e.key === ' ') && e.target.classList && e.target.classList.contains('gapx')) { e.preventDefault(); onGapClick(e); } });")
sub1("if (node.parentNode && node.parentNode.closest && (node.parentNode.closest('mark.hl') || node.parentNode.closest('.inst'))) return;",
     "if (node.parentNode && node.parentNode.closest && (node.parentNode.closest('mark.hl') || node.parentNode.closest('.inst') || node.parentNode.closest('.gapx'))) return;")

# go(): toast text
sub1("toast('Dieser Teil beginnt erst mit dem nächsten Hörtext.')", "toast('Dieser Teil beginnt erst mit dem nächsten Hörtext.')")

# ---------------------------------------------------------------- submit
sub1("if (M.writing) return [1, 2, 3].filter(function (n) { return !String(S.texts[n] || '').trim(); }).length;",
     "if (M.writing) return [1, 2].some(function (n) { return String(S.texts[n] || '').trim(); }) ? 0 : 1;")
block("    if (M.writing) {\n      de = open ?", "    } else {\n      de = open ? 'Sie haben noch '", r"""    if (M.writing) {
      var both = [1, 2].every(function (n) { return String(S.texts[n] || '').trim(); });
      de = open ? 'Sie haben noch keinen Text geschrieben. Möchten Sie das Modul trotzdem abgeben?' : both ? 'Sie haben zu beiden Aufgaben einen Text geschrieben. In der Prüfung wird nur ein Text bewertet. Möchten Sie das Modul jetzt abgeben?' : 'Möchten Sie das Modul jetzt abgeben? Danach können Sie Ihren Text nicht mehr ändern.';
      ko = open ? '아직 아무 글도 쓰지 않았습니다. 그래도 제출할까요?' : both ? '두 과제 모두 글을 썼습니다. 실제 시험에서는 한 과제만 평가됩니다. 지금 제출할까요?' : '지금 제출할까요? 제출하면 더 이상 고칠 수 없습니다.';
""")

# ---------------------------------------------------------------- score / finish
block("  function score() {", "  function finish(byTime) {", r"""  function score() {
    var per = {}, correct = 0, rows = [], pts = 0;
    M.items.forEach(function (it) {
      var g = S.answers[it.no], ok = g != null && g === it.answer;
      if (!per[it.teil]) per[it.teil] = { c: 0, n: 0, p: 0, max: 0 };
      per[it.teil].n++; per[it.teil].max += it.w;
      if (ok) { per[it.teil].c++; per[it.teil].p += it.w; correct++; pts += it.w; }
      rows.push({ no: it.no, teil: it.teil, g: g == null ? null : g, a: it.answer, ok: ok });
    });
    return { correct: correct, total: M.items.length, points: pts, max: M.max, percent: Math.round(pts * 100 / M.max), per: per, rows: rows };
  }

""")
sub1("if (M.writing) res.texts = { 1: S.texts[1] || '', 2: S.texts[2] || '', 3: S.texts[3] || '' };", "if (M.writing) res.texts = { 1: S.texts[1] || '', 2: S.texts[2] || '' };")
sub1("var ans = M.writing ? [1, 2, 3].filter(function (n) { return String(res.texts[n] || '').trim(); }).length + ' von 3 Aufgaben bearbeitet'",
     "var ans = M.writing ? ([1, 2].filter(function (n) { return String(res.texts[n] || '').trim(); }).length ? 'Text abgegeben' : 'kein Text geschrieben')")
sub1("""'<p class="sl" style="margin-top:4px">' + (res.byTime ? '시험 시간이 끝나 자동으로 제출되었습니다.' : '제출이 완료되었습니다.') + ' 결과 화면에서 ' + (M.writing ? '답안을 확인하고 선생님께 보낼 수 있습니다.' : '점수와 정답을 확인하세요.') + '</p>' +""",
     """'<p class="sl" style="margin-top:4px">' + (res.byTime ? '시험 시간이 끝나 자동으로 제출되었습니다.' : '제출이 완료되었습니다.') + ' 결과 화면에서 ' + (M.writing ? '답안을 확인하고 선생님께 보낼 수 있습니다.' : '점수와 정답을 확인하세요.') + '</p>' +""")

# ---------------------------------------------------------------- results
block("  function ansLabel(it, v) {", "  function copyText(txt) {", r"""  function infoName(k) {
    var inf = T.lesen.t3.infos.filter(function (x) { return x.letter === k; })[0];
    return inf ? (inf.header || inf.title || '') : '';
  }
  function ansLabel(it, v) {
    if (v == null) return '—';
    if (it.type === 'rf') return v === 'R' ? 'Richtig (+)' : 'Falsch (–)';
    if (it.type === 'abc' || it.type === 'sb1') return v + ') ' + (it.src.options[v] || '');
    if (it.type === 'sel1') return v + ') ' + ((T.lesen.t1.headlines.filter(function (h) { return h.letter === v; })[0] || {}).text || '');
    if (it.type === 'sb2') return v + ') ' + (T.lesen.sb2.words[v] || '');
    if (it.type === 'sel3') return v === 'x' ? 'x (keine Lösung)' : v + ') ' + infoName(v);
    return v;
  }
  function itemPrompt(it) {
    var s = it.src;
    if (it.type === 'sb1' || it.type === 'sb2') return 'Lücke ' + s.no;
    return s.stem || s.text || '';
  }
  function resultText(res) {
    var lines = ['telc Deutsch B2 · Modelltest ' + T.roman + ' · ' + MOD[R.mod].name + ' (digital)', 'Name: ' + (res.name || '-'), 'Datum: ' + res.finished,
      'Bearbeitungszeit: ' + fmt(res.used) + (res.byTime ? ' (Zeit abgelaufen)' : '')];
    if (res.score) {
      var sc = res.score;
      lines.push('Ergebnis: ' + sc.correct + '/' + sc.total + ' richtig · ' + fp(sc.points) + ' von ' + sc.max + ' Punkten (' + sc.percent + ' %)');
      lines.push('Teile: ' + Object.keys(sc.per).map(function (k) { return M.labels[k] + ' ' + sc.per[k].c + '/' + sc.per[k].n + ' (' + fp(sc.per[k].p) + ' P.)'; }).join(' · '));
      var wrong = sc.rows.filter(function (r) { return !r.ok; });
      if (wrong.length) {
        lines.push('', 'Falsch / offen:');
        wrong.forEach(function (r) { lines.push('  ' + r.no + ': ' + (r.g == null ? 'offen' : r.g) + ' → Lösung ' + r.a); });
      }
    } else {
      [1, 2].forEach(function (n) {
        var tk = T.schreiben.tasks[n - 1], tx = res.texts[n] || '';
        if (!tx.trim()) return;
        lines.push('', '— Aufgabe ' + tk.letter + ' (' + tk.kind + ') · ' + wordCount(tx) + ' Wörter, mindestens ' + WORDS_MIN + ' —', tx.trim());
      });
      if (!res.texts[1].trim() && !res.texts[2].trim()) lines.push('', '(kein Text)');
    }
    return lines.join('\n');
  }
  function fp(n) { return String(Math.round(n * 10) / 10).replace('.', ','); }
""")

block("  function showResult(res) {", "    h += '<div class=\"acts\" style=\"margin-top:22px\"><button class=\"btn pri\" id=\"cp\"", r"""  function showResult(res) {
    stopAll();
    var h = '<div class="page">' + topHTML(false).replace(/<div class="timer"[\s\S]*?<\/div><\/div>/, '') + '<main class="pgm"><section class="sheet" style="max-width:880px">' +
      '<p class="ey">Modelltest ' + esc(T.roman) + ' · Modul ' + MOD[R.mod].name + ' · Ergebnis</p>' +
      '<h1>' + (M.writing ? 'Ihr Text' : 'Ergebnis') + (res.name ? ' · ' + esc(res.name) : '') + '</h1>' +
      '<p class="sl">' + esc(res.finished) + ' · Bearbeitungszeit ' + fmt(res.used) + (res.byTime ? ' · Zeit abgelaufen' : '') + '</p>';
    var pdf = T.pdf, pg = T.pages || {};
    if (res.score) {
      var sc = res.score, ok = sc.percent >= 60;
      h += '<div class="score"><div class="bx"><small>Richtige Antworten</small><b>' + sc.correct + ' / ' + sc.total + '</b></div>' +
        '<div class="bx ' + (ok ? 'ok' : 'no') + '"><small>Punkte (von ' + sc.max + ')</small><b>' + fp(sc.points) + '</b></div>' +
        '<div class="bx ' + (ok ? 'ok' : 'no') + '"><small>Anteil · Richtwert 60 %</small><b>' + sc.percent + ' %</b></div></div>' +
        '<div class="tparts">' + Object.keys(sc.per).map(function (k) { return '<span>' + esc(M.labels[k]) + ' · ' + sc.per[k].c + '/' + sc.per[k].n + ' · ' + fp(sc.per[k].p) + ' / ' + fp(sc.per[k].max) + ' P.</span>'; }).join('') + '</div>' +
        '<p class="note" style="margin:0 0 12px">' + (R.mod === 'lesen' ? 'Leseverstehen 75 Punkte (Teil 1·2 je 5, Teil 3 je 2,5) + Sprachbausteine 30 Punkte (je 1,5) = 105 Punkte.' : 'Hörverstehen 75 Punkte (Teil 1·3 je 5, Teil 2 je 2,5).') +
        ' 실제 telc 시험에서는 필기 전체(225점)의 60 %(135점) 이상이 필요합니다. 60 %는 이 모듈만 볼 때의 참고 기준입니다.</p>';
      h += '<table class="rv"><thead><tr><th>Nr.</th><th>Aufgabe</th><th>Ihre Antwort</th><th>Lösung</th><th></th></tr></thead><tbody>';
      var lastT = 0;
      sc.rows.forEach(function (r) {
        var it = ITEM[r.no]; if (!it) return;
        if (r.teil !== lastT) { h += '<tr class="tp"><td colspan="5">' + esc(M.labels[r.teil]) + '</td></tr>'; lastT = r.teil; }
        h += '<tr class="' + (r.ok ? 'ok' : 'no') + '"><td class="n">' + esc(r.no) + '</td><td class="rvq">' + esc(itemPrompt(it)) + '</td><td class="g">' + esc(ansLabel(it, r.g)) + '</td><td>' + esc(ansLabel(it, r.a)) + '</td><td class="m">' + (r.ok ? '✓' : '✗') + '</td></tr>';
      });
      h += '</tbody></table>';
      h += '<div class="links">' +
        (pg.loesung ? '<a class="btn sm" href="' + pdf + '#page=' + pg.loesung + '" target="_blank" rel="noopener">Lösungsschlüssel (PDF S. ' + pg.loesung + ')</a>' : '') +
        (pg.kommentar ? '<a class="btn sm" href="' + pdf + '#page=' + pg.kommentar + '" target="_blank" rel="noopener">Kommentar für Lehrende (S. ' + pg.kommentar + ')</a>' : '') +
        (R.mod === 'hoeren' && pg.hoertexte ? '<a class="btn sm" href="' + pdf + '#page=' + pg.hoertexte + '" target="_blank" rel="noopener">Hörtexte (S. ' + pg.hoertexte + ')</a>' : '') + '</div>';
    } else {
      var any = false;
      T.schreiben.tasks.forEach(function (tk, i) {
        var tx = res.texts[i + 1] || '', wc = wordCount(tx);
        if (tx.trim()) any = true;
        h += '<div class="wtask"><h3>Aufgabe ' + esc(tk.letter) + ' · ' + esc(tk.kind) + '<small>' + (tx.trim() ? wc + ' Wörter · mindestens ' + WORDS_MIN : 'nicht bearbeitet') + '</small></h3>';
        if (tx.trim()) h += '<pre>' + esc(tx) + '</pre>';
        if (tk.model && tk.model.text) {
          h += '<details><summary>Musterlösung' + (tk.model.label ? ' · ' + esc(tk.model.label) : '') + '</summary><div class="mdl">' + esc(tk.model.text) + '</div></details>';
        }
        h += '</div>';
      });
      void any;
      h += '<p class="note">Schriftlicher Ausdruck wird von Prüfenden bewertet (45 Punkte). Schicken Sie Ihren Text zur Korrektur an Ihre Lehrkraft. · 쓰기는 자동 채점되지 않습니다. 아래 버튼으로 선생님께 답안을 보내 첨삭을 받으세요.</p>';
      h += '<div class="links">' + (pg.muster ? '<a class="btn sm" href="' + pdf + '#page=' + pg.muster + '" target="_blank" rel="noopener">Musterlösungen (PDF S. ' + pg.muster + '–' + (pg.muster + 1) + ')</a>' : '') + '</div>';
    }
""")
sub1("var fname = 'Goethe B1 Modelltest ' + T.roman", "var fname = 'telc B2 Modelltest ' + T.roman")
sub1("var subj = 'Goethe B1 Modelltest ' + T.roman", "var subj = 'telc B2 Modelltest ' + T.roman")
sub1("""'<a class="back" href="index.html#digital">← 디지털 시험 목록</a></section></main></div>';""", """'<a class="back" href="index.html#digital">← 디지털 시험 목록</a></section></main></div>';""")

# overview modal labels
sub1("""if (it.teil !== last) { h += '<span class="tp">Teil ' + it.teil + '</span>'; last = it.teil; }""", """if (it.teil !== last) { h += '<span class="tp">' + esc(M.labels[it.teil]) + '</span>'; last = it.teil; }""")

# ---------------------------------------------------------------- tutorial
block("    if (R.mod === 'lesen') return common.concat([", "  function runTour(done) {", r"""    if (R.mod === 'lesen') return common.concat([
      ['#tabs', 'Hier wechseln Sie zwischen den fünf Teilen: Lesen 1–3 und Sprachbausteine 1–2. Die Zahl zeigt, wie viele Aufgaben Sie im Teil schon gelöst haben.', '다섯 Teil(읽기 1–3, 어휘·문법 1–2) 사이를 이동합니다. 숫자는 그 Teil에서 푼 문항 수입니다.'],
      ['#paneL', 'Links steht der Text. In den Sprachbausteinen erscheint Ihre Antwort direkt in der Lücke.', '왼쪽에는 지문이 있습니다. 어휘·문법에서는 고른 답이 빈칸에 바로 들어갑니다.'],
      ['#paneR', 'Rechts stehen die Aufgaben. Wählen Sie die richtige Lösung aus. Sie können Ihre Antwort jederzeit ändern.', '오른쪽에는 문항이 있습니다. 정답을 고르세요. 답은 언제든 바꿀 수 있습니다.'],
      ['#mk', 'Mit „Markieren“ heben Sie wichtige Textstellen farbig hervor: einschalten, dann Text mit der Maus markieren. Ein Klick auf die Markierung löscht sie wieder.', '‘Markieren’을 켜고 지문을 드래그하면 형광펜이 칠해집니다. 칠한 곳을 누르면 지워집니다.'],
      ['#fz', 'Hier ändern Sie die Schriftgröße.', '글자 크기를 바꿉니다.'],
      ['#ov', 'In der Aufgabenübersicht sehen Sie, welche Aufgaben schon beantwortet (blau) und welche noch offen sind. Mit einem Klick springen Sie direkt zur Aufgabe.', '문항 번호표에서 푼 문항(파랑)과 남은 문항을 확인하고, 번호를 눌러 바로 이동합니다.'],
      ['#nav', 'Mit „Weiter“ und „Zurück“ blättern Sie. Wenn Sie fertig sind, klicken Sie auf „Abgeben“.', '‘Weiter’와 ‘Zurück’으로 넘기고, 다 풀면 ‘Abgeben’을 누릅니다.']
    ]);
    if (R.mod === 'hoeren') return common.concat([
      ['#vol', 'Hier stellen Sie die Lautstärke ein.', '음량을 조절합니다.'],
      ['#abar', 'Hier sehen Sie, welcher Hörtext gerade läuft. Die Hörtexte starten automatisch und werden nur einmal gespielt. Sie können sie nicht anhalten oder wiederholen.', '지금 재생 중인 음원이 표시됩니다. 음원은 자동으로 시작되고 한 번만 재생되며, 멈추거나 다시 들을 수 없습니다.'],
      ['#tabs', 'Mit dem Hörtext wechselt auch der Teil. Spätere Teile sind gesperrt, frühere Teile können Sie wieder öffnen.', '음원에 맞춰 Teil이 바뀝니다. 다음 Teil은 잠겨 있고, 지나간 Teil은 다시 열 수 있습니다.'],
      ['#paneR', 'Lesen Sie die Aussagen und wählen Sie „Richtig“ oder „Falsch“.', '문장을 읽고 ‘Richtig’ 또는 ‘Falsch’를 고르세요.'],
      ['#fz', 'Hier ändern Sie die Schriftgröße.', '글자 크기를 바꿉니다.'],
      ['#ov', 'Die Aufgabenübersicht zeigt, welche Aufgaben noch offen sind.', '문항 번호표에서 남은 문항을 확인합니다.'],
      ['#nav', 'Nach dem letzten Hörtext können Sie Ihre Antworten noch prüfen und dann auf „Abgeben“ klicken.', '마지막 음원이 끝난 뒤 답을 확인하고 ‘Abgeben’을 누릅니다.']
    ]);
    return common.concat([
      ['#tabs', 'Hier wechseln Sie zwischen Aufgabe A und Aufgabe B. Entscheiden Sie sich für eine Aufgabe.', '과제 A와 B 사이를 이동합니다. 하나를 골라 쓰세요.'],
      ['.pane.l', 'Hier steht die Aufgabe mit der Anzeige und den vier Leitpunkten.', '여기에 광고문과 네 가지 안내 항목(Leitpunkte)이 있습니다.'],
      ['#ed', 'Schreiben Sie Ihren Text in dieses Feld.', '이 입력란에 글을 씁니다.'],
      ['#wc', 'Die Wörter werden automatisch gezählt. Schreiben Sie mindestens 150 Wörter.', '단어 수가 자동으로 계산됩니다. 150단어 이상 쓰세요.'],
      ['#sz', 'Mit diesen Tasten fügen Sie ä, ö, ü und ß ein.', '이 버튼으로 ä, ö, ü, ß를 넣습니다.'],
      ['#fz', 'Hier ändern Sie die Schriftgröße.', '글자 크기를 바꿉니다.'],
      ['#nav', 'Wenn Sie fertig sind, klicken Sie auf „Abgeben“.', '다 쓰면 ‘Abgeben’을 누릅니다.']
    ]);
  }
""")

open("/home/claude/work/b2/digital.src.html", "w", encoding="utf-8").write(out)
print("geschrieben:", len(out) // 1024, "KB")
