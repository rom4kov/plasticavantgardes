from __future__ import annotations
from flask_login import UserMixin
from sqlalchemy import Integer, String, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.elements import SQLCoreOperations
from extensions import db
from typing import List, Dict, Any, Optional


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


class User(db.Model, UserMixin): # type: ignore[name-defined]
    __tablename__ = "user_table"

    def __init__(self, name: str, email: str, password: str, 
                     posts: Optional[List[BlogPost]] = None, 
                     comments: Optional[List[Comment]] = None, 
                     liked_posts: Optional[List[BlogPost]] = None, 
                     liked_comments: Optional[List[Comment]] = None):
        self.name = name
        self.email = email
        self.password = password
        self.posts = posts if posts is not None else []
        self.comments = comments if comments is not None else []
        self.liked_posts = liked_posts if liked_posts is not None else []
        self.liked_comments = liked_comments if liked_comments is not None else []

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    posts: Mapped[List["BlogPost"]] = relationship(back_populates="author")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")
    liked_posts: Mapped[List["BlogPost"]] = relationship(secondary=posts_association_table, back_populates="likes")
    liked_comments: Mapped[List["Comment"]] = relationship(secondary=comments_association_table, back_populates="likes")

    def to_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} # type: ignore[repostAttributeAccessIssue]


class BlogPost(db.Model): # type: ignore[name-defined]
    __tablename__ = "blog_post_table"

    def __init__(self, title: str, subtitle: str, img_url: str, body: str, date: str,
             author: SQLCoreOperations[User] | User, author_id: int, 
             comments: Optional[List[Comment]] = None, 
             likes: Optional[List[User]] = None):
        self.title = title
        self.subtitle = subtitle
        self.img_url = img_url
        self.body = body
        self.date = date
        self.author = author
        self.author_id = author_id
        self.comments = comments if comments is not None else []
        self.likes = likes if likes is not None else []

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


class Comment(db.Model): # type: ignore[name-defined]
    __tablename__ = "comment_table"

    def __init__(self, body, blog_post, blog_post_id, author, author_id, date, likes, replied_to_id, replies=[]):
        self.body = body
        self.blog_post = blog_post
        self.blog_post_id = blog_post_id
        self.author = author
        self.author_id = author_id
        self.date = date
        self.likes = likes
        self.replied_to_id = replied_to_id
        self.replies = replies

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    body: Mapped[str] = mapped_column(String(5000), unique=True, nullable=False)
    date: Mapped[str] = mapped_column(String(25), nullable=False)
    blog_post: Mapped["BlogPost"] = relationship(back_populates="comments")
    blog_post_id: Mapped[int] = mapped_column(ForeignKey("blog_post_table.id"))
    author: Mapped["User"] = relationship(back_populates="comments")
    author_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    likes: Mapped[List["User"]] = relationship(secondary=comments_association_table, back_populates="liked_comments")
    replied_to_id: Mapped[int] = mapped_column(ForeignKey("comment_table.id"), nullable=True)
    replied_to: Mapped["Comment"] = relationship(back_populates="replies", remote_side=[id])
    replies: Mapped[List["Comment"]] = relationship(back_populates="replied_to")

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} # type: ignore[repostAttributeAccessIssue]
