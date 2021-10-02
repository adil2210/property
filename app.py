from flask import Flask
from flask import *
from database import *
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
# app.config['SQLALCHEMY_POOL_SIZE'] = 1000
# app.config['SQLALCHEMY_POOL_TIMEOUT'] = 3000
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
db.create_all()



@app.route("/signupp", methods=['GET', 'POST'])
def SignUp():
    if (request.method == 'POST'):
        # if checkPermission(getUserId(),"Accounts"):
        signupAPI = request.get_json()
        username = signupAPI['firstName'] + " " + signupAPI['lastName']
        email = signupAPI['email']
        password = signupAPI['password']
        hashed = pbkdf2_sha256.hash(password)
        phoneno = signupAPI['phone']
        cnic = signupAPI['cnic']
        role = signupAPI['role']
        newUser = signup(username=username, email=email,
                        password=hashed, phoneno=phoneno, cnic=cnic, role=role,resetCode=0)
        print(db.session.add(newUser))
        db.session.commit()
        return make_response("added"), 200
            

@app.route('/getdata',methods=['GET'])
def getdata():
    get=signup.query.all()
    print(get)
    return make_response("ok")


db.create_all()

if __name__ == "__main__":
    app.run()