import os
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model=os.getenv("MODEL_NAME"),
    temperature=0.2
)

