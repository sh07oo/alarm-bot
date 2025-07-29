import os
from notification import Notification

if __name__ == "__main__":
    EMAIL = os.environ.get("EMAIL")
    PASSWD = os.environ.get("PASSWD")

    gallery_url = "https://gall.dcinside.com/mgallery/board/lists?id=seunjae"  # 원하는 갤러리 주소
    keyword_list = None

    notifier = Notification(
        gallery_url=gallery_url,
        use_desktop=False,
        use_mobile=True,
        email=EMAIL,
        password=PASSWD,
        keywords=keyword_list
    )
    notifier.run()
