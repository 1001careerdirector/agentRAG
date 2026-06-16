---
description: 어댑터 규칙 — 실제 SDK 허용, 단위 테스트 제외, .env 키
applyTo: "src/agentic_rag/adapters/**"
---
# 파일마다 적용되는 지침
# 어댑터 규칙
- 여기서만 실제 SDK(langchain-openai, langchain-pinecone, pinecone) import 를 허용한다.
- 각 어댑터는 `ports.py` 의 Protocol 시그니처를 **정확히** 구현한다(LLM.generate / Retriever.search / Reranker.rerank).
- LangChain Document → 코어의 `Doc` 로 변환해 반환한다(코어가 SDK 타입에 노출되지 않게).
- 키는 `.env`(python-dotenv)에서 로드. **하드코딩 금지.**
- 어댑터는 단위 테스트 대상이 아니다(통합 스모크는 scripts 로).
