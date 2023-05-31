import pandas as pd
from scipy.spatial.distance import pdist, squareform
from flask import Flask

app = Flask(__name__)

df = pd.read_csv('data_index_file.csv')

# crop recommendation based on state
crop_state_ct = pd.crosstab(df.MAJOR_CROP, df.state)
crop_state_ct

jaccard_dist_state = pdist(crop_state_ct.values, metric='jaccard')
square_jaccard_dist_state = squareform(jaccard_dist_state)
jaccard_similarity_array_state = 1 - square_jaccard_dist_state

state_distance_df = pd.DataFrame(jaccard_similarity_array_state, index=crop_state_ct.index, 
                                columns=crop_state_ct.index)

# crop recommendation based on vegetation
crop_vegetation_ct = pd.crosstab(df.MAJOR_CROP, df.VEGETATION)
crop_vegetation_ct

jaccard_dist_vegetation = pdist(crop_vegetation_ct.values, metric='jaccard')
square_jaccard_dist_vegetation = squareform(jaccard_dist_vegetation)
jaccard_similarity_array_vegetation = 1 - square_jaccard_dist_vegetation

vegetation_distance_df = pd.DataFrame(jaccard_similarity_array_vegetation, index=crop_vegetation_ct.index, 
                                columns=crop_vegetation_ct.index)


@app.route('/api/v1/recommend/<crop>/<input>')
def make_recommendation(crop, input):
    if input == 'state':
        # try:
        state_recommended_crops = state_distance_df[crop.title()].sort_values(ascending=False)[:5].index.values
        state_recommended_crops_list = list(state_recommended_crops)
        predict_state = df[df['MAJOR_CROP'].isin(state_recommended_crops_list)]
        return str(predict_state.state.unique()[:10])
        # except KeyError:
        #     return 'The inputed crop does not exist in the data'
    elif input == 'vegetation':
        # try:
        vegetation_recommended_crops = vegetation_distance_df[crop.title()].sort_values(ascending=False)[:5].index.values
        vegetation_recommended_crops_list = list(vegetation_recommended_crops)
        predict_vegetation = df[df['MAJOR_CROP'].isin(vegetation_recommended_crops_list)]
        return str(predict_vegetation.VEGETATION.unique()[:10])
        # except KeyError:
        #     return 'The inputed crop does not exist in the data'


if __name__ == '__main__':
    app.run(debug=True)