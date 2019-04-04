from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from bson.json_util import dumps
from datetime import datetime
import pymongo

app = Flask(__name__)

client = pymongo.MongoClient("mongodb://admin:Aa123456@ds231956.mlab.com:31956/inspector")
db = client.inspector


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/get_all', methods=['GET'])
def get_all():
    cursor = db.reports.find({})
    res = []
    for doc in cursor:
        res.append(dumps(doc))

    print('returning {} inspectors'.format(len(res)))
    return jsonify(res)


@app.route('/api/insert', methods=['POST'])
def insert():
    body = request.get_json()
    body['timestamp'] = datetime.now()
    db.reports.insert_one(body)
    print('got insert request from {}'.format(request.remote_addr))
    print('inserting {}'.format(str(body)))
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run()