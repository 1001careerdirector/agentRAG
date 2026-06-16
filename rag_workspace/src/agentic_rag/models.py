"""도메인 타입 정의."""
from dataclasses import dataclass


@dataclass
class Doc:
    """검색 결과 문서."""
    title: str
    text: str
    chunk: int = 0


@dataclass
class State:
    """에이전트 상태."""
    question: str
    route: str
    search_query: str
    context: str
    answer: str
    retries: int
    docs_relevant: bool
    grounded: bool
