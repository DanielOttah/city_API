import os
import traceback
from flask_restful import Api
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json

data = {}

app = Flask(__name__)
# app.secret_key = os.urandom(16)
app.secret_key = 'dany'
CORS(app, supports_credentials=True)
api = Api(app)


@app.route("/")
def hello():
    return render_template("index.html")


@app.route("/all", methods=['POST', 'GET'])
def all():
    return jsonify(list(data.values())), 200


firstKeyType = None


@app.route("/add", methods=['POST'])
def add():
    global data, firstKeyType

    content = request.get_json()

    if 'key' not in content:
        return jsonify({"msg": "There must be a 'key' attribute"}), 400

    key = content['key']

    if firstKeyType:
        if not isinstance(key, firstKeyType):
            return jsonify({"msg": "Keys must be of the same type, that last one was " + str(firstKeyType) + " but this one is " + str(type(key))}), 400
    else:
        firstKeyType = type(key)

    if key in data:
        return jsonify({"msg": "You can not add '" + str(key) + "' again."}), 400

    data[key] = content

    return jsonify({}), 200


@app.route("/delete", methods=['POST'])
def delete():
    global data

    content = request.get_json()

    if 'key' not in content:
        return jsonify({"msg": "There must be a 'key' attribute"}), 400

    key = content['key']

    if key not in data:
        return jsonify({"msg": "You can not delete '" + str(key) + "', it does not exist."}), 400

    del data[key]
    return jsonify({}), 200


@app.route("/read", methods=['POST'])
def read():
    global data

    content = request.get_json()

    if 'key' not in content:
        return jsonify({"msg": "There must be a 'key' attribute"}), 400

    key = content['key']

    if key not in data:
        return jsonify({"msg": "You can not read '" + str(key) + "', it does not exist."}), 400

    return jsonify([data[key]]), 200


@app.route("/update", methods=['POST'])
def update():
    global data

    content = request.get_json()

    if 'key' not in content:
        return jsonify({"msg": "There must be a 'key' attribute"}), 400

    key = content['key']

    if key not in data:
        return jsonify({"msg": "You can not update '" + str(key) + "', it does not exist."}), 400

    data[key] = content
    return jsonify({}), 200


@app.route("/load", methods=['GET'])
def load():
    global data
    print("data1:", data)
    with open('data.json') as json_file:
        data = json.load(json_file)
    return "<h1>EvolveU test</h1> <h2>" + str(len(data)) + " records has been loaded</h2>"


@app.route("/save", methods=['POST'])
def save():
    global data
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
    return jsonify(list(data.values())), 200


@app.route("/clear", methods=['POST', 'GET'])
def clear():
    global data
    data = {}
    return jsonify(data), 200


if __name__ == '__main__':
    print("--- Starting", __file__)
    # app.run(debug=True, use_reloader=True)
    app.run(port=3900, debug=True)
