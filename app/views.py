from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core.files.storage import FileSystemStorage
import fitz  # PyMuPDF

import chromadb
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.prompts import PromptTemplate

from dotenv import load_dotenv
import os

# Initialize ChromaDB Client
chroma_client = chromadb.PersistentClient(path="./chroma_db")

load_dotenv()

openai_key = os.getenv("OPENAI_API_KEY")

def bot(request):
    return render(request, 'app/bot.html')

def home(request):
    if request.method == 'POST' and request.FILES.get('uploaded_file'):
        uploaded_file = request.FILES['uploaded_file']

        # Validate file extension
        if not uploaded_file.name.endswith('.pdf'):
            return render(request, 'app/index.html', {'error': 'Only PDF files are allowed!'})

        # Validate file size (8MB limit)
        max_size = 8 * 1024 * 1024
        if uploaded_file.size > max_size:
            return render(request, 'app/index.html', {'error': 'File size must be less than 8MB!'})

        # Save file
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        extracted_text = extract_text_from_pdf("media/"+uploaded_file.name)
        
        with open("data.txt", "w", encoding="utf-8") as f:
            f.write(extracted_text)

        # Creating embeddings
        loader = TextLoader("data.txt", encoding="utf-8")
        documents = loader.load()

        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.split_documents(documents)

        embedding_function = OpenAIEmbeddings()
        Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db")

        print("Vector DB created and stored in ChromaDB.")

        return render(request, 'app/index.html', {'file_url': file_url})

    return render(request, 'app/index.html')


def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    
    text = ""
    for page in doc:
        text += page.get_text("text")
    
    return text

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def response(request):

    if request.method != 'POST':
        return JsonResponse({"status": "error", "answer": "Only post method allowed"})
    
    query = request.POST.get('query', '')

    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=OpenAIEmbeddings()
    )
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
    retriever = vectorstore.as_retriever()

    prompt_template = PromptTemplate(
        template=(
            "You are a conversational agent.'\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n\n"
            "Answer:"
        ),
        input_variables=["context", "question"]
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=retriever,
        chain_type_kwargs={"prompt": prompt_template}
    )

    custom_question = f"{query}?  Use the given context to answer the question. Do not justify your answer. If you could not find the answer in the context then just mention 'I have no knowledge of this question."
    res = qa_chain.invoke(custom_question)
    
    return JsonResponse({"answer":res['result']}, safe=False)