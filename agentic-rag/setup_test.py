import importlib.metadata as meta

for pkg in ["langgraph", "langchain", "langchain-core",
            "langchain-openai", "langchain-pinecone", "pinecone"]:
    try:
        print(f"{pkg:<22} {meta.version(pkg)}")
    except meta.PackageNotFoundError:
        print(f"{pkg:<22} (미설치)")

print("-" * 40)

# 1.x에서 위치가 갈리는 핵심 심볼 확인 (예제 마이그레이션 시 자주 걸리는 지점)
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.graph.message import add_messages
from langchain.agents import create_agent              # 고수준 에이전트 → langchain.agents
from langgraph.prebuilt import ToolNode, tools_condition  # 그래프 프리미티브 → langgraph.prebuilt (유지)
from langchain_pinecone import PineconeVectorStore, PineconeEmbeddings, PineconeRerank
from langchain_openai import ChatOpenAI
print("핵심 import OK")
