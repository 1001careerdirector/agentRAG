"""생성 함수 — 답변을 생성한다."""
from agentic_rag.ports import LLM


GENERATION_SYSTEM_PROMPT_BASE = (
    "사용자의 질문에 대해 명확하고 정확한 답변을 작성하세요."
)


def generate_answer(
    llm: LLM,
    question: str,
    context: str,
    docs_relevant: bool
) -> str:
    """답변을 생성한다.
    
    Args:
        llm: 언어 모델
        question: 사용자 질문
        context: 검색된 문서 문맥 또는 관련 정보
        docs_relevant: 관련 문서가 있는지 여부
        
    Returns:
        생성된 답변 (공백 제거됨)
    """
    system_prompt = GENERATION_SYSTEM_PROMPT_BASE
    
    if docs_relevant:
        # 관련 문서가 있으면 인용 표기 지시 포함
        system_prompt += (
            "\n\n답변할 때 근거 문서를 명시적으로 인용하세요. "
            "예: [출처: 문서명] 또는 \"문서에 따르면...\"과 같은 형식으로 표기하세요."
        )
    else:
        # 관련 문서가 없으면 그 사실을 명시하고 인용 지시 제외
        system_prompt += (
            "\n\n관련 문서를 찾지 못했습니다. "
            "이 사실을 사용자에게 명확히 전달하고, "
            "일반 지식이나 추측으로 답할 수 있다면 그렇게 표기하세요."
        )
    
    user_prompt = f"질문: {question}"
    if context:
        user_prompt += f"\n\n근거 자료:\n{context}"
    
    raw = llm.generate(system_prompt, user_prompt).strip()
    return raw
