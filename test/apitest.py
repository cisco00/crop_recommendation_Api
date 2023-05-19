import pytest
from main import hello_world

def index_hello():
    assert hello_world == "Hello World!"