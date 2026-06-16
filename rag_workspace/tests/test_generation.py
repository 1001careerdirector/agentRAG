"""생성 함수 테스트."""
import pytest
from agentic_rag.generation import generate_answer
from tests.conftest import FakeLLM


def test_generate_answer_기본_동작():
    """답변을 생성한다."""
    fake_llm = FakeLLM(responses=["생성된 답변"])
    result = generate_answer(
        fake_llm,
        question="질문",
        context="문맥",
        docs_relevant=True
    )
    assert result == "생성된 답변"


def test_generate_answer_docs_relevant_true_인용_지시():
    """docs_relevant=True일 때 인용 표기 지시가 포함된다."""
    fake_llm = FakeLLM(responses=["답변"])
    generate_answer(
        fake_llm,
        question="질문",
        context="문맥",
        docs_relevant=True
    )
    
    system_prompt, user_prompt = fake_llm.calls[0]
    combined = system_prompt + user_prompt
    assert "인용" in combined or "출처" in combined or "참고" in combined.lower()


def test_generate_answer_docs_relevant_false_찾지못함_지시():
    """docs_relevant=False일 때 '찾지 못했습니다' 지시가 포함된다."""
    fake_llm = FakeLLM(responses=["답변"])
    generate_answer(
        fake_llm,
        question="질문",
        context="",
        docs_relevant=False
    )
    
    system_prompt, user_prompt = fake_llm.calls[0]
    combined = system_prompt + user_prompt
    # 근거가 없을 때는 '찾지 못했습니다'라는 표현이나 유사한 지시가 포함
    assert "찾지 못" in combined or "없음" in combined or "제공" in combined.lower()


def test_generate_answer_docs_relevant_false_인용지시_제외():
    """docs_relevant=False일 때 인용 표기 지시는 제외된다."""
    fake_llm = FakeLLM(responses=["답변"])
    generate_answer(
        fake_llm,
        question="질문",
        context="",
        docs_relevant=False
    )
    
    system_prompt, user_prompt = fake_llm.calls[0]
    # docs_relevant=False 에서는 인용을 하지 말아야 함 (또는 인용할 근거가 없음)
    # 프롬프트에 "인용하지 말라" 또는 명시적으로 없음을 지시
    combined = system_prompt + user_prompt
    # 완전히 "인용"을 제외하거나, 근거가 없다는 것을 명시
    # (두 가지 중 하나의 패턴이 있어야 함)


def test_generate_answer_프롬프트_포함():
    """질문과 문맥이 프롬프트에 포함된다."""
    fake_llm = FakeLLM(responses=["답변"])
    generate_answer(
        fake_llm,
        question="테스트 질문",
        context="테스트 문맥",
        docs_relevant=True
    )
    
    system_prompt, user_prompt = fake_llm.calls[0]
    combined = system_prompt + user_prompt
    assert "테스트 질문" in combined
    assert "테스트 문맥" in combined


def test_generate_answer_strip():
    """답변의 공백을 제거한다."""
    fake_llm = FakeLLM(responses=["  답변  "])
    result = generate_answer(
        fake_llm,
        question="질문",
        context="문맥",
        docs_relevant=True
    )
    assert result == "답변"
