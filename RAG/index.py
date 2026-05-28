from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
 
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
texts = text_splitter.split_documents(docs)

#3. Embedding
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    # With the `text-embedding-3` class
    # of models, you can specify the size
    # of the embeddings you want returned.
    # dimensions=1024
)