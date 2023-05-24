import pandas as pd
from flask import Flask, jsonify
import pickle
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

numerical_data = pd.read_csv('model_data/numerical_data')


crop_list = {"Yam": 0, "Maize": 1, "Sorghum": 2, "Cotton": 3, "Cassava": 4,
             "Millets": 5, "Groundnuts": 6, "Rice": 7, "Beans": 8, "Cocoa": 9,
             "Irish Potatoes": 10, "Oil Palm": 11, "Sugercane": 12, "Vegetables": 13, "Banana": 14,
             "Rubber": 15, "MilletsSorghum": 16, "Plaintain": 17, "Acha": 18, "SugerCane": 19, "Yam.": 20,
             "MaizeCocoa": 21}

state_list = {"adamawa": 0, "bauchi": 1, "bayelsa": 2, "benue": 3, "federal capital territory": 4,
              "kaduna": 5, "kano": 6, "katsina": 7, "kebbi": 8, "kogi": 9, "kwara": 10, "nasarawa": 11,
              "niger": 12, "plateau": 13, "taraba": 14}

final_crop1 = pd.read_csv('models/crops_dataset_model_building.csv')
final_crop = final_crop1.iloc[:, 1:]
final_crop.head()


def farmers_input():
    user_input = input("Enter a crop: ")
    return user_input


def pickin_crops(crop):
    crop_type = 0
    for key, value in crop_list.items():
        if crop == key:
            crop_type = value
        else:
            pass

    return crop_type


def picking_crops(crop):
    value = None
    try:
        value = crop_list[crop]
    except KeyError:
        print("The crop is not found in the list of crops trained with this model")

    return value


def picking_state(state):
    states = 0
    for key, value in state_list.items():
        if state == key:
            states = value
        else:
            pass
    return states


value_crop = pickin_crops(farmers_input)


def getting_crop_index(crop):
    return final_crop[final_crop.MAJOR_CROP == crop]["index"].values[0]


crop_index = getting_crop_index(value_crop)

similar_crops = list(enumerate(cosine_similarity[crop_index]))


def get_crop_from_index(index):
    return final_crop[final_crop.index == index]["MAJOR_CROP"].values[0]


lst = []


def get_list_of_similar_crops():
    sorted_similar_crop = sorted(similar_crops, key=lambda x: x[1], reverse=True)
    i = 0
    for crop in sorted_similar_crop:
        lst.append(get_crop_from_index(crop[0]))
        i = i + 1
        if i > 5:
            break


@app.route('/api/v1/recommend')
def hello_world():  # put application's code here
    return jsonify(lst)


if __name__ == '__main__':
    app.run()
