import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

load_dotenv()

# Define paths
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "data", "Medical_book.pdf")
db_path = os.path.join(current_dir, "chroma_db")

if not os.path.exists(file_path):
    print(f"❌ Error: Could not find {file_path}")
    exit(1)

print(f"Loading and processing: {file_path}")
loader = PyPDFLoader(file_path)
documents = loader.load()

# Split text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
chunks = text_splitter.split_documents(documents)
print(f"📄 Total chunks to embed: {len(chunks)}")

# Load local HuggingFace embedding model (downloads ~80MB on first run)
print("🔄 Loading embedding model... (downloading on first run)")
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Create and save the vector database
print("Creating vector database... (This may take a minute)")
try:
    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_path
    )
    print(f"✅ Success! Database saved to {db_path}")
    print(f"📦 Total chunks stored: {len(chunks)}")
except Exception as e:
    print(f"❌ Critical Error during embedding: {e}")