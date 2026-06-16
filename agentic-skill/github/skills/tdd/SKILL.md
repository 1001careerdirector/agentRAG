---
name: tdd
description: >
  이 저장소에서 프로덕션 코드를 만들거나 고치기 전에 반드시 적용하는 Test-First TDD 워크플로.
  pytest로 RED→GREEN→REFACTOR 사이클을 강제하고, LLM·벡터스토어·재순위 같은 외부 의존성은
  가짜(Fake)로 주입해 API 키 없이 결정적으로 테스트한다. 새 함수·모듈 추가, 버그 수정, 동작 변경 시 사용.
---

# Test-First TDD 스킬 (pytest)

## 언제 사용하나
- 새 함수/모듈 추가, 버그 수정, 동작 변경 등 **프로덕션 코드를 건드리는 모든 작업**.
- 사용하지 않는 경우: 순수 문서 수정, 주석 오타, 동작이 없는 설정 변경.

## 핵심 사이클 — RED → GREEN → REFACTOR
1. **RED**: 원하는 동작을 표현하는 **실패하는 테스트**를 하나 작성한다. 실행해서 *기대한 이유로* 실패하는지 확인한다.
   ```bash
   uv run pytest tests/test_<대상>.py -q   # 빨강(fail) 확인
   ```
2. **GREEN**: 그 테스트만 통과시키는 **최소한의 구현**을 작성한다. 영리하게 미리 만들지 않는다.
   ```bash
   uv run pytest tests/test_<대상>.py -q   # 초록(pass) 확인
   ```
3. **REFACTOR**: 중복 제거·이름 개선·구조 정리. **전체** 테스트가 계속 통과해야 한다.
   ```bash
   uv run pytest -q
   ```
4. 다음 동작으로 이동. 한 사이클 = 하나의 작은 동작.

> 한 번에 테스트와 구현을 모두 쏟아내지 않는다. **RED를 먼저 보여주고 멈춘 뒤**, 확인되면 GREEN으로 넘어간다.

## 실패 테스트 먼저 쓰는 법
- "무엇을(입력) 주면 무엇을(출력) 기대하는가"를 한 문장으로 정하고, 그걸 `assert` 로 옮긴다.
- **AAA 구조**:
  ```python
  def test_classify_정책질문이면_search를_돌려준다():
      # Arrange
      llm = FakeLLM(by_marker={"분류": "search"})
      # Act
      result = classify(llm, "연차는 며칠인가요?")
      # Assert
      assert result == "search"
  ```
- 이름: `test_<대상>_<상황>_<기대결과>` (한국어 가능). 한 테스트는 하나만 검증한다.

## 외부 의존성은 가짜로 주입
코어 함수는 `ports.py` 의 Protocol(LLM/Retriever/Reranker)을 **인자로 받는다**. 테스트는 가짜를 주입한다.
`tests/conftest.py` 에 둘 표준 가짜:
```python
from dataclasses import dataclass

@dataclass
class Doc:
    title: str
    text: str
    chunk: int = 0

class FakeLLM:
    """generate(system, user) 호출에 미리 정한 응답을 돌려주는 테스트용 LLM."""
    def __init__(self, responses=None, by_marker=None):
        self.responses = list(responses or [])
        self.by_marker = by_marker or {}     # 프롬프트에 특정 표식이 있으면 그 응답
        self.calls = []                       # (system, user) 기록 — 프롬프트 검증용
    def generate(self, system: str, user: str) -> str:
        self.calls.append((system, user))
        for marker, resp in self.by_marker.items():
            if marker in system or marker in user:
                return resp
        return self.responses.pop(0) if self.responses else ""

class FakeRetriever:
    def __init__(self, docs): self.docs = docs
    def search(self, query: str, k: int):
        return self.docs[:k]

class FakeReranker:
    """주어진 점수 순서대로 재정렬해 top_n 개 반환(결정적)."""
    def __init__(self, order=None): self.order = order   # title 리스트로 우선순위 지정 가능
    def rerank(self, query, docs, top_n):
        if self.order:
            docs = sorted(docs, key=lambda d: self.order.index(d.title)
                          if d.title in self.order else 999)
        return docs[:top_n]
```
- LLM이 만든 텍스트(라우팅 라벨, 채점 yes/no, 점수)는 가짜로 **결정적으로** 통제한다.
- `FakeLLM.calls` 로 "어떤 프롬프트가 들어갔는지"까지 검증할 수 있다(예: 근거 없음일 때 '찾지 못했습니다' 지시가 들어갔는지).

## pytest 관례
- 픽스처는 `conftest.py` 에. 비슷한 케이스는 `@pytest.mark.parametrize` 로 묶는다.
- **경계/예외를 반드시 포함**: 빈 결과, 잘못된 라벨, 상한 도달, 직답 경로, 0/1 점수.
- 빠르고 독립적으로. 테스트 간 상태 공유 금지.

## 안티패턴 (하지 말 것)
- ❌ 구현부터 쓰고 테스트를 나중에 끼워 맞추기.
- ❌ 단위 테스트에서 실제 OpenAI/Pinecone 호출(느리고 비결정적·유료).
- ❌ 한 테스트에서 여러 동작을 한꺼번에 검증.
- ❌ 내부 구현 디테일에 과의존하는 과도한 목(mock). 포트 경계에서만 가짜를 쓴다.

## 예시 사이클 — `router.classify`
**RED** — `tests/test_router.py`
```python
import pytest
from agentic_rag.router import classify

def test_classify_정책질문이면_search():
    llm = FakeLLM(responses=["search"])
    assert classify(llm, "배포 승인 절차 알려줘") == "search"

def test_classify_인사면_direct():
    llm = FakeLLM(responses=["direct"])
    assert classify(llm, "고마워요") == "direct"

def test_classify_이상한_출력이면_search로_안전하게_기본값():
    llm = FakeLLM(responses=["글쎄요 잘 모르겠어요"])
    assert classify(llm, "연차 며칠?") == "search"   # 허용값 외 → 안전한 기본값
```
→ `uv run pytest tests/test_router.py -q` 로 **빨강** 확인.

**GREEN** — `src/agentic_rag/router.py`
```python
from agentic_rag.ports import LLM

ROUTER_SYSTEM = (
    "질문을 'search'(사내 정책·규정·절차·기술·FAQ) 또는 'direct'(인사·잡담·일반상식)로 분류하세요. "
    "회사 생활·업무 규정과 조금이라도 관련 있으면 search. 한 단어만 출력."
)

def classify(llm: LLM, question: str) -> str:
    """질문을 'search' 또는 'direct' 로 분류한다. 허용값 외 출력은 'search' 로 폴백."""
    raw = llm.generate(ROUTER_SYSTEM, question).strip().lower()
    return raw if raw in {"search", "direct"} else "search"
```
→ **초록** 확인 후, 전체 `uv run pytest -q` 로 회귀 없음 확인 → 필요 시 리팩터.

## 완료 기준(Definition of Done)
- 새 동작마다 테스트가 있고, 모든 테스트가 통과한다.
- 코어 모듈은 외부 SDK를 직접 import 하지 않는다(포트만 의존).
- 경계/예외가 테스트로 덮여 있다. 커버리지는 코어 모듈 기준 90%+ 를 목표로 한다.
