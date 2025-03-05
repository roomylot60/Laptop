import ollama

response = ollama.chat(model="llama3", messages=[{"role":"user","content":"안녕! 자기소개 해줘"}])
print(response["message"])