# 해설 데이터 형식 (erkN_lesen.py, erkN_hoeren.py)

Modelltest N의 해설은 파이썬 파일 두 개입니다. **Modelltest 1의 `erk1_lesen.py`, `erk1_hoeren.py`가 기준 예시**입니다. 같은 변수, 같은 키, 같은 분량과 어조로 씁니다.

## 근거 자료 (앱 폴더 `telc-b1/`)

| 자료 | 위치 |
|---|---|
| 문제, 본문, 정답, 쓰기 과제, 모범 답안 | `digital-src/data/mtN.json` |
| 말하기 과제 | `telc B1 Modelltest N.pdf` 15–18쪽 |
| 말하기 모범 대화 | 21쪽 |
| Hörtexte(듣기 대본) | 22–23쪽 |
| Kommentar(함정과 오답 해설, 교사용) | 24쪽 |

PDF 쪽은 `pdftoppm -r 150 -f 22 -l 22 -png "telc B1 Modelltest N.pdf" out`으로 그림으로 만들어 읽습니다. Modelltest 5만 글자층이 있어 `pdftotext -layout -f 22 -l 23`도 됩니다. **정답은 mtN.json이 기준**이고 Kommentar와 어긋나면 보고합니다.

## 변수

`erkN_lesen.py`: `LESEN1`, `LESEN2`, `LESEN3`, `SB1`, `SB2`
`erkN_hoeren.py`: `HOEREN1`, `HOEREN2`, `HOEREN3`, `SCHREIBEN`, `SPRECHEN`

| 변수 | 머리 키 | 문항 키 |
|---|---|---|
| LESEN1 | `tip` | `no, ans, topic, basis, why, trap, vocab` |
| LESEN2 | `intro`(본문 한 줄 요약), `tip` | `no, ans, basis, why, wrong{오답 글자: 이유}, vocab` |
| LESEN3 | `tip` | `no, ans, cond, basis, why, trap`(없으면 "") |
| SB1 | `title`(예: "항의 메일 (Kinderwagen)"), `tip` | `no, ans, sent, ko, why, wrong{오답 글자: 이유}` |
| SB2 | `title`, `tip`, `unused`(쓰이지 않은 단어 5개 설명) | `no, ans, sent, ko, why, wrong`(문자열, 없으면 "") |
| HOEREN1·2·3 | `title`(예: "다섯 사람의 의견", "인터뷰", "안내 방송"), `intro`, `tip` | `no, ans(R/F), st, stko, basis, why` |
| SCHREIBEN | `title`(예: "Julia에게 답장"), `mail_label`(예: "Julia의 메일"), `situation`, `points`[[독일어 Leitpunkt, 한국어, 쓸 수 있는 독일어 문장]]×4, `traps`[], `structure`[[항목, 독일어 예]], `model_ko`[], `redemittel`[[독일어, 한국어]], `criteria`[[I, Berücksichtigung der Leitpunkte, 설명], [II, …], [III, …]] | |
| SPRECHEN | `t1{task, points[], redemittel[]}`, `t2{task, a, b, steps[[Berichten, …]×4], redemittel[]}`, `t3{task, points[], redemittel[]}` | |

- `basis`: `[[원문 인용, 한국어 해석], …]`. 원문 인용은 **본문을 한 글자도 바꾸지 않고 그대로 잘라 옵니다**(따옴표 „ “, 줄표 –, 숫자 표기 포함). Lesen 1·2는 mtN.json 본문, Lesen 3은 광고(infos)의 한 칸 안에서, Hören은 PDF 대본에서 옮깁니다. 문장 일부만 잘라도 되지만 잘라 낸 부분은 원문과 똑같아야 합니다.
- `vocab`: `[[독일어, 한국어], …]` 3–4개. 명사는 관사와 복수형(der Unfall, ¨-e), 전치사 짝은 + Akk./+ Dat.
- `st`: mtN.json의 Hören 문장을 그대로. `stko`: 그 해석.
- SB1·SB2의 `sent`에는 **정답 단어가 들어간 문장**을 씁니다(빌드가 확인합니다). SB2의 `sent`에서 정답 단어는 소문자/대문자 상관없이 들어 있으면 됩니다.
- `model_ko`: 모범 답안(`model.text`)을 `\n\n`로 나눈 문단 수와 같은 개수의 한국어 번역.
- SCHREIBEN `points`는 mtN.json의 Leitpunkt 4개 순서 그대로.

## 쓰는 말

- 한국어는 **합니다체**(‘~입니다, ~합니다’). 반말과 ‘~다’ 체는 쓰지 않습니다. 비유 없이 직접 설명합니다.
- 번역도 존댓말로 씁니다. Hören 문장 해석(`stko`)은 합니다체(‘~합니다’)로, 친구에게 쓰는 편지·메시지의 번역(SB2 `ko`, `model_ko`)은 해요체(‘~해요’)로 씁니다. 공식 편지의 번역은 합니다체입니다.
- 학생은 B1 수험생이고 A2 수준도 있습니다. 문법 용어는 한국어로(2격, 3격, 4격, 관계대명사, 접속법 2식, 분리동사, 종속접속사, 등위접속사), 필요하면 괄호에 독일어 용어.
- 한국어 안의 강조·뜻풀이 따옴표는 ‘…’(U+2018, U+2019). 독일어 인용은 „…“. `‚`(낮은 따옴표)는 쓰지 않습니다.
- 함정(trap/wrong)은 **왜 그 보기를 고르기 쉬운지와 왜 틀렸는지**를 본문 근거와 함께 씁니다. 24쪽 Kommentar를 참고하되 그대로 옮기지 말고 학생에게 풀어서 설명합니다.
- Hören `why`는 문장의 어느 말이 대본의 어느 말과 같거나 다른지 짚습니다(바꿔 말하기, 숫자·요일, 부정, nur/nie/immer/ausschließlich 같은 단어).
- 말하기·쓰기 예문에 „Was machst du von Beruf?“, „Was sind Sie von Beruf?“ 같은 ‘von Beruf’ 표현은 쓰지 않습니다. 직업은 „Was machen Sie beruflich?“로 묻습니다.
- 쓰기 과제가 반격식(halbformell: 학교, 관리 회사, 직장 등)이면 Sie, „Sehr geehrte Frau …,“ / „Mit freundlichen Grüßen“을, 친구면 du, „Liebe/Lieber …,“ / „Liebe Grüße“를 설명합니다.
- 말하기 Teil 2의 `a`, `b`는 15–17쪽 두 사람의 의견을 한국어로 요약합니다. 마지막 `points`·Redemittel은 21쪽 모범 대화를 참고합니다.

## 확인

```
python3 -I digital-src/erklaerung/build.py . N <PretendardVariable.ttf> /tmp/check.html
```

빌드는 정답(mtN.json과 대조), Lesen 인용(본문에 그대로 있는지), Hören 문장, SB 문장 속 정답 단어를 검사하고 하나라도 어긋나면 멈춥니다. Hören 인용은 PDF 대본과 눈으로 대조합니다.
