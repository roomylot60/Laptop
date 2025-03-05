import os

api_key = os.getenv("OPENAI_API_KEY")
print(f"OpenAI API Key: {api_key}")

from openai import OpenAI

client = OpenAI(api_key="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")

models = client.models.list()

for model in models.data:
    print(model.id)