import pytest
from uuid import uuid4
from user.user.domain_model import User
from user.repository import FakeUserRepository
from fastapi_users.exceptions import UserAlreadyExists, UserNotExists


uuid = uuid4()
uuid1 = uuid4()
uuid2 = uuid4()


@pytest.fixture
def user():
    return User(
        id=uuid, email="email@example.com", first_name="Ernest", last_name="Hawkins"
    )
    

@pytest.fixture
def rep():
    fake_users = [
        User(first_name="Ernest", last_name="Hawkins", email="email1@example.com", id=uuid1),
        User(first_name="Ernest", last_name="Hawkins", email="email2@example.com", id=uuid2)
    ]
    rep = FakeUserRepository(fake_users)
    return rep


def test_get_by_id(rep):
    id = uuid1
    assert rep.get_by_id(id) == rep.list_user[0]

    
def test_get_missing_id(rep):
    id = uuid4()
    with pytest.raises(UserNotExists):
        rep.get_by_id(id)


def test_get_by_email(rep):
    email = "email1@example.com"
    assert rep.get_by_email(email) == rep.list_user[0]
 
def test_get_missing_email(rep):
    email = "email4@example.com"
    with pytest.raises(UserNotExists):
        rep.get_by_email(email)    

def test_add(rep, user):
    rep.add(user)
    assert user in rep.list_user


def test_add_duplicate(rep, user):
    rep.add(user)
    with pytest.raises(UserAlreadyExists):
        rep.add(user)