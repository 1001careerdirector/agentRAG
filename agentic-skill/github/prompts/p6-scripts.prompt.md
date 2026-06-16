---
agent: agent
description: 색인/데모 실행 스크립트(실키 필요)
---
# /p6-scripts — 실행 스크립트

전역 지침을 따른다. 실제 키가 필요한 통합 실행이다.

## 요구사항 + 인수 기준
- `scripts/index_corpus.py`: 한국어 코퍼스(누구나테크 핸드북)를 RecursiveCharacterTextSplitter(chunk_size=500)로 쪼개
  Pinecone `agentic-rag-lab` 의 `config.NAMESPACE`(chunk_500)에 색인. `describe_index_stats` 로 네임스페이스별 벡터 수 출력.
- `scripts/run_demo.py`: `.env` 로드 → 어댑터로 deps 구성 → `build_agent(deps)` 와 `naive_rag` 를 `eval_set` 질문으로 비교 실행
  → `evaluation.run_eval` 로 **completeness(통합 vs Naive)** 표 출력.
- 둘 다 `uv run python -m scripts.<이름>` 으로 동작. 실키 필요를 docstring 에 명시.

## 완료 판정
- [ ] `uv run python -m scripts.index_corpus` 가 네임스페이스별 색인 수를 출력.
- [ ] `uv run python -m scripts.run_demo` 가 완전성 비교 표를 출력(통합 ≥ Naive 경향).

## 진행 방식
색인 → 데모 순으로. 단위 테스트는 추가하지 말고(코어는 이미 초록), 통합 동작만 확인하라.
