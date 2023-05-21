from flask import Flask
import pickle

app = Flask(__name__)
model = pickle

@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
