"""스모크 테스트 — 기반 모듈 구조 및 타입 검증."""
import pytest
from agentic_rag.models import Doc, State
from agentic_rag import config
from agentic_rag.ports import LLM, Retriever, Reranker
from tests.conftest import FakeLLM, FakeRetriever, FakeReranker, sample_docs


def test_doc_기본값_chunk은_0():
    """Doc 인스턴스의 chunk 기본값이 0이어야 한다."""
    doc = Doc(title="문서제목", text="문서 내용")
    assert doc.chunk == 0


def test_doc_타입_검증():
    """Doc이 title, text, chunk 필드를 가진다."""
    doc = Doc(title="제목", text="내용", chunk=5)
    assert doc.title == "제목"
    assert doc.text == "내용"
    assert doc.chunk == 5


def test_state_타입_검증():
    """State가 필요한 모든 필드를 가진다."""
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
    assert state.question == "질문"
    assert state.route == "search"
    assert state.retries == 0


def test_config_상수들_존재():
    """설정 상수들이 정의되어 있다."""
    assert hasattr(config, "NAMESPACE")
    assert hasattr(config, "MAX_RETRIES")
    assert hasattr(config, "FETCH_K")
    assert hasattr(config, "TOP_N")
    assert hasattr(config, "MODEL_NAME")


def test_config_상수_값_기대대로():
    """설정 상수값이 기대하는 유형이다."""
    assert isinstance(config.NAMESPACE, str)
    assert isinstance(config.MAX_RETRIES, int)
    assert isinstance(config.FETCH_K, int)
    assert isinstance(config.TOP_N, int)
    assert isinstance(config.MODEL_NAME, str)
    assert config.MAX_RETRIES > 0
    assert config.FETCH_K > 0
    assert config.TOP_N > 0


def test_ports_protocol들_import_가능():
    """포트 Protocol들이 import 가능하다."""
    assert LLM is not None
    assert Retriever is not None
    assert Reranker is not None


def test_fakellm_import_가능_및_사용():
    """FakeLLM이 import되고 사용 가능하다."""
    fake_llm = FakeLLM(responses=["답변"])
    result = fake_llm.generate("시스템", "사용자")
    assert result == "답변"


def test_fakeretriever_import_가능_및_사용(sample_docs):
    """FakeRetriever가 import되고 사용 가능하다."""
    fake_retriever = FakeRetriever(sample_docs)
    results = fake_retriever.search("쿼리", k=2)
    assert len(results) == 2


def test_fakereranker_import_가능_및_사용(sample_docs):
    """FakeReranker가 import되고 사용 가능하다."""
    fake_reranker = FakeReranker()
    results = fake_reranker.rerank("쿼리", sample_docs, top_n=2)
    assert len(results) == 2


def test_sample_docs_fixture_제공():
    """sample_docs 픽스처가 제공된다."""
    # conftest에서 pytest fixture로 제공되는지 확인
    assert callable(sample_docs) or isinstance(sample_docs, list)
