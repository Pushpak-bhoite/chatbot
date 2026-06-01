
import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"✅ Step 7: API key loaded -> {GEMINI_API_KEY[:10]}..." if GEMINI_API_KEY else "❌ API key not found!")

# 1. we need same embedding model
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
print("✅ Step 1: Embedding model ready")

# 2. Get DB
print("⏳ Step 2: Connecting to Qdrant...")
qdrant_vector_DB = QdrantVectorStore.from_existing_collection(
    embedding=embeddings,  # Fixed: 'embedding' not 'embeddings'
    url="http://127.0.0.1:6333", # Changed localhost to 127.0.0.1
    collection_name="pushpak_rag_nodejs_documents",
)

def process_query(query:str):
    print("Searching chunks...")
    search_results = qdrant_vector_DB.similarity_search(query=query)
    
    print(f"📄 Preview of first result: {search_results[0]}")
    
    # 5. Context (created it with iteration )
    context = "\n\n\n".join([f"Page Content: {result.page_content} \nPage Number: {result.metadata['page_label']} \nFile Location: {result.metadata['source']}"
        for result in search_results])
    print(f"✅ Step 3: Context created (length: {len(context)} chars)->\n", context)

    # 6. system prompt
    SYSTEM_PROMPT = f"""
    You are helpful AI assistant who answers user query based on available context retrieved from a PDF file along with page_content and page number. 

    You should ans the user based on following context and navigate the user to open the right page number to know more
    Context:
    {context}
    """
    
    client = OpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )

    print("⏳ Step 9: Sending request to Gemini...")
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {   "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": query
            }
        ]
    )
    print(f"\n{'='*20}")
    print(f"✅ Res==>\n\n {response.choices[0].message.content}")
    return response.choices[0].message.content    