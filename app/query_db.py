from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

# Load ChromaDB
vectorstore = Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())

# Search for relevant documents
query = "What is machine learning?"
results = vectorstore.similarity_search(query, k=2)  # Get top 2 matches

print("Search Results:")
for result in results:
    print(result.page_content)
