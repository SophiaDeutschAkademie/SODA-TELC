# Modelltest JSON schema (telc Deutsch B2, digital exam data)

One file per Modelltest: `digital-src/data/mtN.json`, UTF-8, valid JSON. Source: the PDF `telc B2 Modelltest N.pdf` in the repository root (27 pages, text layer present; page layout is identical for all four tests).
Run `python3 digital-src/validate.py N` until it prints `OK` and the coverage report shows no unexplained differences.

## Page map of every PDF

| page | content |
|---|---|
| 1 | cover, Testformat |
| 2–3 | Leseverstehen Teil 1 (10 Überschriften a–j, 5 Texte 1–5) |
| 4–5 | Leseverstehen Teil 2 (article or interview on p. 4, Aufgaben 6–10 on p. 5) |
| 6–9 | Leseverstehen Teil 3 (Situationen 11–20 on p. 6, twelve Info-Texte a–l on p. 6–9) |
| 10 | Sprachbausteine Teil 1 (text with gaps 21–30, options a/b/c in the right column) |
| 11 | Sprachbausteine Teil 2 (text with gaps 31–40, word box a–o) |
| 12 / 13 / 14 | Hörverstehen Teil 1 (41–45) / Teil 2 (46–55) / Teil 3 (56–60) |
| 15 / 16 | Schriftlicher Ausdruck Aufgabe A / Aufgabe B |
| 17–19 | Mündlicher Ausdruck (not part of the digital screen, ignore) |
| 20 | Lösungsschlüssel (all items 1–60) |
| 21–22 | Musterlösungen Schriftlicher Ausdruck (A on 21, B on 22) |
| 23 | Musterlösungen Mündlicher Ausdruck (ignore) |
| 24–25 | Hörtexte (ignore) |
| 26–27 | Kommentar (ignore, but may help to understand traps) |

## General transcription rules (very important)

- Copy the German text **verbatim** from the PDF: same words, punctuation, capitalisation, „…“ quotes, – dashes, … ellipsis, ß, ä/ö/ü, numbers, units, e-mail/web addresses. Do not correct, shorten, paraphrase or modernise anything.
- Join the lines of one paragraph with single spaces. Remove only word-break hyphenation at line ends (`Wiesen-` + `bach` → `Wiesenbach`). Keep real hyphens of compounds (`E-Mail`, `Vier-Tage-Woche`, `Kleingarten-verein` only if the hyphen is part of the word). When unsure, look at the page image (`pdftoppm -r 110 -f N -l N -png file.pdf out`) and use common German spelling to decide.
- Two-column pages (Lesen Teil 1 texts, Teil 2 article, Teil 3 info texts): read the whole left column first, then the right column. `pdftotext -layout` mixes the columns – **always check the page image**. `pdftotext -raw` may also mix them.
- A new paragraph in the PDF (indent / visible gap) = a new string in `paragraphs`.
- Leave out page furniture: page numbers, the header line (`90 Minuten Leseverstehen und Sprachbausteine`), the rotated side label (`nehetsreveseL`, `enietsuabhcarpS`, `nehetsrevröH`, `kcurdsuA rehciltfirhcS`), and the answer boxes. Keep the italic instruction at the top of each Teil (`instruction`).
- Letter-spaced headings (`K L E I N G A RT E N V E R E I N`) are written normally (`KLEINGARTENVEREIN`); keep the visible capitalisation of the heading.
- Item numbers are strings: `"1"` … `"60"`.
- Answers: Lesen Teil 1 → headline letter `a`–`j`; Teil 2 → `a`/`b`/`c`; Teil 3 → info letter `a`–`l` or `x` (no solution); Sprachbausteine 1 → `a`/`b`/`c`; Sprachbausteine 2 → word letter `a`–`o`; Hören → `R` for `+` (richtig) and `F` for `–` (falsch).
- **Every answer must come from the Lösungsschlüssel on page 20.** `validate.py` parses page 20 and compares automatically.
- Options: keep the text after the letter, without the letter itself, exactly as printed (including capital letters of the word box, e.g. `ANGEWIESEN`).

## Top level

```json
{
  "id": 1,
  "roman": "I",
  "lesen":     { "t1": {...}, "t2": {...}, "t3": {...}, "sb1": {...}, "sb2": {...} },
  "hoeren":    { "t1": {...}, "t2": {...}, "t3": {...} },
  "schreiben": { "intro": "...", "tasks": [ {...A}, {...B} ] },
  "notes": "free text: anything uncertain, discrepancies you found and how you resolved them"
}
```

## Lesen

### t1 – Überschriften zuordnen, items 1–5
```json
"t1": {
  "instruction": "Lesen Sie zuerst die zehn Überschriften. Lesen Sie dann die fünf Texte und entscheiden Sie, welche Überschrift (a–j) am besten zu welchem Text (1–5) passt. Tragen Sie Ihre Lösungen in den Antwortbogen bei den Aufgaben 1–5 ein.",
  "headlines": [ { "letter": "a", "text": "Ältere Mieter sollen große Wohnungen räumen" } ],
  "texts": [ { "no": "1", "paragraphs": ["Hannelore Brandt hat 41 Jahre lang …"] } ],
  "items": [ { "no": "1", "answer": "g" } ]
}
```
10 headlines (a–j), 5 texts, 5 items.

### t2 – Artikel oder Interview, a/b/c, items 6–10
```json
"t2": {
  "instruction": "Lesen Sie zuerst den Artikel und lösen Sie dann die Aufgaben 6–10 zu dem Text.",
  "kind": "article",
  "title": "Die unterschätzte Kraft flüchtiger Begegnungen",
  "lead": "Ein kurzer Plausch beim Bäcker, …",
  "paragraphs": ["Jeden Morgen um halb acht …"],
  "source": "",
  "taskInstruction": "Lösen Sie die Aufgaben 6–10. Entscheiden Sie, welche Lösung (a, b oder c) richtig ist, und tragen Sie Ihre Lösung in den Antwortbogen bei den Aufgaben 6–10 ein.",
  "items": [ { "no": "6", "stem": "Für Frau Behrens ist das Gespräch beim Bäcker", "options": { "a": "ein Ritual, …", "b": "…", "c": "…" }, "answer": "a" } ]
}
```
- `kind` is `"article"` or `"interview"`. For an interview, `paragraphs` entries are objects `{ "q": true, "text": "…?" }` for the interviewer's questions and `{ "text": "…" }` for the answers (as printed; keep the speaker label out unless it is printed in the text). For an article use plain strings.
- `lead` = the printed lead/teaser line(s) below the title (`""` if none); `source` = printed source line (`""` if none).
- The stem is printed without the item number. Keep a trailing `…` if one is printed.

### t3 – Situationen und Info-Texte, items 11–20
```json
"t3": {
  "instruction": "Lesen Sie zuerst die zehn Situationen (11–20) und dann die zwölf Info-Texte (a–l). Welcher Info-Text passt zu welcher Situation? Sie können jeden Info-Text nur einmal verwenden. Markieren Sie Ihre Lösungen auf dem Antwortbogen bei den Aufgaben 11–20. Manchmal gibt es keine Lösung. Markieren Sie dann x.",
  "items": [ { "no": "11", "text": "Ein Bekannter sucht sofort einen Musikkurs für seinen Sohn (5).", "answer": "x" } ],
  "infos": [
    {
      "letter": "a",
      "header": "Stimmwerk",
      "tag": "",
      "title": "SINGEN OHNE NOTEN",
      "subtitle": "",
      "facts": [],
      "body": ["Sie singen gern unter der Dusche, …"],
      "footer": "Kontakt: stimmwerk-chor@web.de"
    }
  ]
}
```
Exactly 10 items and 12 infos a–l. All info fields except `letter` are optional (`""` or `[]`). The info texts are small advertisements/notices with their own layout (see the page image). Use the fields to keep the visible structure: `header` = organisation/brand/heading line at the top, `tag` = small label (e.g. `Saatgutbibliothek`, `17. APRIL`), `title` = main bold heading, `subtitle` = second heading line, `facts` = short detail lines that are printed as separate lines/bullets (times, prices), `body` = running text paragraphs, `footer` = contact/bottom line(s) (several joined with ` · `). Every piece of information printed in the box must end up somewhere. If a box has a heading in two lines (`Es ist nie zu spät` / `für Chopin`) put it into one `title` string separated by a space.
Optional `"design"` and `"deco"` (see the layout table at the end) – leave them out; the app chooses layouts.

### sb1 – Sprachbausteine Teil 1, items 21–30
```json
"sb1": {
  "instruction": "Lesen Sie den folgenden Text und entscheiden Sie, welches Wort (a, b oder c) in die jeweilige Lücke passt. Markieren Sie Ihre Lösungen auf dem Antwortbogen bei den Aufgaben 21–30.",
  "paragraphs": ["Sehr geehrte Frau Dr. Lindner,", "vielleicht erinnern Sie sich noch an mich: … habe Herrn Albrecht unterstützt, {{21}} Team damals die große Kundenbefragung durchgeführt hat. …", "Mit freundlichen Grüßen", "Julia Kowalski"],
  "items": [ { "no": "21", "options": { "a": "dem", "b": "denen", "c": "dessen" }, "answer": "a" } ]
}
```
Write every gap as `{{21}}` (the number printed in the gap). The gap can stand anywhere, also at the start of a sentence. Greeting, salutation and signature lines are separate paragraphs (as printed).

### sb2 – Sprachbausteine Teil 2, items 31–40
```json
"sb2": {
  "instruction": "Lesen Sie den folgenden Text und entscheiden Sie, welches Wort aus dem Kasten (a–o) in die Lücken 31–40 passt. …",
  "title": "Mehrweg statt Einweg: eine ernüchternde Bilanz",
  "paragraphs": ["Seit Januar 2023 sind … verkaufen, {{31}} verpflichtet, …"],
  "words": { "a": "ANGEWIESEN", "b": "AUF", "…": "…", "o": "VERSPROCHEN" },
  "items": [ { "no": "31", "answer": "g" } ]
}
```
15 words a–o exactly as printed in the box (usually capital letters).

## Hören

Three parts, each with true/false statements. Answer `R` (richtig, `+`) or `F` (falsch, `–`).
```json
"t1": {
  "instruction": "Sie hören nun eine Nachrichtensendung. Dazu sollen Sie fünf Aufgaben lösen. Sie hören die Nachrichtensendung nur einmal. Entscheiden Sie beim Hören, ob die Aussagen 41–45 richtig oder falsch sind. Markieren Sie Ihre Lösungen auf dem Antwortbogen bei den Aufgaben 41–45. Markieren Sie PLUS (+) gleich richtig und MINUS (–) gleich falsch auf dem Antwortbogen.",
  "readNote": "Lesen Sie jetzt die Aufgaben 41–45. Sie haben dazu 30 Sekunden Zeit.",
  "items": [ { "no": "41", "text": "Die meisten Menschen über 65, die noch arbeiten, tun das vor allem aus finanziellen Gründen.", "answer": "F" } ]
}
```
`t1` 5 items (41–45), `t2` 10 items (46–55), `t3` 5 items (56–60). `instruction` = the printed intro paragraph(s) joined with a space, **without** the `readNote` sentence (`Lesen Sie jetzt die Aufgaben …`, if printed; otherwise `""`). Statements may wrap over two lines: join them.

## Schreiben

```json
"schreiben": {
  "intro": "Wählen Sie zuerst zwischen Aufgabe A und Aufgabe B. Entscheiden Sie schnell, denn die zur Verfügung stehende Zeit ist begrenzt auf 30 Minuten!",
  "tasks": [
    {
      "letter": "A",
      "kind": "Bitte um Informationen",
      "lead": "Sie lesen im Internet folgende Anzeige:",
      "ad": { "header": "SicherDaheim", "tag": "HAUSNOTRUF", "title": "Allein leben – aber nie allein gelassen.", "subtitle": "", "facts": ["Notrufknopf als Armband oder Kette, wasserdicht", "…"], "body": ["Mit unserem Hausnotruf sind Sie …"], "footer": "Jetzt vier Wochen unverbindlich testen! · info@sicherdaheim.de" },
      "situation": ["Ihre Großmutter lebt allein und ist vor Kurzem in ihrer Wohnung gestürzt. Sie interessieren sich für den Hausnotruf und möchten mehr darüber erfahren. Schreiben Sie eine E-Mail an SicherDaheim."],
      "choice": ["Behandeln Sie darin entweder", "a) drei der folgenden Punkte oder", "b) zwei der folgenden Punkte und einen weiteren Aspekt Ihrer Wahl."],
      "points": ["Beschreiben Sie die Situation Ihrer Großmutter.", "…", "…", "…"],
      "closing": "Überlegen Sie sich vor dem Schreiben eine passende Reihenfolge der Punkte, … Schreiben Sie mindestens 150 Wörter.",
      "words": 150,
      "model": { "label": "Beispiel für Variante a): drei der vier Leitpunkte (ca. 190 Wörter)", "text": "Betreff: Anfrage zu Ihrem Hausnotruf …\n\nSehr geehrte Damen und Herren,\n\nauf Ihrer Internetseite …\n\nMit freundlichen Grüßen\nDaniel Moreno" }
    }
  ]
}
```
- Two tasks, `letter` `"A"` and `"B"` (A = Bitte um Informationen, B = Beschwerde). `ad` uses the same fields as an info text (`header`, `tag`, `title`, `subtitle`, `facts`, `body`, `footer`); if the task prints a different kind of source text (e.g. a poster), still use `ad`. `lead` = the sentence introducing the source (`Sie lesen im Internet folgende Anzeige:`).
- `facts` are bullet lines in the ad, `footer` the bottom line(s) of the ad joined with ` · `.
- `situation` = the paragraph(s) below the ad that describe the situation and the task. `choice` = the lines `Behandeln Sie darin entweder` / `a) …` / `b) …`. `points` = the four Leitpunkte (bullets) without the bullet sign. `closing` = the last paragraph.
- `model.text` = the sample e-mail on page 21 (Aufgabe A) / page 22 (Aufgabe B) **only the e-mail itself** (from `Betreff:` to the signature), paragraphs separated by a blank line (`\n\n`), the `Betreff:` line first. Do **not** copy the margin notes (Leitpunkte, Aufbau, Bewertung, Typische Fehler) or the little grey numbers at the paragraph starts. `model.label` = the printed line below the heading (`Beispiel für Variante a): …`). `model.notes` (optional) = the margin column as plain text (Leitpunkte, Aufbau, Bewertung, Typische Fehler), lines joined with `\n`.
- `words`: 150.

## Optional: ad layouts (`design`, `deco`)

Info texts and the ads of the writing tasks may carry `"design"` and `"deco"`; leave them out – the app picks layouts.
