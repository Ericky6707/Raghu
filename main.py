from flask import Flask, request, render_template_string
import requests
import random
import time

app = Flask(__name__)

# 🔹 Simple HTML Form for User Input
HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Facebook Auto Comment</title>
    <style>
        body { background-color: black; color: white; text-align: center; font-family: Arial, sans-serif; }
        input, textarea { width: 300px; padding: 10px; margin: 5px; border-radius: 5px; }
        button { background-color: green; color: white; padding: 10px 20px; border: none; border-radius: 5px; }
    </style>
</head>
<body>
    <h1>Facebook Auto Comment (Cookies-Based)</h1>
    <form method="POST">
        <input type="text" name="c_user" placeholder="Enter c_user Cookie" required><br>
        <input type="text" name="xs" placeholder="Enter xs Cookie" required><br>
        <input type="text" name="fr" placeholder="Enter fr Cookie" required><br>
        <input type="text" name="post_url" placeholder="Enter Facebook Post URL" required><br>
        <input type="text" name="comment" placeholder="Enter Your Comment" required><br>
        <button type="submit">Post Comment</button>
    </form>
    {% if message %}<p>{{ message }}</p>{% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        c_user = request.form['c_user']
        xs = request.form['xs']
        fr = request.form['fr']
        post_url = request.form['post_url']
        comment = request.form['comment']

        # Extract Post ID
        try:
            post_id = post_url.split("posts/")[1].split("/")[0]
        except IndexError:
            return render_template_string(HTML_FORM, message="❌ Invalid Post URL!")

        # Set Cookies
        cookies = {
            "c_user": c_user,
            "xs": xs,
            "fr": fr
        }

        # Random User-Agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (X11; Linux x86_64)"
        ]
        headers = {
            "User-Agent": random.choice(user_agents),
            "Referer": f"https://www.facebook.com/{post_url}"
        }

        # Send Comment Request
        url = f"https://www.facebook.com/{post_id}"
        data = {"comment_text": comment, "submit": "Post"}
        response = requests.post(url, cookies=cookies, headers=headers, data=data)

        if response.status_code == 200:
            return render_template_string(HTML_FORM, message=f"✅ Comment Posted: {comment}")
        else:
            return render_template_string(HTML_FORM, message=f"❌ Failed! Response: {response.text}")

    return render_template_string(HTML_FORM)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
