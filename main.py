import requests
import time
import random
from flask import Flask

app = Flask(__name__)

# 🔹 Facebook Post ID Extract Function
def get_post_id(post_url):
    try:
        return post_url.split("posts/")[1].split("/")[0]
    except IndexError:
        return None

# 🔹 User-Agent List (Rotation Ke Liye)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_2 like Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.77 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10; SM-G970F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.81 Mobile Safari/537.36"
]

# 🔹 Facebook Post Link
POST_URL = "https://www.facebook.com/100046233720065/posts/555023942715392/?mibextid=rS40aB7S9Ucbxw6v"

# 🔹 Facebook Cookies
COOKIES = "datr=D4ywZ0X9E6MNjCvoCTxIA_le; sb=D4ywZ7gtjO-nHIqqV1zaReOQ; m_pixel_ratio=2; wd=360x615; c_user=61560080098210; fr=0XtupZy5Zm5Cl6zAg.AWWX9O9yg36LSiuCPEQ4Hd0jzKJfo5iyzHeZdQ.BnsIwP..AAA.0.0.BnsIx-.AWVUEbsaX2c; xs=47%3A94hSMKEjmUMb4w%3A2%3A1739623556%3A-1%3A13669; locale=en_GB; ps_l=1; ps_n=1; wl_cbv=v2%3Bclient_version%3A2741%3Btimestamp%3A1739623566; fbl_st=100620419%3BT%3A28993726; vpd=v1%3B615x360x2"

# 🔹 Comments List
COMMENTS = [
    "Samart x3 yash here 😝",
    "Wow, amazing post! 😍",
    "Bohot badiya post! 🔥",
    "Nice one! 👍",
    "Keep it up bro! 💯"
]

# 🔹 Comment Posting Function
def post_comment():
    post_id = get_post_id(POST_URL)
    if not post_id:
        print("❌ Invalid Post URL!")
        return

    url = f"https://www.facebook.com/ufi/add/comment/?ft_ent_identifier={post_id}"
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": COOKIES,
        "Referer": "https://www.facebook.com/",
        "Origin": "https://www.facebook.com",
        "Accept-Language": "en-US,en;q=0.9",
        "DNT": "1",
        "Connection": "keep-alive"
    }
    payload = {
        "comment_text": random.choice(COMMENTS)
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        print(f"✅ Comment Posted Successfully!")
    else:
        print(f"❌ Failed to Post Comment! Status Code: {response.status_code}")
        print(response.text)

# 🔹 Flask Route
@app.route('/')
def home():
    return "✅ Facebook Auto Commenter Running!"

# 🔹 Background Loop For Auto Commenting
def start_commenting():
    while True:
        post_comment()
        time.sleep(100)  # 300 sec = 5 min delay

if __name__ == '__main__':
    from threading import Thread
    Thread(target=start_commenting).start()  # Auto-comment loop start hoga
    app.run(host='0.0.0.0', port=10000)
