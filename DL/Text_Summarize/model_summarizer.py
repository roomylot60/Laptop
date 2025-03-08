import requests
import streamlit as st

# DeepSeek-R1 설정 (Ollama API)
OLLAMA_API_URL = "http://localhost:11434/api/generate"
DEEPSEEK_MODEL = "deepseek-r1:8b"  # deepseek-r1 모델 사용

def extract_text_from_pdf_with_deepseek(pdf_bytes):
    """DeepSeek-R1을 사용하여 PDF에서 텍스트 추출"""
    prompt = "다음 PDF 파일에서 텍스트를 추출하고 핵심 내용만 출력하세요."
    
    # API 요청에 필요한 파라미터 준비
    payload = {
        "model": DEEPSEEK_MODEL,
        "prompt": prompt,
        "stream": False
    }
    
    # 파일을 바이너리 형식으로 전달
    try:
        response = requests.post(OLLAMA_API_URL, data=payload, files={"file": pdf_bytes})
        if response.status_code == 200:
            return response.json().get("response", "응답을 받을 수 없습니다.")
        else:
            return f"오류 발생: Ollama 응답이 없습니다. (Status Code: {response.status_code})"
    except requests.exceptions.RequestException as e:
        return f"요청 오류: {e}"

def summarize_text_with_deepseek(text):
    """DeepSeek-R1을 사용하여 텍스트 요약"""
    prompt = f"다음 내용을 한국어로 간결하게 요약하세요:\n\n{text}"
    
    payload = {
        "model": DEEPSEEK_MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "응답을 받을 수 없습니다.")
        else:
            return f"오류 발생: Ollama 응답이 없습니다. (Status Code: {response.status_code})"
    except requests.exceptions.RequestException as e:
        return f"요청 오류: {e}"

# Streamlit UI
st.title("📄 DeepSeek-R1 기반 PDF 분석기")
st.write("DeepSeek-R1 모델을 이용해 PDF 파일에서 텍스트를 추출하고, 그 내용을 요약합니다!")

uploaded_file = st.file_uploader("📂 PDF 파일을 업로드하세요", type=["pdf"])

if uploaded_file is not None:
    pdf_bytes = uploaded_file.read()

    # 텍스트 추출 요청
    with st.spinner("🔍 DeepSeek-R1이 텍스트를 추출 중..."):
        extracted_text = extract_text_from_pdf_with_deepseek(pdf_bytes)

    if extracted_text:
        st.subheader("📜 추출된 텍스트")
        st.text_area("📖 원본 텍스트", extracted_text[:500] + "...\n\n(중략)", height=300)

        # 요약 버튼
        if st.button("📌 요약하기"):
            with st.spinner("🔍 요약 중..."):
                summary = summarize_text_with_deepseek(extracted_text)
            st.subheader("📑 요약 결과")
            st.write(summary)
    else:
        st.error("❌ PDF에서 텍스트를 추출하지 못했습니다.")
