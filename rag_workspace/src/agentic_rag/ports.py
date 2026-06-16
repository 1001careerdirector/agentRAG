"""포트 (Protocol) — 의존성 주입 인터페이스."""
from typing import Protocol
from agentic_rag.models import Doc


class LLM(Protocol):
    """언어 모델 인터페이스."""
    
    def generate(self, system: str, user: str) -> str:
        """시스템 프롬프트와 사용자 질문으로 응답을 생성한다.
        
        Args:
            system: 시스템 프롬프트
            user: 사용자 질문
            
        Returns:
            생성된 텍스트 응답
        """
        ...


class Retriever(Protocol):
    """검색 인터페이스."""
    
    def search(self, query: str, k: int) -> list[Doc]:
        """쿼리로 문서를 검색한다.
        
        Args:
            query: 검색 쿼리
            k: 반환할 최대 문서 수
            
        Returns:
            검색 결과 문서 리스트
        """
        ...


class Reranker(Protocol):
    """재순위 인터페이스."""
    
    def rerank(self, query: str, docs: list[Doc], top_n: int) -> list[Doc]:
        """검색 결과를 재순위한다.
        
        Args:
            query: 검색 쿼리
            docs: 재순위할 문서 리스트
            top_n: 반환할 상위 문서 수
            
        Returns:
            재순위된 상위 문서 리스트
        """
        ...
