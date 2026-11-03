# erklaerung (telc B2)

Modelltest별 해설 페이지(`telc B2 Modelltest N 해설.html`)의 원본입니다. Modelltest 1–7이 있습니다.

`build.py`와 `style.css`는 `telc-b1/digital-src/erklaerung/`와 같은 파일입니다(B1·B2 공용, 앱 폴더 이름으로 레벨을 구별). 한쪽을 고치면 다른 쪽에도 복사합니다. 데이터 형식은 이 폴더의 `FORMAT.md`(B2에서 달라지는 점)와 `telc-b1/digital-src/erklaerung/FORMAT.md`(기본 형식)에 있습니다.

## 다시 만들기

이 앱 폴더(`telc-b2/`)에서 실행합니다. Pretendard 원본(`PretendardVariable.ttf`)이 필요합니다.

```
for n in 1 2 3 4 5 6 7; do python3 -I digital-src/erklaerung/build.py . $n PretendardVariable.ttf "telc B2 Modelltest $n 해설.html" web; done
```

`index.html`은 손으로 관리하는 파일입니다. 시험 페이지마다 Lösungsschlüssel 버튼 앞에 「해설」 버튼(`telc%20B2%20Modelltest%20N%20%ED%95%B4%EC%84%A4.html`)이 들어 있습니다.
