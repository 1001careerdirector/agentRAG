"""채점 함수 — 문서 관련성과 답변 품질을 평가한다."""
from agentic_rag.ports import LLM


GRADE_DOCS_SYSTEM_PROMPT = (
    "검색된 문서가 사용자의 질문에 대해 관련성이 있는지 평가하세요.\n"
    "관련성이 있으면 'yes', 없으면 'no'만 출력하세요."
)

GRADE_ANSWER_SYSTEM_PROMPT = (
    "생성된 답변이 사용자의 질문에 적절하게 답하는지 평가하세요.\n"
    "적절하면 'yes', 적절하지 않으면 'no'만 출력하세요."
)


def _parse_yes_no(text: str) -> bool:
    """yes/no 응답을 파싱하여 boolean으로 변환한다.
    
    Args:
        text: yes 또는 no를 포함한 텍스트
        
    Returns:
        yes는 True, no는 False, 그 외는 False (폴백)
    """
    text = text.strip().lower()
    if "yes" in text:
        return True
    elif "no" in text:
        return False
    else:
        return False


def grade_docs(llm: LLM, question: str, context: str) -> bool:
    """검색된 문서의 관련성을 평가한다.
    
    Args:
        llm: 언어 모델
        question: 사용자 질문
        context: 검색된 문서 문맥
        
    Returns:
        관련성이 있으면 True, 없으면 False. yes/no 외 응답은 False로 폴백.
    """
    user_prompt = f"질문: {question}\n\n문서: {context}"
    raw = llm.generate(GRADE_DOCS_SYSTEM_PROMPT, user_prompt)
    return _parse_yes_no(raw)


def grade_answer(llm: LLM, question: str, answer: str) -> bool:
    """생성된 답변의 품질을 평가한다.
    
    Args:
        llm: 언어 모델
        question: 사용자 질문
        answer: 생성된 답변
        
    Returns:
        적절하면 True, 적절하지 않으면 False. yes/no 외 응답은 False로 폴백.
    """
    user_prompt = f"질문: {question}\n\n답변: {answer}"
    raw = llm.generate(GRADE_ANSWER_SYSTEM_PROMPT, user_prompt)
    return _parse_yes_no(raw)
