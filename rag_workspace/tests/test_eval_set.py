"""eval_set 검증."""
from eval.eval_set import get_eval_set

def test_eval_set_3개_항목():
    """평가 세트에 3개 항목이 있다."""
    es = get_eval_set()
    assert len(es) == 3

def test_eval_set_각_항목_최소_2개_must():
    """각 항목이 최소 2개 이상의 must 포인트를 가진다."""
    es = get_eval_set()
    for item in es:
        assert len(item["must"]) >= 2
        print(f"{item['id']}: {len(item['must'])} must points")

def test_eval_set_서로_다른_주제():
    """각 must 포인트가 서로 다른 주제를 다룬다."""
    es = get_eval_set()
    # 단순 검증: 각 must 문자열이 겹치지 않음 (기본 검증)
    for item in es:
        must_points = item["must"]
        assert len(must_points) == len(set(must_points))

if __name__ == "__main__":
    es = get_eval_set()
    print(f"Eval set items: {len(es)}")
    for i, item in enumerate(es):
        print(f"{i+1}. {item['id']}: {len(item['must'])} must points")
        for j, m in enumerate(item['must']):
            print(f"   - {m}")
