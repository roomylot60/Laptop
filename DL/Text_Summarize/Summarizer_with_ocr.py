import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import os
import streamlit as st
import requests
import io
import fitz
import tempfile
import difflib
import re

# Local Ollama model setting
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "deepseek-r1:8b" # "llama3"

# PDF에서 일반 텍스트 추출
def extract_text_from_pdf(uploaded_file):
    """PDF에서 일반 텍스트를 추출하는 함수"""
    pdf_bytes = uploaded_file.read()
    pdf_stream = io.BytesIO(pdf_bytes)
    doc = fitz.open("pdf", pdf_stream)
    text = "".join(page.get_text("text") + "\n" for page in doc)
    return text.strip() if text.strip() else None

# OCR을 사용하여 스캔된 PDF에서 텍스트 추출
def extract_text_from_scanned_pdf(uploaded_file):
    """OCR을 사용하여 스캔된 PDF에서 텍스트 추출"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name

    images = convert_from_bytes(open(temp_pdf_path, "rb").read())
    extracted_text = ""

    for img in images:
        text = pytesseract.image_to_string(img, lang="kor+eng")  # 한글 + 영어 OCR
        extracted_text += text + "\n"

    os.unlink(temp_pdf_path)  # 임시 파일 삭제

    return extracted_text.strip() if extracted_text.strip() else None

# Ollama API 요청 함수
def run_ollama_command(prompt):
    """Ollama API를 호출하는 함수"""
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    response = requests.post(OLLAMA_API_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("response", "응답을 받을 수 없습니다.")
    return "오류 발생: Ollama 응답이 없습니다."

# Ollama 모델을 이용한 요약 함수
def summarize_text(text):
    """텍스트를 요약하는 함수"""
    prompt = f"다음 내용을 간결하게 요약해서 한국어로 말해주세요:\n\n{text}"
    return run_ollama_command(prompt)

# 의미 없는 문자 및 비한국어 문장 필터링
def clean_and_filter_text(text):
    """OCR 및 일반 텍스트에서 의미 없는 내용 제거 및 한국어 문장만 남김"""
    # 특수 문자 및 공백 정리
    text = re.sub(r"[^가-힣a-zA-Z0-9\s.,!?()\[\]~%-]", "", text)
    
    # 한글이 포함되지 않은 문장 제거 (단, 영어 단어가 포함된 한글 문장은 허용)
    filtered_lines = []
    for line in text.split("\n"):
        if re.search(r"[가-힣]", line):  # 한글이 포함된 문장만 유지
            filtered_lines.append(line.strip())

    return "\n".join(filtered_lines)

# 텍스트를 비교하여 유효한 내용을 추출
def merge_valid_texts(text1, text2):
    """일반 PDF 텍스트와 OCR 텍스트를 비교하여 신뢰도 높은 내용을 추출"""
    if not text1:
        return clean_and_filter_text(text2)  # 일반 텍스트가 없으면 OCR 텍스트 사용
    if not text2:
        return clean_and_filter_text(text1)  # OCR 텍스트가 없으면 일반 텍스트 사용

    # 텍스트 유사도 비교 (80% 이상 유사하면 중복 제거)
    text1_lines = text1.split("\n")
    text2_lines = text2.split("\n")

    merged_lines = []
    for line in text1_lines:
        match = difflib.get_close_matches(line, text2_lines, n=1, cutoff=0.8)
        if match:
            merged_lines.append(line)  # 유사한 텍스트가 있으면 일반 텍스트 우선
        else:
            merged_lines.append(line)

    for line in text2_lines:
        if line not in merged_lines:
            merged_lines.append(line)  # OCR에서만 존재하는 정보 추가

    merged_text = "\n".join(merged_lines)
    return clean_and_filter_text(merged_text)

# Streamlit UI
st.title("📄 PDF 요약기 (LLaMA3 기반)")
st.write("PDF 파일을 업로드하면 일반 텍스트 및 OCR 텍스트를 비교하여 최적의 요약을 제공합니다.")

# 파일 업로드
uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=["pdf"])

if uploaded_file is not None:
    # 일반 PDF 텍스트 추출
    extracted_text = extract_text_from_pdf(uploaded_file)

    # OCR을 사용한 텍스트 추출
    uploaded_file.seek(0)  # 파일 포인터 초기화
    extracted_ocr_text = extract_text_from_scanned_pdf(uploaded_file)

    # 유효한 텍스트 선택 및 결합
    merged_text = merge_valid_texts(extracted_text, extracted_ocr_text)

    # 원본 텍스트 출력
    st.subheader("📄 최종 선택된 텍스트")
    with st.expander("📖 선택된 텍스트 (펼쳐보기)"):
        st.text(merged_text[:1000] + "\n\n...\n\n" + merged_text[-1000:])

    # 요약 실행 버튼
    if st.button("요약하기"):
        summary = summarize_text(merged_text)
        st.subheader("📌 요약 결과")
        st.write(summary)
