from flask import Flask, jsonify, make_response
from flask_cors import CORS
from datetime import datetime
import json, pandas
from predict import get_prediction

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return "<h1>Hullo</h1>"


@app.route('/predict/<uid>')
def predict(uid):
    return jsonify({'prediction': get_prediction(datetime.now())})


@app.route('/update/<uid>/<health>')
def update(uid, health):
    store = None
    with open("store.json") as file:
        store = json.load(file)
    store["users"][uid].append(int(health))
    with open("store.json", "w") as file:
        json.dump(store, file)
    df = pandas.read_json("data.json")
    temptime = datetime.now()
    time = temptime.isoformat().replace('T', ' ')
    time = time[:time.index('.')]
    df2 = pandas.DataFrame([[time, health]],  columns=['ds', 'y'])
    df = df.append(df2, ignore_index = True)
    df.to_json("data.json")
    return make_response(jsonify({}))


@app.route('/status/<uid>')
def status(uid):
    with open("store.json") as file:
        store = json.load(file)
    health = store['users'][str(uid)]
    response = make_response(jsonify({'health': health}))
    return response


if __name__ == '__main__':
    app.run()
