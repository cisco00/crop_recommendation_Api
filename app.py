from flask import Flask, request, jsonify
import numpy as np
from pandas import DataFrame
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
df = 'null'


def clean_humidity(df: DataFrame):
    data = df.copy()
    data['A'] = data['humidity'].str.replace
    data = data.drop('humidity', axis=1)
    data = data['A'].str.split(n=11, expand=True)
    data.columns = ['Humidity_{}'.format(x+1) for x in data.columns]
    return data


def clean_data(data):
    data.state = data.state.str.strip()
    cleaned_humidity = clean_humidity(data)
    return cleaned_humidity


# Define a function to compute item similarities
def compute_item_similarities(df):
    item_vectors = list(df.values())
    item_matrix = np.stack(item_vectors)
    similarities = cosine_similarity(item_matrix)
    return similarities


# Compute item similarities
item_similarities = compute_item_similarities(df)


@app.route('/recommend/{item}', methods=['POST'])
def recommend():
    list_of_corps = item_similarities
    return jsonify({'recommendations': list_of_corps})


if __name__ == '__main__':
    app.run()
