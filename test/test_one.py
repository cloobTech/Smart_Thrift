from myTest import add, Person
import pytest

@pytest.fixture
def person():
    return Person("Olamide")

@pytest.mark.parametrize("x, y, result", [
    (2, 6, 8),
    (2, 4, 6),
    (2, 7, 9),
    (2, 46, 48),
    (2, 16, 18)
    ]
                         
                         )
def test_add(x, y, result):
    assert add(x, y) == result


def test_person():
    ola = Person("Olamide")
    assert (ola.name) == "Olamide"


def test_person():
    ola = Person("Olamide")
    (ola.set_age(29)) 
    ola.age == 29