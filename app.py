from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Hullo</h1>"

@app.route('/status/<uid>')
def status(uid):
    field = [[100, 110, 120, 120, 120],
             [100, 110, 120, 120, 130],
             [100, 110, 120, 130, 130],
             [100, 110, 130, 130, 130]]
    return jsonify({'field': field})

if __name__ == '__main__':
    app.run()
