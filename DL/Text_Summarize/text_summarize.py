import os
import io  # BytesIO 사용
import streamlit as st
import requests  # Ollama API 호출용
import json

# 📌 Ollama 설정 (로컬 실행)
OLLAMA_API_URL = "http://localhost:11434/api/generate"  # Ollama 기본 API 주소
LLAMA_MODEL = "llama3"  # 사용할 LLaMA 모델 (예: llama2, llama3 등)

# 📌 텍스트 파일에서 텍스트 추출 함수
def extract_text_from_file(uploaded_file):
    """Streamlit에서 업로드한 텍스트 파일을 읽고 텍스트를 추출하는 함수"""
    if uploaded_file is not None:
        text = uploaded_file.read().decode("utf-8")  # 텍스트 파일을 UTF-8로 읽기
        return text
    return None

# 📌 긴 텍스트를 분할하는 함수
def split_text_into_chunks(text, chunk_size=1500):
    """긴 텍스트를 적절한 크기로 분할하여 리스트로 반환하는 함수"""
    # 텍스트를 chunk_size 크기로 나누기
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i + chunk_size])
    return chunks

# 📌 Ollama API를 사용하여 텍스트 요약하기
def summarize_text(text):
    """Ollama API를 사용하여 텍스트 요약 요청"""
    payload = {
        "model": LLAMA_MODEL,
        "prompt": f"다음 내용을 한 문단으로 요약해서 한국어로 말해줘: {text}",  # 한 문단으로 요약 요청
    }

    response = requests.post(OLLAMA_API_URL, json=payload)

    # 응답 확인
    try:
        # 응답이 여러 부분으로 나뉘어 올 경우 이를 합침
        response_text = ""
        for chunk in response.iter_lines():
            if chunk:
                part = chunk.decode("utf-8")
                try:
                    part_json = json.loads(part)  # 부분 응답을 JSON으로 파싱
                    response_text += part_json.get("response", "")
                except json.JSONDecodeError:
                    continue  # 부분 응답이 JSON이 아니면 넘어감
        return response_text.strip()  # 최종적으로 합친 텍스트 반환
    except Exception as e:
        print(f"응답 오류: {e}")
        return "응답 처리에 실패했습니다."

# 📌 Streamlit 웹 UI 구성
st.title("📄 텍스트 파일 요약기 (Ollama 기반)")
st.write("텍스트 파일을 업로드하면 내용을 요약해드립니다!")

# 📌 파일 업로드 UI
uploaded_file = st.file_uploader("텍스트 파일을 업로드하세요", type=["txt"])

if uploaded_file is not None:
    extracted_text = extract_text_from_file(uploaded_file)
    
    # 텍스트에서 데이터를 성공적으로 추출했는지 확인
    if extracted_text:
        st.subheader("📌 원본 텍스트 (일부)")
        st.text(extracted_text[:500] + "...")  # 긴 텍스트는 일부만 표시

        # 긴 텍스트를 나누어 처리
        chunks = split_text_into_chunks(extracted_text)
        
        # 요약을 누를 때마다 텍스트 분할해서 요약
        if st.button("요약하기"):
            full_summary = ""
            for i, chunk in enumerate(chunks):
                st.write(f"📌 요약 {i+1}:")
                summary = summarize_text(chunk)
                full_summary += summary + "\n\n"
            
            st.subheader("📌 최종 요약 결과")
            st.write(full_summary)
    else:
        st.error("❌ 텍스트 파일에서 텍스트를 추출하지 못했습니다.")
