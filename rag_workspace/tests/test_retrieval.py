"""검색 및 재순위 테스트."""
import pytest
from agentic_rag.retrieval import retrieve_reranked
from tests.conftest import FakeLLM, FakeRetriever, FakeReranker, sample_docs


def test_retrieve_reranked_검색_후_재순위(sample_docs):
    """검색 후 재순위한다."""
    retriever = FakeRetriever(sample_docs)
    reranker = FakeReranker()
    result = retrieve_reranked(
        retriever, reranker, "쿼리", fetch_k=4, top_n=2
    )
    assert len(result) == 2
    assert result[0].title == sample_docs[0].title


def test_retrieve_reranked_빈_검색결과면_재순위_호출_안함(sample_docs):
    """검색 결과가 비어있으면 재순위를 호출하지 않는다."""
    retriever = FakeRetriever([])  # 빈 결과
    reranker = FakeReranker()
    result = retrieve_reranked(
        retriever, reranker, "쿼리", fetch_k=4, top_n=2
    )
    assert result == []


def test_retrieve_reranked_fetch_k_전달():
    """fetch_k 가 retriever.search 에 전달된다."""
    docs = [
        {"title": f"doc{i}", "text": f"text{i}", "chunk": 0}
        for i in range(5)
    ]
    from agentic_rag.models import Doc
    docs_obj = [Doc(**d) for d in docs]
    
    retriever = FakeRetriever(docs_obj)
    reranker = FakeReranker()
    result = retrieve_reranked(
        retriever, reranker, "쿼리", fetch_k=3, top_n=2
    )
    # fetch_k=3 이므로 최대 3개가 fetch 되고, top_n=2 이므로 2개만 재순위
    assert len(result) == 2


def test_retrieve_reranked_재정렬_순서_반영(sample_docs):
    """재순위 결과의 순서가 반영된다."""
    retriever = FakeRetriever(sample_docs)
    # order 를 역순으로 지정
    reranker = FakeReranker(order=[sample_docs[3].title, sample_docs[2].title])
    result = retrieve_reranked(
        retriever, reranker, "쿼리", fetch_k=4, top_n=2
    )
    # 재순위 결과: [정책4, 정책3]
    assert result[0].title == sample_docs[3].title
    assert result[1].title == sample_docs[2].title


def test_retrieve_reranked_top_n_초과_문서_제외(sample_docs):
    """top_n 을 초과하는 문서는 제외된다."""
    retriever = FakeRetriever(sample_docs)  # 4개 반환
    reranker = FakeReranker()
    result = retrieve_reranked(
        retriever, reranker, "쿼리", fetch_k=10, top_n=2
    )
    assert len(result) == 2
