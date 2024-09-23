from datetime import datetime
from typing import Annotated
import uuid

from sqlalchemy import TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

created_at = Annotated[
    datetime,
    mapped_column(
        type_=TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
    ),
]
updated_at = Annotated[
    datetime,
    mapped_column(
        type_=TIMESTAMP(timezone=True),
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=text("TIMEZONE('utc', now())"),
        nullable=True,
    ),
]


class Base(DeclarativeBase):
    repr_cols_num = 3
    repr_cols: tuple[str, ...] = ("email", "id", "first_name", "last_name")

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(unique=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    password: Mapped[str]
    created_at: Mapped[created_at]
    update_at: Mapped[updated_at]
    friends: Mapped[list["User"]] = relationship(
        "User",
        secondary="friend",
        back_populates="friends",
        primaryjoin="User.id == friend.c.user_id",
        secondaryjoin="User.id == friend.c.friend_id",
    )


class Friend(Base):
    __tablename__ = "friend"
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id"), primary_key=True
    )
    friend_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id"), primary_key=True
    )
