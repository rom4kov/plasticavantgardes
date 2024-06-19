from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import requests
from smtplib import SMTP

app = Flask(__name__)

blog_url = "https://api.npoint.io/19dfc80fb6109528f946"
response = requests.get(blog_url)
all_posts = response.json()


class LoginForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Password:', validators=[DataRequired(), Length(8)])
    submit = SubmitField(label='Log In')


@app.route('/')
def home():
    return render_template("index.html", posts=all_posts)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        email = "aaronfeininger@gmail.com"
        password = 'svnsqsyfwnzwjahl'
        data = request.form

        with SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=email, password=password)
            connection.sendmail(
                from_addr=email,
                to_addrs="rkowert@posteo.de",
                msg=f"Subject:Du hast eine neue Nachricht\n\n"
                    f"Betreff: {data['subject']}\n\n"
                    f"{data['name']} schreibt:\n\n"
                    f"{data['message']}\n\n"
                    f"Du kannst antworten an: {data['email']}")
            print("Email sent!")
        return render_template("contact.html", flash_message="Email successfully sent!")
    else:
        return render_template("contact.html")


@app.route('/posts/<num>')
def get_post(num):
    return render_template("post.html", post=all_posts[int(num) - 1])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    if form.validate_on_submit() and email == "admin@email.com" and password == "12345678":
        return render_template("success.html")
    elif form.validate_on_submit() and not email == "admin@email.com" and not password == "12345678":
        return render_template("denied.html")
    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.secret_key = "Q!92;x(t9}u#K9U)#)b.=YtP3}e=o?VX*,j"
    app.run(debug=True)
