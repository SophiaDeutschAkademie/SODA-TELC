# telc Deutsch B2 디지털 시험 (digital.html)

- `data/mt1–7.json`: 문제 데이터 (PDF에서 옮긴 것, 정답은 Lösungsschlüssel S. 20과 대조). 형식은 `SCHEMA.md`.
- `template.html`: 시험 화면 (HTML/CSS/JS 한 파일). `build-digital.py`가 데이터·로고·글꼴을 넣어 이 앱 폴더에 `digital.html`을 만듭니다.
- 검사: `python3 digital-src/validate.py 1 2 3 4 5 6 7`
- 빌드: `python3 digital-src/build-digital.py`
- `guidelib.py`, `build-guide.py`, `build-sprechen.py`: 쓰기·말하기 시험 대비 가이드(`schreiben-guide.html`, `sprechen-guide.html`)를 만듭니다. 글은 `guide-data.json`, `sprechen-data.json`에 있고, 모범 답안(본문 150~185단어)과 모범 대화의 단어 수가 범위를 벗어나면 빌드가 멈춥니다.
- 가이드 빌드: `python3 -I digital-src/build-guide.py`, `python3 -I digital-src/build-sprechen.py`
- 응시 방식 화면의 가이드 카드 두 장은 `index.html`에 직접 넣었습니다(이 폴더에는 `index.html`을 만드는 스크립트가 없습니다).
- 글꼴(Pretendard, OFL)은 `make-font.py`로 부분 추출합니다.
- 명령은 이 앱 폴더(`telc-b2/`)에서 실행합니다. 파일을 다시 만들 때마다 `../tools/soda-theme.py`가 Lehrwerk 공통 다크 모드 스위치를 자동으로 넣습니다.

공식 DIGItelc 화면의 복제가 아니라, 공개된 정보(좌우 분할, 컴퓨터 입력, 형광펜, 단어 수 표시 등)에 맞춘 연습용 화면입니다.
