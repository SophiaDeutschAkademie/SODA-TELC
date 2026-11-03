# 해설 데이터 형식 — telc B2 (erkN_lesen.py, erkN_hoeren.py)

telc B2 해설은 telc B1 해설과 같은 빌드(`build.py`, `style.css`)를 씁니다. **기본 형식과 쓰는 규칙은 `../../../telc-b1/digital-src/erklaerung/FORMAT.md`를 따르고, 기준 예시는 `../../../telc-b1/digital-src/erklaerung/erk1_lesen.py`, `erk1_hoeren.py`입니다.** 이 문서는 B2에서 달라지는 점만 적습니다.

## 근거 자료 (앱 폴더 `telc-b2/`)

| 자료 | 위치 |
|---|---|
| 문제, 본문, 정답, 쓰기 과제 A·B, 모범 답안 | `digital-src/data/mtN.json` |
| Kommentar(함정과 오답 해설) | `mtN.json`의 `kommentar.items["1"…"60"]` (PDF 26–27쪽과 같음) |
| 말하기 과제 | `telc B2 Modelltest N.pdf` 17–19쪽 |
| 말하기 모범 예시 | 23쪽 |
| Hörtexte(듣기 대본) | 24–25쪽 |
| 쓰기·말하기 채점 기준 | `digital-src/guide-data.json`, `sprechen-data.json` |

B2 PDF에는 글자층이 있습니다. `pdftotext -layout -f 24 -l 25 "telc B2 Modelltest N.pdf" -`로 읽고, 두 단 순서는 `pdftoppm -r 120 -f 24 -l 24 -png …`로 그림을 만들어 확인합니다. 줄 끝 하이픈은 이어 붙입니다.

## 달라지는 점

- **Lesen Teil 2**는 기사(article) 또는 인터뷰(interview)입니다. 인터뷰의 `basis` 인용은 질문·답의 `text`에서 그대로 자릅니다. LESEN2 `intro`는 글 내용을 한 줄로 요약합니다.
- **Lesen Teil 3**은 광고가 아니라 안내문(Info-Texte)입니다. 인용은 `infos`의 한 칸 안에서 그대로 자릅니다.
- **SB2** `title`은 PDF에 인쇄된 글 제목을 그대로 씁니다(독일어).
- **Hören**은 세 부분 모두 한 번만 듣습니다. `title` 예: "뉴스(Nachrichtensendung)", "라디오 인터뷰", "안내 방송". `tip`에 한 번만 듣는다는 점을 반영합니다.
- **SCHREIBEN**은 과제가 두 개(A: 정보 요청, B: 항의)이고 학생은 하나를 고릅니다. 형식:

```python
SCHREIBEN = {
  "intro": "A·B 중 하나를 고르는 요령과 공통 조건(30분, 최소 150단어, 두 가지 방식 a/b 중 하나)을 한국어로",
  "tasks": [
    {"letter": "A", "title": "SicherDaheim에 정보 요청",          # 짧은 한국어 제목
     "situation": "상황 요약과 편지 형식(Sie, 호칭, 끝인사)",
     "points": [["독일어 Leitpunkt(mtN.json 그대로)", "한국어", "쓸 수 있는 독일어 문장"], … 4개],
     "traps": ["자주 하는 실수", …],
     "structure": [["Betreff", "…"], ["Anrede", "…"], …],
     "model_ko": ["모범 답안 문단별 한국어 번역", …],   # model.text를 \n\n로 나눈 문단 수와 같게
     "redemittel": [["독일어 표현", "한국어 뜻"], …]},
    {"letter": "B", …}
  ],
  "criteria": [["I", "…", "설명"], ["II", "…", "설명"], ["III", "…", "설명"]],  # guide-data.json 기준
  "criteria_note": "배점과 0점 조건을 한 문장으로(guide-data.json 기준)"
}
```

- **SPRECHEN**은 B2 시험 구성에 맞춥니다. 형식:

```python
SPRECHEN = {
  "names": ["Teil 1 이름(PDF 그대로)", "Teil 2 이름", "Teil 3 이름"],
  "head": "약 15분, 두 사람이 함께",            # PDF 기준으로
  "note": "말하기 모범 예시는 PDF 23쪽에 있습니다.",
  "t1": {"task": "과제 설명", "points": ["요령", …], "redemittel": [["독일어", "한국어"], …]},
  "t2": {"task": "…", "a": "A 자료 요약(있으면)", "b": "B 자료 요약(있으면)", "a_label": "A의 자료", "b_label": "B의 자료",
         "steps": [["단계 이름(독일어)", "설명"], …],   # 있으면
         "points": [...], "redemittel": [...]},
  "t3": {"task": "…", "points": [...], "redemittel": [...]}
}
```
  `a`, `b`, `steps`, `points`는 없으면 빼도 됩니다. Teil마다 `redemittel`은 꼭 넣습니다.

## 확인

```
cd telc-b2
python3 -I digital-src/erklaerung/build.py . N <PretendardVariable.ttf> /tmp/check.html
```
빌드는 정답, Lesen 인용, Hören 문장, SB 문장 속 정답 단어, 모범 답안 문단 수를 검사합니다. Hören 인용은 PDF 대본과 대조합니다(글자층이 있으니 스크립트로 확인할 수 있습니다).
