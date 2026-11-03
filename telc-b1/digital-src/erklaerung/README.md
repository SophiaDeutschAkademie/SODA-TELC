# erklaerung

Modelltest별 해설 페이지(`telc B1 Modelltest N 해설.html`)의 원본입니다. 지금은 Modelltest 1만 있습니다.

| 파일 | 내용 |
|---|---|
| `erk1_lesen.py` | Modelltest 1 Lesen 1–20, Sprachbausteine 21–40 해설(근거 문장, 정답 이유, 함정, 어휘) |
| `erk1_hoeren.py` | Modelltest 1 Hören 41–60 해설, Schreiben·Sprechen 해설 |
| `style.css` | 해설 페이지 스타일(라이트·다크) |
| `build.py` | 위 데이터와 `../data/mt1.json`을 합쳐 HTML 한 파일을 만듭니다 |

## 다시 만들기

이 앱 폴더(`telc-b1/`)에서 실행합니다. Pretendard 원본(`PretendardVariable.ttf`, https://github.com/orioncactus/pretendard)이 필요합니다. 페이지에 쓰인 글자만 골라 파일 안에 넣습니다.

```
python3 -I digital-src/erklaerung/build.py . PretendardVariable.ttf "telc B1 Modelltest 1 해설.html" web
python3 digital-src/build-index.py
python3 ../tools/add-sprechen-links.py
python3 ../tools/add-paper-submit.py telc-b1
```

- 마지막 인자 `web`은 저장소용입니다. 오른쪽 위에 「Modelltest I」(시험 페이지로 돌아가기) 버튼과 접속 집계 태그를 넣습니다. 빼면 학생에게 파일로 주는 오프라인판이 됩니다.
- `build.py`는 만들기 전에 해설의 정답을 `mt1.json`의 정답과 대조하고, Lesen 근거 인용이 본문에 그대로 있는지, Hören 문장이 문제지와 같은지 확인합니다. 하나라도 다르면 멈춥니다.
- `build-index.py`는 앱 폴더에 `telc B1 Modelltest N 해설.html`이 있으면 그 시험 페이지의 Lösungsschlüssel 버튼 앞에 「해설」 버튼을 넣습니다.
