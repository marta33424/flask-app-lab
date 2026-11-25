from sqlalchemy.orm import Mapped, mapped_column, relationship
from app import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(255), nullable=False)

    posts: Mapped[list["Post"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )