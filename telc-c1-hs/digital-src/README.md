# digital-src

디지털 시험 화면(`digital.html`)과 목록 페이지(`index.html`)의 원본입니다. 학생은 이 폴더를 쓰지 않습니다.

| 파일 | 내용 |
|---|---|
| `template.html` | 시험 화면 코드. 모든 Modelltest가 함께 씁니다. 이 파일을 직접 고칩니다(telc B1 화면에서 출발해 C1 Hochschule용으로 바꾼 최종본) |
| `data/mtN.json` | Modelltest N의 지문, 문항, 정답, 쓰기 과제, 모범 답안, 구술 과제, 목록 페이지용 `index` 블록. 형식은 `SCHEMA.md` |
| `build-digital.py` | `data`와 `template.html`을 합쳐 이 앱 폴더의 `digital.html`을 만듭니다. 음원 길이는 이 폴더의 MP3에서 읽습니다 |
| `build-index.py` | `data`, PDF, MP3로 이 앱 폴더의 `index.html`(표지·응시 방식·목록·시험별 페이지)을 만듭니다 |
| `index-style.css` | `index.html`의 스타일 |
| `validate.py` | `data/mtN.json` 형식 검사. 정답 64개를 PDF 20쪽 Lösungsschlüssel과 대조하고 본문이 PDF에 모두 있는지 찾습니다 |
| `logo-small.png`, `logo-index.png` | 시험 화면, 목록 페이지의 로고 |
| `fonts/pretendard-soda.woff`, `fonts/pretendard-index.woff` | Pretendard 중 시험 화면, 목록 페이지에 쓰는 글자만 담은 파일(SIL OFL 1.1) |
| `make-font.py` | 시험 화면에 새 한글 문구를 넣어 글자가 빠지면 Pretendard 원본에서 글꼴 파일을 다시 만듭니다 |

## 다시 만들기

```
python3 digital-src/validate.py 1 2 3 4 5
python3 digital-src/build-digital.py
python3 digital-src/build-index.py
```

`ffprobe`(ffmpeg)와 `pdftotext`·`pdfinfo`(poppler)가 필요합니다. 명령은 이 앱 폴더(`telc-c1-hs/`)에서 실행합니다. 파일을 다시 만들 때마다 `../tools/soda-theme.py`가 Lehrwerk 공통 다크 모드 스위치를 자동으로 넣습니다.

## 새 Modelltest 추가

1. 이 앱 폴더에 `telc C1 HS Modelltest N.pdf`와 `telc C1 HS Modelltest N.1.mp3` ~ `N.3.mp3`를 올립니다.
2. `SCHEMA.md` 형식으로 `data/mtN.json`을 만들고 `validate.py`로 확인합니다. 정답은 PDF 20쪽의 Lösungsschlüssel과 대조됩니다.
3. `build-digital.py`, `build-index.py`를 차례로 실행합니다.

시험 화면 주소는 `digital.html#N-lesen`, `digital.html#N-hoeren`, `digital.html#N-schreiben`입니다. 학생의 답과 결과는 학생 브라우저에만 저장됩니다(키 접두어 `sodaTelcC1HS.v1.`).

PDF 쪽 번호(Lösungsschlüssel 20, Musterlösung 21, Hörtexte 25, Kommentar 31)는 `build-digital.py`의 `PAGES`와 `build-index.py`의 `PDF_PAGES`에 있습니다. 쪽 구성이 다른 시험을 추가하면 `build-digital.py`의 `PAGES_OVERRIDE`에 그 시험 번호만 따로 적습니다.

## 시험 구성(telc Deutsch C1 Hochschule)

| 모듈 | 시간 | 구성 | 점수 |
|---|---|---|---|
| Lesen + Sprachbausteine | 90분 | Lesen 1 문장 넣기 1–6, Lesen 2 단락 찾기 7–12, Lesen 3 richtig/falsch/nicht im Text 13–23과 제목 고르기 24, Sprachbausteine 25–46(a–d) | Lesen 1·2·3 문항당 2점, Sprachbausteine 문항당 1점(최대 70점) |
| Hören | 40분(음원은 모두 한 번만, 약 35분) | Teil 1 여덟 명의 의견 47–54, Teil 2 라디오 방송 55–64(a/b/c), Teil 3 강연 메모 65–74(직접 쓰기) | Teil 1 문항당 1점, Teil 2·3 문항당 2점(최대 48점) |
| Schreiben | 70분 | 두 주제 중 하나를 골라 350단어 이상 | 48점(선생님 채점) |
| Sprechen | 약 16분 | 디지털 화면에는 넣지 않음. PDF 16–19쪽 | 48점 |

필기(Lesen·Hören·Schreiben) 만점은 166점이고 합격선은 60 %(99점)입니다. 디지털 화면은 Lesen과 Hören을 자동 채점하고, Hören Teil 3(메모)은 제출 뒤 학생이 정답 예시와 비교해 ✓/✗로 스스로 채점합니다(표시하지 않으면 0점). Schreiben은 정답 예시와 구성 힌트를 보여 줍니다.

## 데이터를 만든 방법

- 다섯 시험의 PDF 모두 글자층이 있어 `pdftotext`로 읽었습니다. `validate.py`가 정답 64개와 본문 전체를 PDF와 자동으로 대조합니다.
- Hören 시간은 시험지에 적힌 40분입니다. 음원이 더 길면 `build-digital.py`가 음원 길이 + 2분으로 늘립니다.
- 시험 화면의 한글 문구는 글꼴 파일에 들어 있는 글자만 씁니다. 새 문구를 넣을 때는 `make-font.py`로 글꼴을 다시 만들어야 하며, 원본 글꼴이 없으면 빠진 글자는 시스템 글꼴로 나옵니다(현재 ‘₂’ 한 글자).
