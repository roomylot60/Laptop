import os
import streamlit as st
import requests
import json
import io
import fitz

# Local Ollama model setting
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Ollama 기본 API 주소
LLAMA_MODEL = "llama3"  # Ollama에 설치된 모델 이름 (llama3)

# Extract text from pdf file
def extract_text_from_pdf(uploaded_file):
    """PDF 파일에서 텍스트 추출"""
    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()
        pdf_stream = io.BytesIO(pdf_bytes)
        doc = fitz.open("pdf", pdf_stream)
        text = "".join(page.get_text("text") + "\n" for page in doc)
        return text
    return None

# Ollama 명령 실행 함수
def run_ollama_command(prompt):
    """Ollama API를 호출하는 함수"""
    payload = {
        "model": LLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("response", "응답을 받을 수 없습니다.")
    return "오류 발생: Ollama 응답이 없습니다."

# Ollama 모델로 텍스트 요약 요청
def summarize_text(text):
    """텍스트를 요약하는 함수"""
    prompt = f"다음 내용을 한국어로 간결하게 요약해 주세요:\n\n{text}"
    return run_ollama_command(prompt)

# Streamlit UI
st.title("📄 PDF 요약기 (LLaMA3 기반)")
st.write("PDF 파일을 업로드하면 LLaMA 모델로 요약해드립니다!")

# 파일 업로드
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=["pdf"])

if uploaded_file is not None:
    extracted_text = extract_text_from_pdf(uploaded_file)
    
    if extracted_text:
        st.subheader("원본 텍스트 (일부)")
        st.text(extracted_text[:250] + "\n\n...\n\n" + extracted_text[-250:])

        if st.button("요약하기"):
            summary = summarize_text(extracted_text)
            st.subheader("요약 결과")
            st.write(summary)
    else:
        st.error("PDF에서 텍스트를 추출하지 못했습니다.")