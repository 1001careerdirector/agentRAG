from langchain_text_splitters import RecursiveCharacterTextSplitter  # 재귀적 문자 분할기
from langchain_core.documents import Document                        # LangChain 표준 문서 객체

# Try to reuse the sample corpus defined in chunk_01.py
try:
    from chunk_01 import raw_docs
except Exception:
    raw_docs = None


def split_corpus(chunk_size: int, chunk_overlap: int = 40):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,            # 한 청크의 최대 글자 수
        chunk_overlap=chunk_overlap,      # 인접 청크 간 겹치는 글자 수
        separators=["\n\n", "\n", ". ", " ", ""],  # 큰 단위→작은 단위 순으로 분할 시도
    )
    if not raw_docs:
        raise SystemExit(
            "raw_docs not found. Either run chunk_01.py first or provide raw_docs in this module."
        )

    chunks = []                            # 결과 청크들을 담을 리스트
    for d in raw_docs:                     # 모든 원본 문서를 순회
        for i, piece in enumerate(splitter.split_text(d["text"])):  # 본문을 청크로 분할
            chunks.append(Document(
                page_content=piece,                                  # 청크 본문
                metadata={"source": d["id"], "title": d["title"], "chunk": i},  # 출처 추적용 메타데이터
            ))
    return chunks

# 세 가지 크기로 각각 몇 개의 청크가 나오는지 비교
for size in [200, 500, 1000, 1500]:
    n = len(split_corpus(size))            # 해당 크기로 분할했을 때 청크 수
    print(f"chunk_size={size:<5} → 청크 {n}개")
