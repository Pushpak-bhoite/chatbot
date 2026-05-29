# Only replaced OpeAI model 
from langchain_community.document_loaders import PyPDFLoader
from langchain_qdrant import QdrantVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings


load_dotenv()
print("✅ Environment loaded")

#1. Loading
loader = PyPDFLoader(
    file_path = "./rag-health.pdf",
    # headers = None
    # password = None,
    mode = "page", # page | single (single parse whole pdf as single chunk, and page is like page wise )
)
docs = loader.load()
print(f"✅ Step 1: Loaded {len(docs)} pages->\n",docs )

#2. Splitting
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)  # overlap - is every chunk takes some part of it's previous chunk(text) so it helps every chunk to keep context. 
#It's kind of recap from previous chunk
chunks = text_splitter.split_documents(docs)
print(f"✅ Step 2: Created {len(chunks)} chunks ->\n", chunks)

#3. Embedding Model 
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
print("✅ Step 3: Embedding model ready ->\n", embeddings)

#4. quadrant vector storage 
print("⏳ Step 4: Storing in Qdrant (this may take a moment)...")
qdrant = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embeddings,  # Fixed: 'embedding' not 'embeddings'
    url="http://localhost:6333", # run container first - visit - http://localhost:6333/dashboard#/collections
    # prefer_grpc=True,
    collection_name="pushpak_rag_health_documents_1",
)
print("✅ Step 4: qdrant -> \n", qdrant)
print("✅ Step 5: Indexing done!")

