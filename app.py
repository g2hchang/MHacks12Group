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

def squish_health(health):
    minimum, maximum = 0, 100
    health = ((maximum - minimum) * (health - minimum)) // (1000)
    return health

@app.route('/update-realtime/<uid>/<health>')
def update_realtime(uid, health):
    health = squish_health(int(health))
    with open("store.json") as file:
        store = json.load(file)
    if not store:
        store = {}
    store['users'][str(uid)] = health
    with open("store.json", "w") as file:
        json.dump(store, file)
    return make_response(jsonify({}))


@app.route('/update/<uid>/<health>')
def update(uid, health):
    health = squish_health(int(health))
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
    import random
    health_matrix = [
        [health]*5,
        [health-(random.randint(5, 15))]*5,
        [health-(random.randint(5, 15))]*5,
        [health-(random.randint(5, 15))]*5,
        [health-(random.randint(5, 15))]*5
    ]
    # 5x5
    # [1,1,1,1,1]
    # [1,1,1,1,1]
    # [1,1,1,0,1]
    # [1,1,1,1,1]
    # [1,1,1,1,1]
    sensor_x = 3
    sensor_y = 2
    for row, row_vals in enumerate(health_matrix):
        for col, location in enumerate(row_vals):
            if row == sensor_y and col == sensor_x:
                health_matrix[row][col] = health
            else:
                euclidean_distance = (row - sensor_y)**2 + (col - sensor_x)**2
                health_matrix[row][col] = health - 3*euclidean_distance

    response = make_response(jsonify({'health': health_matrix}))
    return response


if __name__ == '__main__':
    app.run(port = 5006)
