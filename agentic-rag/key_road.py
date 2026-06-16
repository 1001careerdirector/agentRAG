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
