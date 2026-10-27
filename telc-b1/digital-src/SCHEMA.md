# Modelltest JSON schema (telc Deutsch B1, digital exam data)

One file per Modelltest: `digital-src/data/mtN.json`, UTF-8, valid JSON. Source: the PDF `telc B1 Modelltest N.pdf` in the app folder (24 pages; page layout is identical for all five tests).
Run `python3 digital-src/validate.py N` until it prints `OK`.

Modelltest 1–4 have **no text layer** (the glyphs are vector outlines): `validate.py` checks the structure and skips the automatic comparison with the PDF. Modelltest 5 has a text layer and is compared automatically (answer key and text coverage).

## Page map of every PDF

| page | content |
|---|---|
| 1 | cover, Testformat |
| 2–3 | Leseverstehen Teil 1 (10 Überschriften a–j, 5 Texte 1–5) |
| 4 | Leseverstehen Teil 2 (article or interview) |
| 5 | Leseverstehen Teil 2 (Aufgaben 6–10, a/b/c) |
| 6 | Leseverstehen Teil 3 (Situationen 11–20) |
| 7–8 | Leseverstehen Teil 3 (twelve Anzeigen a–l) |
| 9 | Sprachbausteine Teil 1 (text with gaps 21–30, options a/b/c) |
| 10 | Sprachbausteine Teil 2 (text with gaps 31–40, word box a–o) |
| 11 / 12 / 13 | Hörverstehen Teil 1 (41–45) / Teil 2 (46–55) / Teil 3 (56–60) |
| 14 | Schriftlicher Ausdruck (one e-mail, four Leitpunkte) |
| 15 / 16–17 / 18 | Mündlicher Ausdruck Teil 1 / Teil 2 (A, B) / Teil 3 (not part of the digital screen) |
| 19 | Lösungsschlüssel (all items 1–60) |
| 20 | Musterlösung Schriftlicher Ausdruck |
| 21 | Musterdialoge Mündlicher Ausdruck (ignore) |
| 22–23 | Hörtexte (ignore) |
| 24 | Kommentar (ignore, but may help to understand traps) |

## General transcription rules

- Copy the German text **verbatim** from the PDF: same words, punctuation, capitalisation, „…“ quotes, – dashes, … ellipsis, ß, ä/ö/ü, numbers, units, e-mail/web addresses. Do not correct, shorten, paraphrase or modernise anything.
- Join the lines of one paragraph with single spaces. Remove only word-break hyphenation at line ends. Keep real hyphens of compounds (`E-Mail`). When unsure, look at the page image (`pdftoppm -r 110 -f N -l N -png file.pdf out`).
- Two-column pages (Lesen Teil 1 texts, Teil 2 article, Teil 3 Anzeigen): read the whole left column first, then the right column. Always check the page image.
- A new paragraph in the PDF (indent / visible gap) = a new string in `paragraphs`.
- Leave out page furniture: page numbers, header line, the rotated side label, the answer boxes. Keep the italic instruction at the top of each Teil (`instruction`).
- Item numbers are strings: `"1"` … `"60"`.
- Answers: Lesen Teil 1 → headline letter `a`–`j`; Teil 2 → `a`/`b`/`c`; Teil 3 → Anzeige letter `a`–`l` or `x` (keine passende Anzeige); Sprachbausteine 1 → `a`/`b`/`c`; Sprachbausteine 2 → word letter `a`–`o`; Hören (all three parts) → `R` for `+` (richtig) and `F` for `–` (falsch).
- **Every answer must come from the Lösungsschlüssel on page 19.** For Modelltest 5 `validate.py` parses page 19 and compares automatically; for Modelltest 1–4 compare the page image by eye (`pdftoppm -r 150 -f 19 -l 19`).
- Options: keep the text after the letter, without the letter itself, exactly as printed (including capital letters of the word box, e.g. `ANGEWIESEN`).

## Top level

```json
{
  "id": 1,
  "roman": "I",
  "lesen":     { "t1": {...}, "t2": {...}, "t3": {...}, "sb1": {...}, "sb2": {...} },
  "hoeren":    { "t1": {...}, "t2": {...}, "t3": {...} },
  "schreiben": { "intro": "", "task": {...} },
  "notes": "free text: anything uncertain, discrepancies you found and how you resolved them",
  "index": { ... }
}
```

`build-digital.py` removes the top-level `notes` and `index` from the data it embeds in `digital.html` (they are only for the repository and for `index.html`).

## Lesen

### t1 – Überschriften zuordnen, items 1–5
```json
"t1": {
  "instruction": "Lesen Sie die Überschriften a–j und die Texte 1–5. …",
  "headlines": [ { "letter": "a", "text": "…" } ],
  "texts": [ { "no": "1", "paragraphs": ["…"] } ],
  "items": [ { "no": "1", "answer": "h" } ]
}
```
10 headlines (a–j), 5 texts, 5 items. Each headline is used at most once.

### t2 – Artikel oder Interview, a/b/c, items 6–10
```json
"t2": {
  "instruction": "Lesen Sie den Text und die Aufgaben 6–10. …",
  "kind": "article",
  "title": "Ein Laden, der allen gehört",
  "lead": "Im Dorf Lindenbach hat …",
  "paragraphs": ["…"],
  "source": "",
  "taskInstruction": "",
  "items": [ { "no": "6", "stem": "Bürgermeister Frank Ohler", "options": { "a": "…", "b": "…", "c": "…" }, "answer": "b" } ]
}
```
- `kind` is `"article"` or `"interview"`. For an interview, `paragraphs` entries are objects `{ "q": true, "text": "…?" }` for the questions and `{ "text": "…" }` for the answers; for an article use plain strings.
- `lead` and `source` must exist (`""` if the PDF prints none). `taskInstruction` is the printed second instruction above Aufgaben 6–10 if there is one, otherwise `""`.

### t3 – Situationen und Anzeigen, items 11–20
```json
"t3": {
  "instruction": "Lesen Sie die Situationen 11–20 und die Anzeigen a–l. …",
  "items": [ { "no": "11", "text": "Sie ziehen am Samstag um und brauchen einen Transporter samt Helfern.", "answer": "c" } ],
  "infos": [
    { "letter": "a", "header": "Musikschule Klangwerk", "tag": "", "title": "", "subtitle": "…", "facts": [], "body": ["…"], "footer": "…" }
  ]
}
```
Exactly 10 items and 12 infos a–l. Each Anzeige can be the solution of at most one item; `x` (keine passende Anzeige) is the solution of exactly two items in every Modelltest (`validate.py` warns otherwise). All info fields except `letter` are optional (`""` or `[]`): `header` = organisation/brand line at the top, `tag` = small label, `title` = main bold heading, `subtitle` = second heading line, `facts` = short detail lines printed as separate lines/bullets (times, prices), `body` = running text paragraphs, `footer` = contact/bottom line(s) (several joined with ` · `). Every piece of information printed in the box must end up somewhere. The ads have their own layouts in the PDF; the app chooses its own, so leave out `design` and `deco`.

### sb1 – Sprachbausteine Teil 1, items 21–30
```json
"sb1": {
  "instruction": "Lesen Sie den Text und schließen Sie die Lücken 21–30. …",
  "paragraphs": ["Sehr geehrte Damen und Herren,", "… ist {{21}} einer Woche angekommen, {{22}} …"],
  "items": [ { "no": "21", "options": { "a": "während", "b": "innerhalb", "c": "seit" }, "answer": "b" } ]
}
```
Write every gap as `{{21}}` (the number printed in the gap), in order 21–30. Greeting, salutation and signature lines are separate paragraphs (as printed); a `\n` inside a paragraph is shown as a line break.

### sb2 – Sprachbausteine Teil 2, items 31–40
```json
"sb2": {
  "instruction": "Lesen Sie den Text und schließen Sie die Lücken 31–40. …",
  "title": "",
  "paragraphs": ["…{{31}}…"],
  "words": { "a": "ANGEWIESEN", "b": "…", "o": "…" },
  "items": [ { "no": "31", "answer": "k" } ]
}
```
15 words a–o exactly as printed in the box. B1 has no printed title: `title` exists but stays `""` (the app hides it). Each word is used at most once.

## Hören

Three parts, all richtig/falsch. Answer `R` (richtig) or `F` (falsch).
```json
"t1": {
  "instruction": "Sie hören nun fünf kurze Texte. Dazu sollen Sie fünf Aufgaben lösen. Sie hören diese Texte nur einmal. …",
  "readNote": "Lesen Sie jetzt die Aufgaben 41–45. Sie haben dazu 30 Sekunden Zeit.",
  "items": [ { "no": "41", "text": "Die Sprecherin hat ihren Umzug aufs Land noch nie in Frage gestellt.", "answer": "F" } ]
}
```
`t1` 5 items (41–45, heard once), `t2` 10 items (46–55, heard twice), `t3` 5 items (56–60, each text twice). `instruction` = the printed intro paragraph(s) joined with a space, **without** the `readNote` sentence; `readNote` must exist (`""` if the PDF has none, e.g. Teil 3).

The app derives the audio files from the PDF number: `telc B1 Modelltest N.1.mp3` (Teil 1), `N.2.mp3` (Teil 2), `N.3.mp3` (Teil 3). `build-digital.py` reads the durations with `ffprobe` and sets the Hören timer to the total in minutes, rounded up, plus 2.

## Schreiben

telc B1 has **one** writing task: an e-mail answer with four Leitpunkte (30 minutes). The PDF prints no minimum word count, so the word counter is only a guide.
```json
"schreiben": {
  "intro": "",
  "task": {
    "lead": "Sie haben von Ihrer Freundin Julia folgende E-Mail erhalten:",
    "mail": ["Liebe / Lieber ______,", "endlich habe ich …", "Hast du …", "Ich freue mich riesig!", "Liebe Grüße\nJulia"],
    "instruction": "Antworten Sie auf die E-Mail. Schreiben Sie etwas zu allen vier Punkten:",
    "points": ["ob das Wochenende passt – …", "was Sie zusammen unternehmen können", "…", "…"],
    "closing": "Überlegen Sie sich vor dem Schreiben eine passende Reihenfolge der Punkte, …",
    "model": {
      "label": "Beispiel für eine Antwort, die alle vier Leitpunkte behandelt (ca. 170 Wörter)",
      "text": "Betreff: …\n\nLiebe Julia,\n\n…\n\nLiebe Grüße\nName",
      "marks": ["", "", "1", "2", "3", "4", "", ""],
      "notes": "Leitpunkte\n1 …\nAufbau …\nBewertung\nI …\nTypische Fehler: …"
    }
  }
}
```
- `mail` = the e-mail the student has to answer, at least 3 paragraphs as printed (the salutation line and the signature included); a `\n` inside a paragraph is a line break.
- `points` = exactly 4 Leitpunkte without the bullet sign.
- `model.text` = the sample e-mail on page 20, **only the e-mail itself**, starting with `Betreff:`, paragraphs separated by a blank line (`\n\n`). Do not copy the margin notes.
- `model.marks` (optional) = one entry per paragraph of `model.text`: `""` or the number (`"1"`–`"4"`) of the Leitpunkt that paragraph covers (printed as little grey numbers in the PDF). Each Leitpunkt 1–4 appears exactly once. The result view shows them as badges next to the paragraph.
- `model.notes` (optional) = the margin column of page 20 as plain text (Leitpunkte, Aufbau, Bewertung, Typische Fehler), lines joined with `\n`.

## index (topics for index.html)

```json
"index": {
  "short": "Ein Laden, der allen gehört · Neuanfang mit 45 · …",
  "hoeren": { "t1": "Fünf kurze Texte", "t2": "Gespräch mit Lukas Berger: Neuanfang mit 45", "t3": "Fünf kurze Texte" },
  "sb1": "Beschwerde: Kinderwagen",
  "sb2": "E-Mail an Jonas: Neu in Wien",
  "schreiben": "Antwort an Julia: Besuch im Mai",
  "sprechen": { "t2": "Handys in der Schule", "t3": "Tagesausflug" }
}
```
Short topic labels for the lists in `index.html` (`short` = one line for the overview, the rest per Teil). The Mündlich topics come from PDF pages 16–18.
