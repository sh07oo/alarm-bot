import requests
from bs4 import BeautifulSoup
import time
import smtplib
from email.message import EmailMessage


class Notification:
    def __init__(self, gallery_url, use_desktop, use_mobile, email, password, keywords):
        self.gallery_url = gallery_url
        self.use_mobile = use_mobile
        self.email = email
        self.password = password
        self.keywords = keywords
        self.article_set = set()

    def fetch_articles(self):
        response = requests.get(self.gallery_url)
        soup = BeautifulSoup(response.content, "html.parser")
        titles = soup.select("tr.ub-content.us-post > td.gall_tit.ub-word > a")
        articles = {}

        for title in titles:
            href = title["href"]
            if not href.startswith("http"):
                href = "https://gall.dcinside.com" + href
            articles[href] = title.text.strip()

        return articles

    def send_email(self, title, link):
        msg = EmailMessage()
        msg["Subject"] = f"새 글 발견: {title}"
        msg["From"] = self.email
        msg["To"] = self.email
        msg.set_content(f"{title}\n\n{link}")

        with smtplib.SMTP_SSL("smtp.naver.com", 465) as smtp:
            smtp.login(self.email, self.password)
            smtp.send_message(msg)

    def run(self):
        while True:
            try:
                articles = self.fetch_articles()
                for link, title in articles.items():
                    if link not in self.article_set and any(k in title for k in self.keywords):
                        self.article_set.add(link)
                        print(f"새 글: {title} - {link}")
                        if self.use_mobile:
                            self.send_email(title, link)
            except Exception as e:
                print("오류 발생:", e)

            time.sleep(2)  # 30초마다 새 글 확인
