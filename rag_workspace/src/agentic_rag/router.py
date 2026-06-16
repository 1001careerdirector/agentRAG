"""라우팅 함수 — 질문을 'search' 또는 'direct' 로 분류한다."""
from agentic_rag.ports import LLM


ROUTER_SYSTEM_PROMPT = (
    "사용자 질문을 두 가지 범주 중 하나로 분류하세요:\n"
    "- 'search': 회사의 정책, 규정, 절차, 기술, FAQ, 업무 관련 내용\n"
    "- 'direct': 인사, 잡담, 일반 상식, 감사 인사\n\n"
    "응답은 'search' 또는 'direct' 중 정확히 하나의 단어만 출력하세요."
)


def classify(llm: LLM, question: str) -> str:
    """질문을 'search' 또는 'direct' 로 분류한다.
    
    Args:
        llm: 언어 모델
        question: 분류할 질문
        
    Returns:
        'search' 또는 'direct'. 허용값 외의 출력은 'search' 로 폴백.
    """
    raw = llm.generate(ROUTER_SYSTEM_PROMPT, question).strip().lower()
    return raw if raw in {"search", "direct"} else "search"
