from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

file_path = os.path.join(os.getcwd(), "data/privacy.txt")

# 파일 열기
with open(file_path, "r", encoding='utf-8') as file:
    contents = file.readlines()
    contents = [content.strip() for content in contents]
    contents = [content.split(" : ")[1] for content in contents]
# print(contents)
        
# Velog 로그인 정보
USERNAME = contents[0]
PASSWORD = contents[1]

# 포스팅할 내용
TITLE = "자동화된 Velog 포스팅 🚀"
CONTENT = """# 📢 자동 포스팅 성공!
이 글은 `Selenium`을 사용해 자동으로 작성되었습니다.
"""

# 웹드라이버 설정 (Chrome 기준)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # 창 최대화
driver = webdriver.Chrome(options=options)

try:
    # 1️⃣ Velog 로그인 페이지 이동
    driver.get("https://velog.io/")
    time.sleep(1)

    # 2️⃣ 로그인 버튼 클릭
    login_button = driver.find_element(By.XPATH, "//*[@id='html']/body/div/div[2]/div[2]/div/header/div/div[2]/button")
    login_button.click()
    time.sleep(1)

    # 3️⃣ GitHub 로그인 클릭 (Velog는 GitHub 로그인 방식 사용)
    github_login = driver.find_element(By.XPATH, "//*[@id='html']/body/div/div[3]/div/div[2]/div[2]/div/div[1]/section[2]/div/a[1]")
    github_login.click()
    time.sleep(1)

     # 4️⃣ GitHub 로그인 (이미 로그인된 경우 자동 건너뜀)
    username_input = driver.find_element(By.ID, "login_field")
    password_input = driver.find_element(By.ID, "password")

    username_input.send_keys(USERNAME)
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.RETURN)
    time.sleep(3)

    # 5️⃣ 새 글 작성 페이지 이동
    driver.get("https://velog.io/write")
    time.sleep(3)

    # WebDriverWait을 사용하여 요소가 로드될 때까지 대기
    wait = WebDriverWait(driver, 3)

    # 6️⃣ 제목 입력
    title_input = wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='root']/div[2]/div/div[1]/div/div[1]/div[1]/div/textarea")))

    # 기존 텍스트를 지우고 새로운 제목 입력
    title_input.clear()
    title_input.send_keys(TITLE)
    # X_path of tags : //*[@id='root']/div[2]/div/div[1]/div/div[1]/div[1]/div/div[2]/div/input
    
    # # 7️⃣ 본문 입력
    # content_input = driver.find_element(By.CLASS_NAME, "tui-editor-contents")
    # content_input.send_keys(CONTENT)

    # # 8️⃣ 공개 설정 후 발행 버튼 클릭
    # publish_button = driver.find_element(By.XPATH, "//button[contains(text(), '출간하기')]")
    # publish_button.click()
    # time.sleep(3)

    # confirm_button = driver.find_element(By.XPATH, "//button[contains(text(), '출간하기')]")
    # confirm_button.click()
    # time.sleep(3)

    # print("✅ Velog 포스팅이 자동으로 완료되었습니다!")

except Exception as e:
    print(f"❌ 오류 발생: {e}")

finally:
    driver.quit()
