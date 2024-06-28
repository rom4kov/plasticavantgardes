from datetime import datetime
from smtplib import SMTP

import bleach
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

from flask import Flask, redirect, render_template, request, url_for
from flask_login import LoginManager, UserMixin
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from forms import CreatePostForm, RegisterForm, LoginForm

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

ckeditor = CKEditor(app)


class BlogPost(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    date: Mapped[str] = mapped_column(String(25), nullable=False)
    body: Mapped[str] = mapped_column(String(5000), unique=True, nullable=False)
    author: Mapped[str] = mapped_column(String(100), nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)

    # def __init__(self, title: str, subtitle: str, author: str, img_url: str, body: str, date: str):
    #     self.title = title
    #     self.subtitle = subtitle
    #     self.author = author
    #     self.img_url = img_url
    #     self.body = body
    #     self.body = date


class User(db.Model, UserMixin):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)


def cleanify(text, *, allow_tags=None):
    """
    Clean the input from client, this function rely on bleach.

    parm text: input str
    parm allow_tags: if you don't want to use default `allow_tags`,
        you can provide an Iterable which include html tag string like ['a', 'li',...].
    """
    default_allowed_tags = {'a', 'abbr', 'b', 'blockquote', 'br', 'code',
                            'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                            'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'}
    return bleach.clean(text, tags=allow_tags or default_allowed_tags)


@app.route('/')
def home():
    all_posts = db.session.execute(db.select(BlogPost).order_by(BlogPost.date)).scalars()
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


@app.route('/posts/<post_id>')
def get_post(post_id):
    post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    return render_template("post.html", post=post)


@app.route('/new-post', methods=['GET', 'POST'])
def new_post():
    form = CreatePostForm()
    date = datetime.now().date().strftime("%B %d, %Y")
    heading = request.args.get('heading')
    if form.validate_on_submit():
        new_blogpost = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            # author=form.author.data,
            img_url=form.img_url.data,
            body=form.body.data,
            date=date
        )
        with app.app_context():
            db.session.add(new_blogpost)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template("make-post.html", form=form, heading=heading)


@app.route('/edit-post/<post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    with app.app_context():
        post = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()

        if post is None:
            return redirect(url_for('home'))

        form = CreatePostForm(
            title=post.title,
            subtitle=post.subtitle,
            author=post.author,
            img_url=post.img_url,
            body=post.body,
            date=post.date
        )
        heading = request.args.get('heading')
        if form.validate_on_submit():
            post.title = request.form.get('title')
            post.subtitle = request.form.get('subtitle')
            post.author = request.form.get('author')
            post.img_url = request.form.get('img_url')
            post.body = cleanify(request.form.get('ckeditor'))
            post.date = post.date
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("make-post.html", form=form, post=post, heading=heading)


@app.route('/delete/<post_id>')
def delete(post_id):
    post_to_delete = db.session.execute(db.select(BlogPost).where(BlogPost.id == post_id)).scalar()
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            name=request.form.name,  # type: ignore
            email=request.form.email,  # type: ignore
            password=generate_password_hash(request.form.password, method='pbkdf2', salt_length=8)  # type: ignore
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("register.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    pass


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    email = form.email.data
    password = form.password.data
    if form.validate_on_submit() and email == "admin@email.com" and password == "12345678":
        return render_template("success.html")
    elif form.validate_on_submit() and (email != "admin@email.com" or password != "12345678"):
        return render_template("denied.html")
    return render_template("login.html", form=form)


if __name__ == "__main__":
    app.secret_key = "Q!92;x(t9}u#K9U)#)b.=YtP3}e=o?VX*,j"
    app.run(debug=True)
