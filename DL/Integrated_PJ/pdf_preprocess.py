import io
import fitz
import tempfile
import os
import difflib
import re
import pytesseract
from pdf2image import convert_from_bytes
import streamlit as st

def extract_text_from_pdf(uploaded_file):
    """PDF에서 일반 텍스트 추출"""
    pdf_bytes = uploaded_file.read()
    pdf_stream = io.BytesIO(pdf_bytes)
    doc = fitz.open("pdf", pdf_stream)
    text = "".join(page.get_text("text") + "\n" for page in doc)
    return text.strip() if text.strip() else None

def extract_text_from_scanned_pdf(uploaded_file):
    """OCR을 사용한 PDF 텍스트 추출"""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(uploaded_file.read())
        temp_pdf_path = temp_pdf.name

    try:
        images = convert_from_bytes(open(temp_pdf_path, "rb").read())
    except Exception as e:
        st.error(f"이미지를 추출하는 동안 오류 발생: {e}")
        return ""
    extracted_text = "\n".join(pytesseract.image_to_string(img, lang="kor+eng") for img in images)
    os.unlink(temp_pdf_path)  # 임시 파일 삭제
    return extracted_text.strip() if extracted_text.strip() else None

def merge_valid_texts(text1, text2):
    """일반 텍스트와 OCR 텍스트 비교·정제"""
    if not text1:
        return text2 or ""
    if not text2:
        return text1

    text1_lines = text1.split("\n")
    text2_lines = text2.split("\n")
    merged_lines = []

    for line in text1_lines:
        if difflib.get_close_matches(line, text2_lines, n=1, cutoff=0.8):
            merged_lines.append(line)

    merged_lines.extend([line for line in text2_lines if line not in merged_lines])

    return "\n".join(merged_lines)