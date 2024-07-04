from __future__ import annotations
from flask_login import UserMixin
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from extensions import db
from typing import List


class User(db.Model, UserMixin):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    posts: Mapped[List["BlogPost"]] = relationship(back_populates="author")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")


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
    comments: Mapped[List["Comment"]] = relationship(back_populates="blog_post")


class Comment(db.Model):
    __tablename__ = "comment_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    body: Mapped[str] = mapped_column(String(5000), unique=True, nullable=False)
    date: Mapped[str] = mapped_column(String(25), nullable=False)
    blog_post: Mapped["BlogPost"] = relationship(back_populates="comments")
    blog_post_id: Mapped[int] = mapped_column(ForeignKey("blog_post_table.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    author_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
