from typing import Any
import pandas as pd
from flask import Flask
import pickle


app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'r'))

crop_list = {"Yam":0, "Maize":1, "Sorghum":2, "Cotton":3, "Cassava":4,
             "Millets":5, "Groundnuts":6, "Rice":7, "Beans":8, "Cocoa":9,
             "Irish Potatoes":10, "Oil Palm":11, "Sugercane":12, "Vegetables":13, "Banana":14,
             "Rubber":15, "MilletsSorghum":16, "Plaintain":17, "Acha":18, "SugerCane":19, "Yam.":20,
             "MaizeCocoa":21}


final_crop = pd.read_csv('crops_dataset_model_building.csv')


def farmers_input():
    user_input = input("Enter a crop: ")
    return user_input


def picking_crops(crop):
    for key, value in crop_list.items():
        if crop == key:
            crop_types: int | Any = value
        else:
            pass
    return crop_types


value_crop = picking_crops(farmers_input)


def getting_crop_index(crop):
    return final_crop[final_crop.MAJOR_CROP == crop]["index"].values[0]


crop_index = getting_crop_index(value_crop)
crop_index



@app.route('/')
def hello_world():  # put application's code herea
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
