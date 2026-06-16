---
agent: agent
description: 포트의 실제 SDK 구현(OpenAI/Pinecone) — 단위 테스트 제외
---
# /p5-adapters — 어댑터(실 SDK)

전역 지침과 `#file:.github/instructions/adapters.instructions.md` 를 따른다. 단위 테스트 대상이 아니다(코어와 분리 유지).

## 요구사항 + 인수 기준
- `adapters/openai_llm.py`: `LLM` 포트 구현. ChatOpenAI(model=config.MODEL_NAME) 래핑, generate(system,user)=System/Human 메시지 호출 후 `.content`.
- `adapters/pinecone_store.py`: `Retriever`/`Reranker` 포트 구현.
  - PineconeVectorStore(namespace=config.NAMESPACE) + PineconeEmbeddings("multilingual-e5-large") 로 search.
  - PineconeRerank("bge-reranker-v2-m3", top_n) 로 rerank. LangChain Document → `Doc` 변환.
- 키는 `.env` 로드. 하드코딩 금지.

## 완료 판정
- [ ] 두 어댑터가 포트 시그니처와 정확히 일치(타입 체크/간단한 임포트 확인).
- [ ] 코어 모듈에는 여전히 SDK 직접 import 가 없다.

## 진행 방식
시그니처 일치를 먼저 확인하고 최소 구현. 실제 호출 검증은 scripts 단계에서.
