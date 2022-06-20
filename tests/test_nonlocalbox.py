from os import getenv

import pytest

import nonlocalbox
from nonlocalbox.exceptions import StatusError, ServiceError, UninitializedBoxError


@pytest.fixture
def box_alice():
    return nonlocalbox.NonlocalBox(getenv("ALICE_API_KEY"))


@pytest.fixture
def box_bob():
    return nonlocalbox.NonlocalBox(getenv("BOB_API_KEY"))


@pytest.fixture
def wrong_api_key():
    return nonlocalbox.NonlocalBox("abcde")


def test_error_on_wrong_api_key():
    with pytest.raises(TypeError):
        nonlocalbox.NonlocalBox(123)


def test_invite_raises_error(box_alice):
    with pytest.raises(StatusError):
        box_alice.invite("bob", 7, "testing_box")


def test_invite(box_alice, box_bob):
    box_id = box_alice.invite("bob", 1, "alice_invites_bob")
    assert box_alice.box_id == box_id
    assert box_alice.box_type_id == 1


def test_initialize_box(box_alice, box_bob):
    box_alice.initialize(1)
    box_bob.initialize(1)
    assert box_alice.role == "Alice"
    assert box_bob.role == "Bob"
    assert box_alice.box_id == box_bob.box_id == 1

    box_alice.initialize(137)
    box_bob.initialize(137)
    assert box_alice.role == box_bob.role == "Bob"
    assert box_alice.box_id == box_bob.box_id == 137

    box_id = box_alice.invite("alice", 1, "same_user")
    box_alice.initialize(box_id, i_want_to_be_bob=True)
    assert box_alice.role == "Bob"


def test_use_box_error(box_alice):
    with pytest.raises(UninitializedBoxError):
        box_alice.use(0, "20220101003")

    box_alice.initialize(1)
    with pytest.raises(StatusError):
        box_alice.use(2, "20220101004")


def test_use_box(box_alice, box_bob):
    box_alice.initialize(1)
    box_bob.initialize(1)

    assert box_alice.use(0, "20220101001") in [0, 1]
    assert box_bob.use(1, "20220101001") in [0, 1]
    assert box_bob.use(1, "20220101002") in [0, 1]
    assert box_alice.use(1, "20220101002") in [0, 1]


def test_list_box_types_error(wrong_api_key):
    with pytest.raises(StatusError):
        wrong_api_key.list_box_types()


def test_list_boxes_error(wrong_api_key):
    with pytest.raises(StatusError):
        wrong_api_key.list_boxes()


def test_box_type_info_error(wrong_api_key):
    with pytest.raises(StatusError):
        wrong_api_key.box_type_info()
