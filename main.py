import pandas as pd
from flask import Flask, jsonify
import pickle
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)


crop_list = {"Yam": 0, "Maize": 1, "Sorghum": 2, "Cotton": 3, "Cassava": 4,
             "Millets": 5, "Groundnuts": 6, "Rice": 7, "Beans": 8, "Cocoa": 9,
             "Irish Potatoes": 10, "Oil Palm": 11, "Sugercane": 12, "Vegetables": 13, "Banana": 14,
             "Rubber": 15, "MilletsSorghum": 16, "Plaintain": 17, "Acha": 18, "SugerCane": 19, "Yam.": 20,
             "MaizeCocoa": 21}

state_list = {"adamawa": 0, "bauchi": 1, "bayelsa": 2, "benue": 3, "federal capital territory": 4,
              "kaduna": 5, "kano": 6, "katsina": 7, "kebbi": 8, "kogi": 9, "kwara": 10, "nasarawa": 11,
              "niger": 12, "plateau": 13, "taraba": 14}



data = pd.read_csv("data_index_file.csv")
final_df = data.iloc[:, 1:]

df1 = pd.read_csv('crops_dataset_model_building.csv')
df2 = df1.iloc[:, 1:]

model = cosine_similarity(df2)


cosine_sim = cosine_similarity(numerical_data)

def farmers_input():
    user_input = input("Enter a crop: ")
    return user_input


def picking_crops(crop):
  if crop in crop_list:
    value = crop_list[crop]
  else:
    return -1
  return value


def picking_state(state):
  if state in state_list:
    value = state_list[state]
  else:
    return -1
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
    try:
        return final_df[final_df.MAJOR_CROP == crop]["index"].values[0]
    except:
        return None


crop_dict_value = switching_variables(farmers_input)

get_crop_index = getting_crop_index(crop_dict_value)

similar_crops = list(enumerate(model[get_crop_index]))

sorted_similar_crop = sorted(similar_crops, key=lambda x: x[1], reverse=False)


def get_crop_from_index(index):
    try:
        return final_df[final_df.index == index]["MAJOR_CROP"].values[0]
    except:
        return None


def getting_state_index(state):
    try:
        return final_df[final_df.State == state]['index'].values(0)
    except:
        return None


def get_state_from_index(state):
    try:
        return final_df[final_df.index == state]["State"].values(0)
    except:
        return None

# getting the value of the crop key from the dictionary
state_dict_value = switching_variables(farmers_input)

#getting the index of the crop from the dataframe table
get_state_index = getting_state_index(state_dict_value)

similar_state = list(enumerate(model[get_state_index]))
sorted_similar_state = sorted(similar_state, key=lambda x: x[1], reverse=False)


@app.route('/api/v1/recommend')
def hello_world():  # put application's code here
  
    lst = []
    i = 0
    for crop in sorted_similar_crop:
        lst.append(get_crop_from_index(crop[0]))
        i = i + 1
        if i > 100:
            break
    return str(list(dict.fromkeys(lst)))
    # return str(picking_crops(farmers_input()))


if __name__ == '__main__':
    app.run()
