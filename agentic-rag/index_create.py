import os
from pinecone import Pinecone, ServerlessSpec

INDEX_NAME = "agentic-rag-lab"     # 이 과정 전체에서 재사용할 인덱스 이름
EMBED_DIM  = 1024                  # multilingual-e5-large 의 임베딩 차원

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

existing = [ix["name"] for ix in pc.list_indexes()]   # 현재 인덱스 목록을 다시 조회
if INDEX_NAME not in existing:                         # 같은 이름이 없을 때만 생성
    pc.create_index(
        name=INDEX_NAME,                               # 인덱스 이름
        dimension=EMBED_DIM,                           # 벡터 차원 (임베딩과 반드시 일치)
        metric="cosine",                             # 유사도 측정 방식: 코사인
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),  # 서버리스: 클라우드/리전 지정
    )
    print(f"생성 완료: {INDEX_NAME} (dim={EMBED_DIM})")
else:
    print(f"이미 존재: {INDEX_NAME}")

index = pc.Index(INDEX_NAME)        # 인덱스 핸들 획득 (이후 upsert/query에 사용)
print(index.describe_index_stats()) # 벡터 수·차원 등 현재 상태 확인