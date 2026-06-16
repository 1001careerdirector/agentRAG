"""평가 함수 — 답변의 충실성과 완전성을 평가한다."""
from agentic_rag.ports import LLM


FAITHFULNESS_SYSTEM_PROMPT = (
    "답변이 주어진 문맥에 기반한 정보인지 평가하세요.\n"
    "0~1 사이의 숫자로 충실성 점수를 매기세요. (0=거짓, 1=완전히 참)\n"
    "숫자만 출력하세요."
)

COMPLETENESS_SYSTEM_PROMPT = (
    "답변이 필수 포인트들을 모두 충분히 다루었는지 평가하세요.\n"
    "0~1 사이의 숫자로 완전성 점수를 매기세요. (0=미충족, 1=완전 충족)\n"
    "숫자만 출력하세요."
)


def _parse_float(text: str, default: float = 0.0) -> float:
    """텍스트를 float로 파싱하거나 기본값으로 폴백한다."""
    try:
        return float(text.strip())
    except (ValueError, AttributeError):
        return default


def _clamp_0_1(value: float) -> float:
    """값을 0~1 범위로 클램프한다."""
    return max(0.0, min(1.0, value))


def faithfulness(
    llm: LLM,
    question: str,
    answer: str,
    context: str
) -> float:
    """답변의 충실성을 평가한다 (0~1로 클램프).
    
    Args:
        llm: 언어 모델
        question: 사용자 질문
        answer: 생성된 답변
        context: 참고 문맥
        
    Returns:
        충실성 점수 (0.0~1.0). 파싱 실패 시 0.0 폴백.
    """
    user_prompt = f"질문: {question}\n\n답변: {answer}\n\n문맥: {context}"
    raw = llm.generate(FAITHFULNESS_SYSTEM_PROMPT, user_prompt)
    score = _parse_float(raw, default=0.0)
    return _clamp_0_1(score)


def completeness(
    llm: LLM,
    answer: str,
    must_points: list[str]
) -> float:
    """답변의 완전성을 평가한다 (0~1로 클램프).
    
    Args:
        llm: 언어 모델
        answer: 생성된 답변
        must_points: 필수적으로 포함되어야 할 포인트 리스트
        
    Returns:
        완전성 점수 (0.0~1.0). 파싱 실패 시 0.0 폴백.
    """
    must_str = "\n".join(f"- {point}" for point in must_points)
    system_prompt = (
        COMPLETENESS_SYSTEM_PROMPT +
        f"\n\n필수 포인트들:\n{must_str}"
    )
    user_prompt = f"답변: {answer}"
    raw = llm.generate(system_prompt, user_prompt)
    score = _parse_float(raw, default=0.0)
    return _clamp_0_1(score)


def run_eval(
    integrated_fn,
    naive_fn,
    eval_set: list[dict],
    scorer
) -> dict:
    """통합 에이전트와 나이브 방식을 평가 세트에서 비교한다.
    
    Args:
        integrated_fn: 통합 에이전트 함수 (question dict -> result dict)
        naive_fn: 나이브 방식 함수 (question dict -> result dict)
        eval_set: 평가 항목 리스트 [{"question": ..., "must": [...]}, ...]
        scorer: 채점 함수 (answer, must_points) -> float
        
    Returns:
        {"integrated": [...], "integrated_avg": 0.X,
         "naive": [...], "naive_avg": 0.X}
    """
    integrated_scores = []
    naive_scores = []
    
    for item in eval_set:
        question = item["question"]
        must_points = item.get("must", [])
        
        # 통합 에이전트 평가
        integrated_result = integrated_fn(question)
        integrated_answer = integrated_result.get("answer", "")
        integrated_score = scorer(integrated_answer, must_points)
        integrated_scores.append(integrated_score)
        
        # 나이브 방식 평가
        naive_result = naive_fn(question)
        naive_answer = naive_result.get("answer", "")
        naive_score = scorer(naive_answer, must_points)
        naive_scores.append(naive_score)
    
    # 평균 계산
    integrated_avg = (
        sum(integrated_scores) / len(integrated_scores)
        if integrated_scores else 0.0
    )
    naive_avg = (
        sum(naive_scores) / len(naive_scores)
        if naive_scores else 0.0
    )
    
    return {
        "integrated": integrated_scores,
        "integrated_avg": integrated_avg,
        "naive": naive_scores,
        "naive_avg": naive_avg,
    }
