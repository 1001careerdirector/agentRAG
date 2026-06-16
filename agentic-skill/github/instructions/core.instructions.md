---
description: 코어 모듈 규칙 — 포트만 의존, 순수 함수, SDK 직접 import 금지
applyTo: "src/agentic_rag/**"
---
# 파일마다 적용되는 지침
# 코어 모듈 규칙
- 이 패키지의 코어 모듈은 `ports.py` 의 Protocol(LLM/Retriever/Reranker)만 의존한다.
- `langchain`, `pinecone`, `openai` 를 **직접 import 하지 않는다**. 외부 호출은 주입받은 포트로만.
  (예외: `adapters/` 디렉터리는 `adapters.instructions.md` 의 규칙을 따른다.)
- 작은 순수 함수 우선. 부수효과는 어댑터로 밀어낸다. 타입 힌트 필수, 한국어 docstring.
- LLM이 만든 텍스트(라우팅 라벨, yes/no, 점수)는 방어적으로 파싱·검증하고 안전한 기본값으로 폴백.
- 상수는 `config.py`. 매직 값 금지.
