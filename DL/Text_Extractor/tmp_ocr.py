import pytesseract
from pdf2image import convert_from_bytes, convert_from_path
from PIL import Image
import os

PATH = os.path.join(os.getcwd(), "data")

def extract_text_from_scanned_pdf(pdf_path):
    """OCR을 사용하여 스캔된 PDF에서 텍스트 추출"""
    images = convert_from_path(pdf_path)  # PDF를 이미지로 변환
    extracted_text = ""
    
    for img in images:
        text = pytesseract.image_to_string(img, lang="kor+eng")  # 한글 + 영어 OCR
        extracted_text += text + "\n"
    
    return extracted_text.strip() if extracted_text else None

def extract_text_from_scanned_pdf(pdf_path, output_path):
    """OCR을 사용하여 스캔된 PDF에서 텍스트 추출 후 .txt 파일로 저장"""
    images = convert_from_path(pdf_path)  # PDF를 이미지로 변환
    extracted_text = ""
    
    for img in images:
        text = pytesseract.image_to_string(img, lang="kor+eng")  # 한글 + 영어 OCR
        extracted_text += text + "\n"

    if extracted_text.strip():  # 텍스트가 존재하면 파일 저장
        file_name = os.path.split(pdf_path)[1].replace('pdf','txt')
        txt_file_path = os.path.join(output_path, file_name)
        with open(txt_file_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(extracted_text)
        print(f"📄 OCR 결과가 {output_path}에 저장되었습니다.")
        return extracted_text.strip()
    else:
        print("❌ OCR을 통해 텍스트를 추출하지 못했습니다.")
        return None

# ✅ 테스트 실행
file_list = os.listdir(PATH)
output_path =  os.path.join(os.getcwd(), "output") # 저장할 TXT 파일 경로
if os.path.exists(output_path):
    print(f"{output_path} exists.")
else:
    os.mkdir(output_path)
    print(f"Make {output_path} directory.")

for file in file_list:
    if file.endswith(".pdf"):
        file_path = os.path.join(PATH, file) # pdf 파일 경로
        extracted_text = extract_text_from_scanned_pdf(file_path, output_path)
        if extracted_text:
            print("OCR 결과:\n")
            print(extracted_text[:1000])  # 너무 길 경우 앞부분만 출력
        else:
            print("OCR을 통해 텍스트를 추출하지 못했습니다.")
