import os
from getpass import getpass

# S0 프로젝트 루트의 .env 에서 키 로드 (없으면 입력으로 폴백)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
for name in ["OPENAI_API_KEY", "PINECONE_API_KEY"]:
    if not os.environ.get(name):
        os.environ[name] = getpass(f"{name}: ")
print("키:", {k: bool(os.environ.get(k)) for k in ["OPENAI_API_KEY", "PINECONE_API_KEY"]})

from pinecone import Pinecone, ServerlessSpec
from pinecone.exceptions import NotFoundException
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


embeddings = PineconeEmbeddings(model="multilingual-e5-large")   # 한국어 임베딩(1024차원)
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
index_name = "agentic-rag-lab"
try:
    index = pc.Index(index_name)                              # S2/S3에서 색인한 인덱스
except NotFoundException:
    print(f"Index '{index_name}' not found. Creating it now...")
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )
    index = pc.Index(index_name)

INDEX_NAME = "agentic-rag-lab"     # 이 과정 전체에서 재사용할 인덱스 이름
EMBED_DIM  = 1024                  # multilingual-e5-large 의 임베딩 차원

existing = [ix["name"] for ix in pc.list_indexes()]   # 현재 인덱스 목록을 다시 조회
if INDEX_NAME not in existing:                         # 같은 이름이 없을 때만 생성
    pc.create_index(
        name=INDEX_NAME,                               # 인덱스 이름
        dimension=EMBED_DIM,                           # 벡터 차원 (임베딩과 반드시 일치)
        metric="cosine",                               # 유사도 측정 방식: 코사인
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),  # 서버리스: 클라우드/리전 지정
    )
    print(f"생성 완료: {INDEX_NAME} (dim={EMBED_DIM})")
else:
    print(f"이미 존재: {INDEX_NAME}")

index = pc.Index(INDEX_NAME)        # 인덱스 핸들 획득 (이후 upsert/query에 사용)
print(index.describe_index_stats()) # 벡터 수·차원 등 현재 상태 확인


INDEX_NAME = "agentic-rag-lab"
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
if INDEX_NAME not in [ix["name"] for ix in pc.list_indexes()]:  # 없으면 생성
    pc.create_index(name=INDEX_NAME, dimension=EMBED_DIM, metric="cosine",
                    spec=ServerlessSpec(cloud="aws", region="us-east-1"))
index = pc.Index(INDEX_NAME)
print("인덱스 준비 완료")

# ★ 네임스페이스 미지정 시 빈 기본 네임스페이스를 조회한다. S3에서 색인한 chunk_500 을 메인 코퍼스로 사용.
NAMESPACE = "chunk_500"
vector_store = PineconeVectorStore(index=index, embedding=embeddings, namespace=NAMESPACE)
try:
    _stats = index.describe_index_stats()
    _ns = getattr(_stats, "namespaces", None) or (_stats.get("namespaces") if isinstance(_stats, dict) else {}) or {}
    _cnt = {k: getattr(v, "vector_count", v.get("vector_count") if isinstance(v, dict) else None) for k, v in _ns.items()}
    print("네임스페이스별 벡터 수:", _cnt)
    if not _cnt.get(NAMESPACE):
        print(f"⚠️ '{NAMESPACE}' 네임스페이스에 데이터가 없습니다. S3의 색인 셀을 먼저 실행하세요.")
except Exception as _e:
    print("인덱스 통계 확인 생략:", _e)
llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)            # 기본 LLM
print("연결 완료")

