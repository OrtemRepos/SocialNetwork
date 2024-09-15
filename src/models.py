from datetime import datetime
from typing import Annotated, Any
from uuid import UUID

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import TIMESTAMP, text
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
    repr_cols: tuple[Any]

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
    friend_id: Mapped[UUID | None] = relationship("User")
    friend: Mapped[set["User"]] = relationship(
        "User",
        primaryjoin="User.id == User.friend_id",
        back_populates="friend_of",
    )

    friend_of: Mapped[set["User"]] = relationship(
        "User",
        primaryjoin="User.friend_id == User.id",
        back_populates="friend",
    )
