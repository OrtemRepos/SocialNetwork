import datetime
from uuid import UUID
import pytest
import pytest_asyncio
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError

from src.auth.exception.user import UserAlreadyExists
from src.auth.schema.user import UserRead
from src.database import engine, get_session
from src.model import Base, Friend, User


@pytest_asyncio.fixture(scope="session", loop_scope="session")
async def refresh_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.mark.asyncio(loop_scope="session")
async def test_add(refresh_db):
    user = User(
        first_name="John",
        last_name="Doe",
        email="a@a.com",
        password="12345678",
    )
    async with get_session() as session:
        session.add(user)
        await session.flush()
        user_read = UserRead(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            created_at=datetime.datetime.now(),
        )
        assert user_read
        await session.commit()
        await session.close()


@pytest.mark.asyncio(loop_scope="session")
async def test_get():
    session = get_session()
    stmt = select(User).where(User.email == "a@a.com")
    result = await session.execute(stmt)
    user = result.scalars().one()
    print(user)
    assert user
    assert user.email == "a@a.com"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    await session.close()


@pytest.mark.asyncio(loop_scope="session")
async def test_exception_create_duplicate():
    user = User(
        first_name="John",
        last_name="Doe",
        email="a@a.com",
        password="12345678",
    )
    async with get_session() as session:
        with pytest.raises(IntegrityError):
            session.add(user)
            await session.commit()
            await session.close()


@pytest.mark.asyncio(loop_scope="session")
async def test_create_another():
    user = User(
        first_name="Jane",
        last_name="Doe",
        email="b@b.com",
        password="12345678",
    )
    async with get_session() as session:
        session.add(user)
        await session.flush()
        assert user.id
        await session.commit()
        await session.close()


@pytest.mark.asyncio(loop_scope="session")
async def test_add_friend():
    async with get_session() as session:
        stmt = select(User).where(User.email == "a@a.com")
        stmt_2 = select(User).where(User.email == "b@b.com")
        user_1 = await session.execute(stmt)
        user_2 = await session.execute(stmt_2)

        user_1 = user_1.scalars().one()
        user_2 = user_2.scalars().one()

        assert user_1
        assert user_2

        new_friend = Friend(user_id=user_1.id, friend_id=user_2.id)
        rev_friend = Friend(user_id=user_2.id, friend_id=user_1.id)
        session.add(new_friend)
        session.add(rev_friend)
        await session.commit()

        friends_of_user_1 = await session.execute(
            select(User)
            .join(Friend, User.id == Friend.user_id)
            .where(Friend.friend_id == user_1.id)
        )
        assert user_2 in friends_of_user_1.scalars().all()

        friends_of_user_2 = await session.execute(
            select(User)
            .join(Friend, User.id == Friend.user_id)
            .where(Friend.friend_id == user_2.id)
        )
        assert user_1 in friends_of_user_2.scalars().all()


@pytest.mark.asyncio(loop_scope="session")
async def test_list_friend():
    async with get_session() as session:
        stmt = (
            select(User)
            .where(User.email == "a@a.com")
            .join(Friend, User.id == Friend.user_id)
        )
        user = await session.execute(stmt)

        friends_list = user_list.all()
        assert friends_list == 1


@pytest.mark.asyncio(loop_scope="session")
async def test_get_friend():
    async with get_session() as session:
        stmt = select(User).where(User.email == "a@a.com")
        stmt_2 = select(User).where(User.email == "b@b.com")
        user_1 = await session.execute(stmt)
        user_2 = await session.execute(stmt_2)

        user_1 = user_1.scalars().one()
        user_2 = user_2.scalars().one()

        stmt = (
            select(User)
            .join(Friend, User.id == Friend.user_id)
            .where(Friend.friend_id == user_1.id)
        )

        user_2_friend = await session.execute(stmt)
        user_2_friend = user_2_friend.scalars().one()
        assert user_2_friend == user_2

        stmt = (
            select(User)
            .join(Friend, User.id == Friend.user_id)
            .where(Friend.friend_id == user_2.id)
        )

        user_1_friend = await session.execute(stmt)
        user_1_friend = user_1_friend.scalars().one()
        assert user_1_friend == user_1


@pytest.mark.asyncio(loop_scope="session")
async def test_remove_friend():
    async with get_session() as session:
        stmt = select(User).where(User.email == "a@a.com")
        stmt_2 = select(User).where(User.email == "b@b.com")
        user_1 = await session.execute(stmt)
        user_2 = await session.execute(stmt_2)

        user_1 = user_1.scalars().one()
        user_2 = user_2.scalars().one()

        assert user_1
        assert user_2

        stmt_1 = delete(Friend).where(
            Friend.user_id == user_1.id, Friend.friend_id == user_2.id
        )
        stmt_2 = delete(Friend).where(
            Friend.user_id == user_2.id, Friend.friend_id == user_1.id
        )

        await session.execute(stmt_1)
        await session.execute(stmt_2)
        await session.commit()
        await session.close()
