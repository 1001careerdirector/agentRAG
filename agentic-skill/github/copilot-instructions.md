# Copilot 전역 지침 — 한국어 Agentic RAG (Test-First TDD)
# 프로젝트 전반에 걸쳐 항상 적용되는 표준과 절차. 구현 방법은 `.github/prompts/*.prompt.md` 의 요구사항·인수 기준을 따른다.
# write owned by: @PL, @JH, @JS (공동 작성)

이 저장소는 LangGraph 1.x + LangChain 1.x + Pinecone 기반의 한국어 Agentic RAG 에이전트를
**테스트 우선 TDD**로 구현한다. 아래는 "어떻게"(항상 적용되는 표준)이며, "무엇을 만들지"(요구사항·인수 기준)는
`.github/prompts/*.prompt.md` 로 받는다.

## 스택 · 실행
- Python 3.12, 패키지/실행은 **uv** (`uv add`, `uv run`). 테스트: pytest, pytest-cov.
- langgraph, langchain, langchain-openai, langchain-pinecone, pinecone, python-dotenv.
- 주석·docstring·문서는 한국어. 식별자는 영어.

## 절대 원칙 — Test-First TDD
1. 실패하는 테스트를 먼저(RED) → 최소 구현(GREEN) → 리팩터(REFACTOR). 구현이 테스트보다 앞서지 않는다.
2. 한 사이클 = 하나의 작은 동작. 절차는 `.github/skills/tdd/SKILL.md` 를 따른다.
3. 작업 시작 시 "어떤 실패 테스트부터?"를 먼저 정하고, RED를 보여준 뒤 진행한다.

## 아키텍처 — 포트 & 어댑터
- 외부 의존성(LLM/임베딩/벡터스토어/재순위)은 `src/agentic_rag/ports.py` 의 Protocol 뒤에 둔다.
- 코어 모듈은 포트를 **의존성 주입**으로 받고 langchain/pinecone/openai 를 **직접 import 하지 않는다**.
  (예외: `src/agentic_rag/adapters/` 만 실제 SDK 사용 — 경로별 지침 참조)
- 덕분에 코어 전체를 **API 키 없이** 가짜 의존성으로 테스트한다.

## 폴더 구조 (src 레이아웃)
```
src/agentic_rag/  config.py models.py ports.py router.py rewrite.py retrieval.py
                  grading.py generation.py graph.py naive.py evaluation.py
                  adapters/{openai_llm.py, pinecone_store.py}
tests/   conftest.py(FakeLLM/FakeRetriever/FakeReranker) + test_*.py
eval/    eval_set.py(멀티-문서 질문 + must 라벨)
scripts/ index_corpus.py  run_demo.py
```

## 완료 기준 (Definition of Done) — 모든 작업 공통
- 새 동작마다 테스트가 있고 `uv run pytest -q` 가 **전부 초록**.
- 코어 모듈은 외부 SDK를 직접 import 하지 않는다(포트만 의존).
- 경계/예외가 테스트로 덮인다: 빈 검색결과 · 잘못된 라벨 · 재시도 상한 · 직답(direct) 경로 · 근거없음 시 인용 미표기.
- 매직 값은 `config.py` 로. 키는 `.env`(절대 하드코딩 금지).

## 에이전트 모드 사용 규칙
- 프롬프트 파일(`/p1`~`/p6`)은 **요구사항 + 인수 기준**만 준다. 구현 방법은 위 표준을 따라 **스스로** 정한다.
- 인수 기준이 모두 충족되고 테스트가 초록일 때까지 RED→GREEN→REFACTOR 를 **반복**한다.
- 각 사이클의 RED를 먼저 보여주고, 통과를 확인한 뒤 다음 동작으로 넘어간다.
- 프롬프트 파일(`/p1`~`/p6`)을 실행해서 완료 판정 항목이 완료된 경우 [ ]를 체크한다.
