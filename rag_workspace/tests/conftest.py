"""테스트 픽스처 및 가짜 의존성."""
import pytest
from agentic_rag.models import Doc


class FakeLLM:
    """테스트용 가짜 LLM — 미리 정한 응답을 반환한다."""
    
    def __init__(self, responses=None, by_marker=None):
        """초기화.
        
        Args:
            responses: 호출 순서대로 반환할 응답 리스트
            by_marker: {프롬프트에 포함된 표식: 응답} 매핑
                      (프롬프트에 표식이 포함되면 그 응답 반환)
        """
        self.responses = list(responses or [])
        self.by_marker = by_marker or {}
        self.calls = []  # (system, user) 튜플 기록 — 프롬프트 검증용
    
    def generate(self, system: str, user: str) -> str:
        """응답을 생성한다.
        
        Args:
            system: 시스템 프롬프트
            user: 사용자 질문
            
        Returns:
            미리 정한 응답
        """
        self.calls.append((system, user))
        
        # by_marker 우선 확인
        for marker, resp in self.by_marker.items():
            if marker in system or marker in user:
                return resp
        
        # 응답 큐에서 반환
        return self.responses.pop(0) if self.responses else ""


class FakeRetriever:
    """테스트용 가짜 검색기."""
    
    def __init__(self, docs):
        """초기화.
        
        Args:
            docs: 반환할 문서 리스트
        """
        self.docs = docs
    
    def search(self, query: str, k: int):
        """검색한다.
        
        Args:
            query: 검색 쿼리
            k: 반환할 최대 문서 수
            
        Returns:
            문서 리스트 (최대 k개)
        """
        return self.docs[:k]


class FakeReranker:
    """테스트용 가짜 재순위기 — 결정적으로 재정렬한다."""
    
    def __init__(self, order=None):
        """초기화.
        
        Args:
            order: 우선순위 (title 문자열 리스트)
                  리스트에 먼저 나타나는 문서가 상위에 정렬됨
        """
        self.order = order
    
    def rerank(self, query: str, docs: list[Doc], top_n: int):
        """재순위한다.
        
        Args:
            query: 검색 쿼리
            docs: 재순위할 문서 리스트
            top_n: 반환할 상위 문서 수
            
        Returns:
            재순위된 상위 문서 리스트
        """
        sorted_docs = docs
        if self.order:
            sorted_docs = sorted(
                docs,
                key=lambda d: self.order.index(d.title)
                if d.title in self.order else 999
            )
        return sorted_docs[:top_n]


@pytest.fixture
def sample_docs():
    """샘플 문서 픽스처."""
    return [
        Doc(title="정책1", text="정책 1 내용", chunk=0),
        Doc(title="정책2", text="정책 2 내용", chunk=0),
        Doc(title="정책3", text="정책 3 내용", chunk=0),
        Doc(title="정책4", text="정책 4 내용", chunk=0),
    ]
