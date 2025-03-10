# import fitz

# def check_pdf_with_fitz(pdf_file):
#     try:
#         doc = fitz.open(pdf_file)
#         if doc.page_count == 0:
#             raise ValueError("PDF에 페이지가 없습니다.")
#         page = doc[0]  # 첫 페이지 가져오기
#         text = page.get_text("text")  # 첫 페이지 텍스트 추출
#         return text
#     except Exception as e:
#         raise ValueError(f"PDF를 열 때 오류가 발생했습니다: {e}")


# import streamlit as st

# st.title("📄 PDF 요약 & 음성 변환")

# # 📌 PDF 파일 업로드
# uploaded_file = st.file_uploader("📂 PDF 파일을 업로드하세요", type=["pdf"])

# if uploaded_file:
#     st.write("🔍 텍스트 추출 중...")
#     check_pdf_with_fitz(uploaded_file)