# digital-src

디지털 시험 화면(`digital.html`)과 목록 페이지(`index.html`)의 원본입니다. 학생은 이 폴더를 쓰지 않습니다.

| 파일 | 내용 |
|---|---|
| `template.html` | 시험 화면 코드. 모든 Modelltest가 함께 씁니다. 직접 고치지 않고 `make_template.py`로 만듭니다 |
| `b2.template.html` | telc B2 시험 화면 원본(변경 없는 복사본). `make_template.py`의 입력입니다 |
| `make_template.py` | `b2.template.html`에서 B1용 `template.html`을 만듭니다(Lesen·Hören·Schreiben 구성, 점수, 이메일 한 통, 단어 수 제한 없음) |
| `data/mtN.json` | Modelltest N의 지문, 문항, 정답, 쓰기 과제, 모범 답안, 목록 페이지용 `index` 블록. 형식은 `SCHEMA.md` |
| `build-digital.py` | `data`와 `template.html`을 합쳐 이 앱 폴더의 `digital.html`을 만듭니다. 음원 길이는 이 폴더의 MP3에서 읽어 Hören 시간(올림한 분 + 2분)을 정합니다 |
| `build-index.py` | `data`, PDF, MP3로 이 앱 폴더의 `index.html`(표지·응시 방식·목록·시험별 페이지)을 만듭니다 |
| `guidelib.py`, `build-guide.py`, `build-sprechen.py` | 쓰기·말하기 시험 대비 가이드(`schreiben-guide.html`, `sprechen-guide.html`)를 만듭니다. 글은 `guide-data.json`, `sprechen-data.json`에 있고, 모범 답안·대화의 단어 수가 범위를 벗어나면 빌드가 멈춥니다 |
| `index-style.css` | `index.html`의 스타일 |
| `validate.py` | `data/mtN.json` 형식 검사. PDF에 글자층이 있으면 정답 40개를 Lösungsschlüssel와 대조하고 본문 누락을 찾습니다 |
| `logo-small.png`, `logo-index.png` | 시험 화면, 목록 페이지의 로고 |
| `fonts/pretendard-soda.woff`, `fonts/pretendard-index.woff` | Pretendard 중 시험 화면, 목록 페이지에 쓰는 글자만 담은 파일(SIL OFL 1.1) |
| `make-font.py` | 시험 화면에 새 한글 문구를 넣어 글자가 빠지면 Pretendard 원본에서 글꼴 파일을 다시 만듭니다 |

## 다시 만들기

```
python3 digital-src/make_template.py       # template.html을 고쳤을 때만 (b2.template.html에서 다시 만듭니다)
python3 digital-src/validate.py 1 2 3 4 5
python3 digital-src/build-digital.py
python3 digital-src/build-index.py
python3 -I digital-src/build-guide.py      # 쓰기 가이드
python3 -I digital-src/build-sprechen.py   # 말하기 가이드
```

`ffprobe`(ffmpeg)와 `pdftotext`(poppler)가 필요합니다. 명령은 이 앱 폴더(`telc-b1/`)에서 실행합니다. 파일을 다시 만들 때마다 `../tools/soda-theme.py`가 Lehrwerk 공통 다크 모드 스위치를 자동으로 넣습니다.

## 새 Modelltest 추가

1. 이 앱 폴더에 `telc B1 Modelltest N.pdf`와 `telc B1 Modelltest N.1.mp3` ~ `N.3.mp3`를 올립니다.
2. `SCHEMA.md` 형식으로 `data/mtN.json`을 만들고 `validate.py`로 확인합니다. 정답은 PDF 19쪽의 Lösungsschlüssel과 대조합니다.
3. `build-digital.py`, `build-index.py`를 차례로 실행합니다.

시험 화면 주소는 `digital.html#N-lesen`, `digital.html#N-hoeren`, `digital.html#N-schreiben`입니다. 학생의 답과 결과는 학생 브라우저에만 저장됩니다(키 접두어 `sodaTelcB1.v1.`).

PDF 쪽 번호(Lösungsschlüssel 19, Musterlösung 20, Hörtexte 22, Kommentar 24)는 `build-digital.py`의 `PAGES`와 `build-index.py`의 `PDF_PAGES`에 있습니다. 쪽 구성이 다른 시험을 추가하면 `build-digital.py`의 `PAGES_OVERRIDE`에 그 시험 번호만 따로 적습니다.

## 시험 구성(telc Deutsch B1)

| 모듈 | 시간 | 구성 | 점수 |
|---|---|---|---|
| Lesen + Sprachbausteine | 90분 | Teil 1 제목 연결 1–5, Teil 2 기사 선택 6–10, Teil 3 광고 연결 11–20(해당 없음 x), Sprachbausteine 1 선택 21–30, Sprachbausteine 2 단어 상자 31–40 | Teil 1·2 문항당 5점, Teil 3 문항당 2,5점, Sprachbausteine 문항당 1,5점(최대 105점) |
| Hören | 약 20–30분(음원 길이로 계산) | Teil 1 짧은 글 5개 41–45(1회), Teil 2 대화 46–55(2회), Teil 3 짧은 글 5개 56–60(2회), 모두 richtig/falsch | Teil 1·3 문항당 5점, Teil 2 문항당 2,5점(최대 75점) |
| Schreiben | 30분 | 이메일 한 통 답장, Leitpunkt 4개. 최소 단어 수는 시험지에 없음 | 45점(선생님 채점) |
| Sprechen | 약 15분 | 디지털 화면에는 넣지 않음. PDF 15–18쪽 | 75점 |

필기(Lesen·Hören·Schreiben) 합격선은 60 %(225점 중 135점)입니다. 디지털 화면은 Lesen과 Hören을 자동 채점하고 Schreiben은 모범 답안과 Leitpunkt 해설을 보여 줍니다.

## 데이터를 만든 방법

- Modelltest 1–4의 PDF에는 글자층이 없습니다(글자가 윤곽선 도형). 글자 모양을 맞춰 읽고 사전으로 고친 뒤 tesseract OCR과 대조해 오류를 잡았고, 광고 상자는 사람이 직접 옮겨 적었습니다. 정답은 Lösungsschlüssel 쪽(19쪽)의 이미지와 눈으로 대조했습니다. 이 네 시험은 `validate.py`가 PDF와의 자동 대조를 건너뜁니다.
- Modelltest 5의 PDF에는 글자층이 있어 `validate.py`가 정답과 본문을 PDF와 자동으로 대조합니다.
- Hören 시간은 시험지에 적혀 있지 않아 음원 길이에서 계산합니다.
