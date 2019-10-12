from flask import Flask, jsonify, make_response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<h1>Hullo</h1>"

@app.route('/update/<uid>/<health>')
def update(uid, health):
    store = None
    with open("store.json") as file:
        store = json.load(file)
    store['users'][uid].append(health)
    with open("store.json", "w") as file:
        json.dump(file, store)

@app.route('/status/<uid>')
def status(uid):
    health = 130
    response = make_response(jsonify({'health': health}))
    return response

if __name__ == '__main__':
    app.run()
