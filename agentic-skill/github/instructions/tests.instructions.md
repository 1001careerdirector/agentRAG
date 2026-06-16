---
description: 테스트 규칙 — 실제 API 금지, 가짜 주입, AAA, 경계 우선
applyTo: "tests/**"
---
# 파일마다 적용되는 지침
# 테스트 규칙
- **실제 OpenAI/Pinecone 를 호출하지 않는다.** `conftest.py` 의 FakeLLM/FakeRetriever/FakeReranker 를 주입한다.
- 결정적·빠름·독립적. 네트워크/시간/파일에 의존하지 않는다.
- 구조는 AAA(Arrange-Act-Assert). 이름은 `test_<대상>_<상황>_<기대결과>`(한국어 가능). 한 테스트는 하나만 검증.
- 경계/예외를 반드시 포함: 빈 검색결과 · 허용값 밖 라벨 · 재시도 상한 도달 · 직답 경로 · 근거없음 인용 미표기 · 0/1 점수.
- 프롬프트 분기는 반환값이 아니라 `FakeLLM.calls`(전달된 프롬프트)로 검증한다.
