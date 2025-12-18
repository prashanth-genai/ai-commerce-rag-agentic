import faiss
from sentence_transformers import SentenceTransformer
from langchain.prompts import PromptTemplate
from ai_service.llm_config import llm
from ai_service.prompt_templates import RAG_PROMPT

model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("vector_store/faiss_index/index.bin")

def run_rag(query):
    query_vec = model.encode([query])
    _, idx = index.search(query_vec, 5)

    context = "Retrieved enterprise data based on similarity search"

    prompt = PromptTemplate(
        template=RAG_PROMPT,
        input_variables=["context", "question"]
    )

    return llm.invoke(
        prompt.format(context=context, question=query)
    ).content

