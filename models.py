from __future__ import annotations
from flask_login import UserMixin
from sqlalchemy import Integer, String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from extensions import db
from typing import List


class Base(DeclarativeBase):
    pass


posts_association_table = Table(
    "posts_association_table",
    db.Model.metadata,
    Column("user_id", ForeignKey("user_table.id"), primary_key=True),
    Column("blog_post_id", ForeignKey("blog_post_table.id"), primary_key=True),
)

comments_association_table = Table(
    "comment_association_table",
    db.Model.metadata,
    Column("user_id", ForeignKey("user_table.id"), primary_key=True),
    Column("comments_id", ForeignKey("comment_table.id"), primary_key=True),
)


class User(db.Model, UserMixin):
    __tablename__ = "user_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    posts: Mapped[List["BlogPost"]] = relationship(back_populates="author")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")
    liked_posts: Mapped[List["BlogPost"]] = relationship(secondary=posts_association_table, back_populates="likes")
    liked_comments: Mapped[List["Comment"]] = relationship(secondary=comments_association_table, back_populates="likes")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


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
    likes: Mapped[List["User"]] = relationship(secondary=posts_association_table, back_populates="liked_posts")


class Comment(db.Model):
    __tablename__ = "comment_table"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    body: Mapped[str] = mapped_column(String(5000), unique=True, nullable=False)
    date: Mapped[str] = mapped_column(String(25), nullable=False)
    blog_post: Mapped["BlogPost"] = relationship(back_populates="comments")
    blog_post_id: Mapped[int] = mapped_column(ForeignKey("blog_post_table.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    author_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    likes: Mapped[List["User"]] = relationship(secondary=comments_association_table, back_populates="liked_comments")
    replied_to_id: Mapped[int] = mapped_column(ForeignKey("comment_table.id"))
    replied_to: Mapped["Comment"] = relationship(back_populates="replies", remote_side=[id])
    replies: Mapped[List["Comment"]] = relationship(back_populates="replied_to")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
