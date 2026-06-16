---
agent: agent
description: 테스트 가능한 골격(설정·도메인 타입·포트·가짜)을 TDD로 구성
---
# /p1-foundation — 기반 골격

전역 지침과 `#file:.github/skills/tdd/SKILL.md` 를 따른다. 구현 방법은 스스로 정하되 아래 인수 기준을 모두 만족시켜라.

## 목표
키 없이 테스트 가능한 프로젝트 기반을 만든다.

## 요구사항 (무엇을)
- src 레이아웃 + pytest 설정(`pythonpath=["src"]`, `testpaths=["tests"]`).
- 도메인 타입: `Doc`(title, text, chunk=0), `State`(question, route, search_query, context, answer, retries, docs_relevant, grounded).
- 설정 상수: `NAMESPACE`, `MAX_RETRIES`, `FETCH_K`, `TOP_N`, `MODEL_NAME`.
- 포트(Protocol): `LLM.generate(system,user)->str`, `Retriever.search(query,k)->list[Doc]`, `Reranker.rerank(query,docs,top_n)->list[Doc]`.
- `tests/conftest.py`: FakeLLM/FakeRetriever/FakeReranker + sample_docs 픽스처.

## 인수 기준 (완료 판정)
- [ ] `uv run pytest -q` 가 초록(스모크 포함).
- [ ] `Doc` 기본값 `chunk==0`, config 상수값이 기대대로임을 테스트가 검증.
- [ ] conftest 의 가짜들이 import·주입 가능.

## 진행 방식
인수 기준이 모두 충족되고 테스트가 초록일 때까지 RED→GREEN→REFACTOR 를 반복하라. 각 사이클의 RED를 먼저 보여줘라.
