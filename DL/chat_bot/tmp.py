import os
from openai import OpenAI

file_name = os.path.join(os.getcwd(), 'data/openai_api.txt')

# OpenAI API 설정
f = open(file_name, "r")
OPENAI_API_KEY = f.read()

# api_key = os.getenv("OPENAI_API_KEY")
# print(f"OpenAI API Key: {api_key}")

# client = OpenAI(OPENAI_API_KEY)
# models = client.models.list()

# for model in models.data:
#     print(model.id)
