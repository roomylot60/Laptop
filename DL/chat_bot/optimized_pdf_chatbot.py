import openai
import fitz  # PyMuPDF
import io # ByetesIO 사용
import streamlit as st
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain_openai import ChatOpenAI  # 최신 버전 import 방식 변경

# OpenAI API 설정
OPENAI_API_KEY = "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"

# LLM 모델 초기화
llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

# PDF에서 텍스트 추출 함수
def extract_text_from_pdf(uploaded_file):
    """Streamlit에서 업로드한 PDF를 읽고 텍스트를 추출하는 함수"""
    if uploaded_file is not None:
        pdf_bytes = uploaded_file.read()  # 파일을 바이너리 형태로 읽기
        pdf_stream = io.BytesIO(pdf_bytes)  # BytesIO 객체로 변환
        doc = fitz.open("pdf", pdf_stream)  # 🔹 파일이 아닌 'pdf' 타입의 stream을 열기
        text = ""
        for page in doc:
            text += page.get_text("text") + "\n"
        return text
    return None


# 📌 PDF 요약 함수
def summarize_text(text):
    """LangChain을 이용하여 텍스트 요약"""
    prompt = PromptTemplate(
        input_variables=["text"],
        template="다음 내용을 한 문단으로 요약해줘:\n{text}"
    )
    response = llm.invoke(prompt.format(text=text))
    return response.content

# 📌 Streamlit 웹 UI 구성
st.title("📄 PDF 요약기")
st.write("PDF 파일을 업로드하면 내용을 요약해드립니다!")

# 파일 업로드 UI
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=["pdf"])

if uploaded_file is not None:
    extracted_text = extract_text_from_pdf(uploaded_file)
    
    # PDF에서 텍스트를 성공적으로 추출했는지 확인
    if extracted_text:
        st.subheader("📌 원본 텍스트 (일부)")
        st.text(extracted_text[:500] + "...")  # 긴 텍스트는 일부만 표시

        if st.button("요약하기"):
            summary = summarize_text(extracted_text)
            st.subheader("📌 요약 결과")
            st.write(summary)
    else:
        st.error("❌ PDF에서 텍스트를 추출하지 못했습니다.")