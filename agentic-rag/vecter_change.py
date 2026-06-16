import os
from pinecone import Pinecone

# Ensure Pinecone client is available
api_key = os.getenv("PINECONE_API_KEY")
if not api_key:
    message = (
        "Environment variable PINECONE_API_KEY is not set.\n"
        "Set it in PowerShell (temporary for session):\n"
        "  $env:PINECONE_API_KEY = 'your_key'\n"
        "Then re-run this script.\n"
        "Exiting."
    )
    raise SystemExit(message)

pc = Pinecone(api_key=api_key)

# Pinecone 호스팅 임베딩으로 텍스트 → 벡터 변환 (외부 임베딩 서버 불필요)
sentences = [
    "연차 휴가는 15일입니다.",
    "재택근무는 주 3일까지 가능합니다.",
    "점심 메뉴로 김치찌개를 먹었습니다.",
]

# Prepare index handle (uses default INDEX_NAME 'agentic-rag-lab' if exists)
try:
    index = pc.Index("agentic-rag-lab")
except Exception:
    # If the index doesn't exist, let the user know to run index creation first
    raise SystemExit("Index 'agentic-rag-lab' not found. Run index_create.py to create it.")

# inference.embed: 문장 리스트를 임베딩 벡터 리스트로 변환
emb = pc.inference.embed(
    model="multilingual-e5-large",            # 한국어 지원 임베딩 모델 (1024차원)
    inputs=sentences,                          # 임베딩할 입력 문장들
    parameters={"input_type": "passage"},      # 'passage'=저장용 문서, 'query'=검색용 질의
)
vectors = [
    {
        "id": f"s{i}",                         # 각 벡터의 고유 ID
        "values": emb[i].values,               # 1024개 실수로 이루어진 임베딩 값
        "metadata": {"text": sentences[i]},    # 원문을 메타데이터로 함께 저장 (검색 후 사람이 읽기 위함)
    }
    for i in range(len(sentences))
]

index.upsert(vectors=vectors, namespace="demo")   # 'demo' 네임스페이스에 벡터 저장(upsert=삽입/갱신)
print("upsert 완료:", len(vectors), "개")
