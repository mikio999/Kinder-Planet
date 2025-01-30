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
    current_year = datetime.now().year
    month, day = map(int, date_str.split('/'))

    # 12월 데이터가 1월에 수집된 경우, 년도를 하나 줄임
    if month == 12 and datetime.now().month == 1:
        current_year -= 1

    return f"{current_year}-{month:02}-{day:02}"

# URL 설정
url = "https://www.gogane.kr/c/main.cgi?board=gi5&ryal=&view=2&back=&search=%EC%84%9C%EC%9A%B8&where=5&how=1"

# URL로부터 HTML 페이지 가져오기
response = requests.get(url)
response.encoding = 'euc-kr'  # 인코딩 설정 (필요한 경우)

# HTML 페이지를 BeautifulSoup 객체로 파싱
soup = BeautifulSoup(response.text, 'html.parser')

# 채용공고와 날짜 데이터 추출
job_postings = []

# 'tr' 태그를 순회하며 각 게시글의 제목, 날짜, 링크 추출
for row in soup.find_all('tr'):
    location_cell = row.find('td', class_='CellStyle8')
    location = location_cell.get_text(strip=True) if location_cell else "위치 미정"

    title_cell = row.find('td', class_='CellStyle2')
    date_cell = row.find('td', class_='CellStyle4')
    link_cell = title_cell.find('a', href=True) if title_cell else None

    if title_cell and date_cell and link_cell:
        title = f"[{location}] {title_cell.text.strip()}"  # 위치 정보를 제목에 포함
        date = format_date(date_cell.text.strip())  # 날짜 형식 변환
        link = "https://www.gogane.kr/c/" + link_cell['href']
        job_postings.append({'title': title, 'date': date, 'link': link})

# Firestore에 데이터 저장
for job in job_postings:
    db.collection("gogane_jobs").add(job)
    print(f"✅ Firestore에 저장: {job['title']} ({job['link']})")

print("🔥 Firestore 업데이트 완료!")
