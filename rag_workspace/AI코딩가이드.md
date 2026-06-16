# S11 Agentic RAG — Copilot 요구사항 기반 TDD 키트 (사용 가이드)

"무엇을(요구사항·인수 기준)"은 **프롬프트 파일**로 주고, "어떻게(스택·구조·패턴·TDD)"는 **항상 켜진 지침**으로 고정한 뒤,
**에이전트 모드**가 인수 기준이 충족될 때까지 반복하게 하는 구성이다.

## 1. 파일 배치
```
.github/
├── copilot-instructions.md            # 전역(항상 적용): 스택·구조·패턴·TDD 의무·완료기준
├── instructions/
│   ├── core.instructions.md           # applyTo: src/agentic_rag/**  (포트만 의존, SDK import 금지)
│   ├── tests.instructions.md          # applyTo: tests/**            (실 API 금지, 가짜 주입, 경계)
│   └── adapters.instructions.md       # applyTo: src/agentic_rag/adapters/**  (실 SDK 허용)
├── prompts/
│   ├── p1-foundation.prompt.md        # /p1 … /p6 로 호출
│   ├── p2-pipeline.prompt.md
│   ├── p3-agent.prompt.md
│   ├── p4-evaluation.prompt.md
│   ├── p5-adapters.prompt.md
│   └── p6-scripts.prompt.md
└── skills/tdd/SKILL.md                # RED→GREEN→REFACTOR 절차
```
> 파일명 주의: 전역은 **하이픈** `copilot-instructions.md`. 경로별은 `*.instructions.md` + 프런트매터 `applyTo`. 프롬프트는 `*.prompt.md`.
ㄱㅈㄱㅈㅅ
## 2. 레이어가 하는 일 (요약)
- **전역 지침**: 모든 요청에 자동 주입. 스택·폴더구조·포트&어댑터·TDD 의무·완료기준·보안.
- **경로별 지침**: 해당 경로 파일을 편집할 때만 자동 적용 → 규칙을 좁게 유지(전역 비대화 방지).
- **프롬프트 파일**: `/이름` 으로 수동 호출. **요구사항 + 인수 기준 + "초록까지 반복"** 만 담는다(구현 방법은 안 적는다).
- **스킬**: TDD 절차의 단일 출처.

## 3. 진행 절차 (에이전트 모드)
사전: `uv add --dev pytest pytest-cov` (런타임 의존성은 이미 설치 가정).

1. VS Code Copilot Chat을 **Agent 모드**로 전환.
2. 채팅에 `/p1-foundation` 입력 → 에이전트가 RED(실패 테스트)부터 제시.
3. 에이전트가 테스트를 실행(`uv run pytest`)하고, 실패를 읽어 구현 → 재실행을 **인수 기준이 충족되고 초록이 될 때까지 반복**.
4. 체크리스트(인수 기준)가 모두 채워지면 다음 단계 `/p2-pipeline` … 순서대로 `/p6` 까지.
5. 코어 단계(`/p1`~`/p4`)는 **키 없이** 전부 초록이어야 한다. `/p5`~`/p6` 만 실키로 통합 실행.

> 한 프롬프트로 끝까지 못 가고 멈추면, 그대로 "계속해. 인수 기준 중 남은 항목을 마저 충족시켜라."로 한 번 더 밀어주면 된다.
> 에이전트는 "테스트 통과"라는 **명확한 정지 조건**이 있을 때 반복을 잘 수행한다 — 그래서 인수 기준에 항상 `uv run pytest -q 초록`을 넣었다.

## 4. 검증 명령
```bash
uv run pytest -q
uv run pytest --cov=agentic_rag --cov-report=term-missing
uv run python -m scripts.index_corpus     # 실키
uv run python -m scripts.run_demo          # 실키
```

## 5. 왜 이 구성인가 (설계 의도)
- 프롬프트에 구현을 적지 않으니, 모델이 바뀌어도(프롬프트 재작성 없이) 동일한 표준으로 결과가 수렴한다.
- 규칙을 경로별로 좁히면 컨텍스트 낭비가 줄고 충돌이 적다(전역은 간결 유지가 권장).
- "완료 기준 = 통과하는 테스트"이므로, 에이전트의 반복이 주관이 아니라 **객관적 정지 조건**으로 끝난다.

## 6. 선택 확장
- `mode: agent` 프롬프트 프런트매터에 `model:`(예: 강력 모델) 이나 `tools:` 를 추가해 단계별로 다른 모델/도구를 쓸 수 있다.
- 라우터를 `with_structured_output` 기반으로 바꾸고 싶으면, 어댑터에 structured 변형을 추가하는 `/p2`용 보조 프롬프트를 별도로 만들면 된다(코어 텍스트-파싱 버전은 테스트 유지).
