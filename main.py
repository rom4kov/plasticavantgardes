from flask import Flask, render_template
import requests


app = Flask(__name__)

blog_url = "https://api.npoint.io/19dfc80fb6109528f946"
response = requests.get(blog_url)
all_posts = response.json()


@app.route('/')
def home():
    return render_template("index.html", posts=all_posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/posts/<num>')
def get_post(num):
    return render_template("post.html", post=all_posts[int(num) - 1])


if __name__ == "__main__":
    app.run(debug=True)
