import requests
from bs4 import BeautifulSoup
import firebase_admin
from firebase_admin import credentials, firestore

# Firebase 초기화 (서비스 계정 JSON 파일 사용)
cred = credentials.Certificate("firebase-adminsdk.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# URL 설정
url = "https://cauece.cau.ac.kr/bbs/board.php?bo_table=s0405"
response = requests.get(url)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'html.parser')

job_postings = []

# 'tr' 태그를 순회하며 각 게시글의 제목, 날짜, URL 추출
for row in soup.find_all('tr'):
    title_cell = row.find('td', class_='fz_subject')
    date_cell = next((td for td in row.find_all('td', class_='td_num') if '-' in td.text), None)

    # a 태그에서 href 추출
    link_tag = title_cell.find('a') if title_cell else None
    link = link_tag['href'] if link_tag else None

    if title_cell and date_cell and link:
        title = title_cell.get_text(strip=True).replace("파일첨부", "").replace("텍스트", "")
        date = date_cell.text.strip()

        # 상대 경로일 경우만 도메인을 추가
        if not link.startswith("http"):
            link = f"https://cauece.cau.ac.kr{link}"

        job_postings.append({'title': title, 'date': date, 'link': link})

# Firestore에 저장
for job in job_postings:
    db.collection("cau_jobs").add(job)
    print(f"✅ Firestore에 저장: {job['title']} ({job['link']})")

print("🔥 Firestore 업데이트 완료!")
