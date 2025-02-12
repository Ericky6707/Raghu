from flask import Flask, render_template_string, request, jsonify
import requests
import time

app = Flask(__name__)

# Function to comment on Facebook post using Token
def comment_using_token(post_id, token, message):
    url = f"https://graph.facebook.com/{post_id}/comments"
    payload = {'access_token': token, 'message': message}
    response = requests.post(url, data=payload)
    return response

# Function to comment on Facebook post using Cookies (custom approach)
def comment_using_cookies(post_url, cookies, message):
    headers = {'User-Agent': 'Mozilla/5.0', 'referer': post_url}
    response = requests.post(post_url, data={'message': message}, cookies=cookies, headers=headers)
    return response

# Function to fetch all post IDs from a page URL
def fetch_all_posts_from_page(page_url, token):
    page_id = page_url.split('/')[-1]  # Extract the page ID from URL
    url = f"https://graph.facebook.com/{page_id}/posts?access_token={token}"
    response = requests.get(url)
    
    if response.ok:
        posts_data = response.json()
        return [post['id'] for post in posts_data['data']]  # List of post IDs
    else:
        print(f"Error fetching posts: {response.status_code} - {response.text}")
        return []

# HTML template for the form
html_form = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facebook Auto Commenter</title>
</head>
<body>
    <h2>Facebook Auto Commenter</h2>
    <form method="POST">
        <label for="page_url">Page URL:</label><br>
        <input type="text" id="page_url" name="page_url" placeholder="Enter Facebook Page URL" required><br><br>

        <label for="token">Facebook Token (Optional):</label><br>
        <input type="text" id="token" name="token" placeholder="Enter Facebook Token"><br><br>

        <label for="cookies">Facebook Cookies (Optional):</label><br>
        <textarea id="cookies" name="cookies" placeholder="Enter cookies in key=value format, separated by semicolons."></textarea><br><br>

        <label for="message">Message:</label><br>
        <input type="text" id="message" name="message" placeholder="Enter your comment message" required><br><br>

        <label for="time_set">Time Delay (in seconds):</label><br>
        <input type="number" id="time_set" name="time_set" value="0"><br><br>

        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        token = request.form.get("token", "").strip()
        cookies = request.form.get("cookies", "").strip()
        page_url = request.form.get("page_url", "").strip()
        message = request.form.get("message", "").strip()
        time_set = int(request.form.get("time_set", 0))

        # Fetch all post IDs from the page
        post_ids = fetch_all_posts_from_page(page_url, token)

        # Delay before sending the comment
        time.sleep(time_set)

        # Post comments on all posts
        success_count = 0
        failure_count = 0
        for post_id in post_ids:
            if token:
                response = comment_using_token(post_id, token, message)
            elif cookies:
                cookies_dict = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in cookies.split(';')}
                response = comment_using_cookies(page_url, cookies_dict, message)
            else:
                return jsonify({"error": "No token or cookies provided!"})

            if response.ok:
                success_count += 1
            else:
                failure_count += 1

        return jsonify({
            "success": f"Successfully commented on {success_count} posts.",
            "failed": f"Failed to comment on {failure_count} posts."
        })

    return render_template_string(html_form)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
