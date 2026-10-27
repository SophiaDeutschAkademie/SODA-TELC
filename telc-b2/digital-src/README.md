# telc Deutsch B2 디지털 시험 (digital.html)

- `data/mt1–6.json`: 문제 데이터 (PDF에서 옮긴 것, 정답은 Lösungsschlüssel S. 20과 대조). 형식은 `SCHEMA.md`.
- `template.html`: 시험 화면 (HTML/CSS/JS 한 파일). `build-digital.py`가 데이터·로고·글꼴을 넣어 이 앱 폴더에 `digital.html`을 만듭니다.
- 검사: `python3 digital-src/validate.py 1 2 3 4 5 6`
- 빌드: `python3 digital-src/build-digital.py`
- 글꼴(Pretendard, OFL)은 `make-font.py`로 부분 추출합니다.
- 명령은 이 앱 폴더(`telc-b2/`)에서 실행합니다. 파일을 다시 만들 때마다 `../tools/soda-theme.py`가 Lehrwerk 공통 다크 모드 스위치를 자동으로 넣습니다.

공식 DIGItelc 화면의 복제가 아니라, 공개된 정보(좌우 분할, 컴퓨터 입력, 형광펜, 단어 수 표시 등)에 맞춘 연습용 화면입니다.
