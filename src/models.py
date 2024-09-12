from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
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
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class User(SQLAlchemyBaseUserTableUUID, Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    created_at: Mapped[created_at]
    update_at: Mapped[updated_at]
    friend: Mapped[set["Friend"]] = relationship()


class Friend(Base):
    __tablename__ = "friend"
    user_id: Mapped[UUID] = mapped_column(primary_key=True)
    friend_id: Mapped[UUID] = mapped_column(ForeignKey("user.id"))
