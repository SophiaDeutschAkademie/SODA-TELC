# 작문 연습 데이터 형식 — telc Deutsch B2 (swN.py)

`sw1.py`(Modelltest I)가 기준 예시입니다. 같은 키, 같은 분량과 어조로 씁니다.

```python
AUFGABEN = [
  {"ko": "과제 요약(합니다체, 한두 문장)",                       # Aufgabe A · Bitte um Informationen
   "parts": [
     {"role": "Betreff", "short": True,                        # 한 줄 칸. 단어 수에 넣지 않습니다
      "b1": "Betreff: Frage",
      "use": "Betreff: Anfrage zu …",                           # 쓸 B2 표현
      "use_ko": "…에 관한 문의",                                # 표현의 뜻(합니다체나 명사구)
      "tip": "도움말(합니다체). 독일어 조각은 «…»로 감쌉니다.",
      "b2": "Betreff: {Anfrage zum} Hausnotruf für meine Großmutter"},   # {…}는 강조
     {"fix": "Sehr geehrte Damen und Herren,"},                 # 고치지 않는 줄(호칭)
     {"role": "도입", "b1": "ich habe …", …},                    # 호칭 다음 줄은 소문자로 시작
     {"role": "Leitpunkt 1", …},                                # 같은 Leitpunkt가 이어지면 한 문단
     {"role": "Leitpunkt 1", …},
     {"role": "Leitpunkt 2", …},
     …,
     {"role": "마무리", …},
     {"fix": "Mit freundlichen Grüßen\nMinji Park"}],          # 끝인사와 이름. 단어 수에 넣지 않습니다
   "sum": ["B1 → B2에서 바뀐 점(합니다체)", …]},              # 네 줄
  {…},                                                          # Aufgabe B · Beschwerde
]
```

## 짜는 법

- 번호는 Betreff, 도입, Leitpunkt 칸들, 마무리 순서로 일곱~아홉 개입니다. 번호 하나에 주어진 표현 하나를 씁니다.
- 시험의 a) 방식처럼 Leitpunkt 네 개 가운데 세 개를 고르고, Leitpunkt마다 칸 한두 개를 씁니다. 빌드가 세 개인지, 차례대로인지 확인합니다. 과제 상자에서 이 세 개에 「이 답안」 표시가 붙습니다.
- B1 답안에는 고른 Leitpunkt의 내용이 모두 들어 있어야 합니다. 문법은 맞게, 문장은 짧게, 질문은 직접(Was kostet …?), 요구는 단순하게(Ich möchte das Geld zurück.), 낱말은 brauchen·machen·bekommen처럼 쉽게 씁니다. 호칭과 끝인사는 B2와 같은 격식 있는 말입니다.
- B2 예시는 B1 문장에 주어진 표현을 넣어 고친 문장입니다. 내용은 B1 답안과 같게 두고, 작은 보충만 합니다. 표현이 들어간 자리를 `{…}`로 감쌉니다.
- 광고와 과제의 사실(기간, 금액, 약속)과 어긋나지 않게 씁니다. 해설 페이지의 모범 답안과 같은 문장이 되지 않게 합니다.
- B2 예시의 본문(호칭부터 맺음 문장까지, Betreff·끝인사·이름 제외)은 150–185단어입니다. B1 답안은 그보다 짧게(대개 110–135단어) 씁니다. 빌드가 확인합니다.
- 호칭 뒤 다음 줄은 소문자로 시작합니다(명사와 Sie·Ihr는 대문자). 빌드가 확인합니다.
- 회차마다 표현이 겹치지 않게 고릅니다. 다섯 회차를 합쳐 관계문(전치사 + 관계대명사), 간접 의문문, 수동태(화법조동사, 과거완료), 접속법 1식(간접 화법)과 2식, 명사-동사 결합(in Anspruch nehmen, Auskunft geben), 2격 전치사(aufgrund, bezüglich, trotz), 격식 있는 요구와 맺음 표현이 고루 나오게 합니다.

## 쓰는 말

- 한국어는 **합니다체**입니다. 반말과 ‘~다’ 체는 쓰지 않습니다(빌드가 `ko`, `tip`, `use_ko`, `sum`을 확인합니다). 도움말 안의 뜻풀이는 ‘…을 예상하다’처럼 따옴표 안에서만 사전형을 씁니다.
- 문법 용어는 한국어로: 부문장, 관계대명사, 관계문, 간접 의문문, 접속법 1식·2식, 분리동사, 화법조동사, 2격, 3격, 4격, 수동태, 과거완료, 명사-동사 결합. 현재완료의 haben/sein은 ‘조동사’라고 부르지 않습니다(‘sein과 함께 완료형을 만듭니다’).
- 독일어 조각 뒤의 조사는 한국어로 읽은 소리에 맞춥니다: dass(다스)로, während(베렌트)는, wenn(벤)으로. 헷갈리면 «…» 뒤에 한국어 낱말을 두거나 괄호로 씁니다.
- ‘von Beruf’ 표현은 쓰지 않습니다.
