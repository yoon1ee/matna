from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask.json import JSONEncoder
from bson import json_util
from mongoengine.base import BaseDocument
from mongoengine.queryset.base import BaseQuerySet
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, get_jwt_identity, unset_jwt_cookies, create_refresh_token,
)

from apscheduler.schedulers.background import BackgroundScheduler
import datetime

import bcrypt, jwt
from setting import SECRET_KEY, ALGORITHM


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

##로그인 데코레이터
@app.route("/create_event", methods=["POST"])
def post_event():
    user_id = request.form["userId"]
    restaurant_id = request.form["restaurantId"]
    meeting_time = int(request.form["meetingTime"])
    number_of_participants = request.form["numberOfParticipants"]

    expire_time = datetime.datetime.now() + datetime.timedelta(minutes=meeting_time) 

    user = db.user.find_one({"_id": ObjectId(user_id)})
    user_name = user["fullname"]

    db.restaurant.update_one({"_id": ObjectId(restaurant_id)}, {"$set" : {"creator": user_id, "time": expire_time, "number_of_participants": number_of_participants, "participant_name": user_name, "gathering": "Y"}})

    def event_expire():
        db.restaurant.findOneAndUpdate({"_id": ObjectId(restaurant_id)}, {"$unset" : {"creator" : "", "gathering" : "", "meeting_time" : "", "participants_name": "", "participants_number": ""}})

    sched = BackgroundScheduler(daemon=True)
    sched.add_job(event_expire, 'interval', minutes = meeting_time)
    sched.start()

    return jsonify({ "result" : "success"})

##로그인 데코레이터
@app.route("/join_event", methods=["POST"])
def join_event():
    ##
    user_id = request.form["userId"]
    ##
    restaurant_id = request.form["restaurantId"]

    user_info = db.user.find_one({"_id" : ObjectId(user_id)})
    user_name = user_info["fullname"]

    user = db.restaurant.update_one({"_id": restaurant_id}, {"$push": {"participant_name": user_name}})

    return jsonify({ "result" : "success"})

##로그인 데코레이터
@app.route("/like", methods=["POST"])       ####join_event 데코레이터 오류나서 이름 바꾸겠습니다.
def like_event():
    ##
    user_id = request.form["userId"]
    ##
    restaurant_id = request.form["restaurantId"]

    user_info = db.user.find_one({"_id" : ObjectId(user_id)})
    user_name = user_info["fullname"]

    user = db.restaurant.update_one({"_id": restaurant_id}, {"$inc": {"like_number": 1}})

    return jsonify({ "result" : "success"})


@app.route("/listing", methods=["GET"])
def main_listing():
    all_restaurants = db.restaurant.find({})

    open_list = []
    close_list = []
    for restaurant in all_restaurants:
        if "event" in restaurant:
            expire_time = restaurant["event"]["expire_time"]
            tmp = datetime.strptime(expire_time, "%Y-%m-%d %H:%M")
            restaurant["event"]["expire_time"] = tmp
            open_list.append(restaurant)
        else:
            close_list.append(restaurant)

    open_list.sort(key = lambda x: x["event"]["expire_time"])
    close_list.sort(key = lambda x: x["likes"], reverse=True)

    result = open_list + close_list

    return render_template('index.html')
    #jsonify({ "result" : "success", "memo" : result })



@app.route("/signup", methods=["POST"])
def sign_up():
    fullname = request.form["name_give"]
    email = request.form["email_give"]
    password = request.form["password_give"]
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("UTF-8")

    if db.user.count_documents({"email" : email}):
        return jsonify({ "result" : "fail", "message": "EMAIL_ALREADY_EXISTS" }), 401
    else:
        user = {"email" : email, "password": hashed_password, "fullname": fullname }
        db.user.insert_one(user)

    return jsonify({"result": "success"})

@app.route("/login", methods=["POST"])
def sign_in():
    email = request.form["email_give"]
    password = request.form["password_give"]

    if not db.user.count_documents({"email" : email}):
        return jsonify({ "result": "fail", "message": "INVALID_USER" }), 401
#####
    user = db.user.find_one({"email" : email}, {"_id":False})
    # return jsonify({"user" : user["password"]})

    if bcrypt.checkpw(password.encode("UTF-8"), user["password"].encode("UTF-8")):
        ###
        access_token = jwt.encode({"fullname": user["fullname"]}, SECRET_KEY, algorithm = ALGORITHM)
        ###
        return jsonify({ "result": "success", "access_token": access_token}), 200

    else:
        return jsonify({ "result": "fail", "message": "INVALID_USER_INFO"}), 200






    

if __name__ == '__main__':
    app.run("0.0.0.0", port=5000, debug=True)