import cv2
import os
import numpy as np

# 1. 이미지 전처리 : OpenCV 사용
# OCR의 성능을 향상시키기 위해서는 먼저 입력 이미지를 전처리해야 합니다. 전처리는 이미지에서 불필요한 정보를 제거하고 텍스트 인식을 쉽게 만들어 줍니다. 전처리 단계에서는 주로 이진화, 노이즈 제거, 회전 교정 등을 수행합니다.
# 이미지 전처리 단계:
# 1. 이진화: 이미지를 흑백으로 변환하여, 텍스트와 배경의 차이를 강조합니다.
# 2. 노이즈 제거: 이미지에 있는 불필요한 점들을 제거하여 OCR 성능을 향상시킵니다.
# 3. 이미지 크기 조정: 이미지의 크기를 일정하게 맞추어줍니다.
# 4. 왜곡 보정: 텍스트가 왜곡되었을 때, 그 왜곡을 교정합니다.

image_file = os.path.join(os.getcwd(), 'data/image.png')
# 이미지 로드
image = cv2.imread(image_file)

# 그레이스케일로 변환
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 이진화 (Otsu's Thresholding)
_, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 노이즈 제거 (여기서는 미디언 필터 사용)
denoised_image = cv2.medianBlur(binary_image, 3)

# 이미지를 화면에 표시
cv2.imshow('Processed Image', denoised_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 2. 문자 영역 탐지
# OCR의 핵심은 텍스트 영역을 정확히 찾고, 그 영역에서 글자를 추출하는 것입니다. 이를 위해 텍스트 영역 탐지가 필요합니다. 이를 위해 윤곽선 추적, 연결 요소 분석, 슬라이딩 윈도우 기법 등을 사용할 수 있습니다.

# 윤곽선 추적을 통한 텍스트 영역 탐지
# 이진화된 이미지에서 윤곽선 찾기
contours, _ = cv2.findContours(denoised_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 각 윤곽선을 사각형으로 표시
for contour in contours:
    if cv2.contourArea(contour) > 100:  # 작은 노이즈 영역은 무시
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# 텍스트 영역이 표시된 이미지를 화면에 표시
cv2.imshow('Text Areas', image)
cv2.waitKey(0)
cv2.destroyAllWindows()


# 3. 문자 인식
# 문자 인식을 위한 핵심적인 방법은 기계 학습 모델을 사용하는 것입니다. 텍스트를 인식하는 모델을 구축하기 위해서는 딥러닝을 활용할 수 있습니다. 
# 특히 **Convolutional Neural Networks (CNN)**와 **Recurrent Neural Networks (RNN)**를 결합하여 CTC (Connectionist Temporal Classification) 손실 함수로 학습시키는 방법이 효과적입니다.
# 딥러닝 모델 구축:
# CNN: 이미지를 처리하여 특징을 추출합니다.
# RNN: 시퀀스 데이터를 처리하여, 글자의 순서를 인식합니다.
# CTC 손실 함수: 시간적으로 정렬되지 않은 레이블을 처리할 수 있게 해줍니다.

# 4. 딥러닝 모델 학습
# OCR 모델을 학습시키기 위해서는 데이터셋이 필요합니다. 여러 오픈소스 데이터셋이 있지만, 가장 많이 사용되는 것은 MNIST (손글씨 숫자), ICDAR (다양한 문서 이미지) 데이터셋입니다. 데이터셋을 준비한 후, 텍스트 인식을 위한 모델을 학습시켜야 합니다.

# 5. 후처리 및 텍스트 출력
# OCR 모델이 이미지를 텍스트로 변환한 후, 그 텍스트를 가공하여 최종 결과를 얻습니다. 후처리에서는 맞춤법 교정, 텍스트 정리 등을 할 수 있습니다.
# 후처리 예시:
# - 단어 단위로 텍스트 필터링: 인식된 텍스트에서 불필요한 공백, 기호 등을 제거합니다.
# - 맞춤법 교정: 인식된 텍스트가 비정상적일 경우, 교정 알고리즘을 통해 정확한 텍스트로 수정할 수 있습니다.

# 6. 배포 및 성능 최적화
# 완성된 OCR 시스템을 배포하고, 실시간으로 텍스트를 추출하거나 대규모 문서에서 텍스트를 추출하는 시스템을 구축할 수 있습니다. 또한, 성능 최적화 단계에서는 GPU 사용, 배치 처리, 병렬 처리 등을 고려하여 OCR 시스템의 처리 속도를 개선할 수 있습니다.