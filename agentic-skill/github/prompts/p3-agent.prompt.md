---
agent: agent
description: 통합 그래프(분기+조립)와 Naive 베이스라인을 TDD로 구현
---
# /p3-agent — 통합 그래프 & Naive

전역 지침과 `#file:.github/skills/tdd/SKILL.md` 를 따른다.

## 요구사항 + 인수 기준
- 순수 분기 함수(`graph.after_docs`, `graph.after_answer`):
  - after_docs: relevant→"generate"; 아니면 retries<MAX_RETRIES→"rewrite", 상한도달→"generate".
  - after_answer: grounded→END, 아니면 "regenerate".
- `graph.build_agent(deps)`: LangGraph StateGraph 조립. 노드들은 deps(포트 묶음)를 주입받는다.
  - 통합 흐름을 **가짜 의존성**으로 end-to-end 검증:
    - 인사 → direct 경로(검색 노드 미경유).
    - 관련 문서 있음 → 한 번에 generate, retries==0.
    - 관련성 반복 False → rewrite 루프가 돌고 retries 가 상한에서 멈춘 뒤 generate(근거없음)로 종료.
- `naive.naive_rag(llm, retriever, question, k=3) -> {"answer","context"}`: 한 번 검색→바로 답(라우팅·재순위·평가 없음); context 에 `[title] text` 포함.

## 완료 판정
- [ ] 위 세 경로가 가짜 의존성으로 테스트되고 `uv run pytest -q` 초록.

## 진행 방식
순수 분기 함수를 먼저 RED→GREEN 으로 끝내고, 그다음 통합 흐름을 시나리오별로. 전부 초록까지 반복하라.
