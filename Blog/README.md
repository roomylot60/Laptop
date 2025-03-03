#### 1. 사전 준비
먼저, Google Cloud에서 API를 활성화하고 OAuth 인증을 설정해야 합니다.

1) Google API Console에서 API 키 및 OAuth 설정
Google API Console(링크)에 접속
새 프로젝트 생성 (Blogger API 사용)
Blogger API v3 활성화
OAuth 2.0 클라이언트 ID 설정
credentials.json 다운로드

#### 2. 필요한 라이브러리 설치
아래 명령어로 필요한 패키지를 설치합니다.

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 googleapiclient
```

#### 3. Python 코드 작성
Selenium과 Request를 활용한 웹 자동화

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from webdriver_manager.chrome import ChromeDriverManager

# Blogger 로그인 정보
EMAIL = "min2max.dev@gmail.com"
PASSWORD = "gensou4075"
BLOGGER_URL = "https://www.blogger.com/"  # Blogger 로그인 URL

# 게시할 글 정보
POST_TITLE = "자동 포스팅 테스트 (Selenium)"
POST_CONTENT = """<h2>Python을 이용한 자동 포스팅</h2>
<p>이 글은 Selenium을 이용하여 자동으로 게시되었습니다.</p>
<pre><code>print("Hello, Blogger!")</code></pre>"""

def login_to_blogger(driver):
    """Blogger 로그인 수행"""
    driver.get(BLOGGER_URL)
    time.sleep(2)

    # 이메일 입력
    email_input = driver.find_element(By.ID, "identifierId")
    email_input.send_keys(EMAIL)
    email_input.send_keys(Keys.ENTER)
    time.sleep(3)

    # 비밀번호 입력
    password_input = driver.find_element(By.NAME, "password")
    password_input.send_keys(PASSWORD)
    password_input.send_keys(Keys.ENTER)
    time.sleep(5)

def create_new_post(driver):
    """새 글 작성 및 게시"""
    # 새 글 작성 버튼 클릭
    driver.get("https://www.blogger.com/blog/posts/your-blog-id")  # 본인 블로그 URL로 변경
    time.sleep(3)

    # "새 글 작성" 버튼 클릭
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
    # 웹 드라이버 실행
    driver = webdriver.Chrome(ChromeDriverManager().install())

    try:
        login_to_blogger(driver)
        create_new_post(driver)
    finally:
        driver.quit()
```
#### 4. 실행 방법
`credentials.json` 파일을 프로젝트 폴더에 저장
위 코드를 실행 (`python script.py`)
최초 실행 시 브라우저에서 Google 계정 로그인 및 인증
승인 후 자동으로 Blogger에 글이 게시됨
추가 기능
게시글 업데이트: `service.posts().update()` 사용
삭제: `service.posts().delete()` 사용
예약 게시: published 필드에 날짜 추가
