"""평가 함수 테스트."""
import pytest
from agentic_rag.evaluation import faithfulness, completeness, run_eval
from tests.conftest import FakeLLM


# ===== faithfulness 테스트 =====
def test_faithfulness_0_값_반환():
    """faithfulness 점수가 0을 반환한다."""
    fake_llm = FakeLLM(responses=["0"])
    result = faithfulness(fake_llm, "질문", "답변", "문맥")
    assert result == 0.0


def test_faithfulness_1_값_반환():
    """faithfulness 점수가 1을 반환한다."""
    fake_llm = FakeLLM(responses=["1"])
    result = faithfulness(fake_llm, "질문", "답변", "문맥")
    assert result == 1.0


def test_faithfulness_중간_값_반환():
    """faithfulness 점수가 0.5 같은 중간 값을 반환한다."""
    fake_llm = FakeLLM(responses=["0.5"])
    result = faithfulness(fake_llm, "질문", "답변", "문맥")
    assert result == 0.5


def test_faithfulness_음수_클램프():
    """음수 출력은 0으로 클램프된다."""
    fake_llm = FakeLLM(responses=["-0.5"])
    result = faithfulness(fake_llm, "질문", "답변", "문맥")
    assert result == 0.0


def test_faithfulness_1_초과_클램프():
    """1 초과 출력은 1로 클램프된다."""
    fake_llm = FakeLLM(responses=["1.5"])
    result = faithfulness(fake_llm, "질문", "답변", "문맥")
    assert result == 1.0


def test_faithfulness_파싱_실패_0_폴백():
    """파싱 불가능한 출력은 0으로 폴백된다."""
    fake_llm = FakeLLM(responses=["점수를 매길 수 없음"])
    result = faithfulness(fake_llm, "질문", "답변", "문맥")
    assert result == 0.0


# ===== completeness 테스트 =====
def test_completeness_0_값_반환():
    """completeness 점수가 0을 반환한다."""
    fake_llm = FakeLLM(responses=["0"])
    result = completeness(fake_llm, "답변", ["필수 포인트 1"])
    assert result == 0.0


def test_completeness_1_값_반환():
    """completeness 점수가 1을 반환한다."""
    fake_llm = FakeLLM(responses=["1"])
    result = completeness(fake_llm, "답변", ["필수 포인트 1"])
    assert result == 1.0


def test_completeness_중간_값_반환():
    """completeness 점수가 0.7 같은 중간 값을 반환한다."""
    fake_llm = FakeLLM(responses=["0.7"])
    result = completeness(fake_llm, "답변", ["필수 포인트 1"])
    assert result == 0.7


def test_completeness_음수_클램프():
    """음수 출력은 0으로 클램프된다."""
    fake_llm = FakeLLM(responses=["-0.2"])
    result = completeness(fake_llm, "답변", ["필수 포인트 1"])
    assert result == 0.0


def test_completeness_1_초과_클램프():
    """1 초과 출력은 1로 클램프된다."""
    fake_llm = FakeLLM(responses=["2.0"])
    result = completeness(fake_llm, "답변", ["필수 포인트 1"])
    assert result == 1.0


def test_completeness_must_points_프롬프트_포함():
    """must_points가 프롬프트에 포함된다."""
    fake_llm = FakeLLM(responses=["0.8"])
    must_points = ["재택근무 보안정책", "배포 최종승인 절차"]
    completeness(fake_llm, "답변 테스트", must_points)
    
    system_prompt, user_prompt = fake_llm.calls[0]
    combined = system_prompt + user_prompt
    assert "재택근무 보안정책" in combined
    assert "배포 최종승인 절차" in combined


def test_completeness_파싱_실패_0_폴백():
    """파싱 불가능한 출력은 0으로 폴백된다."""
    fake_llm = FakeLLM(responses=["평가 불가"])
    result = completeness(fake_llm, "답변", ["필수 포인트"])
    assert result == 0.0


# ===== run_eval 테스트 =====
def test_run_eval_두_함수_모두_호출():
    """integrated_fn과 naive_fn을 모두 호출한다."""
    calls = []
    
    def integrated_fn(q):
        calls.append("integrated")
        return {"answer": "통합 답변"}
    
    def naive_fn(q):
        calls.append("naive")
        return {"answer": "나이브 답변"}
    
    fake_llm = FakeLLM(responses=["0.8", "0.6"])
    eval_set = [{"question": "질문1", "must": ["포인트1"]}]
    
    def scorer(answer, must_points):
        return completeness(fake_llm, answer, must_points)
    
    run_eval(integrated_fn, naive_fn, eval_set, scorer)
    
    assert "integrated" in calls
    assert "naive" in calls


def test_run_eval_결과_dict_반환():
    """결과를 dict로 반환한다."""
    def integrated_fn(q):
        return {"answer": "답변"}
    
    def naive_fn(q):
        return {"answer": "답변"}
    
    fake_llm = FakeLLM(responses=["0.8", "0.6"])
    eval_set = [{"question": "질문1", "must": ["포인트1"]}]
    
    def scorer(answer, must_points):
        return completeness(fake_llm, answer, must_points)
    
    result = run_eval(integrated_fn, naive_fn, eval_set, scorer)
    
    assert isinstance(result, dict)
    assert "integrated" in result
    assert "naive" in result


def test_run_eval_항목별_점수_포함():
    """각 항목별 completeness 점수를 포함한다."""
    def integrated_fn(q):
        return {"answer": "답변"}
    
    def naive_fn(q):
        return {"answer": "답변"}
    
    fake_llm = FakeLLM(responses=["0.9", "0.7", "0.8", "0.5"])
    eval_set = [
        {"question": "질문1", "must": ["포인트1"]},
        {"question": "질문2", "must": ["포인트2"]},
    ]
    
    def scorer(answer, must_points):
        return completeness(fake_llm, answer, must_points)
    
    result = run_eval(integrated_fn, naive_fn, eval_set, scorer)
    
    # 각 함수의 점수가 리스트 형태로 포함되어야 함
    assert "integrated" in result
    assert "naive" in result
    assert isinstance(result["integrated"], dict) or isinstance(result["integrated"], list)


def test_run_eval_평균_포함():
    """통합과 나이브의 평균 점수를 포함한다."""
    def integrated_fn(q):
        return {"answer": "답변"}
    
    def naive_fn(q):
        return {"answer": "답변"}
    
    # 2개 항목: integrated [0.8, 0.6], naive [0.7, 0.5]
    fake_llm = FakeLLM(responses=["0.8", "0.7", "0.6", "0.5"])
    eval_set = [
        {"question": "질문1", "must": ["포인트1"]},
        {"question": "질문2", "must": ["포인트2"]},
    ]
    
    def scorer(answer, must_points):
        return completeness(fake_llm, answer, must_points)
    
    result = run_eval(integrated_fn, naive_fn, eval_set, scorer)
    
    # 평균 점수가 포함되어야 함
    assert "integrated_avg" in result or (isinstance(result["integrated"], dict) and "avg" in result["integrated"])
    assert "naive_avg" in result or (isinstance(result["naive"], dict) and "avg" in result["naive"])


def test_run_eval_정확한_평균_계산():
    """평균을 정확하게 계산한다."""
    def integrated_fn(q):
        return {"answer": "답변"}
    
    def naive_fn(q):
        return {"answer": "답변"}
    
    # integrated: (0.8 + 0.6) / 2 = 0.7
    # naive: (0.5 + 0.5) / 2 = 0.5
    fake_llm = FakeLLM(responses=["0.8", "0.5", "0.6", "0.5"])
    eval_set = [
        {"question": "질문1", "must": ["포인트1"]},
        {"question": "질문2", "must": ["포인트2"]},
    ]
    
    def scorer(answer, must_points):
        return completeness(fake_llm, answer, must_points)
    
    result = run_eval(integrated_fn, naive_fn, eval_set, scorer)
    
    # 평균 검증 (형식에 따라 다를 수 있으므로 유연하게)
    if isinstance(result.get("integrated"), dict):
        assert abs(result["integrated"].get("avg", 0) - 0.7) < 0.01
        assert abs(result["naive"].get("avg", 0) - 0.5) < 0.01
    else:
        assert abs(result.get("integrated_avg", 0) - 0.7) < 0.01
        assert abs(result.get("naive_avg", 0) - 0.5) < 0.01
