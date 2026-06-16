---
agent: agent
description: 완전성 중심 평가(faithfulness/completeness/run_eval)와 멀티-문서 평가셋을 TDD로 구현
---
# /p4-evaluation — 평가

전역 지침과 `#file:.github/skills/tdd/SKILL.md` 를 따른다.

## 요구사항 + 인수 기준
- `evaluation.faithfulness(llm, question, answer, context) -> float`: 0~1 클램프.
- `evaluation.completeness(llm, answer, must_points) -> float`: 0~1 클램프; must_points 가 프롬프트에 포함(FakeLLM.calls 검증).
- `evaluation.run_eval(integrated_fn, naive_fn, eval_set, scorer)`: 항목별 (통합/Naive) completeness 를 모아 **평균 포함** 결과 dict 반환(집계 로직을 가짜 점수로 결정적 검증).
- `eval/eval_set.py`: **서로 다른 두 문서를 결합해야 답하는** 멀티-문서 질문 3개 + `must` 라벨(데이터만). 예: 재택 보안+배포 최종승인 / 온보딩 첫주+성과평가 주기 / Sev1 대응시간+보안사고 조치.

## 완료 판정
- [ ] 클램프·집계·프롬프트 포함이 테스트로 검증되고 `uv run pytest -q` 초록.
- [ ] eval_set 의 각 항목이 must 를 2개 이상(서로 다른 주제) 가진다.

## 진행 방식
함수별 RED→GREEN→REFACTOR. 전부 초록까지 반복하라.
