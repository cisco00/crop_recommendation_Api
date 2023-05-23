from typing import Any
import pandas as pd
from flask import Flask, jsonify
import pickle

app = Flask(__name__)
# model = pickle.load(open('model.pkl', 'r'))

crop_list = {"Yam": 0, "Maize": 1, "Sorghum": 2, "Cotton": 3, "Cassava": 4,
             "Millets": 5, "Groundnuts": 6, "Rice": 7, "Beans": 8, "Cocoa": 9,
             "Irish Potatoes": 10, "Oil Palm": 11, "Sugercane": 12, "Vegetables": 13, "Banana": 14,
             "Rubber": 15, "MilletsSorghum": 16, "Plaintain": 17, "Acha": 18, "SugerCane": 19, "Yam.": 20,
             "MaizeCocoa": 21}

final_crop = pd.read_csv('models/final dataframe.csv')


def farmers_input():
    user_input = input("Enter a crop: ")
    return user_input


def picking_crops(crop):
    value = None
    try:
        value = crop_list[crop]
    except KeyError:
        print("The crop is not found in the list of crops trained with this model")
    return value


value_crop = picking_crops(farmers_input)


def getting_crop_index(crop):
    return final_crop[final_crop.MAJOR_CROP == crop]["index"].values[0]


crop_index = getting_crop_index(value_crop)
similarity = pickle.load(open('models/model.pkl', 'rb'))


def get_crop_similarities(crop_index):
    similar_crops = list(enumerate(similarity[crop_index]))
    return sorted(similar_crops, key=lambda x: x[1], reverse=True)


def get_title_from_index(index):
    return final_crop[final_crop.index == index]["MAJOR_CROP"].values[0]


lst = []


def get_list_of_similar_crop():
    i = 0
    for index in get_crop_similarities(crop_index):
        lst.append(get_title_from_index(index[0]))
        i = i + 1
        if i > 5:
            break


@app.route('/api/v1/recommend')
def recommendation():
    return jsonify(lst)


if __name__ == '__main__':
    app.run()
