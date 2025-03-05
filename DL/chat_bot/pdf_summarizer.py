import openai
import fitz  # PyMuPDF
import streamlit as st

# OpenAI API 키 입력
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# PDF에서 텍스트 추출 함수
def extract_text_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

# GPT를 활용한 요약 함수
def summarize_text(text):
    prompt = f"다음 문서를 요약해줘:\n\n{text[:3000]}"  # 첫 3000자만 사용 (API 제한 방지)
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# GPT를 활용한 질문 응답 함수
def ask_question(text, question):
    prompt = f"다음 문서를 참고하여 질문에 답해주세요:\n\n{text[:3000]}\n\n질문: {question}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

# Streamlit 웹 앱
st.title("📄 PDF 문서 요약 및 Q&A 챗봇")
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type="pdf")

if uploaded_file:
    with st.spinner("문서 처리 중..."):
        text = extract_text_from_pdf(uploaded_file)
        summary = summarize_text(text)
    
    st.subheader("📌 문서 요약")
    st.write(summary)

    st.subheader("💬 문서 관련 질문하기")
    user_question = st.text_input("질문을 입력하세요")
    if st.button("질문하기"):
        answer = ask_question(text, user_question)
        st.write("🤖 AI 답변:", answer)
