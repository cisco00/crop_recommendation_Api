import pandas as pd
from flask import Flask, request, render_template
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


def state_with_max_crop_output(index):
    return final_df[final_df.index == index]['State'].values[0]


def getting_state_index(state):
    return final_df[final_df.State == state]['index'].values[0]


def get_state_from_index(state):
    return final_df[final_df.index == state]["State"].values[0]

  
@app.route('/api/v1/recommend/crop', methods=['GET', 'POST'])
def make_recommendation():
    if request.method == 'POST':
        crop_input = request.form['input_field']
        crops_dict_value = switching_variables(crop_input)
        get_crop_index = getting_crop_index(crops_dict_value)
        similar_crop = list(enumerate(model[get_crop_index]))
        sorted_similar_crop = sorted(similar_crop, key=lambda x: x[1], reverse=False)

        lists = []
        count = 1
        for crop in sorted_similar_crop:
            lists.append(get_crop_from_index(crop[0]))
            count = count + 1
            if count > 100:
                break
        return str(list(dict.fromkeys(lists)))
    else:
        return render_template('form.html')



# @app.route('/api/v1/recommend/crop/<crop>', method=['GET', 'POST'])
# def crop_recommendation(crop):  # put application's code here
#
#     crop_dict_value = switching_variables(crop)
#     get_crop_index = getting_crop_index(crop_dict_value)
#     similar_crops = list(enumerate(model[get_crop_index]))
#     sorted_similar_crop = sorted(similar_crops, key=lambda x: x[1], reverse=False)
#
#     lists = []
#     count = 1
#     for crop in sorted_similar_crop:
#         lists.append(get_crop_from_index(crop[0]))
#         count = count + 1
#         if count > 100:
#             break
#     return str(list(dict.fromkeys(lists)))
#     # return str(picking_crops(farmers_input()))

#
# @app.route('/api/v1/recommend/state/<input>', method=['GET', 'POST'])
# def make_recommendation(state, input):
#     if input == 'state':
#         try:
#             state_dict_value = switching_variables(state)
#             get_state_index = getting_state_index(state_dict_value)
#             similar_state = list(enumerate(model[get_state_index]))
#             sorted_similar_state = sorted(similar_state, key=lambda x: x[1], reverse=False)
#             return str(list(dict.fromkeys(sorted_similar_state)))
#         except KeyError:
#             return 'The inputed state does not exist in the data'
#

if __name__ == '__main__':
    app.run()