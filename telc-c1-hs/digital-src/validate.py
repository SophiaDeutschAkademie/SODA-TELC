#!/usr/bin/env python3
"""Pruefung von digital-src/data/mtN.json (telc Deutsch C1 Hochschule).

python3 digital-src/validate.py 1 2 3 4 5     # Nummern
python3 digital-src/validate.py 1 --no-pdf    # ohne PDF-Vergleich

1. Struktur (SCHEMA.md): Anzahl der Aufgaben, Buchstaben, Lueckenmarken {{n}}, Antwortmengen.
2. Loesungsschluessel: liest Seite 20 der PDF (pdftotext -raw) und vergleicht alle 64 Antworten (Lesen 1-46, Hoeren 47-64).
3. Textabdeckung: jede Zeichenkette der JSON-Datei (ohne Leerzeichen und Bindestriche verglichen) muss in den
   Seiten 2-22 der PDF vorkommen (Aufgaben, Loesungen der Notizen 65-74, Musterloesungen, muendliche Aufgaben).
   index und notes werden nicht verglichen (eigene Kurzbezeichnungen fuer index.html).
Exit-Code 1 bei Strukturfehlern oder falschen Antworten. Abweichungen der Textabdeckung werden ausgegeben und
muessen von Hand geprueft werden (Zeilenumbruch-Trennstriche, Spaltenreihenfolge, einzelne Ziffern).
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
errors, warnings = [], []


def err(m):
    errors.append(m)


def warn(m):
    warnings.append(m)


def is_str(x):
    return isinstance(x, str)


def nonempty(t, where):
    if not is_str(t) or not t.strip():
        err(f"{where}: Text fehlt/leer")
        return False
    if t != t.strip() or "  " in t or "\n" in t:
        err(f"{where}: Leerzeichen/Zeilenumbruch fehlerhaft: {t[:50]!r}")
    if re.search(r"[A-Za-zäöüß]-$", t):
        warn(f"{where}: endet auf Trennstrich: {t[-30:]!r}")
    return True


def gaps(paragraphs):
    return [int(x) for p in paragraphs for x in re.findall(r"\{\{(\d+)\}\}", p)]


def check_items(items, nos, answers, where, extra=None):
    got = [str(it.get("no")) for it in items or []]
    if got != [str(n) for n in nos]:
        err(f"{where}: Nummern {got} statt {nos[0]}-{nos[-1]}")
    for it in items or []:
        if it.get("answer") not in answers:
            err(f"{where} {it.get('no')}: Antwort {it.get('answer')!r} nicht in {sorted(answers)}")
        if extra:
            extra(it, f"{where} {it.get('no')}")


def options_abc(it, where, letters):
    o = it.get("options") or {}
    if sorted(o) != list(letters):
        err(f"{where}: Optionen {sorted(o)} statt {list(letters)}")
    for k, v in o.items():
        nonempty(v, f"{where}.{k}")


def check_structure(d, n):
    if d.get("id") != n:
        err(f"id ist {d.get('id')!r}, erwartet {n}")
    if not is_str(d.get("roman")):
        err("roman fehlt")
    L, H, W = d.get("lesen") or {}, d.get("hoeren") or {}, d.get("schreiben") or {}
    # ---- Lesen Teil 1
    t1 = L.get("t1") or {}
    for k in ("instruction", "intro", "title"):
        nonempty(t1.get(k), f"lesen.t1.{k}")
    if gaps(t1.get("paragraphs") or []) != list(range(0, 7)):
        err(f"lesen.t1.paragraphs: Luecken {gaps(t1.get('paragraphs') or [])} statt 0-6")
    for i, p in enumerate(t1.get("paragraphs") or []):
        nonempty(p.replace("{{", "").replace("}}", ""), f"lesen.t1.paragraphs[{i}]")
    if [s.get("letter") for s in t1.get("sentences") or []] != list("abcdefgh"):
        err("lesen.t1.sentences: Buchstaben a-h erwartet")
    for s in t1.get("sentences") or []:
        nonempty(s.get("text"), f"lesen.t1.sentences {s.get('letter')}")
    if (t1.get("example") or {}).get("letter") != "z":
        err("lesen.t1.example: Buchstabe z erwartet")
    nonempty((t1.get("example") or {}).get("text"), "lesen.t1.example.text")
    check_items(t1.get("items"), range(1, 7), set("abcdefgh"), "lesen.t1")
    a1 = [it.get("answer") for it in t1.get("items") or []]
    if len(set(a1)) != len(a1):
        err(f"lesen.t1: Satz mehrfach verwendet {a1}")
    # ---- Lesen Teil 2
    t2 = L.get("t2") or {}
    nonempty(t2.get("instruction"), "lesen.t2.instruction")
    nonempty(t2.get("title"), "lesen.t2.title")
    if [s.get("letter") for s in t2.get("sections") or []] != list("abcde"):
        err("lesen.t2.sections: Buchstaben a-e erwartet")
    for s in t2.get("sections") or []:
        nonempty(s.get("text"), f"lesen.t2.sections {s.get('letter')}")
    nonempty(t2.get("itemsLead"), "lesen.t2.itemsLead")
    ex = t2.get("example") or {}
    nonempty(ex.get("stem"), "lesen.t2.example.stem")
    if ex.get("answer") not in set("abcde"):
        err("lesen.t2.example.answer")
    check_items(t2.get("items"), range(7, 13), set("abcde"), "lesen.t2",
                lambda it, w: nonempty(it.get("stem"), w + ".stem"))
    # ---- Lesen Teil 3
    t3 = L.get("t3") or {}
    nonempty(t3.get("instruction"), "lesen.t3.instruction")
    nonempty(t3.get("itemsLead"), "lesen.t3.itemsLead")
    if not (isinstance(t3.get("paragraphs"), list) and len(t3["paragraphs"]) >= 5):
        err("lesen.t3.paragraphs: mindestens 5 Absaetze erwartet")
    for i, p in enumerate(t3.get("paragraphs") or []):
        nonempty(p, f"lesen.t3.paragraphs[{i}]")
    check_items(t3.get("items"), range(13, 24), set("rfn"), "lesen.t3", lambda it, w: nonempty(it.get("text"), w + ".text"))
    hd = t3.get("headline") or {}
    if str(hd.get("no")) != "24" or hd.get("answer") not in set("abc"):
        err("lesen.t3.headline: Nr. 24 und Antwort a/b/c erwartet")
    nonempty(hd.get("instruction"), "lesen.t3.headline.instruction")
    options_abc(hd, "lesen.t3.headline", "abc")
    # ---- Sprachbausteine
    sb = L.get("sb") or {}
    nonempty(sb.get("instruction"), "lesen.sb.instruction")
    nonempty(sb.get("title"), "lesen.sb.title")
    if gaps(sb.get("paragraphs") or []) != [0] + list(range(25, 47)):
        err(f"lesen.sb.paragraphs: Luecken {gaps(sb.get('paragraphs') or [])} statt 0, 25-46")
    ex = sb.get("example") or {}
    options_abc(ex, "lesen.sb.example", "abcd")
    if ex.get("answer") not in set("abcd"):
        err("lesen.sb.example.answer")
    check_items(sb.get("items"), range(25, 47), set("abcd"), "lesen.sb", lambda it, w: options_abc(it, w, "abcd"))
    # ---- Hoeren
    h1, h2, h3 = H.get("t1") or {}, H.get("t2") or {}, H.get("t3") or {}
    for k in ("instruction", "readNote", "title"):
        nonempty(h1.get(k), f"hoeren.t1.{k}")
    if [s.get("letter") for s in h1.get("statements") or []] != list("abcdefghij"):
        err("hoeren.t1.statements: Buchstaben a-j erwartet")
    for s in h1.get("statements") or []:
        nonempty(s.get("text"), f"hoeren.t1.statements {s.get('letter')}")
    check_items(h1.get("items"), range(47, 55), set("abcdefghij"), "hoeren.t1", lambda it, w: nonempty(it.get("label"), w + ".label"))
    a47 = [it.get("answer") for it in h1.get("items") or []]
    if len(set(a47)) != len(a47):
        err(f"hoeren.t1: Aussage mehrfach verwendet {a47}")
    for k in ("instruction", "readNote"):
        nonempty(h2.get(k), f"hoeren.t2.{k}")
    check_items(h2.get("items"), range(55, 65), set("abc"), "hoeren.t2",
                lambda it, w: (nonempty(it.get("stem"), w + ".stem"), options_abc(it, w, "abc")))
    for k in ("instruction", "exampleNote", "readNote", "finalNote", "exampleAnswer"):
        nonempty(h3.get(k), f"hoeren.t3.{k}")
    nos = [ln.get("no") for sl in h3.get("slides") or [] for ln in sl.get("lines") or [] if ln.get("no")]
    if nos != ["0"] + [str(i) for i in range(65, 75)]:
        err(f"hoeren.t3.slides: Nummern {nos} statt 0, 65-74")
    for sl in h3.get("slides") or []:
        nonempty(sl.get("title"), "hoeren.t3.slides.title")
        for ln in sl.get("lines") or []:
            nonempty(ln.get("text"), f"hoeren.t3.slides {ln.get('no') or '-'}")
    got = [str(it.get("no")) for it in h3.get("items") or []]
    if got != [str(i) for i in range(65, 75)]:
        err(f"hoeren.t3.items: Nummern {got}")
    for it in h3.get("items") or []:
        nonempty(it.get("solution"), f"hoeren.t3.items {it.get('no')}")
    # ---- Schreiben
    nonempty(W.get("instruction"), "schreiben.instruction")
    if W.get("minWords") != 350 or W.get("minutes") != 70:
        err("schreiben: minWords 350 und minutes 70 erwartet")
    th = W.get("themes") or []
    if [t.get("no") for t in th] != ["1", "2"]:
        err("schreiben.themes: Nummern 1, 2 erwartet")
    for t in th:
        w = f"schreiben.themes {t.get('no')}"
        if not (isinstance(t.get("paragraphs"), list) and t["paragraphs"]):
            err(f"{w}: paragraphs fehlt")
        for i, p in enumerate(t.get("paragraphs") or []):
            nonempty(p, f"{w}[{i}]")
        nonempty(t.get("quoteLead"), f"{w}.quoteLead")
        if len(t.get("quotes") or []) != 2:
            err(f"{w}: zwei Zitate erwartet")
        for i, q in enumerate(t.get("quotes") or []):
            nonempty(q, f"{w}.quotes[{i}]")
        m = t.get("model") or {}
        nonempty(m.get("title"), f"{w}.model.title")
        if not (isinstance(m.get("paragraphs"), list) and len(m["paragraphs"]) >= 3):
            err(f"{w}.model.paragraphs: mindestens 3 Absaetze erwartet")
        for i, p in enumerate(m.get("paragraphs") or []):
            nonempty(p, f"{w}.model.paragraphs[{i}]")
        if not is_str(m.get("hint")):
            err(f"{w}.model.hint fehlt")
    # ---- Muendlich (nur index.html)
    mu = d.get("muendlich") or {}
    if [c.get("who") for c in mu.get("teil1") or []] != ["A", "B", "C"]:
        err("muendlich.teil1: Teilnehmer A, B, C erwartet")
    for c in mu.get("teil1") or []:
        if len(c.get("themes") or []) != 2:
            err(f"muendlich.teil1 {c.get('who')}: zwei Themen erwartet")
    if [q.get("no") for q in mu.get("teil2") or []] != ["1", "2", "3"]:
        err("muendlich.teil2: Zitate 1-3 erwartet")
    # ---- index
    ix = d.get("index") or {}
    nonempty(ix.get("short"), "index.short")
    for part, keys in (("lesen", ("t1", "t2", "t3", "sb")), ("hoeren", ("t1", "t2", "t3")), ("schreiben", ("t1", "t2"))):
        for k in keys:
            nonempty((ix.get(part) or {}).get(k), f"index.{part}.{k}")
    sp = ix.get("sprechen") or {}
    if [c.get("who") for c in sp.get("t1") or []] != ["A", "B", "C"] or any(len(c.get("topics") or []) != 2 for c in sp.get("t1") or []):
        err("index.sprechen.t1: A, B, C mit je zwei Themen erwartet")
    if [q.get("no") for q in sp.get("t2") or []] != ["1", "2", "3"]:
        err("index.sprechen.t2: Zitate 1-3 erwartet")


def pdf_text(path, first, last):
    return subprocess.run(["pdftotext", "-raw", "-f", str(first), "-l", str(last), path, "-"], capture_output=True, text=True, check=True).stdout


def despace(s):
    s = re.sub(r"\{\{(\d+)\}\}", r"\1", s)
    return re.sub(r"[\s\-­]+", "", s)


def check_key(d, pdf):
    """Seite 20: Zeilen '1 e', '15 –' ... fuer 1-64"""
    key = {}
    for ln in pdf_text(pdf, 20, 20).splitlines():
        m = re.fullmatch(r"(\d{1,2}) ([a-jrf]|[–-])", ln.strip())
        if m:
            key[m.group(1)] = m.group(2)
    mine = {}
    L, H = d["lesen"], d["hoeren"]
    for sec in (L["t1"], L["t2"], L["sb"], H["t1"], H["t2"]):
        for it in sec["items"]:
            mine[str(it["no"])] = it["answer"]
    for it in L["t3"]["items"]:
        mine[str(it["no"])] = {"n": "–"}.get(it["answer"], it["answer"])
    mine["24"] = L["t3"]["headline"]["answer"]
    bad = 0
    for no in sorted(mine, key=int):
        k = key.get(no)
        if k is not None and k == "-":
            k = "–"
        if k != mine[no]:
            err(f"Loesungsschluessel S. 20: Nr. {no} PDF {k!r}, JSON {mine[no]!r}")
            bad += 1
    if len(key) != 64:
        warn(f"Loesungsschluessel S. 20: {len(key)} Eintraege gelesen (erwartet 64)")
    return bad


def units(o, path=""):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, list):
        for i, x in enumerate(o):
            yield from units(x, f"{path}[{i}]")
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in ("answer", "no", "letter", "id", "roman", "who", "minWords", "minutes", "bullet", "dash", "index", "notes"):
                continue
            yield from units(v, f"{path}.{k}")


def check_coverage(d, pdf):
    raw = pdf_text(pdf, 2, 22)
    lines = []
    for ln in raw.splitlines():
        t = ln.strip()
        if re.fullmatch(r"\d{1,2}", t) or re.match(r"^(90|40|70|ca\. 16) Minuten", t) or re.fullmatch(r"[A-Za-zÄÖÜäöü]", t) or (t.startswith("Modelltest") and "Lösungsschlüssel" in t):
            continue
        lines.append(ln)
    page = despace("\n".join(lines))
    page_all = despace(raw)   # Luckennummern stehen im Textlayer teils in eigener Zeile (dann nicht als Seitenzahl entfernen)
    miss = []
    for path, u in units(d):
        du = despace(u)
        if du and du not in page and du not in page_all:
            miss.append((path, u[:80]))
    return miss


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    no_pdf = "--no-pdf" in sys.argv
    if not args:
        sys.exit(__doc__)
    for a in args:
        n = int(a)
        errors.clear()
        warnings.clear()
        d = json.load(open(os.path.join(HERE, "data", f"mt{n}.json"), encoding="utf-8"))
        check_structure(d, n)
        msg = ""
        if not no_pdf:
            pdf = os.path.join(REPO, f"telc C1 HS Modelltest {n}.pdf")
            if os.path.exists(pdf):
                check_key(d, pdf)
                miss = check_coverage(d, pdf)
                for p, u in miss:
                    warn(f"Text nicht im PDF gefunden (von Hand pruefen): {p}: {u!r}")
                msg = f" · Schluessel 64 Antworten, {len(miss)} Textabweichungen"
            else:
                warn(f"PDF fehlt: {pdf}")
        for w in warnings:
            print(f"MT{n} WARN {w}")
        for e in errors:
            print(f"MT{n} FEHLER {e}")
        print(f"MT{n} {'OK' if not errors else 'FEHLERHAFT'}{msg}")
        if errors:
            sys.exit(1)


if __name__ == "__main__":
    main()
