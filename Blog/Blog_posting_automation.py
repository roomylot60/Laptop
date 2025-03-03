from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# 기존에 실행 중인 Chrome을 활용하기 위한 설정
CHROME_DEBUG_PORT = 9222  # 기존 Chrome을 실행할 때 설정한 디버그 포트

# 게시할 글 정보
POST_TITLE = "자동 포스팅 테스트 (Selenium)"
POST_CONTENT = """<h2>Python을 이용한 자동 포스팅</h2>
<p>이 글은 기존 Chrome 창을 활용하여 자동으로 게시되었습니다.</p>
<pre><code>print("Hello, Blogger!")</code></pre>"""

def create_new_post(driver):
    """새 글 작성 및 게시"""
    driver.get("https://www.blogger.com/blog/posts/8534340124223051273")  # 본인 블로그 ID 변경
    time.sleep(3)

    # "새 게시물" 버튼 클릭
    new_post_btn = driver.find_element(By.XPATH, "//div[contains(text(),'새 게시물')]")
    new_post_btn.click()
    time.sleep(3)

    # 제목 입력
    title_input = driver.find_element(By.XPATH, "//input[@placeholder='제목 추가']")
    title_input.send_keys(POST_TITLE)
    time.sleep(2)

    # 본문 입력
    content_input = driver.find_element(By.XPATH, "//div[@aria-label='게시물 본문']")
    content_input.send_keys(POST_CONTENT)
    time.sleep(2)

    # 게시 버튼 클릭
    post_button = driver.find_element(By.XPATH, "//span[contains(text(),'게시')]")
    post_button.click()
    time.sleep(5)

    print("✅ 포스트 게시 완료!")

if __name__ == "__main__":
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.debugger_address = f"127.0.0.1:{CHROME_DEBUG_PORT}"

    # 기존 Chrome 창에 연결
    driver = webdriver.Chrome(options=chrome_options)

    try:
        create_new_post(driver)
    finally:
        driver.quit()
