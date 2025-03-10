import streamlit as st
import os
from pdf_preprocess import extract_text_from_pdf, extract_text_from_scanned_pdf, merge_valid_texts
from ollama_summarizer import summarize_text
from moegoe_tts import text_to_speech

st.title("📄 PDF 요약 & 음성 변환")

# 📌 PDF 파일 업로드
uploaded_file = st.file_uploader("📂 PDF 파일을 업로드하세요", type=["pdf"])

# PDF 파일 업로드 시 텍스트 추출 및 요약
if uploaded_file:
    st.session_state.uploaded_pdf = uploaded_file  # 세션 상태에 PDF 파일 저장

# 세션 상태에 저장된 PDF 파일이 있는 경우
if "uploaded_pdf" in st.session_state:
    uploaded_file = st.session_state.uploaded_pdf
    st.write("🔍 텍스트 추출 중...")
    
    # 일반 텍스트 및 OCR 텍스트 비교
    normal_text = extract_text_from_pdf(uploaded_file)
    scanned_text = extract_text_from_scanned_pdf(uploaded_file)
    final_text = merge_valid_texts(normal_text, scanned_text)

    st.subheader("📌 추출된 텍스트")
    st.text_area("Extracted Text", final_text, height=200)

    # 📜 Ollama 요약 실행
    if st.button("📜 요약 실행"):
        summary_text = summarize_text(final_text)
        st.subheader("📌 요약된 텍스트")
        st.write(summary_text)

        # 🗣️ TTS 변환
        st.subheader("🔊 TTS 변환")

        # 모델 및 설정 파일 업로드
        model_file = st.file_uploader("MoeGoe 모델 파일 (.pth)", type=["pth"])
        config_file = st.file_uploader("MoeGoe 설정 파일 (.json)", type=["json"])

        # 세션 상태에 모델과 설정 파일이 저장되었는지 확인
        if model_file is not None:
            st.session_state.model = model_file  # 모델 파일을 세션 상태에 저장
        if config_file is not None:
            st.session_state.config = config_file  # 설정 파일을 세션 상태에 저장

        # 사용자 지정 출력 파일명
        output_filename = st.text_input("🎵 출력 파일명 (예: output.wav)", "output.wav")

        if st.button("🎙️ 음성 변환"):
            if "model" in st.session_state and "config" in st.session_state:
                try:
                    # 업로드된 파일을 임시 디렉토리에 저장
                    model_path = os.path.join("temp", st.session_state.model.name)
                    config_path = os.path.join("temp", st.session_state.config.name)

                    os.makedirs("temp", exist_ok=True)
                    with open(model_path, "wb") as f:
                        f.write(st.session_state.model.read())
                    with open(config_path, "wb") as f:
                        f.write(st.session_state.config.read())
                except Exception as e:
                    st.error(f"파일 저장 중 오류 발생: {e}")

                # 음성 변환 실행
                wav_file = text_to_speech(summary_text, model_path, config_path, output_filename)

                if os.path.exists(wav_file):
                    st.success("✅ 음성 변환 완료!")
                    st.audio(wav_file, format="audio/wav")
                else:
                    st.error("⚠️ 음성 변환에 실패했습니다.")
            else:
                st.warning("⚠️ 모델과 설정 파일을 업로드해주세요.")
