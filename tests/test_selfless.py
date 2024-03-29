import pytest

from ptera.selfless import ConflictError, Override, selfless

from .common import one_test_per_assert


@selfless
def iceberg(x, y):
    z: int
    return sum([x, y, z])


@selfless(add1=False)
def chocolat(x, y):
    z = x + y
    rval = z * z
    if add1:
        rval = rval + 1
    return rval


@selfless
def puerh(x=2, y=3):
    return x + y


@selfless
def helicopter(x, y):
    return min(x, y)


@one_test_per_assert
def test_selfless():
    assert iceberg.new(z=5)(2, 3) == 10

    assert chocolat(2, 3) == 25
    assert chocolat.new(add1=True)(2, 3) == 26
    assert chocolat.new(x=2, y=3)() == 25
    assert chocolat.new(x=2, y=3)(4) == 49
    assert chocolat.new(x=2, y=3)(y=4) == 36

    assert puerh() == 5
    assert puerh.new(x=7)() == 10
    assert puerh.new(y=10)() == 12
    assert puerh(4, 5) == 9
    assert puerh.new(x=10, y=15)(4, 5) == 9

    assert helicopter(2, 10) == 2
    assert helicopter.new(min=max)(2, 10) == 10


def test_name_error():
    with pytest.raises(NameError):
        iceberg(2, 3)
    with pytest.raises(Exception):
        chocolat()


@pytest.mark.xfail(
    reason="Selfless raises a NameError but to be consistent with Python"
    " it should be a TypeError."
)
def test_missing_argument():
    with pytest.raises(TypeError):
        chocolat()


def test_state_get():

    assert puerh.state.x == 2
    assert puerh.state.y == 3

    puerh2 = puerh.new(x=4, y=5)

    assert puerh2.state.x == 4
    assert puerh2.state.y == 5

    # Test that global variables are in the state
    assert iceberg.state.sum is sum


def test_state_set():
    puerh2 = puerh.new(x=4, y=5)

    # Test setting the state in place
    assert puerh2() == 9
    puerh2.state.x = 10
    puerh2.state.y = 20
    assert puerh2() == 30

    # Verify that the original function still works as before
    assert puerh() == 5


def test_state_invalid_variables():
    puerh2 = puerh.new(x=4, y=5)

    with pytest.raises(AttributeError):
        puerh2.state.z = 50


def test_state_unset_variables():
    with pytest.raises(AttributeError):
        iceberg.state.x

    with pytest.raises(AttributeError):
        iceberg.state.z


def test_override_return_value():
    with pytest.raises(ConflictError):
        chocolat.new(rval=1234)(2, 3)

    assert chocolat.new(rval=Override(1234))(2, 3) == 1234


def test_override_arguments():
    assert chocolat.new(x=2, y=3)(4) == 49
    assert chocolat.new(x=Override(2), y=3)(4) == 25
    with pytest.raises(ConflictError):
        chocolat.new(x=Override(2), y=3)(Override(4))
    assert chocolat.new(x=Override(2), y=3)(Override(4, priority=2)) == 49
