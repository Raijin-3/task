import chromadb
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

from dotenv import load_dotenv
import os

# Initialize ChromaDB Client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

# Load text data (Example: from a file)
loader = TextLoader("data.txt")
documents = loader.load()

# Split text into smaller chunks
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

# Create OpenAI Embeddings
embedding_function = OpenAIEmbeddings()

# Store in ChromaDB
vectorstore = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db")

print("Vector DB created and stored in ChromaDB.")
