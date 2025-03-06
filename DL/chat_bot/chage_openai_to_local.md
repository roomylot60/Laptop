✅ 실행 방법

#### 1️⃣ Ollama 실행 (백그라운드에서 작동)
Ollama가 실행 중인지 확인 후 실행합니다.

```bash
ollama serve
```

#### 2️⃣ Streamlit 앱 실행
```bash
streamlit run pdf_summary_local.py
```

---

#### 변경된 핵심 내용 정리

|기존 코드 (OpenAI)|변경된 코드 (Ollama + LLaMA)|
|--------------|--------------|
|ChatOpenAI 사용|requests.post() 사용하여 Ollama API 호출|
|OpenAI API 키 필요|API 키 불필요 (로컬 실행)|
|OpenAI 서버 사용|로컬에서 LLaMA 모델 실행|
|`llm.invoke(prompt.format(text=text))`|`requests.post()`로 Ollama API 호출|
