"""채점 함수 테스트."""
import pytest
from agentic_rag.grading import grade_docs, grade_answer
from tests.conftest import FakeLLM


def test_grade_docs_yes_파싱():
    """'yes' 응답은 True 로 파싱된다."""
    fake_llm = FakeLLM(responses=["yes"])
    result = grade_docs(fake_llm, "질문", "문맥")
    assert result is True


def test_grade_docs_no_파싱():
    """'no' 응답은 False 로 파싱된다."""
    fake_llm = FakeLLM(responses=["no"])
    result = grade_docs(fake_llm, "질문", "문맥")
    assert result is False


def test_grade_docs_yes_대소문자_무시():
    """'YES', 'Yes' 등도 True 로 파싱된다."""
    for variant in ["YES", "Yes", "  YES  "]:
        fake_llm = FakeLLM(responses=[variant])
        result = grade_docs(fake_llm, "질문", "문맥")
        assert result is True


def test_grade_docs_no_대소문자_무시():
    """'NO', 'No' 등도 False 로 파싱된다."""
    for variant in ["NO", "No", "  NO  "]:
        fake_llm = FakeLLM(responses=[variant])
        result = grade_docs(fake_llm, "질문", "문맥")
        assert result is False


def test_grade_docs_애매한_출력이면_false_폴백():
    """yes/no 외의 출력은 False 로 폴백한다."""
    fake_llm = FakeLLM(responses=["글쎄요"])
    result = grade_docs(fake_llm, "질문", "문맥")
    assert result is False


def test_grade_docs_프롬프트_검증():
    """grade_docs 가 적절한 프롬프트를 LLM에 전달한다."""
    fake_llm = FakeLLM(responses=["yes"])
    grade_docs(fake_llm, "테스트 질문", "테스트 문맥")
    
    system_prompt, user_prompt = fake_llm.calls[0]
    assert "테스트 질문" in system_prompt or "테스트 질문" in user_prompt
    assert "테스트 문맥" in system_prompt or "테스트 문맥" in user_prompt


def test_grade_answer_yes_파싱():
    """'yes' 응답은 True 로 파싱된다."""
    fake_llm = FakeLLM(responses=["yes"])
    result = grade_answer(fake_llm, "질문", "답변")
    assert result is True


def test_grade_answer_no_파싱():
    """'no' 응답은 False 로 파싱된다."""
    fake_llm = FakeLLM(responses=["no"])
    result = grade_answer(fake_llm, "질문", "답변")
    assert result is False


def test_grade_answer_애매한_출력이면_false_폴백():
    """yes/no 외의 출력은 False 로 폴백한다."""
    fake_llm = FakeLLM(responses=["모르겠는데요"])
    result = grade_answer(fake_llm, "질문", "답변")
    assert result is False


def test_grade_answer_프롬프트_검증():
    """grade_answer 가 적절한 프롬프트를 LLM에 전달한다."""
    fake_llm = FakeLLM(responses=["yes"])
    grade_answer(fake_llm, "테스트 질문", "테스트 답변")
    
    system_prompt, user_prompt = fake_llm.calls[0]
    assert "테스트 질문" in system_prompt or "테스트 질문" in user_prompt
    assert "테스트 답변" in system_prompt or "테스트 답변" in user_prompt
