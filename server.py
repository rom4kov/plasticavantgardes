from flask import Flask, render_template
from random import randint
from datetime import datetime
import requests
import json

app = Flask(__name__)


@app.route("/")
def home():
    rand_num = randint(1, 3)
    year = datetime.now().year
    return render_template("index.html", num=rand_num, year=year)


@app.route("/guess/<name>")
def guess(name):
    genderize_response = requests.get(f"https://api.genderize.io?name={name}").text
    agify_response = requests.get(f"https://api.agify.io?name={name}").text
    guessed_age = json.loads(agify_response)['age']
    guessed_gender = json.loads(genderize_response)['gender']
    gender_prob = json.loads(genderize_response)['probability']
    return render_template("guess.html",
                           name=name.title(),
                           gender=guessed_gender,
                           age=guessed_age,
                           probability=gender_prob)


@app.route("/blog/<num>")
def get_blog(num):
    blog_url = "https://api.npoint.io/c790b4d5cab58020d391"
    response = requests.get(blog_url)
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts, num=int(num))


if __name__ == "__main__":
    app.run(debug=True)
