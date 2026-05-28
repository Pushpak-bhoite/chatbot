from langchain_community.document_loaders import PyPDFLoader
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()
#1. Loading
loader = PyPDFLoader(
    file_path = "./rag-health.pdf",
    # headers = None
    # password = None,
    mode = "page", # page | single (single parse whole pdf as single chunk, and page is like page wise )
)
docs = loader.load()
print(f"Total pages loaded: {len(docs)}")
print(f"First page -> {docs[0]}")

#2. Splitting
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)  # overlap - is every chunk takes some part of it's previous chunk(text) so it helps every chunk to keep context. 
#It's kind of recap from previous chunk
chunks = text_splitter.split_documents(docs)

#3. Embedding Model 
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    # With the `text-embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    # dimensions=1024
)

#4. quadrant vector storage 
qdrant = QdrantVectorStore.from_documents(
    documents=chunks,
    embeddings=embeddings,
    url="http://localhost:6333", # run container first - visit - http://localhost:6333/dashboard#/collections
    # prefer_grpc=True,
    collection_name="pushpak_rag_health_documents_1",
)

print(f"indexing of documents done....")

