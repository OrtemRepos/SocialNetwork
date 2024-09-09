from user.user.error import (
    AlreadyFriend,
    AlreadySentRequest,
    NotFound
)
from uuid import uuid4
import pytest
from user.user.domain_model import User

uuid1 = uuid4()
uuid2 = uuid4()


@pytest.fixture
def sample():
    return User(
        id=uuid1, email="email@example.com",
        first_name="first", last_name="last"
    )


@pytest.fixture
def two_samples():
    return (
        User(
            id=uuid1, email="email1@example.com",
            first_name="first", last_name="last"),
        User(
            id=uuid2, email="email2@example.com",
            first_name="first", last_name="last")
    )


def test_create(sample):
    assert sample
    assert sample.id == uuid1
    assert sample.email == "email@example.com"
    assert sample.first_name == "first"
    assert sample.last_name == "last"


def test_eq(sample):
    assert sample == User(
        id=uuid1, email="email@example.com",
        first_name="first", last_name="last"
    )

    assert sample == User(
        id=uuid1, email="email@example.com",
        first_name="as", last_name="last"
    )

    assert sample == User(
        id=uuid1, email="email@example.com",
        first_name="first", last_name="as"
    )

    assert sample == User(
        id=uuid1, email="email@example.com",
        first_name="d", last_name="d"
    )

    assert sample == User(
        id=uuid1, email="email1@example.com",
        first_name="first", last_name="last"
    )

    assert sample != User(
        id=uuid2, email="email@example.com",
        first_name="first", last_name="last"
    )


def test_add_friend(two_samples):
    user_1, user_2 = two_samples

    user_1.send_friendrequest(user_2)
    user_2.send_friendrequest(user_1)
    assert user_2 in user_1._friend
    assert user_1 in user_2._friend


def test_not_friend(two_samples):
    user_1, user_2 = two_samples
    assert user_2 not in user_1._friend
    assert user_1 not in user_2._friend


def test_send_request(two_samples):
    user_1, user_2 = two_samples
    request = user_1.send_friendrequest(user_2)
    assert request in user_1._request
    assert request in user_2._request


def test_dont_send_two_request(two_samples):
    user_1, user_2 = two_samples
    user_1.send_friendrequest(user_2)
    with pytest.raises(AlreadySentRequest):
        user_1.send_friendrequest(user_2)


def test_reject_request(two_samples):
    user_1, user_2 = two_samples
    request = user_1.send_friendrequest(user_2)
    request2 = user_2.reject_friendrequest(user_1)
    assert request2 == request
    assert request not in user_1._request
    assert request not in user_2._request


def test_try_reject_missing_request(two_samples):
    user_1, user_2 = two_samples
    with pytest.raises(NotFound):
        user_1.reject_friendrequest(user_2)


def test_try_send_request_if_you_friend(two_samples):
    user_1, user_2 = two_samples
    user_1.send_friendrequest(user_2)
    user_2.send_friendrequest(user_1)
    with pytest.raises(AlreadyFriend):
        user_1.send_friendrequest(user_2)
    with pytest.raises(AlreadyFriend):
        user_2.send_friendrequest(user_1)


def test_remove_from_friend(two_samples):
    user_1, user_2 = two_samples
    user_1.send_friendrequest(user_2)
    user_2.send_friendrequest(user_1)
    res = user_1.remove_from_friend(user_2)

    assert res == user_2
    assert user_2 not in user_1._friend
    assert user_1 not in user_2._friend


def test_auto_friendrequest_after_remove_from_friend(two_samples):
    user_1, user_2 = two_samples
    user_1.send_friendrequest(user_2)
    user_2.send_friendrequest(user_1)
    user_1.remove_from_friend(user_2)

    assert user_1 not in user_2._friend
    assert user_2 not in user_1._friend

    request = user_2.get_request(user_1)
    assert request in user_1.receive_request
    assert request in user_2.send_request
