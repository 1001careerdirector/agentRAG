import os                                       # 환경변수에서 키를 읽기 위해
from pinecone import Pinecone, ServerlessSpec     # Pinecone 클라이언트와 Serverless 설정 클래스

api_key = os.getenv("PINECONE_API_KEY")
if not api_key:
	message = (
		"Environment variable PINECONE_API_KEY is not set.\n"
		"Set it in PowerShell (temporary for session):\n"
		"  $env:PINECONE_API_KEY = 'your_key'\n"
		"Or set it persistently in PowerShell:\n"
		"  Set-Item -Path Env:PINECONE_API_KEY -Value 'your_key'\n"
		"Or on Windows CMD: setx PINECONE_API_KEY \"your_key\"\n"
		"Or in bash/mac: export PINECONE_API_KEY='your_key'\n"
		"Alternatively, create a .env file and load it from Python (python-dotenv).\n"
		"Exiting."
	)
	raise SystemExit(message)

pc = Pinecone(api_key=api_key)   # API 키로 클라이언트 생성
print("기존 인덱스:", [ix["name"] for ix in pc.list_indexes()])  # 계정에 있는 인덱스 이름 목록
