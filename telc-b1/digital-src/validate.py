#!/usr/bin/env python3
"""Pruefung von digital-src/data/mtN.json (telc Deutsch B1).

python3 digital-src/validate.py 1 2 3 4      # Nummern oder Dateipfade
python3 digital-src/validate.py 1 --no-pdf   # ohne PDF-Vergleich

1. Struktur (Schema.md): Anzahl der Aufgaben, Buchstaben, Lueckenmarken {{n}}.
2. Loesungsschluessel: liest Seite 19 der PDF und vergleicht jede Antwort.
3. Textabdeckung: vergleicht die Woerter der Seiten 2-14 (PDF) mit den Woertern der JSON-Datei
   in beiden Richtungen und die Musterloesung (Seite 20) in einer Richtung.
   Hat eine PDF keine Textebene (Modelltest 1-4 sind Vektorgrafiken), werden Punkt 2 und 3 uebersprungen;
   dort wurden Loesungsschluessel und Text per Bildvergleich und OCR geprueft (siehe README).
Exit-Code 1 bei Strukturfehlern oder falschen Antworten. Abweichungen der Textabdeckung werden
ausgegeben und muessen von Hand geprueft werden (Zeilenumbruch-Trennstriche, Spaltenreihenfolge).
"""
import collections
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)

errors = []
warnings = []


def err(msg):
    errors.append(msg)


def warn(msg):
    warnings.append(msg)


def is_str(x):
    return isinstance(x, str)


def need(obj, key, typ, where):
    if not isinstance(obj, dict) or key not in obj:
        err(f"{where}: Feld '{key}' fehlt")
        return None
    v = obj[key]
    if typ is not None and not isinstance(v, typ):
        err(f"{where}.{key}: falscher Typ ({type(v).__name__})")
        return None
    return v


def check_items(items, nos, answers, where, extra=None):
    if not isinstance(items, list):
        err(f"{where}: items ist keine Liste")
        return
    got = [str(it.get("no")) for it in items if isinstance(it, dict)]
    if got != [str(n) for n in nos]:
        err(f"{where}: Nummern {got} statt {nos[0]}-{nos[-1]}")
    for it in items:
        if not isinstance(it, dict):
            err(f"{where}: Eintrag kein Objekt")
            continue
        no = it.get("no")
        a = it.get("answer")
        if a not in answers:
            err(f"{where} {no}: Antwort {a!r} nicht in {sorted(answers)}")
        if extra:
            extra(it, f"{where} {no}")


def check_text(t, where, allow_empty=False):
    if not is_str(t) or (not allow_empty and not t.strip()):
        err(f"{where}: Text fehlt/leer")
        return
    if t != t.strip() or "  " in t or "\n" in t:
        err(f"{where}: Leerzeichen/Zeilenumbruch fehlerhaft: {t[:50]!r}")
    if re.search(r"[A-Za-zäöüß]-$", t):
        warn(f"{where}: endet auf Trennstrich: {t[-30:]!r}")


def check_ad(ad, where):
    if not isinstance(ad, dict):
        err(f"{where}: kein Objekt")
        return
    for k in ("header", "tag", "title", "subtitle", "footer"):
        if k in ad and not is_str(ad[k]):
            err(f"{where}.{k}: kein String")
    for k in ("facts", "body"):
        if k in ad and not (isinstance(ad[k], list) and all(is_str(x) for x in ad[k])):
            err(f"{where}.{k}: keine String-Liste")
    for k in ("header", "tag", "title", "subtitle", "footer"):
        if is_str(ad.get(k)) and ad[k]:
            check_text(ad[k], f"{where}.{k}")
    for k in ("facts", "body"):
        for i, s in enumerate(ad.get(k) or []):
            check_text(s, f"{where}.{k}[{i}]")
    if not any(ad.get(k) for k in ("header", "tag", "title", "subtitle", "facts", "body", "footer")):
        err(f"{where}: Anzeige ohne Inhalt")


def gaps(paragraphs):
    return re.findall(r"\{\{(\d+)\}\}", " ".join(paragraphs))


def check_structure(d, n):
    if d.get("id") != n:
        err(f"id ist {d.get('id')!r}, erwartet {n}")
    need(d, "roman", str, "Wurzel")
    L = need(d, "lesen", dict, "lesen") or {}
    # Teil 1
    t1 = need(L, "t1", dict, "lesen.t1") or {}
    need(t1, "instruction", str, "lesen.t1")
    hl = t1.get("headlines") or []
    if [h.get("letter") for h in hl] != list("abcdefghij"):
        err("lesen.t1.headlines: Buchstaben a-j erwartet")
    for h in hl:
        check_text(h.get("text"), f"lesen.t1.headlines {h.get('letter')}")
    tx = t1.get("texts") or []
    if [str(x.get("no")) for x in tx] != ["1", "2", "3", "4", "5"]:
        err("lesen.t1.texts: Nummern 1-5 erwartet")
    for x in tx:
        if not (isinstance(x.get("paragraphs"), list) and x["paragraphs"]):
            err(f"lesen.t1.texts {x.get('no')}: paragraphs fehlt")
        for i, p in enumerate(x.get("paragraphs") or []):
            check_text(p, f"lesen.t1.texts {x.get('no')}[{i}]")
    check_items(t1.get("items"), range(1, 6), set("abcdefghij"), "lesen.t1")
    # Teil 2
    t2 = need(L, "t2", dict, "lesen.t2") or {}
    need(t2, "instruction", str, "lesen.t2")
    if t2.get("kind") not in ("article", "interview"):
        err("lesen.t2.kind: 'article' oder 'interview'")
    check_text(t2.get("title"), "lesen.t2.title")
    if "lead" not in t2 or not is_str(t2["lead"]):
        err("lesen.t2.lead fehlt (auch leer als \"\")")
    if "source" not in t2 or not is_str(t2["source"]):
        err("lesen.t2.source fehlt (auch leer als \"\")")
    need(t2, "taskInstruction", str, "lesen.t2")
    ps = t2.get("paragraphs") or []
    if not ps:
        err("lesen.t2.paragraphs leer")
    for i, p in enumerate(ps):
        if t2.get("kind") == "interview":
            if not (isinstance(p, dict) and is_str(p.get("text"))):
                err(f"lesen.t2.paragraphs[{i}]: bei interview Objekt mit 'text' erwartet")
            else:
                check_text(p["text"], f"lesen.t2.paragraphs[{i}]")
        else:
            check_text(p, f"lesen.t2.paragraphs[{i}]")

    def abc(it, w):
        check_text(it.get("stem"), w + ".stem")
        o = it.get("options")
        if not (isinstance(o, dict) and sorted(o) == ["a", "b", "c"]):
            err(f"{w}: options a/b/c erwartet")
        else:
            for k, v in o.items():
                check_text(v, f"{w}.options.{k}")
    check_items(t2.get("items"), range(6, 11), set("abc"), "lesen.t2", abc)
    # Teil 3
    t3 = need(L, "t3", dict, "lesen.t3") or {}
    need(t3, "instruction", str, "lesen.t3")

    def sit(it, w):
        check_text(it.get("text"), w + ".text")
    check_items(t3.get("items"), range(11, 21), set("abcdefghijklx"), "lesen.t3", sit)
    inf = t3.get("infos") or []
    if [i.get("letter") for i in inf] != list("abcdefghijkl"):
        err("lesen.t3.infos: Buchstaben a-l erwartet")
    for i in inf:
        check_ad(i, f"lesen.t3.infos {i.get('letter')}")
    used = [it.get("answer") for it in (t3.get("items") or []) if it.get("answer") != "x"]
    if len(set(used)) != len(used):
        err("lesen.t3: ein Info-Text wird mehrfach als Loesung verwendet")
    if [it.get("answer") for it in (t3.get("items") or [])].count("x") != 2:
        warn("lesen.t3: nicht genau zwei x-Loesungen (alle fuenf Modelltests haben zwei, pruefen)")
    # Sprachbausteine 1
    s1 = need(L, "sb1", dict, "lesen.sb1") or {}
    need(s1, "instruction", str, "lesen.sb1")
    for i, p in enumerate(s1.get("paragraphs") or []):
        check_text(p.replace("\n", " "), f"lesen.sb1.paragraphs[{i}]")   # Zeilenumbruch nur bei Gruss + Name
    g = gaps(s1.get("paragraphs") or [])
    if g != [str(k) for k in range(21, 31)]:
        err(f"lesen.sb1: Luecken {g} statt 21-30 in Reihenfolge")

    def opt3(it, w):
        o = it.get("options")
        if not (isinstance(o, dict) and sorted(o) == ["a", "b", "c"]):
            err(f"{w}: options a/b/c erwartet")
        else:
            for k, v in o.items():
                check_text(v, f"{w}.options.{k}")
    check_items(s1.get("items"), range(21, 31), set("abc"), "lesen.sb1", opt3)
    # Sprachbausteine 2
    s2 = need(L, "sb2", dict, "lesen.sb2") or {}
    need(s2, "instruction", str, "lesen.sb2")
    if not is_str(s2.get("title")):
        err("lesen.sb2.title fehlt (bei B1 leer, aber vorhanden)")
    for i, p in enumerate(s2.get("paragraphs") or []):
        check_text(p.replace("\n", " "), f"lesen.sb2.paragraphs[{i}]")   # Zeilenumbruch nur bei Gruss + Name
    g = gaps(s2.get("paragraphs") or [])
    if g != [str(k) for k in range(31, 41)]:
        err(f"lesen.sb2: Luecken {g} statt 31-40 in Reihenfolge")
    w = s2.get("words")
    if not (isinstance(w, dict) and sorted(w) == list("abcdefghijklmno")):
        err("lesen.sb2.words: Buchstaben a-o erwartet")
    else:
        for k, v in w.items():
            check_text(v, f"lesen.sb2.words.{k}")
    check_items(s2.get("items"), range(31, 41), set("abcdefghijklmno"), "lesen.sb2")
    ans = [it.get("answer") for it in (s2.get("items") or [])]
    if len(set(ans)) != len(ans):
        err("lesen.sb2: ein Wort wird mehrfach als Loesung verwendet")
    # Hoeren
    H = need(d, "hoeren", dict, "hoeren") or {}
    for key, rng in (("t1", range(41, 46)), ("t2", range(46, 56)), ("t3", range(56, 61))):
        t = need(H, key, dict, f"hoeren.{key}") or {}
        check_text(t.get("instruction"), f"hoeren.{key}.instruction")
        if "readNote" not in t or not is_str(t["readNote"]):
            err(f"hoeren.{key}.readNote fehlt (auch leer als \"\")")
        elif t["readNote"]:
            check_text(t["readNote"], f"hoeren.{key}.readNote")

        def st(it, w):
            check_text(it.get("text"), w + ".text")
        check_items(t.get("items"), rng, {"R", "F"}, f"hoeren.{key}", st)
    # Schreiben
    S = need(d, "schreiben", dict, "schreiben") or {}
    if "intro" not in S or not is_str(S["intro"]):
        err("schreiben.intro fehlt (auch leer als \"\")")
    t = S.get("task")
    if not isinstance(t, dict):
        err("schreiben.task fehlt")
        return
    w = "schreiben.task"
    check_text(t.get("lead"), w + ".lead")
    mail = t.get("mail")
    if not (isinstance(mail, list) and len(mail) >= 3):
        err(f"{w}.mail: Liste mit mindestens 3 Absaetzen erwartet")
    else:
        for i, s_ in enumerate(mail):
            if not is_str(s_) or not s_.strip() or s_ != s_.strip() or "  " in s_:
                err(f"{w}.mail[{i}]: Text fehlerhaft")
    check_text(t.get("instruction"), w + ".instruction")
    pts = t.get("points")
    if not (isinstance(pts, list) and len(pts) == 4):
        err(f"{w}.points: 4 Leitpunkte erwartet")
    else:
        for i, s_ in enumerate(pts):
            check_text(s_, f"{w}.points[{i}]")
    check_text(t.get("closing"), w + ".closing")
    m = t.get("model")
    if not isinstance(m, dict):
        err(f"{w}.model fehlt")
    else:
        check_text(m.get("label"), w + ".model.label")
        mt = m.get("text")
        if not is_str(mt) or not mt.startswith("Betreff:"):
            err(f"{w}.model.text muss mit 'Betreff:' beginnen")
        elif "  " in mt or mt != mt.strip():
            err(f"{w}.model.text: Leerzeichen")
        else:
            ps = mt.split("\n\n")
            mk = m.get("marks")
            if not (isinstance(mk, list) and len(mk) == len(ps)):
                err(f"{w}.model.marks: {len(ps)} Eintraege erwartet")
            else:
                got = [x for x in mk if x]
                if sorted(got) != ["1", "2", "3", "4"]:
                    err(f"{w}.model.marks: Leitpunkte 1-4 je einmal erwartet, gefunden {got}")
            if not is_str(m.get("notes")) or not m["notes"].startswith("Leitpunkte"):
                warn(f"{w}.model.notes fehlen oder beginnen nicht mit 'Leitpunkte'")
    ix = d.get("index")
    if not isinstance(ix, dict):
        err("index fehlt (Themen fuer index.html)")
    else:
        for k in ("short", "sb1", "sb2", "schreiben"):
            check_text(ix.get(k), "index." + k)
        for k in ("t1", "t2", "t3"):
            check_text((ix.get("hoeren") or {}).get(k), "index.hoeren." + k)
        for k in ("t2", "t3"):
            check_text((ix.get("sprechen") or {}).get(k), "index.sprechen." + k)


def walk_strings(o, skip=()):
    if isinstance(o, str):
        yield o
    elif isinstance(o, list):
        for x in o:
            yield from walk_strings(x, skip)
    elif isinstance(o, dict):
        for k, v in o.items():
            if k in skip:
                continue
            yield from walk_strings(v, skip)


def has_text(pdf):
    txt = subprocess.check_output(["pdftotext", "-f", "19", "-l", "19", pdf, "-"]).decode("utf-8")
    return "Lösungsschlüssel" in txt


def parse_key(pdf):
    txt = subprocess.check_output(["pdftotext", "-layout", "-f", "19", "-l", "19", pdf, "-"]).decode("utf-8")
    key = {}
    head = txt.split("Bestehen")[0]
    for m in re.finditer(r"(?<!\d)(\d{1,2})\s+([a-ox+–−-])(?=\s|$)", head, flags=re.M):
        no, a = m.group(1), m.group(2)
        if 1 <= int(no) <= 60:
            key.setdefault(no, a)
    return key


def check_key(d, pdf):
    key = parse_key(pdf)
    miss = [str(i) for i in range(1, 61) if str(i) not in key]
    if miss:
        warn(f"Loesungsschluessel: Nummern nicht gelesen: {miss}")
    sections = [(d["lesen"]["t1"], "lesen.t1"), (d["lesen"]["t2"], "lesen.t2"), (d["lesen"]["t3"], "lesen.t3"),
                (d["lesen"]["sb1"], "lesen.sb1"), (d["lesen"]["sb2"], "lesen.sb2"),
                (d["hoeren"]["t1"], "hoeren.t1"), (d["hoeren"]["t2"], "hoeren.t2"), (d["hoeren"]["t3"], "hoeren.t3")]
    n = 0
    for sec, where in sections:
        for it in sec.get("items", []):
            k = key.get(str(it.get("no")))
            if k is None:
                continue
            a = it.get("answer")
            exp = {"+": "R", "–": "F", "−": "F", "-": "F"}.get(k, k)
            n += 1
            if a != exp:
                err(f"{where} {it.get('no')}: Antwort {a!r}, Loesungsschluessel Seite 19 sagt {k!r}")
    print(f"  Loesungsschluessel: {n} Antworten verglichen")


FURN = re.compile(r"^(\d{1,2}|\d+ Minuten Leseverstehen und Sprachbausteine|ca\. \d+ Minuten Hörverstehen|30 Minuten Schriftlicher Ausdruck|"
                  r"nehetsreveseL|enietsuabhcarpS|nehetsrevröH|kcurdsuA rehciltfirhcS|kcurdsuA rehcildnüM|"
                  r"Leseverstehen Teil \d|Sprachbausteine Teil \d|Hörverstehen Teil \d|Schriftlicher Ausdruck)$")
TOK = re.compile(r"[0-9A-Za-zÄÖÜäöüßéèêàáç€%]+")


def pdf_tokens(pdf, first, last):
    raw = subprocess.check_output(["pdftotext", "-raw", "-f", str(first), "-l", str(last), pdf, "-"]).decode("utf-8")
    raw = raw.replace("⁠", "").replace("­", "")
    lines = []
    for ln in raw.split("\n"):
        s = ln.strip()
        if not s or FURN.match(s):
            continue
        lines.append(s)
    txt = "\n".join(lines)
    txt = re.sub(r"([a-zäöüß])-\n([a-zäöüß])", r"\1\2", txt)
    return collections.Counter(TOK.findall(txt))


def json_tokens(strings):
    txt = "\n".join(strings).replace("{{", " ").replace("}}", " ")
    return collections.Counter(TOK.findall(txt))


def despace(t):
    return re.sub(r"[^0-9a-zäöüßé€%]", "", t.lower())


def pdf_flat(pdf, first, last):
    """Seitentext ohne Leerzeichen/Satzzeichen (die PDF-Textebene klebt Woerter teils zusammen)"""
    raw = subprocess.check_output(["pdftotext", "-raw", "-f", str(first), "-l", str(last), pdf, "-"]).decode("utf-8")
    raw = raw.replace("⁠", "").replace("­", "")
    lines = [ln.strip() for ln in raw.split("\n") if ln.strip() and not FURN.match(ln.strip())]
    txt = "\n".join(lines)
    txt = re.sub(r"([a-zäöüß])-\n([a-zäöüß])", r"\1\2", txt)
    return despace(txt)


def chunks(strings, size=5):
    for s_ in strings:
        w = re.sub(r"\{\{(\d+)\}\}", r"\1", s_).split()
        for k in range(0, len(w), size):
            c = w[k:k + size]
            if len(" ".join(c)) >= 8:
                yield " ".join(c)


def check_coverage(d, pdf):
    """jedes Stueck (5 Woerter) des JSON-Textes muss im PDF-Text vorkommen (Leerzeichen und Satzzeichen egal)"""
    skip = ("kind", "answer", "no", "letter", "design", "deco", "label", "notes", "model", "marks", "index", "minutes")
    strs = list(walk_strings({k: v for k, v in d.items() if k not in ("notes", "id", "roman")}, skip))
    body = pdf_flat(pdf, 2, 14)
    miss = [c for c in chunks(strs) if despace(c) not in body]
    n = sum(1 for _ in chunks(strs))
    print(f"  Textabdeckung PDF S.2-14: {n} Textstuecke geprueft, {len(miss)} nicht im PDF gefunden")
    for c in miss[:40]:
        print("   ?", c)
    models = [d["schreiben"]["task"]["model"]["text"]]
    pm = pdf_flat(pdf, 20, 20)
    mm = [c for c in chunks(models) if despace(c) not in pm]
    print(f"  Musterloesung: {len(mm)} Textstuecke nicht im PDF gefunden")
    for c in mm[:20]:
        print("   ?", c)
    return not miss and not mm


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    nopdf = "--no-pdf" in sys.argv
    if not args:
        print(__doc__)
        return 2
    rc = 0
    for a in args:
        path = a if a.endswith(".json") else os.path.join(HERE, "data", f"mt{a}.json")
        n = int(re.search(r"mt(\d+)", os.path.basename(path)).group(1))
        errors.clear()
        warnings.clear()
        print(f"== {os.path.relpath(path, REPO)}")
        try:
            d = json.load(open(path, encoding="utf-8"))
        except Exception as e:
            print("  JSON-Fehler:", e)
            rc = 1
            continue
        check_structure(d, n)
        clean = True
        if not nopdf:
            pdf = os.path.join(REPO, f"telc B1 Modelltest {n}.pdf")
            if errors:
                print("  (Struktur fehlerhaft, PDF-Vergleich uebersprungen)")
            elif not has_text(pdf):
                print("  (PDF ohne Textebene: Loesungsschluessel/Textabdeckung nicht automatisch pruefbar)")
            else:
                check_key(d, pdf)
                clean = check_coverage(d, pdf)
        for w in warnings:
            print("  WARNUNG:", w)
        for e in errors:
            print("  FEHLER:", e)
        if errors:
            rc = 1
        print("  OK" if not errors and clean else ("  Struktur OK, Textabweichungen pruefen" if not errors else "  FEHLER vorhanden"))
    return rc


if __name__ == "__main__":
    sys.exit(main())
