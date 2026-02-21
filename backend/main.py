import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from openai import OpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

app = FastAPI()

# Enable CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Paths and Embeddings
current_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(current_dir, "chroma_db")

# HuggingFace embeddings (local, no API needed)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Load existing vector database
if not os.path.exists(DB_PATH):
    print("⚠️ Warning: chroma_db folder not found. Run ingest.py first!")
    vector_store = None
else:
    vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

# Setup OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

MODEL = "nvidia/nemotron-3-nano-30b-a3b:free"

def get_relevant_context(question: str, k: int = 3) -> str:
    """Retrieve relevant chunks from vector store."""
    if vector_store is None:
        return ""
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(question)
    return "\n\n".join([doc.page_content for doc in docs])

def chat_with_model(question: str, context: str) -> str:
    """Call OpenRouter model with retrieved context."""
    system_prompt = (
        "You are a helpful medical assistant. "
        "Use the following retrieved medical context to answer the user's question accurately. "
        "If the answer is not found in the context, say you don't know. "
        "Do not make up medical information.\n\n"
        f"Context:\n{context}"
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question},
        ],
        extra_body={"reasoning": {"enabled": True}}
    )

    return response.choices[0].message.content


class QueryRequest(BaseModel):
    question: str


@app.get("/")
async def root():
    return {"status": "Medical chatbot API is running"}


@app.post("/chat")
async def chat(request: QueryRequest):
    if vector_store is None:
        raise HTTPException(
            status_code=500,
            detail="Vector database not initialized. Run ingest.py first."
        )

    try:
        # Step 1: Retrieve relevant context from vector DB
        context = get_relevant_context(request.question)

        # Step 2: Send to OpenRouter model with context
        answer = chat_with_model(request.question, context)

        return {"answer": answer}

    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))