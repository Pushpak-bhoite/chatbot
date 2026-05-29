# Prompt styles 

##1. Alpaca Prompt - used by alpeca - meta llama. 
# - Instructions: <SYSTEM_PROMPT>\n
# - Input: <USER_QUERY>
# - Response:\n

##2. ChatML - used by gemini, openAI
# - so the format we were using is the chatML, where we pass content as per role
# - EX: messages = [
#     {
#         "role": "system",
#         "content": "You are a helpful assistant."
#     },
#     {
#         "role": "user",
#         "content": "Explain AI simply"
#     },
#     {
#         "role": "assistant",
#         "content": "AI helps computers learn patterns from data."
#     }
# ]
# - 

##3. INST ( Instruction prompting ) - used by llama 2 
#      <s>[INST] Explain AI in simple words [/INST]
#       AI is a technology that allows computers to learn from data and perform tasks intelligently.
