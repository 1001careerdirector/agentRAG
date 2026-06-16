---
agent: agent
description: 순수 파이프라인 함수(라우팅·재작성·검색·채점·생성)를 TDD로 구현
---
# /p2-pipeline — 코어 파이프라인 함수

전역 지침과 `#file:.github/skills/tdd/SKILL.md` 를 따른다. 모든 함수는 포트를 주입받는 순수 함수다. 각 함수마다 RED→GREEN→REFACTOR.

## 요구사항 + 인수 기준 (함수별)
- `router.classify(llm, question) -> "search"|"direct"`: 정책질문→search, 인사→direct, 허용값 밖 출력→search 폴백, 공백/대소문자 정규화.
- `rewrite.rewrite_query(llm, question, tried) -> str`: 출력 strip; `tried` 가 있으면 그 검색어들이 프롬프트에 포함(FakeLLM.calls 검증).
- `retrieval.retrieve_reranked(retriever, reranker, query, fetch_k, top_n)`: search→rerank; 빈 검색결과면 `[]`(재순위 호출 안 함); 재정렬 순서 반영.
- `grading.grade_docs / grade_answer -> bool`: yes/no(true/false) 파싱; 애매한 출력은 False 폴백.
- `generation.generate_answer(llm, question, context, docs_relevant) -> str`: docs_relevant=True면 인용 표기 지시 포함; False면 '찾지 못했습니다' 지시 포함 + 인용 표기 지시 제외(FakeLLM.calls 로 프롬프트 분기 검증).

## 완료 판정
- [ ] 위 동작과 경계 케이스가 각각 테스트로 존재하고 `uv run pytest -q` 초록.
- [ ] 코어가 langchain/pinecone/openai 를 직접 import 하지 않음.

## 진행 방식
함수 하나씩 RED를 먼저 보여주고, 통과 후 다음으로. 전부 초록일 때까지 반복하라.
