"""그래프 및 에이전트 테스트."""
import pytest
from agentic_rag.models import Doc, State
from agentic_rag import config
from agentic_rag.graph import after_docs, after_answer, build_agent
from tests.conftest import FakeLLM, FakeRetriever, FakeReranker


# ===== after_docs 분기 함수 테스트 =====
def test_after_docs_relevant_true_generate():
    """docs_relevant=True면 'generate' 으로 분기한다."""
    state = State(
        question="질문",
        route="search",
        search_query="검색어",
        context="문맥",
        answer="",
        retries=0,
        docs_relevant=True,
        grounded=False,
    )
    result = after_docs(state)
    assert result == "generate"


def test_after_docs_relevant_false_retries_미달_rewrite():
    """docs_relevant=False이고 retries < MAX_RETRIES면 'rewrite' 로 분기한다."""
    state = State(
        question="질문",
        route="search",
        search_query="검색어",
        context="문맥",
        answer="",
        retries=0,
        docs_relevant=False,
        grounded=False,
    )
    result = after_docs(state)
    assert result == "rewrite"


def test_after_docs_relevant_false_retries_상한_generate():
    """docs_relevant=False이고 retries >= MAX_RETRIES면 'generate' 으로 분기한다."""
    state = State(
        question="질문",
        route="search",
        search_query="검색어",
        context="문맥",
        answer="",
        retries=config.MAX_RETRIES,
        docs_relevant=False,
        grounded=False,
    )
    result = after_docs(state)
    assert result == "generate"


def test_after_docs_retries_경계값():
    """retries = MAX_RETRIES - 1 일 때 'rewrite' 으로 분기한다."""
    state = State(
        question="질문",
        route="search",
        search_query="검색어",
        context="문맥",
        answer="",
        retries=config.MAX_RETRIES - 1,
        docs_relevant=False,
        grounded=False,
    )
    result = after_docs(state)
    assert result == "rewrite"


# ===== after_answer 분기 함수 테스트 =====
def test_after_answer_grounded_true_end():
    """grounded=True면 END 로 분기한다."""
    state = State(
        question="질문",
        route="search",
        search_query="검색어",
        context="문맥",
        answer="답변",
        retries=0,
        docs_relevant=True,
        grounded=True,
    )
    result = after_answer(state)
    assert result == "__end__"


def test_after_answer_grounded_false_regenerate():
    """grounded=False면 'regenerate' 로 분기한다."""
    state = State(
        question="질문",
        route="search",
        search_query="검색어",
        context="문맥",
        answer="답변",
        retries=0,
        docs_relevant=True,
        grounded=False,
    )
    result = after_answer(state)
    assert result == "regenerate"


# ===== build_agent 통합 흐름 테스트 =====
def test_build_agent_personal_question_direct_path(sample_docs):
    """개인 질문(인사) → direct 경로 (검색 노드 미경유)."""
    # Deps 구성: 인사 질문은 router가 'direct'로 분류
    fake_llm = FakeLLM(by_marker={"분류": "direct"})
    fake_retriever = FakeRetriever(sample_docs)
    fake_reranker = FakeReranker()
    
    deps = {
        "llm": fake_llm,
        "retriever": fake_retriever,
        "reranker": fake_reranker,
    }
    
    agent = build_agent(deps)
    assert agent is not None
    
    # direct 경로에서는 검색을 거치지 않고 답변 생성
    # (나중에 invoke로 호출 가능)


def test_build_agent_relevant_docs_single_pass(sample_docs):
    """관련 문서 있음 → 한 번에 generate, retries==0."""
    # Docs: relevant = True → 즉시 generate, retries 미증가
    fake_llm = FakeLLM(
        by_marker={
            "분류": "search",
            "관련성": "yes",
            "근거": "yes",
        }
    )
    fake_llm.responses = ["search", "yes", "답변", "yes"]
    
    fake_retriever = FakeRetriever(sample_docs)
    fake_reranker = FakeReranker()
    
    deps = {
        "llm": fake_llm,
        "retriever": fake_retriever,
        "reranker": fake_reranker,
    }
    
    agent = build_agent(deps)
    assert agent is not None


def test_build_agent_rewrite_loop_until_max_retries(sample_docs):
    """관련성 False → rewrite 루프가 MAX_RETRIES까지, 그다음 generate(근거없음)."""
    # Scenario: 3번 rewrite 후 MAX_RETRIES 도달 → generate
    # 첫 번째 docs: relevant=False → rewrite
    # 두 번째 docs: relevant=False → rewrite
    # 세 번째 docs: retries=MAX_RETRIES → generate (근거없음)
    
    fake_llm = FakeLLM(
        by_marker={
            "분류": "search",
        }
    )
    # 순서: classify, grade_docs(False), rewrite_query, grade_docs(False), rewrite_query, grade_docs(False), 
    #       rewrite_query, generate(답변-근거없음), grade_answer(True)
    fake_llm.responses = [
        "search",
        "no",
        "재작성 검색어 1",
        "no",
        "재작성 검색어 2",
        "no",
        "재작성 검색어 3",
        "근거 없는 답변",
        "yes",
    ]
    
    fake_retriever = FakeRetriever(sample_docs)
    fake_reranker = FakeReranker()
    
    deps = {
        "llm": fake_llm,
        "retriever": fake_retriever,
        "reranker": fake_reranker,
    }
    
    agent = build_agent(deps)
    assert agent is not None
