# https://docs.mem0.ai/open-source/configuration
import json
import os
from dotenv import load_dotenv
from mem0 import Memory
from openai import OpenAI, RateLimitError

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# ================  mem0 config ================
config = {
    "version": "v1.1",
    "embedder": {
        "provider": "gemini",
        "config": {"model": "models/gemini-embedding-001", "api_key": api_key}, #https://docs.mem0.ai/components/embedders/models/google_AI#usage
    },
    "llm": {
        "provider": "gemini",
        "config": {"model": "gemini-3.5-flash", "api_key": api_key}, #https://docs.mem0.ai/components/llms/models/google_AI
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost", 
            "port": 6333,
            "embedding_model_dims": 768,
                "collection_name": "mem0_gemini_pushpak_v2"  # fresh collection for Gemini 768 dims
            },
    },
    # "reranker": {
    #     "provider": "cohere",
    #     "config": {"model": "rerank-english-v3.0"},
    # },
}

memory_client = Memory.from_config(config)

# ==================== Call AI ================================

client = OpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

while True:
    user_query = input(" Ask > ")
    if user_query.strip().lower() in {"exit", "quit"}:
        print("Bye!")
        break
    
    search_memory = memory_client.search(query=user_query, filters={"user_id": "pushpak"}) #while adding and searching we must have a same user_id
    
    memories = [f"ID: {mem.get('id')}\n Memory: {mem.get('memory')}" for mem in search_memory.get("results")]
    
    print(f"fount memories ->\n{memories}")
    
    SYSTEM_PROMPT = f"""
    Here is the context about the user:
    {json.dumps(memories)}
    """
    
    # try:
    response = client.chat.completions.create(
        model="gemini-3.5-flash",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query}
        ]
    )
    ai_response = response.choices[0].message.content
    # except RateLimitError:
    #     ai_response = "I'm temporarily unavailable due to API quota limits. Please retry after a minute."
    #     print("Gemini quota exceeded (429). Continuing without crash.")

    print(f"\n\nai_response==>\n", ai_response)
    
    # ====================Store in mem0 ================================

    result = memory_client.add(user_id="pushpak",
                        messages=[
                            {"role": "user", "content": user_query},
                            {"role": "assistant", "content": ai_response},
                            ]
                        )
    print("memory has been saved... ")