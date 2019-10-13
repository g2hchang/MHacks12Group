from flask import Flask, jsonify, make_response
import requests
from flask_cors import CORS
from datetime import datetime
import json, pandas
from predict import get_prediction

app = Flask(__name__)
CORS(app)
counter = 0

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
    data = requests.get("https://mhacks12-c37e8.firebaseio.com/users/.json")
    df = pandas.read_json(data.content)
    temptime = datetime.now()
    time = temptime.isoformat().replace('T', ' ')
    time = time[:time.index('.')]
    df2 = pandas.DataFrame([[time, health]],  columns=['ds', 'y'])
    df = df.append(df2, ignore_index = True)
    df.to_json("data2.json")
    ################################################################################
    # FIREBASE
    with open("data2.json") as f:
        content = json.load(f)

    url = "https://mhacks12-c37e8.firebaseio.com/users/.json"
    payload = content
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.17.1",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "e7e1ce3d-c916-44fa-b94b-1b61bd6cb630,baf09016-fb5f-4fe6-899a-d1c0615ba294",
        'Host': "mhacks12-c37e8.firebaseio.com",
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "36",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    # response = requests.request("POST", url, data=payload, headers=headers)
    response = requests.put(url, json=payload, headers=headers)
    return make_response(jsonify({}))


@app.route('/status/<uid>')
def status(uid):
    with open("store.json") as file:
        store = json.load(file)
    health = store['users'][str(uid)]
    import random
    health_matrix = [
        [health]*5,
        [max(health-(random.randint(5, 15)), 0)]*5,
        [max(health-(random.randint(5, 15)), 0)]*5,
        [max(health-(random.randint(5, 15)), 0)]*5,
        [max(health-(random.randint(5, 15)), 0)]*5
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
                health_matrix[row][col] = max(health - 3*euclidean_distance, 0)
    global counter
    if counter == 0:
        health_matrix[-1][-1] = 100
        counter += 1
    response = make_response(jsonify({'health': health_matrix}))
    return response


if __name__ == '__main__':
    app.run(port = 5006)
