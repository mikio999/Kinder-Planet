import requests
from bs4 import BeautifulSoup
import firebase_admin 
from firebase_admin import credentials, firestore
from datetime import datetime

# Firebase 초기화
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def format_date(date_str):
    """날짜를 YYYY-MM-DD 형식으로 변환"""
    current_year = datetime.now().year
    month, day = map(int, date_str.split('/'))

    # 12월 데이터가 1월에 수집된 경우, 년도를 하나 줄임
    if month == 12 and datetime.now().month == 1:
        current_year -= 1

    return f"{current_year}-{month:02}-{day:02}"

def is_existing_job(link):
    """Firestore에서 동일한 링크가 존재하는지 확인"""
    docs = db.collection("gogane_jobs").where("link", "==", link).stream()
    return any(docs)  # 하나라도 존재하면 True

# ✅ Scraping 대상 URL
url = "https://www.gogane.kr/c/main.cgi?board=gi5&ryal=&view=2&back=&search=%EC%84%9C%EC%9A%B8&where=5&how=1"

response = requests.get(url)
response.encoding = 'euc-kr'  # 한글 페이지 인코딩 설정

soup = BeautifulSoup(response.text, 'html.parser')

job_postings = []

for row in soup.find_all('tr'):
    location_cell = row.find('td', class_='CellStyle8')
    location = location_cell.get_text(strip=True) if location_cell else "위치 미정"

    title_cell = row.find('td', class_='CellStyle2')
    date_cell = row.find('td', class_='CellStyle4')
    link_cell = title_cell.find('a', href=True) if title_cell else None

    if title_cell and date_cell and link_cell:
        title = f"[{location}] {title_cell.text.strip()}" 
        date = format_date(date_cell.text.strip()) 
        link = "https://www.gogane.kr/c/" + link_cell['href']

        job_posting = {'title': title, 'date': date, 'link': link}

        # ✅ 중복 검사 후 Firestore에 저장
        if not is_existing_job(link):
            db.collection("gogane_jobs").add(job_posting)
            print(f"✅ Firestore에 저장: {title} ({link})")

print("🔥 Firestore 업데이트 완료!")
