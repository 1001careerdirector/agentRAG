"""쿼리 재작성 함수 — 검색어를 재작성한다."""
from agentic_rag.ports import LLM


REWRITE_SYSTEM_PROMPT_BASE = (
    "사용자의 원래 질문을 다시 표현하여 검색 엔진에 더 적합한 검색어로 변환하세요.\n"
    "검색어는 간결하고 핵심 키워드 위주여야 합니다.\n"
    "한 줄의 검색어만 출력하세요."
)


def rewrite_query(llm: LLM, question: str, tried: list[str]) -> str:
    """검색어를 재작성한다.
    
    Args:
        llm: 언어 모델
        question: 원래 질문
        tried: 이전에 시도한 검색어 리스트 (새로 시도할 검색어를 피하기 위해)
        
    Returns:
        재작성된 검색어 (공백 제거됨)
    """
    system_prompt = REWRITE_SYSTEM_PROMPT_BASE
    
    # tried 가 있으면 프롬프트에 포함
    if tried:
        tried_str = "\n".join(f"- {q}" for q in tried)
        system_prompt += (
            f"\n\n이전에 시도한 검색어들 (피해야 함):\n{tried_str}"
        )
    
    user_prompt = f"원래 질문: {question}"
    raw = llm.generate(system_prompt, user_prompt).strip()
    return raw
