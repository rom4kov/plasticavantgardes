from __future__ import annotations
from datetime import datetime
from smtplib import SMTP

import bleach

from typing import List

from flask import Flask, redirect, render_template, request, url_for, session, flash
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
from flask_ckeditor import CKEditor
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm

app = Flask(__name__)
app.secret_key = b'94551be546b23efeac0374ea76d056dfe962b1f0e928a2fcdd06d9bf8a717367'


class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

ckeditor = CKEditor()
ckeditor.init_app(app)


class User(db.Model, UserMixin):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    posts: Mapped[List["BlogPost"]] = relationship(back_populates="author")


class BlogPost(db.Model):
    __tablename__ = "blog_post_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    date: Mapped[str] = mapped_column(String(25), nullable=False)
    body: Mapped[str] = mapped_column(String(5000), unique=True, nullable=False)
    img_url: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    author: Mapped["User"] = relationship(back_populates="posts")
    author_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))


class Comment(db.Model):
    __tablename__ = "comment"


# with app.app_context():
#     db.create_all()


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
    print(app.config)
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
    form = CommentForm()
    return render_template("post.html", post=post, form=form)


@app.errorhandler(401)
def custom_401(error):
    return redirect(url_for('home'))


@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('You need to be logged in to access this page.')
    return redirect(url_for('login'))


def admin_only(function):
    def wrapper(*args, **kwargs):
        if current_user and current_user.id == 1:
            return function(*args, **kwargs)
        else:
            flash("You are not authorized to access this route.")
            return redirect(url_for('home'))
    wrapper.__name__ = function.__name__
    return wrapper


@app.route('/new-post', methods=['GET', 'POST'])
@login_required
@admin_only
def new_post():
    form = CreatePostForm()
    date = datetime.now().date().strftime("%B %d, %Y")
    heading = request.args.get('heading')
    print(request.form.get('ckeditor'))
    if form.validate_on_submit():
        print("form validated")
        new_blogpost = BlogPost(  # type: ignore
            title=request.form.get('title'),
            subtitle=request.form.get('subtitle'),
            img_url=request.form.get('img_url'),
            body=request.form.get('ckeditor'),
            author=current_user,
            author_id=current_user.id,
            date=date,
        )
        db.session.add(new_blogpost)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("make-post.html", form=form, heading=heading)


@app.route('/edit-post/<post_id>', methods=['GET', 'POST'])
@login_required
@admin_only
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
        date = datetime.now().date().strftime("%B %d, %Y")
        if form.validate_on_submit():
            print(request.form.get('ckeditor'))
            for field in post.__table__.columns:
                if field.name == 'date' and date != str(getattr(post, 'date')):
                    setattr(post, 'date', date)
                else:
                    new_value = request.form.get(field.name)
                    if new_value and new_value != str(getattr(post, field.name)):
                        setattr(post, field.name, new_value)
            db.session.commit()
            return redirect(url_for('home'))
    return render_template("make-post.html", form=form, post=post, heading=heading)


@app.route('/delete/<post_id>')
@login_required
@admin_only
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
            name=request.form.get('name'),  # type: ignore
            email=request.form.get('email'),  # type: ignore
            password=generate_password_hash(request.form.get('password'),  # type: ignore
                                            method='pbkdf2', salt_length=8)  # type: ignore
        )
        try:
            db.session.add(new_user)
            db.session.commit()
        except IntegrityError:
            flash("Someone already signed up with that email. If it's you, log in instead.")
            return redirect(url_for('login'))
        else:
            user = db.session.execute(db.select(User).where(User.email == request.form.get('email'))).scalar()
            session['username'] = user.name # type: ignore
            login_user(user)
            flash("You were successfully registered")
            return redirect(url_for('home'))
    return render_template("register.html", form=form)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.execute(db.select(User).where(User.email == request.form['email'])).scalar()
        if user:
            if check_password_hash(user.password, request.form['password']):
                login_user(user)
                session['username'] = user.name
                flash('You have been successfully logged in.')
                return redirect(url_for('home'))
            else:
                flash('Incorrect password. Please try again.')
        else:
            flash('No user found with that email.')
    return render_template("login.html", form=form)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash('You have been successfully logged out.')
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.secret_key = "Q!92;x(t9}u#K9U)#)b.=YtP3}e=o?VX*,j"
    app.run(debug=True)
