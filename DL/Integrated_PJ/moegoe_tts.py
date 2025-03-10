import os
import subprocess

def text_to_speech(text, model_path, config_path, output_path):
    """
    MoeGoe TTS 모델을 사용하여 입력된 텍스트를 음성으로 변환하는 함수.

    Args:
        text (str): 변환할 텍스트
        model_path (str): MoeGoe 모델 파일 경로 (.pth)
        config_path (str): MoeGoe 설정 파일 경로 (.json)
        output_path (str): 저장할 음성 파일 경로 (.wav)

    Returns:
        str: 변환된 음성 파일 경로 (성공 시) / None (실패 시)
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"모델 파일을 찾을 수 없습니다: {model_path}")
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"설정 파일을 찾을 수 없습니다: {config_path}")

    # MoeGoe 실행 명령어
    command = [
        "MoeGoe.exe",
        "-m", model_path,
        "-c", config_path,
        "-t", text,
        "-o", output_path  # 사용자가 지정한 경로로 저장
    ]

    try:
        subprocess.run(command, check=True)
        return output_path if os.path.exists(output_path) else None
    except subprocess.CalledProcessError as e:
        print(f"음성 변환 실패: {e}")
        return None
