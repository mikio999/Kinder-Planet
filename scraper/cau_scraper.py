import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def format_date(date_str):
    current_year = datetime.now().year
    month, day = map(int, date_str.split('-'))

    # 12월 데이터가 1월에 수집된 경우, 년도를 하나 줄임
    if month == 12 and datetime.now().month == 1:
        current_year -= 1

    return f"{current_year}-{month:02}-{day:02}"

url = "https://cauece.cau.ac.kr/bbs/board.php?bo_table=s0405"
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

job_postings = []

for row in soup.find_all('tr'):
    title_cell = row.find('td', class_='fz_subject')
    date_cell = next((td for td in row.find_all('td', class_='td_num') if '-' in td.text), None)

    link_tag = title_cell.find('a') if title_cell else None
    link = link_tag['href'] if link_tag else None

    if title_cell and date_cell and link:
        title = title_cell.get_text(strip=True).replace("파일첨부", "").replace("텍스트", "")
        date = format_date(date_cell.text.strip())

        if not link.startswith("http"):
            link = f"https://cauece.cau.ac.kr{link}"

        job_postings.append({'title': title, 'date': date, 'link': link})

for job in job_postings:
    db.collection("cau_jobs").add(job)
    print(f"✅ Firestore에 저장: {job['title']} ({job['link']}")

print("🔥 Firestore 업데이트 완료!")
