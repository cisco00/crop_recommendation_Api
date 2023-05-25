import pandas as pd
from scipy.spatial.distance import pdist, squareform
from flask import Flask

app = Flask(__name__)

df = pd.read_csv('data/final_df.csv')

crop_state_ct = pd.crosstab(df.MAJOR_CROP, df.state)
crop_state_ct

jaccard_dist_state = pdist(crop_state_ct.values, metric='jaccard')
square_jaccard_dist_state = squareform(jaccard_dist_state)
jaccard_similarity_array_state = 1 - square_jaccard_dist_state
jaccard_similarity_array_state

state_distance_df = pd.DataFrame(jaccard_similarity_array_state, index=crop_state_ct.index, 
                                columns=crop_state_ct.index)

recommended_crops = state_distance_df['Rice'].sort_values(ascending=False)[:5].index.values

recommended_crops_list = list(recommended_crops)

predict = df[df['MAJOR_CROP'].isin(recommended_crops_list)]

@app.route('/api/v1/recommend')
def hello_world():  # put application's code here
    return str(predict.state.unique())


if __name__ == '__main__':
    app.run()