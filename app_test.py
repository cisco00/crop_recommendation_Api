import pytest
import requests
from main import crop_recommendation
from main import picking_crops
from main import farmers_input


def test_hello_world():
    assert crop_recommendation() == "Hello World!"


def test_crops_picked():
    assert picking_crops() == int


def test_api_response():
    base_url = "http://127.0.0.1:5000/api/v1/recommend"
    response = requests.get(base_url + "/endpoint")
    assert response.status == 200, "API is not working. Status code: " + str(response.status_code)


def test_user_input(monkeypatch):
    mock_input = "Test Value"
    monkeypatch.setattr('builtins.input', lambda _: mock_input)

    result = farmers_input()
    assert result == mock_input


