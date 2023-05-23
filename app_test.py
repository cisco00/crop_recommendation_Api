import pytest
import requests
from main import hello_world
from main import picking_crops
from main import farmers_input


crop_list = {"Yam":0, "Maize":1, "Sorghum":2, "Cotton":3, "Cassava":4,
             "Millets":5, "Groundnuts":6, "Rice":7, "Beans":8, "Cocoa":9,
             "Irish Potatoes":10, "Oil Palm":11, "Sugercane":12, "Vegetables":13, "Banana":14,
             "Rubber":15, "MilletsSorghum":16, "Plaintain":17, "Acha":18, "SugerCane":19, "Yam.":20,
             "MaizeCocoa":21}


def test_hello_world():
    assert hello_world() == "Hello World!"


def test_crops_picked():
    assert picking_crops(crop_list) == int


def test_api_response():
    base_url = "courses.csrrinzqubik.us-east-1.rds.amazonaws.com"
    response = requests.get(base_url + "/endpoint")
    assert response.status == 200, "API is not working. Status code: " + str(response.status_code)


def test_user_input(monkeypatch):
    mock_input = "Test Value"
    monkeypatch.setattr('builtins.input', lambda _: mock_input)

    result = farmers_input()
    assert result == mock_input


