# telc Deutsch B2 작문 연습 — 모든 Modelltest가 함께 쓰는 글
# 글 속의 «…»는 독일어 조각입니다(빌드가 <b lang="de">로 바꿉니다).

LEAD = "B1 수준의 답안을 주어진 B2 표현으로 고쳐 씁니다 · Schriftlicher Ausdruck Aufgabe A·B"

STEPS = [
    ["과제와 B1 답안 읽기",
     "B1 답안에는 Leitpunkt 세 개의 내용이 다 들어 있습니다. 다만 짧은 문장을 늘어놓았고, 질문과 요구가 직접적이며 쉬운 낱말만 씁니다."],
    ["주어진 표현으로 고쳐 쓰기",
     "번호마다 B1 문장과 쓸 표현, 도움말이 있습니다. 그 표현을 넣어 B1 문장을 B2 문장으로 다시 씁니다. 쓴 내용은 이 브라우저에 저절로 저장됩니다."],
    ["예시와 비교하기",
     "다 쓴 뒤 「예시 보기」를 눌러 B2 예시와 비교합니다. 예시는 답의 한 가지일 뿐입니다. 주어진 표현을 맞게 썼다면 다르게 써도 됩니다."],
    ["글 전체 확인하기",
     "「내 글 전체」에서 고쳐 쓴 문장이 이어진 편지와 단어 수를 확인합니다. 소피아 독일어학원 수강생은 맨 아래에서 선생님께 제출할 수 있습니다."],
]

DIFF_TITLE = "B1 답안과 B2 답안은 이렇게 다릅니다"
DIFF = [
    ["문장 잇기", "짧은 문장을 마침표로 늘어놓습니다. «Ich brauche einen Führerschein. Ich muss jeden Tag Kunden besuchen.»",
     "관계문과 da, während, sodass로 묶어 한 문장에 담습니다. «… eine Stelle, für die ich einen Führerschein benötige, da …»"],
    ["질문", "그대로 묻습니다. «Was kostet der Kurs?»",
     "간접 의문문과 접속법 2식으로 묻습니다. «Könnten Sie mir mitteilen, mit welchen Kosten ich rechnen muss?»"],
    ["요구", "«Ich möchte das Geld zurück.»",
     "«Ich bestehe darauf, dass … / Ich erwarte, dass … / Sorgen Sie bitte dafür, dass …»"],
    ["낱말", "brauchen, machen, bekommen, sagen",
     "benötigen, eine Prüfung ablegen, einen Vertrag abschließen, mitteilen, Auskunft geben"],
    ["문법", "능동문, 현재형과 현재완료",
     "수동태(… übersetzt werden), 접속법 1식과 2식(laufe, hätte, wäre), 과거완료"],
    ["Betreff", "«Betreff: Kurs»", "«Betreff: Bitte um Informationen zu Ihrem Intensivkurs»"],
]
DIFF_NOTE = ("이 차이는 채점 기준 II Kommunikative Gestaltung(편지 형식, Sie 말투, 문장 연결, 접속법 2식)과 "
             "III Formale Richtigkeit(문장 구조와 어형)에 그대로 나타납니다. "
             "같은 내용이라도 문장을 잇고 격식 있는 표현을 쓰면 B2 답안이 됩니다.")

# 과제마다 맨 위에 붙는 짧은 안내(과제 종류는 mtN.json의 kind)
KIND = "격식 있는 E-Mail · Sie"

# 내 글 전체 아래의 제출 전 확인
CHECK = {
    "Bitte um Informationen": [
        "Betreff에 무엇을 묻는 편지인지 썼습니까?",
        "도입에서 광고를 어디에서 보았는지, 왜 쓰는지 밝혔습니까?",
        "고른 Leitpunkt 세 개를 빠짐없이, 한 문단에 하나씩 썼습니까?",
        "질문을 간접 의문문(ob …, wie …)이나 접속법 2식(Könnten Sie …?)으로 썼습니까?",
        "«Sie, Ihnen, Ihr»를 대문자로 쓰고, 부문장의 동사를 맨 끝에 두었습니까?",
        "호칭부터 맺음 문장까지 150단어 이상입니까?",
    ],
    "Beschwerde": [
        "Betreff에 무엇이 문제인지 썼습니까?",
        "도입에서 무엇을 언제 신청했는지(샀는지) 밝혔습니까?",
        "고른 Leitpunkt 세 개를 빠짐없이, 한 문단에 하나씩 썼습니까?",
        "화를 내기보다 날짜, 금액, 광고의 약속을 근거로 썼습니까?",
        "무엇을 원하는지(환불, 보상, 확인)와 기한을 분명히 썼습니까?",
        "호칭부터 맺음 문장까지 150단어 이상입니까?",
    ],
}

# 내 글 전체와 예시의 단어 수 기준(쓰기 가이드와 같음): 호칭부터 맺음 문장까지의 본문.
# Betreff, 끝인사(Mit freundlichen Grüßen), 이름은 세지 않습니다.
RANGE = (150, 185)
COUNT_NOTE = "호칭부터 맺음 문장까지 · Betreff, 끝인사, 이름은 세지 않습니다"

SUBMIT_TITLE = "선생님께 제출하기"
SUBMIT_TAG = "소피아 독일어학원 수강생 전용"
SUBMIT_TEXT = [
    "이 제출하기는 <b>소피아 독일어학원 수강생 전용</b>입니다. 수강생이 아니라면 제출하지 말고 「전체 복사」나 「txt 저장」으로 글을 보관하십시오.",
    "제출하면 Aufgabe A·B에서 고쳐 쓴 문장과 완성한 편지가 선생님 메일로 전송됩니다. 선생님이 확인한 뒤 알려 드립니다. 제출 전에 이름을 확인하십시오.",
]
