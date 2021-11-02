from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask.json import JSONEncoder
from bson import json_util
from mongoengine.base import BaseDocument
from mongoengine.queryset.base import BaseQuerySet

from apscheduler.schedulers.background import BackgroundScheduler
import datetime



app = Flask(__name__)

class MongoEngineJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, BaseDocument):
            return json_util._json_convert(obj.to_mongo())
        elif isinstance(obj, BaseQuerySet):
            return json_util._json_convert(obj.as_pymongo())
        return JSONEncoder.default(self, obj)

app.json_encoder = MongoEngineJSONEncoder

client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb://test:test@3.34.194.45', 27017)
db = client.matna


@app.route("/create_event", methods=["POST"])
def post_event():
    user_id = request.form["userId"]
    restaurant_id = request.form["restaurantId"]
    meeting_time = int(request.form["meetingTime"])
    number_of_participants = request.form["numberOfParticipants"]

    expire_time = datetime.datetime.now() + datetime.timedelta(minutes=meeting_time) 

    db.restaurant.update_one({"_id": ObjectId(restaurant_id)}, {"$push" : { "event": {"creator": user_id, "time": expire_time, "number_of_participants": number_of_participants }}})

    def event_expire():
        db.restaurant.findOneAndUpdate({"_id": ObjectId(restaurant_id)}, {"$unset" : {"event" : ""}})

    sched = BackgroundScheduler(daemon=True)
    sched.add_job(event_expire, 'interval', minutes = meeting_time)
    sched.start()

    return jsonify({ "result" : "success"})



if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)
