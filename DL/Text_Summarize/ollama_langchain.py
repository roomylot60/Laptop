from langchain_community.llms import Ollama

llm = Ollama(model="llama3")

response = llm.invoke("LLaMA 모델을 로컬에서 실행하는 방법을 설명해줘")
print(response)