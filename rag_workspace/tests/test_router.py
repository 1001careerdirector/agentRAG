"""라우터 테스트."""
import pytest
from agentic_rag.router import classify
from tests.conftest import FakeLLM


def test_classify_정책질문이면_search():
    """정책·규정·절차 질문은 'search' 로 분류한다."""
    fake_llm = FakeLLM(responses=["search"])
    result = classify(fake_llm, "연차 정책이 뭐에요?")
    assert result == "search"


def test_classify_인사질문이면_direct():
    """인사·잡담·일반상식 질문은 'direct' 로 분류한다."""
    fake_llm = FakeLLM(responses=["direct"])
    result = classify(fake_llm, "고마워요")
    assert result == "direct"


def test_classify_허용값_밖_출력이면_search로_폴백():
    """LLM이 'search'/'direct' 외의 값을 반환하면 'search' 로 폴백한다."""
    fake_llm = FakeLLM(responses=["글쎄요 잘 모르겠네요"])
    result = classify(fake_llm, "질문입니다")
    assert result == "search"


def test_classify_대소문자_정규화():
    """LLM 출력의 대소문자를 정규화한다."""
    fake_llm = FakeLLM(responses=["SEARCH"])
    result = classify(fake_llm, "질문")
    assert result == "search"


def test_classify_공백_제거():
    """LLM 출력의 앞뒤 공백을 제거한다."""
    fake_llm = FakeLLM(responses=["  direct  "])
    result = classify(fake_llm, "질문")
    assert result == "direct"


def test_classify_프롬프트_검증():
    """LLM이 적절한 시스템 프롬프트를 받는다."""
    fake_llm = FakeLLM(responses=["search"])
    classify(fake_llm, "연차")
    
    system_prompt, user_prompt = fake_llm.calls[0]
    assert "search" in system_prompt.lower()
    assert "direct" in system_prompt.lower()
    assert "연차" in user_prompt
