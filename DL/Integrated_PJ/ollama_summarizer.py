import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3"  # 또는 "deepseek-r1:8b"

def run_ollama_command(prompt):
    """Ollama API 호출"""
    payload = {"model": OLLAMA_MODEL, "prompt": prompt, "stream": False}
    response = requests.post(OLLAMA_API_URL, json=payload)
    return response.json().get("response", "요약 실패") if response.status_code == 200 else "오류 발생"

def summarize_text(text, max_length=300):
    """Ollama 모델을 활용한 텍스트 요약"""
    prompt = f"다음 내용을 {max_length}자 이내의 한국어로 요약해주세요:\n\n{text}"
    return run_ollama_command(prompt)
