import os
from getpass import getpass

# 프로젝트 루트의 .env 를 환경변수로 로드
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# .env 에 없으면 입력으로 폴백 (값은 화면에 노출되지 않음)
for name in ["OPENAI_API_KEY", "PINECONE_API_KEY"]:
    if not os.environ.get(name):
        os.environ[name] = getpass(f"{name}: ")

print("키 설정:", {k: bool(os.environ.get(k)) for k in ["OPENAI_API_KEY", "PINECONE_API_KEY"]})
