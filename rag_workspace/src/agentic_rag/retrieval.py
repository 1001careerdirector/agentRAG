"""검색 및 재순위 함수 — 문서를 검색하고 재순위한다."""
from agentic_rag.models import Doc
from agentic_rag.ports import Retriever, Reranker


def retrieve_reranked(
    retriever: Retriever,
    reranker: Reranker,
    query: str,
    fetch_k: int,
    top_n: int,
) -> list[Doc]:
    """문서를 검색하고 재순위한다.
    
    Args:
        retriever: 검색 엔진
        reranker: 재순위 엔진
        query: 검색 쿼리
        fetch_k: 초기 검색 결과 수
        top_n: 최종 상위 문서 수
        
    Returns:
        재순위된 상위 문서 리스트. 검색 결과가 없으면 []를 반환하고
        재순위를 호출하지 않는다.
    """
    # 검색
    docs = retriever.search(query, k=fetch_k)
    
    # 빈 검색결과면 재순위 호출 안함
    if not docs:
        return []
    
    # 재순위
    reranked = reranker.rerank(query, docs, top_n=top_n)
    return reranked
