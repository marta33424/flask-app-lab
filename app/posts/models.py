from datetime import datetime as dt
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db

post_tags = Table(
    "post_tags",
    db.metadata,
    db.Column("post_id", ForeignKey("posts.id"), primary_key=True),
    db.Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Post(db.Model):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    posted: Mapped[dt] = mapped_column(DateTime, default=dt.now)
    category: Mapped[str] = mapped_column(
        Enum("news", "publication", "tech", "other", name="post_categories"),
        default="other",
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="posts")

    tags: Mapped[list["Tag"]] = relationship(
        secondary=post_tags, back_populates="posts"
    )

    def __repr__(self) -> str:
        return f"<Post(title={self.title})>"


class Tag(db.Model):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        secondary=post_tags, back_populates="tags"
    )

    def __repr__(self) -> str:
        return f"<Tag(name={self.name})>"