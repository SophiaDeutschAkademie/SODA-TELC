# Modelltest JSON schema (telc Deutsch C1 Hochschule, digital exam data)

One file per Modelltest: `digital-src/data/mtN.json`, UTF-8, valid JSON. Source: the PDF `telc C1 HS Modelltest N.pdf` in the app folder (33 pages for Modelltest 1–2, 34 pages for 3–5; the first page numbers below are identical for all five tests).
Run `python3 digital-src/validate.py N` until it prints `OK`. All five PDFs have a text layer, so `validate.py` also compares the answer key (64 answers) and the text with the PDF automatically.

## Page map of every PDF

| page | content |
|---|---|
| 1 | cover, Testformat |
| 2–3 | Leseverstehen 1 (article with six gaps 1–6, sentences a–h, example gap 0 with sentence z) |
| 4–5 | Leseverstehen 2 (text in five Abschnitte a–e, "In welchem Abschnitt …" 7–12, example 0) |
| 6–8 | Leseverstehen 3 (text, statements 13–23 richtig / falsch / nicht im Text, headline 24 a/b/c) |
| 9–10 | Sprachbausteine (text with gaps 25–46, options a–d, example gap 0) |
| 11 / 12 / 13 | Hörverstehen Teil 1 (47–54) / Teil 2 (55–64) / Teil 3 (65–74, Handzettel) |
| 15 | Schriftlicher Ausdruck (two Themen, choose one) |
| 16–19 | Mündlicher Ausdruck (Teil 1 A, B, C on 16–18, Teil 2 on 19; not part of the digital screen) |
| 20 | Lösungsschlüssel (items 1–64; the notes 65–74 are printed as text) |
| 21 | Musterlösung Schriftlicher Ausdruck (both Themen) |
| 23 | Musterlösungen Mündlicher Ausdruck (ignore for the digital screen; linked from index.html) |
| 25– | Hörtexte (ignore) |
| 31– | Kommentar (ignore, but may help to understand traps) |

The numbers of the answer-key, model-text, Hörtexte and Kommentar pages are set in `build-digital.py` (`PAGES`) and `build-index.py` (`PDF_PAGES`).

## General transcription rules

- Copy the German text **verbatim** from the PDF: same words, punctuation, capitalisation, „…“ quotes, – dashes, … ellipsis, ß, ä/ö/ü, numbers. Do not correct, shorten, paraphrase or modernise anything.
- Join the lines of one paragraph with single spaces. Remove only word-break hyphenation at line ends. Keep real hyphens of compounds (`1950er-Jahren`). When unsure, look at the page image (`pdftoppm -r 110 -f N -l N -png file.pdf out`).
- A new paragraph in the PDF = a new string in `paragraphs`.
- Leave out page furniture: page numbers, header line, the answer boxes. Keep the italic instruction at the top of each Teil (`instruction`).
- Item numbers are strings: `"1"` … `"74"`.
- Answers: Lesen 1 → sentence letter `a`–`h`, each used once; Lesen 2 → Abschnitt `a`–`e`; Lesen 3 statements → `r` (richtig), `f` (falsch), `n` (nicht im Text; printed as `–` in the key), headline → `a`/`b`/`c`; Sprachbausteine → `a`–`d`; Hören Teil 1 → statement letter `a`–`j`, each used at most once; Teil 2 → `a`/`b`/`c`; Teil 3 → free text (`solution`).
- **Every answer must come from the Lösungsschlüssel on page 20.** `validate.py` parses the page and compares all 64 closed answers.

## Top level

```json
{
  "id": 1,
  "roman": "I",
  "lesen":     { "t1": {...}, "t2": {...}, "t3": {...}, "sb": {...} },
  "hoeren":    { "t1": {...}, "t2": {...}, "t3": {...} },
  "schreiben": { "instruction": "", "minWords": 350, "minutes": 70, "themes": [ {...}, {...} ] },
  "muendlich": { "teil1": [...], "teil2": [...] },
  "notes": "free text: anything uncertain, discrepancies you found and how you resolved them",
  "index": { ... }
}
```

`build-digital.py` removes the top-level `notes`, `muendlich` and `index` from the data it embeds in `digital.html` (they are only for the repository and for `index.html`).

## Lesen

### t1 – Sätze in Lücken einsetzen, items 1–6
```json
"t1": {
  "instruction": "Lesen Sie den folgenden Text. Welche der Sätze a–h gehören in die Lücken 1–6? …",
  "intro": "In der Wissenschaftsbeilage Ihrer Hochschulzeitung lesen Sie folgenden Artikel:",
  "title": "Basisdemokratie im Bienenschwarm",
  "paragraphs": ["Wird ein Bienenvolk zu groß, … {{0}} Danach …", "… {{1}}"],
  "sentences": [ { "letter": "a", "text": "…" } ],
  "example": { "letter": "z", "text": "Dort hängt er als dichte Traube, …" },
  "items": [ { "no": "1", "answer": "e" } ]
}
```
Write every gap as `{{n}}` in the paragraph where it is printed: `{{0}}` is the example gap (filled with sentence `z`), then `{{1}}`–`{{6}}` in order. 8 sentences a–h (two stay unused), 6 items.

### t2 – In welchem Abschnitt …, items 7–12
```json
"t2": {
  "instruction": "Lesen Sie den folgenden Text. In welchem Textabsatz a–e finden Sie die Antworten auf die Fragen 7–12? …",
  "title": "Englisch für alle – ein Gewinn mit Nebenwirkungen",
  "sections": [ { "letter": "a", "text": "…" } ],
  "exampleLead": "In welchem Abschnitt …",
  "example": { "stem": "nennt der Autor politische Ereignisse …?", "answer": "a" },
  "itemsLead": "In welchem Abschnitt …",
  "items": [ { "no": "7", "stem": "beklagt der Autor, dass …?", "answer": "c" } ]
}
```
5 sections a–e, 6 items. `stem` continues the printed lead ("In welchem Abschnitt …").

### t3 – richtig / falsch / nicht im Text, items 13–23, and headline 24
```json
"t3": {
  "instruction": "Lesen Sie den folgenden Text und die Aussagen 13–23. Welche der Aussagen sind richtig (r), …",
  "title": "",
  "paragraphs": ["…"],
  "itemsLead": "Aussagen 13–23",
  "items": [ { "no": "13", "text": "Auch wer unter Zeitdruck …", "answer": "f" } ],
  "headline": {
    "instruction": "Welche der Überschriften a, b oder c trifft die Aussage des Textes am besten? …",
    "no": "24",
    "options": { "a": "…", "b": "…", "c": "…" },
    "answer": "b"
  }
}
```
11 statements with answer `r`, `f` or `n`. `title` may be `""`.

### sb – Sprachbausteine, items 25–46
```json
"sb": {
  "instruction": "Lesen Sie den folgenden Text. Welche Lösung (a, b, c oder d) ist jeweils richtig? …",
  "title": "Wie die deutsche Rechtschreibung einheitlich wurde",
  "paragraphs": ["Wer um 1870 … {{0}} …", "… {{25}} …"],
  "example": { "options": { "a": "vor allem", "b": "vor Allem", "c": "vor allen", "d": "vorallem" }, "answer": "a" },
  "items": [ { "no": "25", "options": { "a": "dem", "b": "den", "c": "denen", "d": "der" }, "answer": "d" } ]
}
```
Gaps in the text: `{{0}}` (example), then `{{25}}`–`{{46}}`. Options exactly as printed, without the letter.

## Hören

Heard **once** (all three parts). Answer types: Teil 1 letter, Teil 2 letter, Teil 3 free text.
```json
"t1": {
  "instruction": "Sie hören die Meinungen von acht Personen. …",
  "readNote": "Lesen Sie jetzt die Aussagen a–j. Sie haben dazu eine Minute Zeit.",
  "title": "KI-Werkzeuge im Studium",
  "statements": [ { "letter": "a", "text": "…" } ],
  "items": [ { "no": "47", "label": "Sprecherin 1", "answer": "f" } ]
},
"t2": {
  "instruction": "…", "readNote": "Lesen Sie jetzt die Aufgaben 55–64. Sie haben dazu drei Minuten Zeit.",
  "items": [ { "no": "55", "stem": "Frau Ostendorf hat … ins Leben gerufen, weil", "options": { "a": "…", "b": "…", "c": "…" }, "answer": "a" } ]
},
"t3": {
  "instruction": "Sie hören einen Vortrag. …",
  "exampleNote": "Die Lösung 0 ist ein Beispiel.",
  "readNote": "Lesen Sie jetzt die Stichworte. …",
  "finalNote": "Sie haben jetzt fünf Minuten Zeit, Ihre Antworten …",
  "exampleAnswer": "Medizin im Gespräch",
  "slides": [ { "title": "Ringvorlesung", "lines": [ { "no": "0", "bullet": false, "dash": false, "text": "…" } ] } ],
  "items": [ { "no": "65", "solution": "zufriedenzustellen / zu beruhigen (nicht: zu heilen)" } ]
}
```
- `t1`: 10 statements a–j, 8 items 47–54 (eight different answers). `label` = `Sprecherin 1` etc.
- `t3.slides`: the Handzettel as printed, one object per Folie. A line with `"no": "n"` is a gap to fill in (the app shows an input field); lines without `no` are fixed text. `bullet` / `dash` mark the list sign printed before the line. `no` appears exactly for `"0"` (example) and `"65"`–`"74"`. `text` of a gap line holds the fixed text around the gap with `…` where the answer belongs.
- `t3.items[].solution` = the printed solution from page 20 (variants separated by ` / `, hints in parentheses).

The app derives the audio files from the PDF number: `telc C1 HS Modelltest N.1.mp3` (Teil 1), `N.2.mp3`, `N.3.mp3`. The Hören timer is the printed 40 minutes; `build-digital.py` sets `minutes.hoeren` to `max(40, audio minutes + 2)`.

Notes (Teil 3) are **self-assessed** in the app: after submitting, each note is shown with the printed solution and the student marks it ✓ / ✗ (richtig 2 Punkte). Unrated notes count as 0.

## Schreiben

```json
"schreiben": {
  "instruction": "Wählen Sie eines der folgenden zwei Themen. Schreiben Sie einen Text, in dem Sie …",
  "minWords": 350,
  "minutes": 70,
  "themes": [
    {
      "no": "1",
      "paragraphs": ["In einem hochschuldidaktischen Seminar sollen Sie …"],
      "quoteLead": "Die folgenden Zitate geben Ihnen erste Ideen:",
      "quotes": ["„Ein Seminar lebt vom Gespräch …“", "„Erwachsene …“"],
      "model": {
        "title": "Anwesenheitspflicht – Bevormundung oder Voraussetzung für gute Lehre?",
        "paragraphs": ["Kaum eine Regelung …", "…", "…"],
        "hint": "Aufbau: Einleitung mit Problemaufriss – Position 1 …"
      }
    }
  ]
}
```
Exactly two Themen (`"1"`, `"2"`), two quotes each. `model` = the sample text of page 21 (title + at least 3 paragraphs); `hint` = the printed Aufbau/Bewertungs-Hinweis (may be `""`).

## muendlich (index.html only, not digitised)

```json
"muendlich": {
  "teil1": [ { "who": "A", "themes": ["Beschreiben Sie …", "…"] } ],
  "teil2": [ { "no": "1", "text": "„Man muss das Wahre …“", "author": "Johann Wolfgang von Goethe, 1749–1832, Dichter" } ]
}
```
Teil 1: participants A, B, C with two themes each (PDF pages 16–18); Teil 2: three quotes (page 19).

## index (topics for index.html)

```json
"index": {
  "short": "Basisdemokratie im Bienenschwarm · Englisch für alle … · …",
  "lesen":     { "t1": "…", "t2": "…", "t3": "…", "sb": "…" },
  "hoeren":    { "t1": "KI-Werkzeuge im Studium", "t2": "…", "t3": "Placebo und Nocebo" },
  "schreiben": { "t1": "Anwesenheitspflicht in Lehrveranstaltungen", "t2": "Direkt nach der Schule studieren?" },
  "sprechen":  { "t1": [ { "who": "A", "topics": ["…", "…"] } ], "t2": [ { "no": "1", "author": "Johann Wolfgang von Goethe" } ] }
}
```
Short topic labels for the lists in `index.html` (`short` = one line for the overview, the rest per Teil).
