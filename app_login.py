from flask import *
from flask_jwt_extended import *
from pymongo import MongoClient
from datetime import datetime, timedelta
import bcrypt
from bson.objectid import ObjectId

app = Flask(__name__, template_folder="templates")

client = MongoClient('localhost', 27017)
db = client.dbmatna

@app.route("/signup", methods=['GET','POST'])
def sign_up():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        # 회원정보 생성
        username = request.form.get('name_give')
        #email = request.form.get('email')
        #ordinal = request.form.get('ordinal')
        useremail = request.form.get('email_give')
        password = request.form.get('password_give')
        
        if username == "":
            flash("Please Input Username")
            return render_template("index.html")
        elif useremail == "":
            flash("Please Input Userid")
            return render_template("index.html")
        elif password == "":
            flash("Please Input password")
            return render_template("index.html")
        
        signup = client.dbmatna.signup
        check_cnt = signup.find({"useremail": useremail}).count()
        if check_cnt > 0:
            flash("It is a registered userid")
            return render_template("index.html")    
        to_db = {
            "useremail" : useremail,
            "username": username,
            "password": bcrypt.hashpw(password),
        }

        to_db_signup = signup.insert_one(to_db)
        return jsonify({'result': 'success'})


        ####### 로그인용 ##########
        #last_signup = signup.find_one({"useremail":useremail})
        #if bcrypt.checkpw(password)

        



    # new_user_id = app.database.execute(text("""
    #     INSERT INTO users (
    #         name,
    #         email,
    #         hashed_password
    #     ) VALUES (
    #         :name,
    #         :email,
    #         :password
    #     )
    # """), new_user).lastrowid
    # new_user_info = get_user(new_user_id)

    #return jsonify(new_user_info)

@app.route('/login', methods=['POST'])
def login():
    data        = request.json
    email       = data['email']				# 2)
    password    = data['password']			# 3)

    row = database.execute(text("""			# 4)
        SELECT
            id,
            hashed_password
        FROM users
        WHERE email = :email
    """), {'email' : email}).fetchone()

    if row and bcrypt.checkpw(password.encode('UTF-8'),
    row['hashed_password'].encode('UTF-8')):				# 5)
        user_id = row['id']
        payload = {											# 6)
            'user_id' : user_id,
            'exp'     : datetime.utcnow() + timedelta(seconds = 60 * 60 * 24)
        }
        token = jwt.encode(payload, app.config['JWT_SECRET_KEY'], 'HS256')	# 7)

        return jsonify({
            'acces_token' : token.decode('UTF-8')					# 8)
        })
    else:
        return '', 401

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)