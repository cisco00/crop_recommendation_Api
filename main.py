import pandas as pd
from flask import Flask
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

crop_list = {"Yam": 0, "Maize": 1, "Sorghum": 2, "Cotton": 3, "Cassava": 4,
             "Millets": 5, "Groundnuts": 6, "Rice": 7, "Beans": 8, "Cocoa": 9,
             "Irish Potatoes": 10, "Oil Palm": 11, "Sugarcane": 12, "Vegetables": 13, "Banana": 14,
             "Rubber": 15, "MilletsSorghum": 16, "Plaintain": 17, "Acha": 18, "SugarCane": 19, "Yam.": 20,
             "MaizeCocoa": 21}

state_list = {"Adamawa": 0, "Bauchi": 1, "Bayelsa": 2, "Benue": 3, "Federal Capital territory": 4,
              "Kaduna": 5, "Kano": 6, "Katsina": 7, "Kebbi": 8, "Kogi": 9, "Kwara": 10, "Nasarawa": 11,
              "Niger": 12, "Plateau": 13, "Taraba": 14}

data = pd.read_csv("data_index_file.csv")
final_df = data.iloc[:, 1:]

df1 = pd.read_csv('model_building.csv')
df2 = df1.iloc[:, 1:]
df2.set_index('index', inplace=True)
df2.reset_index(inplace=True)

model = cosine_similarity(df2)


def farmers_input():
    user_input = input("Enter a crop: ")
    return user_input


def picking_crops(crop):
    if crop in crop_list:
        value = crop_list[crop]
    else:
        return 404
    return value


def picking_state(state):
    if state in state_list:
        value = state_list[state]
    else:
        return 404
    return value


def switching_variables(user_entry):
    value = None
    if user_entry in crop_list:
        return picking_crops(user_entry)
    else:
        if user_entry in state_list:
            value = picking_state(user_entry)
            return value
        return value


def getting_crop_index(crop):
    return df2[df2.MAJOR_CROP == crop]["index"].values[0]


def get_crop_from_index(index):
    return final_df[final_df.index == index]["MAJOR_CROP"].values[0]


crop_dict_value = switching_variables(farmers_input)
get_crop_index = getting_crop_index(crop_dict_value)
similar_crops = list(enumerate(model[get_crop_index]))
sorted_similar_crop = sorted(similar_crops, key=lambda x: x[1], reverse=False)


def state_with_max_crop_output(index):
    try:
        return final_df[final_df.index == index]['State'].values[0]
    finally:
        return None


state_for_crop = switching_variables(farmers_input)
get_crop_max_prod = getting_crop_index(state_for_crop)
state_with_max = list(enumerate(model[get_crop_max_prod]))
sorted_similar_state_with_max = sorted(state_with_max, key=lambda x: x[1], reverse=False)


def getting_state_index(state):
    try:
        return final_df[final_df.State == state]['index'].values(0)
    finally:
        return None


def get_state_from_index(state):
    try:
        return final_df[final_df.index == state]["State"].values(0)
    finally:
        return None


state_dict_value = switching_variables(farmers_input)
get_state_index = getting_state_index(state_dict_value)
similar_state = list(enumerate(model[get_state_index]))
sorted_similar_state = sorted(similar_state, key=lambda x: x[1], reverse=True)


@app.route('/api/v1/recommend/crop', method=['Get', 'Post'])
def crop_recommendation():  # put application's code here
    crop_dict_value = switching_variables(farmers_input())
    get_crop_index = getting_crop_index(crop_dict_value)
    similar_crops = list(enumerate(model[get_crop_index]))
    sorted_similar_crop = sorted(similar_crops, key=lambda x: x[1], reverse=True)
    lists = []
    count = 1
    for crop in sorted_similar_crop:
        lists.append(get_crop_from_index(crop[0]))
        count = count+1
        if count > 5:
            break
    return str(list(dict.fromkeys(lists)))
    # return str(picking_crops(farmers_input()))


@app.route('/api/v1/recommend/crop-state', method=['POST', 'GET'])
def state_recommendation():
    lst = []
    i = 0
    for state in sorted_similar_state:
        lst.append(get_state_from_index(state[0]))
        i = i+1
        if i > 100:
            break
    return str(list(dict.fromkeys(lst)))


@app.route('/api/v1/recommend/state-max')
def state_max_output_recommendation():
    lists = []
    i = 0

    for state_max in sorted_similar_state_with_max:
        lists.append(get_crop_from_index(state_max[0]))
        i = i+1
        if i > 100:
            break
    return str(list(dict.fromkeys(lists)))


if __name__ == '__main__':
    app.run()