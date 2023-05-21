import pytest
from main import hello_world
from main import picking_crops


def test_hello_world():
    assert hello_world() == "Hello World!"


def test_crops_picked():
    assert picking_crops() == dict()