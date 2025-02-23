from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
import time
from datetime import datetime
import re  # 정규 표현식 사용

# ✅ Firestore 초기화
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ✅ Chrome WebDriver 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # GUI 없이 실행
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ✅ Chrome WebDriver 실행 (경로 지정 없이)
driver = webdriver.Chrome(options=chrome_options)

# ✅ 서울시 교육청 구인구직 페이지 URL
url = "https://work.sen.go.kr/work/search/recInfo/BD_selectSrchRecInfo.do?school=cst001&q_srchType=rcrtTtl&q_srchText=&q_currPage=1&q_rowPerPage=15&q_srchArea=&q_srchSchl=cst001&q_tabId=schlTab&q_sortBy=regDt&q_mySrchArea=&q_srchJob=&q_recClosed=closed&q_today=&q_jobCategory="
driver.get(url)
time.sleep(5)  # 🚨 페이지 로딩 대기

# ✅ HTML 가져오기
soup = BeautifulSoup(driver.page_source, "html.parser")

# ✅ Firestore 중복 검사 함수
def is_existing_job(link):
    docs = db.collection("seoul_jobs").where("link", "==", link).stream()
    return any(docs)

# ✅ 구인 공고 데이터 수집
job_postings = []

for job in soup.select("ul > li.flex_cont"):
    try:
        # 📝 유치원명, 등록일 정보가 들어있는 span
        info_span = job.select_one("span.s_title")
        if not info_span:
            continue

        # 📝 제목과 링크
        title_element = job.select_one("h4.list_title a")
        if not title_element:
            continue
        
        title = title_element.text.strip()
        link = "https://work.sen.go.kr" + title_element["href"]

        # 📝 등록일
        date_text = info_span.text.strip().split("|")[2].replace("등록일 :", "").strip()
        date = datetime.strptime(date_text, "%Y-%m-%d").strftime("%Y-%m-%d")

        # 📝 지역 정보 가져오기 (00구로 끝나는 경우만)
        location = "지역 미확인"
        location_elements = job.select("span.border-r")

        for loc in location_elements:
            loc_text = loc.text.strip()
            if re.search(r".*구$", loc_text):  # "00구"로 끝나는 경우만 지역으로 저장
                location = loc_text
                break  # 첫 번째로 찾은 구 이름을 사용하고 종료

        # ✅ 지역을 포함한 새로운 제목 생성
        full_title = f"[{location}] {title}"

        # ✅ Firestore에 저장할 데이터
        job_posting = {"title": full_title, "date": date, "link": link}

        # 🔥 Firestore 중복 검사 후 저장
        if not is_existing_job(link):
            db.collection("seoul_jobs").add(job_posting)
            print(f"✅ Firestore에 저장: {full_title} ({link})")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

driver.quit()
print("🔥 Firestore 업데이트 완료!")
