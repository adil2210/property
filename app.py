from distutils.log import debug
from sqlalchemy import and_, or_, not_, update, func, delete
from sqlalchemy.sql.dml import Update
from flask import Flask
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import *
from wtforms import *
from passlib.hash import pbkdf2_sha256
import hashlib
import datetime
from functools import wraps
from flask import *
import pymysql
import jwt
import datetime
from flask_mail import Mail, Message
from sqlalchemy import create_engine
import random
from database import *
from construction import construction

import sqlite3 as sql
from flask_marshmallow import Marshmallow
import os


pymysql.install_as_MySQLdb()


app = Flask(__name__, static_url_path='',
            static_folder='files')

CORS(app)
mail = Mail(app)
app.secret_key = 'ghjc'
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
# app.config['SQLALCHEMY_POOL_SIZE'] = 1000
# app.config['SQLALCHEMY_POOL_TIMEOUT'] = 3000
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://adil2210:adilraheel@database-1.clxvaukfjppa.us-east-2.rds.amazonaws.com:3332/property'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:adil2210@localhost:3307/propertymanagment'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://arzmark_abr:3c~B~sYq3lqF@162.55.131.89:3306/arzmark_propertManagment'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://abr-fd9d:Asdf1234@mysql.stackcp.com:57504/propertyManagment-31373362f0'
db = SQLAlchemy(app)


db.create_all()

app.register_blueprint(construction)

UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PLOT_FOLDER = 'plotimg'
app.config['PLOT_FOLDER'] = PLOT_FOLDER
app.config['SECRET_KEY'] = 'JustDemonstrating'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['SQLALCHEMY_POOL_SIZE'] = 1000
app.config['SQLALCHEMY_POOL_TIMEOUT'] = 3000


app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'adil22108@gmail.com'
app.config['MAIL_PASSWORD'] = 'adil4329156457'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False

mail = Mail(app)


@app.route('/images/<path:path>')
def serve_page(path):
    print(path)
    return send_from_directory('images', path)


@app.route("/", methods=['POST'])
def deploy():
    return make_response("badar")


@app.route("/email")
def index():
    msg = Message('Hello cake', sender=app.config['MAIL_USERNAME'], recipients=[
                  'badarbaig21@gmail.com'])
    msg.body = "Hello Flask message sent from Flask-Mail"
    mail.send(msg)
    return "Sent"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def checkPermission(userid, name):
    checkP = db.session.query(permissions).filter(
        permissions.uid == userid).all()
    print(checkP)
    for i in checkP:
        if i.Supper and name == "Supper":
            return True
        elif i.Sale and name == "Sale":
            return True
        elif i.Accounts and name == "Accounts":
            return True
        elif i.Purchase and name == "Purchase":
            return True
        else:
            return False


def getUserId():
    jwtToken = request.headers.get('Authorization')
    cleared_header = jwtToken[7:]
    print("token is:", cleared_header)
    decodedToken = jwt.decode(
        cleared_header, app.config['SECRET_KEY'], algorithms=["HS256"])
    return decodedToken['id']


@app.route("/signup", methods=['GET', 'POST'])
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
        Accounts = signupAPI['permissions']['accounts']
        Purchase = signupAPI['permissions']['purchase']
        Sale = signupAPI['permissions']['sale']
        Supper = signupAPI['permissions']['supper']
        construction = signupAPI['permissions']['construction']
        checkEmail = signup.query.filter_by(email=email).first()
        checkphone = signup.query.filter_by(phoneno=phoneno).first()
        checkcnic = signup.query.filter_by(cnic=cnic).first()
        if checkEmail != None and checkphone != None and checkcnic != None:
            return make_response("Email or Phone No or CNIC both already exists"), 400
        else:
            if checkEmail == None:
                if checkphone == None:
                    if checkcnic == None:
                        newUser = signup(username=username, email=email,
                                         password=hashed, phoneno=phoneno, cnic=cnic, role=role, resetCode=0)
                        db.session.add(newUser)
                        db.session.commit()
                        getId = signup.query.all()
                        n = 0
                        for i in getId:
                            n = i.id
                        addPerm = permissions(uid=n, Accounts=Accounts, Purchase=Purchase,
                                              Sale=Sale, Supper=Supper, construction=construction)
                        db.session.add(addPerm)
                        db.session.commit()
                        return make_response("added"), 200
                    else:
                        return make_response("CNIC already exist"), 400
                else:
                    return make_response("Phone-NO already exist"), 400
            else:
                return make_response("Email already exist"), 400

# delete user


@app.route('/deleteUser/<int:idd>', methods=['DELETE'])
def deleteUser(idd):
    if (request.method == 'DELETE'):
        # stmt = (delete(signup).where(signup.id == id))
        # stmt = signup.query.get(id)
        # db.session.delete(stmt)
        # db.session.commit()
        getData = accountsdetail.query.filter(accountsdetail.uid == idd).all()
        id = 0
        for i in getData:
            id = i.id
        print(id)
        if getData:
            stmt1 = accountsdetail.query.get(id)
            db.session.delete(stmt1)
            db.session.commit()
        stmt = signup.query.get(idd)
        db.session.delete(stmt)
        db.session.commit()
    return make_response("ok"), 200


@app.route('/updateUser', methods=['PUT'])
def updateUser():
    if (request.method == 'PUT'):
        updateObj = request.get_json()
        stmt = (update(signup).where(signup.id == updateObj['id']).values(
            username=updateObj['username'], email=updateObj['email'], phoneno=updateObj['phoneno'], cnic=updateObj['cnic']))
        db.session.execute(stmt)
        db.session.commit()
        q = signup.query.filter_by(id=updateObj['id']).all()
        for i in q:
            dict = {
                "username": i.username,
                "email": i.email,
                "phoneno": i.phoneno,
                "cnic": i.cnic
            }
        return dict
    else:
        return make_response('using put method for update!'), 400


# get all users from sign up
@app.route('/getallusers', methods=['GET'])
def getAllDataFromSignUp():
    if (request.method == 'GET'):
        allData = []
        getAllData = signup.query.all()
        print(getAllData)
        if getAllData:
            for data in getAllData:
                dict = {"id": data.id,
                        "username": data.username,
                        "email": data.email,
                        "phoneno": data.phoneno,
                        "cnic": data.cnic,
                        "role": data.role}
                allData.append(dict)
            print(allData)
            plotAllDataJson = json.dumps(allData)
            return plotAllDataJson
        else:
            return make_response("No data Found"), 400
    else:
        return make_response("Request in error"), 400


@app.route('/reset', methods=['POST'])
def resetPassword():
    if (request.method == 'POST'):
        resetApi = request.get_json()
        email = resetApi['email']
        email = str(email)
        checkEmailExist = signup.query.filter(signup.email == email).all()
        print(checkEmailExist)
        if checkEmailExist:
            randNo = random.randint(100000, 999999)
            print(randNo)
            print(email)
            msg = Message(
                'reset code', sender=app.config['MAIL_USERNAME'], recipients=[email])
            msg.body = str(randNo)
            mail.send(msg)
            stmt = (update(signup). where(
                signup.email == email). values(resetCode=randNo))
            db.session.execute(stmt)
            db.session.commit()
            return make_response("Code has sent on your email"), 200
        else:
            print('no such email found')
            return make_response('no such email found!'), 400
    else:
        return make_response("error")


@app.route('/checkCode', methods=['POST'])
def checkCodee():
    if (request.method == 'POST'):
        codeCheckApi = request.get_json()
        code = codeCheckApi['code']
        check = signup.query.filter(signup.resetCode == code).all()
        if check == None:
            return make_response("Enter Code is wrong"), 400
        else:
            return make_response("correct code"), 200


@app.route('/newPassword', methods=['POST'])
def newPassword():
    if (request.method == 'POST'):
        newPassApi = request.get_json()
        code = newPassApi['code']
        password = newPassApi['password']
        confirmPass = newPassApi['confirmPass']
        check = signup.query.filter(signup.resetCode == code).all()
        if check == None:
            return make_response("Enter Code is wrong"), 400
        else:
            if(password == confirmPass):
                hashed = pbkdf2_sha256.hash(password)
                stmt = (update(signup). where(
                    signup.resetCode == code). values(password=hashed))
                db.session.execute(stmt)
                db.session.commit()
            return make_response("correct code"), 200


@app.route('/login', methods=['POST'])
def login():
    if (request.method == 'POST'):
        loginApi = request.get_json()
        username = loginApi['username']
        email = loginApi['email']
        password = loginApi['password']
        if not username:
            return 'Missing username', 400
        if not email:
            return 'Missing email', 400
        if not password:
            return 'Missing password', 400
        user = signup.query.filter(signup.email == email).all()
        if not user:
            return 'User Not Found!', 404
        #session["uid"] = user.id
        for i in user:
            idd = i.id
            passs = i.password
            name = i.username
            emaill = i.email
            role = i.role
        getPermissions = permissions.query.filter(permissions.uid == idd).all()
        print(getPermissions)
        for n in getPermissions:
            acc = n.Accounts
            pur = n.Purchase
            s = n.Sale
            su = n.Supper
            con = n.construction

        if pbkdf2_sha256.verify(password, passs):
            session['logged in'] = True
            data = {
                'id': idd,
                'username': name,
                'email': emaill,
                'role': role,
                'Accounts': acc,
                'Purchase': pur,
                'Sale': s,
                'Supper': su,
                'construction': con,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }
            token = (jwt.encode(data, app.config['SECRET_KEY']))
            temp = [token]
            obj = json.dumps(temp)
            return obj
        else:
            return 'Invalid Login Info!', 400


@app.route('/addsociety', methods=['POST'])
def addsocietydataa():
    if (request.method == 'POST'):
        if checkPermission(getUserId(), "Supper"):
            jwtToken = request.headers.get('Authorization')
            cleared_header = jwtToken[7:]
            #stripHeader = cleared_header.strip(".")
            print("token is:", cleared_header)
            #decoded = base64.b64decode(jwtToken)
            decodedToken = jwt.decode(
                cleared_header, app.config['SECRET_KEY'], algorithms=["HS256"])
            print("decode token id is : ", decodedToken["id"])
            addSocietApi = request.get_json()
            societyname = addSocietApi['societyname']
            sectorno = addSocietApi['sectorno']
            plotno = addSocietApi['plotno']
            plotsize = addSocietApi['plotsize']
            plottype = addSocietApi['plottype']
            description = addSocietApi['description']
            # sectormapimg = request.files['sectormapimg']
            checkPlotSociety = addsocietydata.query.filter(and_(addsocietydata.plotno == plotno,
                                                                addsocietydata.societyname == societyname)).first()
            # if sectormapimg and allowed_file(sectormapimg.filename):
            #     sectorFilename = secure_filename(sectormapimg.filename)
            #     sectormapimg.save(os.path.join(
            #         app.config['UPLOAD_FOLDER'], sectorFilename))
            #     print(sectormapimg.read())
            #     sectormapimgPath = ('images/' + sectorFilename)
            # else:
            #     return make_response("Wrong Sector Image Extension"), 400

            print(checkPlotSociety)

            if checkPlotSociety:
                return make_response("Plot No already exists in this society"), 400
            else:
                addSocitey = addsocietydata(uid=decodedToken["id"], societyname=societyname, sectorno=sectorno, plotno=plotno, plotsize=plotsize,
                                            plottype=plottype, description=description)
                db.session.add(addSocitey)
                db.session.commit()
                # for file in files:
                #     if file and allowed_file(file.filename):
                #         Plotfilename = secure_filename(file.filename)
                #         file.save(os.path.join(
                #             app.config['PLOT_FOLDER'], Plotfilename))
                #         plotimgPath = ('plotimg/' + Plotfilename)
                #         multipleimages = plotimages(
                #             plotnum=plotno, img=plotimgPath)
                #         db.session.add(multipleimages)
                #         db.session.commit()
                #     else:
                #         return make_response("Wrong Plot Image Extension"), 400
                return make_response("added"), 200
        else:
            return make_response("Access Denied"), 400


@app.route('/getalladdsocietydata', methods=['GET'])
def getAllDataFromAddSocietyData():
    if (request.method == 'GET'):
        allData = []
        getAllData = addsocietydata.query.all()
        print(getAllData)
        if getAllData:
            for data in getAllData:
                dict = {"id": data.id,
                        "societyname": data.societyname,
                        "sectorno": data.sectorno,
                        "plotno": data.plotno,
                        "plotsize": data.plotsize,
                        "plottype": data.plottype,
                        "description": data.description,
                        }
                allData.append(dict)
            print(allData)
            plotAllDataJson = json.dumps(allData)
            return plotAllDataJson
        else:
            return make_response("No data Found"), 400
    else:
        return make_response("Request in error"), 400


# get accounts data
@app.route('/getAccountData/<int:id>', methods=['GET'])
def getAccountDataa(id):
    if request.method == 'GET':
        accountData = accountsdetail.query.filter(
            accountsdetail.id == id).all()
        print(accountData)
        return "accountData"
    else:
        print('error in appp')


# get society name for add plot to purchase
@app.route('/getsocietiesname', methods=['GET'])
def getAllSocieties():
    societiesName = []
    allSocietyData = addsocietydata.query.all()
    for name in allSocietyData:
        if name.societyname not in societiesName:
            societiesName.append(name.societyname)
    print("all society names ", societiesName)
    societyNameJson = json.dumps(societiesName)
    return societyNameJson


# get sector no for add plot to purchase

@app.route('/getsectors', methods=['POST'])
def getAllSectors():
    sectorlist = []
    allsectors = request.get_json()
    societyname = allsectors['societyname']
    getSectors = addsocietydata.query.filter(
        (addsocietydata.societyname == societyname)).all()
    for sector in getSectors:
        if sector.sectorno not in sectorlist:
            sectorlist.append(sector.sectorno)
    sectorJson = json.dumps(sectorlist)
    return sectorJson


# get plot no for add plot to purchase

@app.route('/getplots', methods=['POST'])
def getAllplots():
    plotlist = []
    temp = []
    allplots = request.get_json()
    sectorno = allplots['sectorno']
    societyname = allplots['societyname']
    getData = plottopurchase.query.filter(and_(plottopurchase.sectorno == sectorno,
                                               plottopurchase.societyname == societyname)).all()
    getplots = addsocietydata.query.filter(and_(addsocietydata.sectorno == sectorno,
                                                addsocietydata.societyname == societyname)).all()
    for n in getData:
        temp.append(n.plotno)
    print(temp)
    for plot in getplots:
        p = plot.plotno
        if (p not in temp):
            plotlist.append(plot.plotno)
    plotJson = json.dumps(plotlist)
    return plotJson


@app.route('/plottopurchase', methods=['POST'])
def addPlotToPurchase():
    if (request.method == 'POST'):
        if checkPermission(getUserId(), "Supper"):
            plotToPurchaseApi = request.get_json()
            societyname = plotToPurchaseApi['societyname']
            sectorno = plotToPurchaseApi['sectorno']
            plotno = plotToPurchaseApi['plot']
            development = bool(plotToPurchaseApi['development'])
            description = plotToPurchaseApi['description']
            plotamount = float(plotToPurchaseApi['plotamount'])
            plotownername = plotToPurchaseApi['plotownername']
            getplots = addsocietydata.query.filter(and_(addsocietydata.sectorno == sectorno,
                                                        addsocietydata.societyname == societyname, addsocietydata.plotno == plotno)).all()
            idd = 0
            for plot in getplots:
                idd = plot.id
            addtoPurchase = plottopurchase(uid=idd, societyname=societyname, sectorno=sectorno, plotno=plotno, development=development,
                                           description=description, plotamount=plotamount, plotownername=plotownername, dateTime=datetime.datetime.now())
            db.session.add(addtoPurchase)
            db.session.commit()
            return make_response("ok"), 200
        else:
            return make_response("Access Denied")


@app.route('/allplotforpurchasesummary', methods=['GET'])
def getAllDataForPurchaseSummary():
    if (request.method == 'GET'):
        allData = []
        temp = []
        getAllData = db.session.query(plottopurchase, addsocietydata).filter(
            plottopurchase.uid == addsocietydata.id).all()
        print(getAllData)
        if getAllData:
            for data in getAllData:
                dict = {"id": data.plottopurchase.id,
                        "societyname": data.plottopurchase.societyname,
                        "sectorno": data.plottopurchase.sectorno,
                        "plotno": data.plottopurchase.plotno,
                        "development": data.plottopurchase.development,
                        "plotamount": data.plottopurchase.plotamount,
                        "plotownername": data.plottopurchase.plotownername,
                        "plottype": data.addsocietydata.plottype,
                        "plotsize": data.addsocietydata.plotsize
                        }
                allData.append(dict)
            plotAllDataJson = json.dumps(allData)
            return plotAllDataJson
        else:
            return make_response("No data Found"), 400
    else:
        return make_response("Request in error"), 400


@app.route('/updatePlot', methods=['PUT'])
def updatePlot():
    if (request.method == 'PUT'):
        plotObj = request.get_json()
        stmt = (update(plottopurchase).where(plottopurchase.id == plotObj['id']).values(
            development=plotObj['development'], plotamount=plotObj['plotamount'], plotownername=plotObj['plotownername']))
        getData = plottopurchase.query.filter(
            plottopurchase.id == plotObj['id']).all()
        for i in getData:
            uidd = i.uid
        stmt1 = (update(addsocietydata).where(addsocietydata.id == uidd).values(
            plottype=plotObj['plottype'], plotsize=plotObj['plotsize']))
        db.session.execute(stmt1)
        db.session.commit()
        db.session.execute(stmt)
        db.session.commit()
        return ("ok"), 200


@app.route('/deletePlot/<int:id>', methods=['DELETE'])
def deletePlot(id):
    if (request.method == 'DELETE'):
        # stmt = (delete(signup).where(signup.id == id))
        getData = plottopurchase.query.filter(plottopurchase.id == id).all()
        for i in getData:
            uidd = i.uid
        stmt = plottopurchase.query.get(id)
        print(stmt)
        db.session.delete(stmt)
        db.session.commit()
        stmt1 = addsocietydata.query.get(uidd)
        db.session.delete(stmt1)
        db.session.commit()
    return make_response("ok"), 200


#  get all data from plot to purchase table

@app.route('/getallpptdata', methods=['GET'])
def getAllDataFromPlotToPurchase():
    if (request.method == 'GET'):
        allData = []
        temp = []
        getAllData = plottopurchase.query.all()
        getData = payments.query.all()
        for n in getData:
            temp.append(n.plotid)
        print(temp)
        if getAllData:
            for data in getAllData:
                s = data.id
                if s not in temp:
                    dict = {"id": data.id,
                            "societyname": data.societyname,
                            "sectorno": data.sectorno,
                            "plotno": data.plotno,
                            "development": data.development,
                            "description": data.description,
                            "plotamount": data.plotamount,
                            "plotownername": data.plotownername,
                            "dateTime": data.dateTime,
                            }
                    allData.append(dict)
            plotAllDataJson = json.dumps(allData)
            return plotAllDataJson
        else:
            return make_response("No data Found"), 400
    else:
        return make_response("Request in error"), 400


# get society name from plot to purchase module for purchase ppt module

@app.route('/getsocietiesnameforppt', methods=['GET'])
def getAllSocietyForppt():
    societiesName = []
    temp = []
    getData = payments.query.all()
    allSocietyData = plottopurchase.query.all()
    for n in getData:
        temp.append(n.plotid)
    for name in allSocietyData:
        s = name.id
        if name.societyname not in societiesName:
            if s not in temp:
                societiesName.append(name.societyname)
    print("all society names ", societiesName)
    societyNamePPTJson = json.dumps(societiesName)
    return societyNamePPTJson


# get sector no for purchase ppt module

@app.route('/getsectorsforppt', methods=['POST'])
def getAllSectorsForppt():
    sectorlist = []
    temp = []
    allsectors = request.get_json()
    societyname = allsectors['societyname']
    getData = payments.query.all()
    getSectors = plottopurchase.query.filter(
        (plottopurchase.societyname == societyname)).all()
    for n in getData:
        temp.append(n.plotid)
    for sector in getSectors:
        s = sector.id
        if sector.sectorno not in sectorlist:
            if s not in temp:
                sectorlist.append(sector.sectorno)
    sectorpptJson = json.dumps(sectorlist)
    return sectorpptJson

# get plot information from plot to purchase table


@app.route('/getplotsforppt', methods=['GET'])
def getAllplotsInfoFromPPT():
    if [request.method == 'GET']:
        plotlist = []
        allplots = request.get_json()
        sectorno = allplots['sectorno']
        societyname = allplots['societyname']
        getplots = plottopurchase.query.filter(and_(plottopurchase.sectorno == sectorno,
                                                    plottopurchase.societyname == societyname)).all()
        for plot in getplots:
            dict = {"id": plot.id,
                    "societyname": plot.societyname,
                    "sectorno": plot.sectorno,
                    "plotno": plot.plotno,
                    "development": plot.development,
                    "description": plot.description,
                    "plotamount": plot.plotamount,
                    "plotownername": plot.plotownername,
                    "dateTime": plot.dateTime,
                    }
            plotlist.append(dict)
        plotpptJson = json.dumps(plotlist)
        return plotpptJson
    else:
        return make_response("Error"), 400


@app.route('/infoAgainstSocietyNameSectorNo/<societyname>/<sectorno>', methods=['GET'])
def infoAgainstSocietyNameSectorNo(societyname, sectorno):
    if [request.method == 'GET']:
        plotlist = []
        temp = []
        # allplots = request.get_json()
        getData = plottopurchase.query.filter(and_(
            plottopurchase.societyname == societyname, plottopurchase.sectorno == sectorno)).all()
        for plot in getData:
            dict = {"plotno": plot.plotno}
            temp.append(dict)
        for i in temp:
            getData1 = addsocietydata.query.filter(and_(addsocietydata.sectorno == sectorno,
                                                        addsocietydata.societyname == societyname, addsocietydata.plotno == i['plotno'])).all()
        for plot, plot1 in zip(getData, getData1):
            dict = {"id": plot.id,
                    "societyname": plot.societyname,
                    "sectorno": plot.sectorno,
                    "plotno": plot.plotno,
                    "plotamount": plot.plotamount,
                    "description1": plot1.description,
                    "plotownername": plot.plotownername,
                    "dateTime": plot.dateTime,
                    "plotsize": plot1.plotsize,
                    "plottype": plot1.plottype,
                    "description": plot1.description,
                    }
            plotlist.append(dict)
        plotpptJson = json.dumps(plotlist)
        return plotpptJson
    else:
        return make_response("Error"), 400


@app.route('/saleInfoAgainstSocietyNameSectorNo/<societyname>/<sectorno>', methods=['POST'])
def saleInfoAgainstSocietyNameSectorNo(societyname, sectorno):
    if [request.method == 'POST']:
        plotlist = []
        temp = []
        temp1 = []
        partners = []
        admin = []
        # allplots = request.get_json()
        getData = payments.query.filter(
            and_(payments.societyName == societyname, payments.sectorNo == sectorno)).all()
        for plot in getData:
            dict = {"plotno": plot.plotNo}
            temp.append(dict)
        getData1 = ""
        getData2 = ""
        getData3 = ""
        for i in temp:
            getData1 = plottopurchase.query.filter(and_(plottopurchase.sectorno == sectorno,
                                                        plottopurchase.societyname == societyname, plottopurchase.plotno == i['plotno'])).all()
            getData2 = addsocietydata.query.filter(and_(addsocietydata.sectorno == sectorno,
                                                        addsocietydata.societyname == societyname, addsocietydata.plotno == i['plotno'])).all()
            getData3 = memberinplots.query.filter(and_(memberinplots.sectorNo == sectorno,
                                                       memberinplots.societyName == societyname, memberinplots.plotid == i['plotno'])).all()
        for n in getData3:
            if n.role == "partner":
                partners.append(n.names)
            if n.role == "admin":
                admin.append(n.names)
        for plot, plot1 in zip(getData1, getData2):
            dict = {"id": plot.id,
                    "societyname": plot.societyname,
                    "sectorno": plot.sectorno,
                    "plotno": plot.plotno,
                    "plotamount": plot.plotamount,
                    "description1": plot1.description,
                    "plotownername": plot.plotownername,
                    "dateTime": plot.dateTime,
                    "plotsize": plot1.plotsize,
                    "plottype": plot1.plottype,
                    "description": plot1.description,
                    "partner": partners,
                    "admin": admin
                    }
            plotlist.append(dict)
        plotpptJson = json.dumps(plotlist)
        return plotpptJson
    else:
        return make_response("Error"), 400


@app.route('/moregetplotsforppt/<int:id>', methods=['GET'])
def moreGetAllplotsInfoFromPPT(id):
    if [request.method == 'GET']:
        plotlist = []
        temp = []
        # allplots = request.get_json()
        getplots = plottopurchase.query.filter(
            and_(plottopurchase.id == id)).all()
        # getplots1 = addsocietydata.query.filter(and_(addsocietydata.id == id)).all()
        for plot in getplots:
            dict = {"societyname": plot.societyname,
                    "sectorno": plot.sectorno,
                    "plotno": plot.plotno}
            temp.append(dict)
        for i in temp:
            getplots1 = addsocietydata.query.filter(and_(addsocietydata.sectorno == i['sectorno'],
                                                    addsocietydata.societyname == i['societyname'], addsocietydata.plotno == i['plotno'])).all()
        for plot, plot1 in zip(getplots, getplots1):
            dict = {"id": plot.id,
                    "societyname": plot.societyname,
                    "sectorno": plot.sectorno,
                    "plotno": plot.plotno,
                    "plotamount": plot.plotamount,
                    "description1": plot.description,
                    "plotownername": plot.plotownername,
                    "dateTime": plot.dateTime,
                    "plotsize": plot1.plotsize,
                    "plottype": plot1.plottype,
                    "description": plot1.description
                    }
            plotlist.append(dict)
        plotpptJson = json.dumps(plotlist)
        return plotpptJson
    else:
        return make_response("Error"), 400


@app.route('/infoAgainstSocietyName/<societyname>', methods=['GET'])
def infoAgainstSocietyName(societyname):
    if [request.method == 'GET']:
        plotlist = []
        temp = []
        # allplots = request.get_json
        getData = plottopurchase.query.filter(
            and_(plottopurchase.societyname == societyname)).all()
        for plot in getData:
            dict = {"sectorno": plot.sectorno,
                    "plotno": plot.plotno}
            temp.append(dict)
        for i in temp:
            getData1 = addsocietydata.query.filter(and_(addsocietydata.sectorno == i['sectorno'],
                                                        addsocietydata.societyname == societyname, addsocietydata.plotno == i['plotno'])).all()
        for plot, plot1 in zip(getData, getData1):
            dict = {"id": plot.id,
                    "societyname": plot.societyname,
                    "sectorno": plot.sectorno,
                    "plotno": plot.plotno,
                    "plotamount": plot.plotamount,
                    "description1": plot.description,
                    "plotownername": plot.plotownername,
                    "dateTime": plot.dateTime,
                    "plotsize": plot1.plotsize,
                    "plottype": plot1.plottype,
                    "description": plot1.description,
                    }
            plotlist.append(dict)
        plotpptJson = json.dumps(plotlist)
        return plotpptJson
    else:
        return make_response("Error"), 400


@app.route('/saleInfoAgainstSocietyName/<societyname>', methods=['GET'])
def saleInfoAgainstSocietyName(societyname):
    if [request.method == 'GET']:
        plotlist = []
        temp = []
        # allplots = request.get_json
        getData = payments.query.filter(
            and_(payments.societyName == societyname)).all()
        for plot in getData:
            dict = {"sectorno": plot.sectorNo,
                    "plotno": plot.plotNo}
            temp.append(dict)
        for i in temp:
            getData2 = addsocietydata.query.filter(and_(addsocietydata.sectorno == i['sectorno'],
                                                        addsocietydata.societyname == societyname, addsocietydata.plotno == i['plotno'])).all()
            getData1 = plottopurchase.query.filter(and_(plottopurchase.sectorno == i['sectorno'],
                                                        plottopurchase.societyname == societyname, plottopurchase.plotno == i['plotno'])).all()
        for plot, plot1 in zip(getData1, getData2):
            dict = {"id": plot.id,
                    "societyname": plot.societyname,
                    "sectorno": plot.sectorno,
                    "plotno": plot.plotno,
                    "plotamount": plot.plotamount,
                    "description1": plot.description,
                    "plotownername": plot.plotownername,
                    "dateTime": plot.dateTime,
                    "plotsize": plot1.plotsize,
                    "plottype": plot1.plottype,
                    "description": plot1.description,
                    }
            plotlist.append(dict)
        plotpptJson = json.dumps(plotlist)
        return plotpptJson
    else:
        return make_response("Error"), 400


@app.route('/getallpartners', methods=['GET'])
def getAllpartners():
    if (request.method == 'GET'):
        partnerlist = []
        allUsers = signup.query.filter(signup.role == 'partner')
        for user in allUsers:
            dict = {"id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phoneno": user.phoneno,
                    "cnic": user.cnic,
                    "role": user.role}
            partnerlist.append(dict)
        partnerListJson = json.dumps(partnerlist)
        return partnerListJson
    else:
        return make_response("Error"), 400


@app.route('/getalladmins', methods=['GET'])
def getAlladmins():
    if (request.method == 'GET'):
        adminslist = []
        allUsers = signup.query.filter(signup.role == 'admin')
        for user in allUsers:
            dict = {"id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "phoneno": user.phoneno,
                    "cnic": user.cnic,
                    "role": user.role}
            adminslist.append(dict)
        adminListJson = json.dumps(adminslist)
        return adminListJson
    else:
        return make_response("Error"), 400


def checkTotalOfPayments(aIc, cA, pOa, ot):
    aIc = (aIc)
    cA = (cA)
    pOa = (pOa)
    ot = (ot)
    if aIc and cA and pOa and ot:
        add = aIc+cA+pOa+ot
        return add
    elif aIc and cA and pOa:
        add = aIc+cA+pOa
        return add
    elif aIc and cA and ot:
        add = aIc+cA+ot
        return add
    elif aIc and pOa and ot:
        add = aIc+pOa+ot
        return add
    elif cA and pOa and ot:
        add = cA+pOa+ot
        return add
    elif aIc and cA:
        add = aIc+cA
        return add
    elif aIc and pOa:
        add = aIc+pOa
        return add
    elif aIc and ot:
        add = aIc+ot
        return add
    elif cA and pOa:
        add = cA+pOa
        return add
    elif cA and ot:
        add = cA+ot
        return add
    elif pOa and ot:
        add = pOa+ot
        return add
    elif aIc:
        return aIc
    elif cA:
        return cA
    elif pOa:
        return pOa
    elif ot:
        return ot


@app.route('/accountdetails', methods=['POST'])
def accountsData():
    if (request.method == 'POST'):
        if checkPermission(getUserId(), "Accounts"):
            accountsApi = request.get_json()
            uid = accountsApi['uid']
            user = signup.query.filter_by(id=uid).all()
            for use in user:
                print('adil')
                cnic = use.cnic
                role = use.role
                name = use.username
                contactNo = use.phoneno
            accName = accountsApi['accName']
            bankName = accountsApi['bankName']
            accNo = accountsApi['accNo']
            amountToInvest = accountsApi['amountToInvest']
            amountInCash = accountsApi['amountInCash']
            chequeAmount = accountsApi['chequeAmount']
            noOfCheques = accountsApi['noOfCheques']
            chequeNo = accountsApi['chequeNo']
            chequeDescription = accountsApi['chequeDescription']
            payorderAmount = accountsApi['payorderAmount']
            noOfPayOrder = accountsApi['noOfPayOrder']
            payOrderNo = accountsApi['payOrderNo']
            payOrderDescription = accountsApi['payorderDescription']
            onlineTransfer = accountsApi['onlineTransfer']
            onlineDescription = accountsApi['onlineDescription']
            accDetails = accountsdetail.query.filter(
                accountsdetail.uid == uid).all()
            print(accDetails)
            if accDetails:
                print('already have account')
                return make_response('already have account'), 400
            else:
                if chequeAmount or payorderAmount or onlineTransfer or amountInCash:
                    tOp = checkTotalOfPayments(
                        amountInCash, chequeAmount, payorderAmount, onlineTransfer)
                    print(tOp)
                    if(tOp != float(amountToInvest)):
                        return make_response("added amount of is greater or smaller than total investment"), 400
                    else:
                        if(accDetails):
                            return make_response("user already exists"), 400
                        else:
                            accounts = accountsdetail(uid=uid, name=name, cnic=cnic, contactNo=contactNo, role=role, accName=accName, bankName=bankName, accNo=accNo, amountToInvest=amountToInvest,
                                                      dateTime=datetime.datetime.now(), amountInCash=amountInCash, chequeAmount=chequeAmount, noOfCheques=noOfCheques, chequeNo=chequeNo, chequeDescription=chequeDescription,
                                                      payorderAmount=payorderAmount, noOfPayOrder=noOfPayOrder, payOrderNo=payOrderNo, payOrderDescription=payOrderDescription, onlineTransfer=onlineTransfer, onlineDescription=onlineDescription)
                            db.session.add(accounts)
                            db.session.commit()
                            return make_response("added"), 200
        else:
            return make_response("Access Denied")


@app.route('/getIndividualAccountDetails/<int:id>', methods=['GET'])
def getAccountDetails(id):
    if [request.method == 'GET']:
        dataList = []
        # allplots = request.get_json()
        accDetails = accountsdetail.query.filter(
            and_(accountsdetail.uid == id)).all()
        print(accDetails)
        for data in accDetails:
            dict = {
                "id": data.id,
                "accName": data.accName,
                "bankName": data.bankName,
                "accNo": data.accNo,
                "amountToInvest": data.amountToInvest
            }
            if dict not in dataList:
                dataList.append(dict)
            # dataList.append(dict)
        dataListJson = json.dumps(dataList)
        return dataListJson
    else:
        return make_response("Error"), 400


# get all users from accounts table

@app.route('/getAccountData', methods=['GET'])
def getsAccountsData():
    if (request.method == 'GET'):
        accountslist = []
        accountsUsers = accountsdetail.query.all()
        for user in accountsUsers:
            dict = {"id": user.id,
                    "name": user.name,
                    "bankName": user.bankName,
                    "amountToInvest": user.amountToInvest,
                    "accName": user.accName
                    }
            accountslist.append(dict)
        accountslist = json.dumps(accountslist)
        return accountslist
    else:
        return make_response("Error"), 400


@app.route('/updateAccount', methods=['PUT'])
def updateAccountsData():
    if (request.method == 'PUT'):
        updateObj = request.get_json()
        stmt = (update(accountsdetail). where(
            accountsdetail.id == updateObj['id']). values(amountToInvest=updateObj['amountToInvest'], name=updateObj['name'], accName=updateObj['accName'], bankName=updateObj['bankName']))
        db.session.execute(stmt)
        db.session.commit()
        return make_response("yes"), 200
    else:
        return make_response('method error!'), 400


@app.route('/deleteAccount/<int:idd>', methods=['DELETE'])
def deleteUdeleteConstructionAccountser(idd):
    if (request.method == 'DELETE'):
        getData = accountsdetail.query.filter(accountsdetail.id == idd).all()
        id = 0
        for i in getData:
            id = i.id
        print(id)
        if getData:
            stmt = accountsdetail.query.get(idd)
            app.db.session.delete(stmt)
            app.db.session.commit()
        return make_response("ok"), 200


# get partner from account details table

@app.route('/getallpartnersforpayments', methods=['GET'])
def getAllpartnersForPayments():
    if (request.method == 'GET'):
        partnerlist = []
        allUsers = accountsdetail.query.filter(
            accountsdetail.role == 'partner')
        for user in allUsers:
            dict = {"id": user.id,
                    "name": user.name,
                    "contactNo": user.contactNo,
                    "cnic": user.cnic,
                    "amountToInvest": user.amountToInvest}
            partnerlist.append(dict)
        partnerListJson = json.dumps(partnerlist)
        return partnerListJson
    else:
        return make_response("Error"), 400


@app.route('/getalladminsforpayments', methods=['GET'])
def getAlladminsForPayments():
    if (request.method == 'GET'):
        adminslist = []
        allUsers = accountsdetail.query.filter(
            accountsdetail.role == 'admin')
        print("adil")
        print(allUsers)
        for user in allUsers:
            dict = {"id": user.id,
                    "name": user.name,
                    "amountToInvest": user.amountToInvest}
            adminslist.append(dict)
        adminListJson = json.dumps(adminslist)
        return adminListJson
    else:
        return make_response("Error"), 400


# function of sum of partner amounts is not greater than plot total amount

def checkTotalAmount(userid):
    totalPartnerAdmAmounts = 0
    for partner in userid:
        checkpAmount = float(partner['amount'])
        print("asdadf ", partner['amount'])
        totalPartnerAdmAmounts = float(
            totalPartnerAdmAmounts+checkpAmount)
    return totalPartnerAdmAmounts


def checkPartnerInvestmentWithAmount(partner):
    account = accountsdetail.query.filter(
        accountsdetail.id == partner['id']).all()
    for i in account:
        pInvestment = float(i.amountToInvest)
        pName = i.name
    pAmount = float(partner['amount'])
    if (pAmount > pInvestment):
        return pName


def checkAdminInvestmentWithAmount(partner):
    account = accountsdetail.query.filter(
        accountsdetail.id == partner['id']).all()
    for i in account:
        pInvestment = float(i.amountToInvest)
        pName = i.name
    pAmount = float(partner['amount'])
    if (pAmount > pInvestment):
        return pName


# all the payments are handling in this route

@app.route('/payments', methods=['POST'])
def paymentsDetails():
    if (request.method == 'POST'):
        print(getUserId())
        if checkPermission(getUserId(), "Purchase"):
            paymentsAPI = request.get_json()
            decodedToken = paymentsAPI['admData']

            # member in plots objectss
            userid = paymentsAPI['userid']
            adm_amounts = decodedToken["amount"]

            # payments objects
            societyName = paymentsAPI['societyname']
            sectorNo = paymentsAPI['sectorno']
            plotNo = paymentsAPI['plotno']
            amountInCash = paymentsAPI['amountInCash']
            chequeAmount = paymentsAPI['chequeAmount']
            noOfCheques = paymentsAPI['noOfCheques']
            chequeNo = paymentsAPI['chequeNo']
            chequeDescription = paymentsAPI['chequeDescription']
            payorderAmount = paymentsAPI['payorderAmount']
            noOfPayOrder = paymentsAPI['noOfPayOrder']
            payOrderNo = paymentsAPI['payOrderNo']
            payOrderDescription = paymentsAPI['payOrderDescription']
            tokenAmount = paymentsAPI['tokenAmount']
            tokenDays = paymentsAPI['tokenDays']
            tokenDescription = paymentsAPI['tokenDescription']
            taxAmount = paymentsAPI['taxAmount']
            taxDescription = paymentsAPI['taxDescription']
            onlineTransfer = paymentsAPI['onlineTransfer']
            onlineDescription = paymentsAPI['onlineDescription']
            completeOrNot = "complete"
            print(decodedToken["amount"])
            data = plottopurchase.query.filter(plottopurchase.societyname == societyName,
                                               plottopurchase.sectorno == sectorNo, plottopurchase.plotno == plotNo).all()
            for i in data:
                idd = i.id

            getTotalPlotAmount = plottopurchase.query.filter(
                plottopurchase.societyname == societyName, plottopurchase.sectorno == sectorNo, plottopurchase.plotno == plotNo).all()
            print(getTotalPlotAmount)
            totalAmount = 0
            # totalAmount = getTotalPlotAmount.plotamount
            for i in getTotalPlotAmount:
                totalAmount = i.plotamount
            totalAmount = float(totalAmount)
            remBalance = 0
            if tokenAmount:
                completeOrNot = "not"
                remBalance = totalAmount-tokenAmount
            else:
                remBalance = 0
                completeOrNot = "yes"

            if userid and adm_amounts:
                if checkTotalAmount(userid)+float((adm_amounts)) != float(totalAmount):
                    return make_response("The total sum of all the investments is greater or less than the plot total amount"), 400

                # check the total sum of cheque amount , amount in cash or payorder amount is equal to plot total amount
                if tokenAmount:
                    if amountInCash or chequeAmount or payorderAmount or onlineTransfer:
                        tOp = checkTotalOfPayments(
                            amountInCash, chequeAmount, payorderAmount, onlineTransfer)
                    if(tOp != float(tokenAmount)):
                        return make_response("added amount of token in cash, cheque, payorder or online transfer is greater or smaller than plot total amount"), 400
                else:
                    if amountInCash or chequeAmount or payorderAmount or onlineTransfer:
                        tOp = checkTotalOfPayments(
                            amountInCash, chequeAmount, payorderAmount, onlineTransfer)
                    if(tOp != (totalAmount)):
                        return make_response("added amount in cash, cheque, payorder or online transfer is greater or smaller than plot total amount"), 400
                if userid:
                    # checking the amount of partners amount is greater than their total investment
                    for partner in userid:
                        a = checkPartnerInvestmentWithAmount(partner)
                        if a:
                            return make_response("Added amount is greater than total investment of " + a), 400
                    if tokenAmount:
                        # deducting the amount of partners from their investments
                        for partner in userid:
                            account = accountsdetail.query.filter(
                                accountsdetail.id == partner['id']).all()
                            for i in account:
                                pInvestment = float(i.amountToInvest)
                                # pName = i.name
                            pAmount = float(partner['amount'])
                            percInPlotPart = float(
                                (pAmount/float(totalAmount))*100)
                            pTokenAmount = float(
                                (percInPlotPart/100)*float(tokenAmount))
                            taxDeductionValuePart = float(
                                (percInPlotPart/100)*float(taxAmount))
                            newInvest = float(pInvestment-pTokenAmount -
                                              taxDeductionValuePart)
                            stmt = (update(accountsdetail). where(
                                accountsdetail.id == partner['id']). values(amountToInvest=newInvest))
                            db.session.execute(stmt)
                            db.session.commit()
                            partnerAmountAgainstPLot = memberinplots(
                                userid=partner['id'], names=partner['name'], p_amounts=partner['amount'], adm_amounts="0", percentageInPlot=percInPlotPart, plotid=plotNo, role="partner", societyName=societyName, sectorNo=sectorNo, saleOrNot="No")
                            db.session.add(partnerAmountAgainstPLot)
                            db.session.commit()
                    else:
                        # deducting the amount of partners from their investments
                        for partner in userid:
                            account = accountsdetail.query.filter(
                                accountsdetail.id == partner['id']).all()
                            for i in account:
                                pInvestment = float(i.amountToInvest)
                                # pName = i.name
                            pAmount = float(partner['amount'])
                            percInPlotPart = float(
                                (pAmount/float(totalAmount))*100)
                            taxDeductionValuePart = float(
                                (percInPlotPart/100)*float(taxAmount))
                            newInvest = float(pInvestment-pAmount -
                                              taxDeductionValuePart)
                            stmt = (update(accountsdetail). where(
                                accountsdetail.id == partner['id']). values(amountToInvest=newInvest))
                            db.session.execute(stmt)
                            db.session.commit()
                            partnerAmountAgainstPLot = memberinplots(
                                userid=partner['id'], names=partner['name'], p_amounts=partner['amount'], adm_amounts="0", percentageInPlot=percInPlotPart, plotid=plotNo, role="partner", societyName=societyName, sectorNo=sectorNo, saleOrNot="No")
                            db.session.add(partnerAmountAgainstPLot)
                            db.session.commit()
                if adm_amounts:
                    # checking the amount of admin is greater than their total investment
                    adminaccount = accountsdetail.query.filter(
                        accountsdetail.id == decodedToken["id"]).all()
                    print(adminaccount)
                    for i in adminaccount:
                        adInvestment = int(i.amountToInvest)
                        adName = i.name
                    print("adil")
                    print(adInvestment)

                    if (int(adm_amounts) > adInvestment):
                        return make_response("Added amount is greater than total investment of " + adName), 400

                    if tokenAmount:
                        if amountInCash or chequeAmount or payorderAmount or onlineTransfer:
                            tOp = checkTotalOfPayments(
                                amountInCash, chequeAmount, payorderAmount, onlineTransfer)
                        if(tOp > float(tokenAmount)):
                            return make_response("added amount greater than plot total amount"), 400

                        adminaccount = accountsdetail.query.filter(
                            accountsdetail.uid == decodedToken["id"]).all()
                        for i in adminaccount:
                            adInvestment = float(i.amountToInvest)
                            adName = i.name

                        percInPlotadm = (
                            (float(adm_amounts)/float(totalAmount))*100)
                        admTokenAmount = float(
                            (percInPlotadm/100)*float(tokenAmount))
                        taxDeductionValueadm = (
                            float(percInPlotadm/100)*float(taxAmount))
                        adnewInvest = float(
                            adInvestment-float(admTokenAmount)-taxDeductionValueadm)
                        acc = accountsdetail.query.filter(
                            accountsdetail.id == decodedToken["id"]).all()
                        temp = []
                        for i in acc:
                            dict = {"id": i.id}
                            temp.append(dict)
                        stmt = (update(accountsdetail). where(
                            accountsdetail.id == decodedToken['id']). values(amountToInvest=adnewInvest))
                        db.session.execute(stmt)
                        db.session.commit()
                        partnerAmountAgainstPLot = memberinplots(
                            userid=temp[0]['id'], names=adName, adm_amounts=adm_amounts, p_amounts="0", percentageInPlot=percInPlotadm, plotid=plotNo, role="admin", societyName=societyName, sectorNo=sectorNo, saleOrNot="No")
                        db.session.add(partnerAmountAgainstPLot)
                        db.session.commit()
                    else:
                        # deducting the amount of admin from their investments
                        adminaccount = accountsdetail.query.filter(
                            accountsdetail.uid == decodedToken["id"]).all()
                        for i in adminaccount:
                            adInvestment = float(i.amountToInvest)
                            adName = i.name
                            print(adName)
                        percInPlotadm = (
                            (float(adm_amounts)/float(totalAmount))*100)
                        taxDeductionValueadm = (
                            float(percInPlotadm/100)*float(taxAmount))
                        adnewInvest = float(
                            adInvestment-float(adm_amounts)-taxDeductionValueadm)
                        acc = accountsdetail.query.filter(
                            accountsdetail.id == decodedToken["id"]).all()
                        print(acc)
                        temp = []
                        for i in acc:
                            dict = {"id": i.id}
                            temp.append(dict)
                        print(temp)
                        stmt = (update(accountsdetail). where(
                            accountsdetail.id == decodedToken['id']). values(amountToInvest=adnewInvest))
                        db.session.execute(stmt)
                        db.session.commit()
                        partnerAmountAgainstPLot = memberinplots(
                            userid=temp[0]['id'], names=adName, adm_amounts=adm_amounts, p_amounts="0", percentageInPlot=percInPlotadm, plotid=plotNo, role="admin", societyName=societyName, sectorNo=sectorNo, saleOrNot="No")
                        db.session.add(partnerAmountAgainstPLot)
                        db.session.commit()

            elif userid:
                # check partners investments is not grater than or less than total plot amount
                if checkTotalAmount(userid) != float(totalAmount):
                    return make_response("The total sum of all the investments is greater or less than the plot total amount"), 400

                # checking the amount of partners amount is greater than their total investment
                for partner in userid:
                    a = checkPartnerInvestmentWithAmount(partner)
                    if a:
                        return make_response("Added amount is greater than total investment of " + a), 400

                # check the total sum of cheque amount , amount in cash or payorder amount is equal to plot total amount
                if tokenAmount:
                    if amountInCash or chequeAmount or payorderAmount:
                        tOp = checkTotalOfPayments(
                            amountInCash, chequeAmount, payorderAmount)
                    if(tOp != float(tokenAmount)):
                        return make_response("added amount of token in cash, cheque, payorder or online transfer is greater or smaller than plot total amount"), 400
                else:
                    if amountInCash or chequeAmount or payorderAmount:
                        tOp = checkTotalOfPayments(
                            amountInCash, chequeAmount, payorderAmount, onlineTransfer)
                    if(tOp != float(totalAmount)):
                        return make_response("added amount in cash, cheque, payorder or online transfer is greater or smaller than plot total amount"), 400

                if tokenAmount:
                    # deducting the amount of partners from their investments
                    for partner in userid:
                        account = accountsdetail.query.filter(
                            accountsdetail.id == partner['id']).all()
                        for i in account:
                            pInvestment = float(i.amountToInvest)
                            # pName = i.name
                        pAmount = float(partner['amount'])
                        percInPlotPart = float(
                            (pAmount/float(totalAmount))*100)
                        pTokenAmount = float(
                            (percInPlotPart/100)*float(tokenAmount))
                        taxDeductionValuePart = float(
                            (percInPlotPart/100)*float(taxAmount))
                        newInvest = float(pInvestment-pTokenAmount -
                                          taxDeductionValuePart)
                        stmt = (update(accountsdetail). where(
                            accountsdetail.id == partner['id']). values(amountToInvest=newInvest))
                        db.session.execute(stmt)
                        db.session.commit()
                        partnerAmountAgainstPLot = memberinplots(
                            userid=partner['id'], names=partner['name'], p_amounts=partner['amount'], adm_amounts="0", percentageInPlot=percInPlotPart, plotid=plotNo, role="partner", societyName=societyName, sectorNo=sectorNo, saleOrNot="No")
                        db.session.add(partnerAmountAgainstPLot)
                        db.session.commit()
                else:
                    # deducting the amount of partners from their investments
                    for partner in userid:
                        account = accountsdetail.query.filter(
                            accountsdetail.id == partner['id']).all()
                        for i in account:
                            pInvestment = float(i.amountToInvest)
                            # pName = i.name
                        pAmount = float(partner['amount'])
                        percInPlotPart = float(
                            (pAmount/float(totalAmount))*100)
                        taxDeductionValuePart = float(
                            (percInPlotPart/100)*float(taxAmount))
                        newInvest = float(pInvestment-pAmount -
                                          taxDeductionValuePart)
                        stmt = (update(accountsdetail). where(
                            accountsdetail.id == partner['id']). values(amountToInvest=newInvest))
                        db.session.execute(stmt)
                        db.session.commit()
                        partnerAmountAgainstPLot = memberinplots(
                            userid=partner['id'], names=partner['name'], p_amounts=partner['amount'], adm_amounts="0", percentageInPlot=percInPlotPart, plotid=plotNo, role="partner", societyName=societyName, sectorNo=sectorNo, saleOrNot="No")
                        db.session.add(partnerAmountAgainstPLot)
                        db.session.commit()

            elif adm_amounts:
                # check the admin investment is not grater than or less than total plot amount
                if float(adm_amounts) > float(totalAmount):
                    return make_response("The total sum of the investments is greater or less than the plot total amount"), 400

                # checking the amount of admin is greater than their total investment
                adminaccount = accountsdetail.query.filter(
                    accountsdetail.id == decodedToken["id"]).all()
                for i in adminaccount:
                    adInvestment = int(i.amountToInvest)
                    adName = i.name
                if (int(adm_amounts) > adInvestment):
                    return make_response("Added amount is greater than total investment of " + adName), 400

                # check the total sum of cheque amount , amount in cash or payorder amount is equal to plot total amount
                if tokenAmount:
                    if amountInCash or chequeAmount or payorderAmount:
                        tOp = checkTotalOfPayments(
                            amountInCash, chequeAmount, payorderAmount, onlineTransfer)
                    if(tOp != float(tokenAmount)):
                        return make_response("added amount of token in cash, cheque, payorder or online transfer is greater or smaller than plot total amount"), 400
                else:
                    if amountInCash or chequeAmount or payorderAmount:
                        tOp = checkTotalOfPayments(
                            amountInCash, chequeAmount, payorderAmount, onlineTransfer)
                    if(tOp != float(totalAmount)):
                        return make_response("added amount in cash, cheque, payorder or online transfer is greater or smaller than plot total amount"), 400

                if tokenAmount:
                    adminaccount = accountsdetail.query.filter(
                        accountsdetail.id == decodedToken["id"]).all()
                    for i in adminaccount:
                        adInvestment = float(i.amountToInvest)
                        adName = i.name
                        print(adName)
                    percInPlotadm = (
                        (float(adm_amounts)/float(totalAmount))*100)
                    admTokenAmount = float(
                        (percInPlotadm/100)*float(tokenAmount))
                    taxDeductionValueadm = (
                        float(percInPlotadm/100)*float(taxAmount))
                    adnewInvest = float(
                        adInvestment-float(admTokenAmount)-taxDeductionValueadm)
                    acc = accountsdetail.query.filter(
                        accountsdetail.id == decodedToken["id"]).all()
                    print(acc)
                    temp = []
                    for i in acc:
                        dict = {"id": i.id}
                        temp.append(dict)
                    print(temp)
                    stmt = (update(accountsdetail). where(
                        accountsdetail.id == decodedToken['id']). values(amountToInvest=adnewInvest))
                    db.session.execute(stmt)
                    db.session.commit()
                    partnerAmountAgainstPLot = memberinplots(
                        userid=temp[0]['id'], names=adName, adm_amounts=adm_amounts, p_amounts="0", percentageInPlot=percInPlotadm, plotid=plotNo, role="admin", societyName=societyName, sectorNo=sectorNo, saleOrNot="No")
                    db.session.add(partnerAmountAgainstPLot)
                    db.session.commit()
                else:
                    adminaccount = accountsdetail.query.filter(
                        accountsdetail.id == decodedToken["id"]).all()
                    for i in adminaccount:
                        adInvestment = float(i.amountToInvest)
                        adName = i.name
                        print(adName)
                    percInPlotadm = (
                        (float(adm_amounts)/float(totalAmount))*100)
                    taxDeductionValueadm = (
                        float(percInPlotadm/100)*float(taxAmount))
                    adnewInvest = float(
                        adInvestment-float(adm_amounts)-taxDeductionValueadm)
                    acc = accountsdetail.query.filter(
                        accountsdetail.id == decodedToken["id"]).all()
                    print(acc)
                    temp = []
                    for i in acc:
                        dict = {"id": i.id}
                        temp.append(dict)
                    print(temp)
                    stmt = (update(accountsdetail). where(
                        accountsdetail.id == decodedToken['id']). values(amountToInvest=adnewInvest))
                    db.session.execute(stmt)
                    db.session.commit()
                    partnerAmountAgainstPLot = memberinplots(
                        userid=decodedToken['id'], names=adName, adm_amounts=adm_amounts, p_amounts="0", percentageInPlot=percInPlotadm, plotid=plotNo, role="admin", societyName=societyName, sectorNo=sectorNo, saleOrNot="No")
                    db.session.add(partnerAmountAgainstPLot)
                    db.session.commit()

            paymentsAdd = payments(plotid=idd, societyName=societyName, sectorNo=sectorNo, plotNo=plotNo, amountInCash=amountInCash, chequeAmount=chequeAmount, noOfCheques=noOfCheques, chequeNo=chequeNo, chequeDescription=chequeDescription,
                                   payorderAmount=payorderAmount, noOfPayOrder=noOfPayOrder, payOrderNo=payOrderNo, payOrderDescription=payOrderDescription, remaningBalance=remBalance, completeOrNot=completeOrNot,
                                   tokenAmount=tokenAmount, tokenDays=tokenDays, tokenDate=datetime.date.today(), tokenDescription=tokenDescription, taxAmount=taxAmount, taxDescription=taxDescription, onlineTransfer=onlineTransfer, onlineDescription=onlineDescription)
            db.session.add(paymentsAdd)
            db.session.commit()
            return make_response("add"), 200
        else:
            return make_response("access denied"), 400


@app.route('/paymentImages', methods=['POST'])
def payment_image_against_plot():
    societyName = request.form['societyName']
    sectorNo = request.form['sectorNo']
    plotNo = request.form['plotNo']
    image = request.files['paymentImage']
    if image:
        paymentFilename = secure_filename(image.filename)
        image.save(os.path.join(
            app.config['UPLOAD_FOLDER'], paymentFilename))
        imagePath = ('images/' + paymentFilename)
        print(imagePath)
        imageObj = paymentImage(
            societyName=societyName, sectorNo=sectorNo, plotNo=plotNo, imagePath=imagePath)
        db.session.add(imageObj)
        db.session.commit()
        return make_response("ok")
    else:
        return make_response("Wrong Sector Image Extension"), 400


@app.route('/getAllPaymentsDetails', methods=['GET'])
def getAllDataFromPayments():
    if (request.method == 'GET'):
        allData = []
        getAllData = payments.query.all()
        print(getAllData)
        if getAllData:
            for data in getAllData:
                dict = {"id": data.id,
                        "plotid": data.plotid,
                        "societyName": data.societyName,
                        "sectorNo": data.sectorNo,
                        "plotNo": data.plotNo,
                        "amountInCash": data.amountInCash,
                        "chequeAmount": data.chequeAmount,
                        "noOfCheques": data.noOfCheques,
                        "chequeNo": data.chequeNo,
                        "chequeDescription": data.chequeDescription,
                        "payorderAmount": data.payorderAmount,
                        "noOfPayOrder": data.noOfPayOrder,
                        "payOrderNo": data.payOrderNo,
                        "payOrderDescription": data.payOrderDescription,
                        "tokenAmount": data.tokenAmount,
                        "tokenDays": data.tokenDays,
                        "tokenDate": data.tokenDate,
                        "tokenDescription": data.tokenDescription,
                        "taxDescription": data.taxDescription,
                        "onlineTransfer": data.onlineTransfer,
                        "onlineDescription": data.onlineDescription,
                        "taxAmount": data.taxAmount,
                        "remaningBalance": data.remaningBalance}
                allData.append(dict)
            print(allData)
            plotAllDataJson = json.dumps(allData)
            return plotAllDataJson
        else:
            return make_response("No data Found"), 400
    else:
        return make_response("Request in error"), 400


# return indication if token days less than or equal to 3

@app.route('/checkTokenofPurchase', methods=['GET', 'Post'])
def checkTokenOfPurchase():
    return tokenForPurchase(payments, "paymentsToken")


@app.route('/checkTokenofSale', methods=['GET', 'Post'])
def checkTokenofSale():
    return tokenForPurchase(salepaymentmethod, "saleToken")


def tokenForPurchase(tableName, type):
    if request.method == 'GET':
        tokendict = {}
        tokenlist = []
        tokenobj = tableName.query.all()
        print(tokenobj)
        for i in tokenobj:
            print(i.tokenAmount)
            if i.tokenAmount:
                day = int(i.tokenDays)
                tokenExp = i.tokenDate + datetime.timedelta(days=day)
                remDays = tokenExp-i.tokenDate
                if remDays.days <= 3 and remDays.days > 0:
                    tokendict = {
                        'id': i.id,
                        'plotNo':  i.plotNo,
                        'sectorNo':  i.sectorNo,
                        'societyName':  i.societyName,
                        'tokenAmount':  i.tokenAmount,
                        'remainingBalance':  i.remaningBalance,
                        'type': type
                    }
                    tokenlist.append(tokendict)
        tokenlist = json.dumps(tokenlist)
        return tokenlist
    else:
        return make_response('bad Request 400'), 400


# get all plot information from plot to purchase table for sale ppt module


@app.route('/getplotsforsaleppt', methods=['GET'])
def getAllplotsInfoForSalePPT():
    if [request.method == 'GET']:
        if checkPermission(getUserId(), "Sale"):
            plotlist = []
            allInfo = []
            temp = []
            getData = salepaymentmethod.query.all()
            for i in getData:
                idd = i.id
                temp.append(idd)
            getplots = payments.query.all()
            for plot in getplots:
                if plot.id not in temp:
                    dict = {"societyName": plot.societyName,
                            "sectorNo": plot.sectorNo,
                            "plotNo": plot.plotNo}
                    plotlist.append(dict)
            for i in plotlist:
                getplots = plottopurchase.query.filter(and_(plottopurchase.sectorno == i['sectorNo'],
                                                            plottopurchase.societyname == i['societyName'], plottopurchase.plotno == i['plotNo'])).all()
                getplots1 = addsocietydata.query.filter(and_(addsocietydata.sectorno == i['sectorNo'],
                                                        addsocietydata.societyname == i['societyName'], addsocietydata.plotno == i['plotNo'])).all()
                for plot, plot1 in zip(getplots, getplots1):
                    dict = {"id": plot.id,
                            "societyname": plot.societyname,
                            "sectorno": plot.sectorno,
                            "plotno": plot.plotno,
                            "plotamount": plot.plotamount,
                            "description1": plot.description,
                            "plotownername": plot.plotownername,
                            "dateTime": plot.dateTime,
                            "plotsize": plot1.plotsize,
                            "plottype": plot1.plottype,
                            "description": plot1.description,
                            }
                    if dict not in allInfo:
                        allInfo.append(dict)
            allInfoJson = json.dumps(allInfo)
            return allInfoJson
        else:
            return make_response("Error"), 400


@app.route('/getsocietiesnameforsaleppt', methods=['GET'])
def getAllSocietyForSaleppt():
    societiesName = []
    allSocietyData = payments.query.all()
    for name in allSocietyData:
        if name.societyName not in societiesName:
            societiesName.append(name.societyName)
    print("all society names ", societiesName)
    societyNamePPTJson = json.dumps(societiesName)
    return societyNamePPTJson


@app.route('/getsectorsforsaleppt', methods=['GET'])
def getAllSectorsFoSalerppt():
    sectorlist = []
    allsectors = request.get_json()
    societyname = allsectors['societyname']
    getSectors = payments.query.filter(
        (payments.societyName == societyname)).all()
    for sector in getSectors:
        if sector.sectorNo not in sectorlist:
            sectorlist.append(sector.sectorNo)
    sectorpptJson = json.dumps(sectorlist)
    return sectorpptJson


@app.route('/getplotsforsalePPTagainst', methods=['GET'])
def getAllplotsInfoForSalePPTagainst():
    if [request.method == 'GET']:
        allInfo = []
        allplots = request.get_json()
        sectorno = allplots['sectorno']
        societyname = allplots['societyname']
        getplots = payments.query.filter(and_(payments.sectorNo == sectorno,
                                              payments.societyName == societyname)).all()
        for i in getplots:
            # info = plottopurchase.query.filter(and_(
            #     plottopurchase.societyname == i.societyName, plottopurchase.sectorno == i.sectorNo, plottopurchase.plotno == i.plotNo))
            getplots = plottopurchase.query.filter(and_(
                plottopurchase.societyname == i.societyName, plottopurchase.sectorno == i.sectorNo, plottopurchase.plotno == i.plotNo)).all()
            getplots1 = addsocietydata.query.filter(and_(
                addsocietydata.societyname == i.societyName, addsocietydata.sectorno == i.sectorNo, addsocietydata.plotno == i.plotNo)).all()
            for plot, plot1 in zip(getplots, getplots1):
                dict = {"id": plot.id,
                        "societyname": plot.societyname,
                        "sectorno": plot.sectorno,
                        "plotno": plot.plotno,
                        "plotamount": plot.plotamount,
                        "description1": plot.description,
                        "plotownername": plot.plotownername,
                        "dateTime": plot.dateTime,
                        "plotsize": plot1.plotsize,
                        "plottype": plot1.plottype,
                        "description": plot1.description,
                        }
                if dict not in allInfo:
                    allInfo.append(dict)
        allInfoJson = json.dumps(allInfo)
        return allInfoJson


@app.route('/saleplotdetails', methods=['POST'])
def salePlotDetails():
    if (request.method == 'POST'):
        if checkPermission(getUserId(), "Sale"):
            # plotDesc = []
            plotToPurchaseApi = request.get_json()
            societyname = plotToPurchaseApi['societyname']
            sectorno = plotToPurchaseApi['sectorno']
            plotno = plotToPurchaseApi['plotno']
            development = plotToPurchaseApi['development']
            plotdescription = plotToPurchaseApi['plotdescription']
            plotamount = plotToPurchaseApi['plotamount']
            plotownername = plotToPurchaseApi['plotownername']
            # getPlotDesc = plottopurchase.query.filter(
            #     plottopurchase.societyname == societyname, plottopurchase.sectorno == sectorno, plottopurchase.plotno == plotno)
            # for i in getPlotDesc:
            #     dict = {"description": i.description}
            #     if dict not in plotDesc:
            #         plotDesc.append(dict)
            # print(plotDesc)
            addtoPurchase = saleplotdetail(societyname=societyname, sectorno=sectorno, plotno=plotno, development=development,
                                           plotdescription=plotdescription, plotamount=plotamount, plotownername=plotownername)
            db.session.add(addtoPurchase)
            db.session.commit()
            return make_response("ok"), 200
        else:
            return make_response("access denied")


@app.route('/getAllSalePlotDetail', methods=['GET'])
def getAllSalePlotDetail():
    if (request.method == 'GET'):
        allData = []
        getAllData = saleplotdetail.query.all()
        print(getAllData)
        if getAllData:
            for data in getAllData:
                dict = {"id": data.id,
                        "societyname": data.societyname,
                        "sectorno": data.sectorno,
                        "plotno": data.plotno,
                        "development": data.development,
                        "plotdescription": data.plotdescription,
                        "plotamount": data.plotamount,
                        "plotownername": data.plotownername
                        }
                allData.append(dict)
            print(allData)
            plotAllDataJson = json.dumps(allData)
            return plotAllDataJson
        else:
            return make_response("No data Found"), 400
    else:
        return make_response("Request in error"), 400


@app.route('/updateSalePlotDetails', methods=['PUT'])
def updateSalePlotDetails():
    if (request.method == 'PUT'):
        updateObj = request.get_json()
        stmt = (update(signup).where(saleplotdetail.id == updateObj['id']).values(societyname=updateObj['societyname'], sectorno=updateObj['sectorno'], plotno=updateObj['plotno'],
                plotamount=updateObj['plotamount'], plotdescription=updateObj['plotdescription'], plotownername=updateObj['plotownername'], development=updateObj['development']))
        db.session.execute(stmt)
        db.session.commit()
        q = saleplotdetail.query.filter_by(id=updateObj['id']).all()
        for data in q:
            dict = {
                "societyname": data.societyname,
                "sectorno": data.sectorno,
                "plotno": data.plotno,
                "development": data.development,
                "plotdescription": data.plotdescription,
                "plotamount": data.plotamount,
                "plotownername": data.plotownername
            }
        return dict
    else:
        return make_response('using put method for update!'), 400


@app.route('/deleteConstructionAddSupplier/<int:idd>', methods=['DELETE'])
def deleteConstructionAddSupplier(idd):
    if (request.method == 'DELETE'):
        getData = saleplotdetail.query.filter(saleplotdetail.id == idd).all()
        id = 0
        for i in getData:
            id = i.id
        print(id)
        if getData:
            stmt = saleplotdetail.query.get(idd)
            app.db.session.delete(stmt)
            app.db.session.commit()
        else:
            print("Not such id in database"), 400
        return make_response("ok"), 200


@app.route('/salepayments', methods=['POST'])
def SalePaymentsDetails():
    if (request.method == 'POST'):
        if checkPermission(getUserId(), "Sale"):
            salePaymentsAPI = request.get_json()
            plotInfo = salePaymentsAPI["plotInfo"]
            amn = 0
            getTotalAmount = saleplotdetail.query.filter(and_(
                saleplotdetail.societyname == plotInfo['societyname'], saleplotdetail.sectorno == plotInfo['sectorno'], saleplotdetail.plotno == plotInfo['plotno'])).all()
            for i in getTotalAmount:
                amn = i.plotamount
            getTotalAmount = plottopurchase.query.filter(and_(
                plottopurchase.societyname == plotInfo['societyname'], plottopurchase.sectorno == plotInfo['sectorno'], plottopurchase.plotno == plotInfo['plotno'])).all()
            for i in getTotalAmount:
                amnBefore = i.plotamount
            print(amnBefore)
            plotInfo['plotAmount'] = amn
            amountInCash = salePaymentsAPI['amountInCash']
            chequeAmount = salePaymentsAPI['chequeAmount']
            noOfCheques = salePaymentsAPI['noOfCheques']
            chequeNo = salePaymentsAPI['chequeNo']
            chequeDescription = salePaymentsAPI['chequeDescription']
            payorderAmount = salePaymentsAPI['payorderAmount']
            noOfPayOrder = salePaymentsAPI['noOfPayOrder']
            payOrderNo = salePaymentsAPI['payOrderNo']
            payOrderDescription = salePaymentsAPI['payOrderDescription']
            tokenAmount = salePaymentsAPI['tokenAmount']
            tokenDays = salePaymentsAPI['tokenDays']
            tokenDescription = salePaymentsAPI['tokenDescription']
            taxAmount = salePaymentsAPI['taxAmount']
            taxDescription = salePaymentsAPI['taxDescription']
            onlineTransfer = salePaymentsAPI['onlineTransfer']
            onlineDescription = salePaymentsAPI['onlineDescription']

            plotSaleAmount = float(plotInfo["plotAmount"])
            print(plotSaleAmount)
            prof = float(amn)-float(amnBefore)
            if tokenAmount:
                completeORNot = "not"
            else:
                completeORNot = "yes"
            updatedValue = 0
            remBalance = 0
            # getTotalAmount = saleplotdetail.query.filter(and_(saleplotdetail.societyName == plotInfo['societyname'],saleplotdetail.sectorNo == plotInfo['sectorno'],saleplotdetail.plotid == plotInfo['plotno'])).all()
            # for i in getTotalAmount:
            #     plotInfo['plotAmount']=i.plotamount
            getPartner = memberinplots.query.filter(and_(
                memberinplots.societyName == plotInfo['societyname'], memberinplots.sectorNo == plotInfo['sectorno'], memberinplots.plotid == plotInfo['plotno'])).all()
            # check the total sum of cheque amount , amount in cash or payorder amount is equal to plot total amount
            if tokenAmount:
                if amountInCash or chequeAmount or payorderAmount or onlineTransfer:
                    tOp = checkTotalOfPayments(
                        amountInCash, chequeAmount, payorderAmount, onlineTransfer)
                if(tOp != float(tokenAmount)):
                    return make_response("added amount of token is greater or smaller than plot total amount")
            else:
                print(plotInfo["plotAmount"])
                if amountInCash or chequeAmount or payorderAmount or onlineTransfer:
                    tOp = checkTotalOfPayments(
                        amountInCash, chequeAmount, payorderAmount, onlineTransfer)
                if(tOp != float(plotInfo["plotAmount"])):
                    return make_response("added amount is greater or smaller than plot total amount")
            if getPartner:
                for i in getPartner:
                    per = float(i.percentageInPlot)
                    if i.role == "partner":
                        if tokenAmount:
                            profit = float((per/100)*float(tokenAmount))
                            taxDeductionValuePart = float(
                                (per/100)*float(taxAmount))
                            currentAmount = accountsdetail.query.filter(
                                accountsdetail.id == i.userid).all()
                            for n in currentAmount:
                                updatedValue = float(
                                    n.amountToInvest)+profit-taxDeductionValuePart
                                stmt = (update(accountsdetail). where(
                                    accountsdetail.id == i.userid). values(amountToInvest=updatedValue))
                                remBalance = float(
                                    plotInfo['plotAmount']) - float(tokenAmount)
                                db.session.execute(stmt)
                                db.session.commit()
                        else:
                            profit = float((per/100)*float(plotSaleAmount))
                            taxDeductionValuePart = float(
                                (per/100)*float(taxAmount))
                            currentAmount = accountsdetail.query.filter(
                                accountsdetail.id == i.userid).all()
                            for n in currentAmount:
                                updatedValue = float(
                                    n.amountToInvest)+profit-taxDeductionValuePart
                                stmt = (update(accountsdetail). where(
                                    accountsdetail.id == i.userid). values(amountToInvest=updatedValue))
                                db.session.execute(stmt)
                                db.session.commit()
                    if i.role == "admin":
                        if tokenAmount:
                            profit = float((per/100)*float(tokenAmount))
                            taxDeductionValueAdm = float(
                                (per/100)*float(taxAmount))
                            currentAmount = accountsdetail.query.filter(
                                accountsdetail.id == i.userid).all()
                            for n in currentAmount:
                                updatedValue = float(
                                    n.amountToInvest)+profit-taxDeductionValueAdm
                                stmt = (update(accountsdetail). where(
                                    accountsdetail.id == i.userid). values(amountToInvest=updatedValue))
                                remBalance = float(
                                    plotInfo['plotAmount']) - float(tokenAmount)
                                print("line 841", remBalance)
                                print(plotInfo['societyname'])
                                print(plotInfo['sectorno'])
                                print(plotInfo['plotno'])
                                print(plotInfo['plotAmount'])

                                db.session.execute(stmt)
                                db.session.commit()
                        else:
                            per = float(i.percentageInPlot)
                            profit = float((per/100)*float(plotSaleAmount))
                            taxDeductionValueAdm = float(
                                (per/100)*float(taxAmount))
                            currentAmount = accountsdetail.query.filter(
                                accountsdetail.id == i.userid).all()
                            for n in currentAmount:
                                updatedValue = float(
                                    n.amountToInvest)+profit-taxDeductionValueAdm
                                stmt = (update(accountsdetail). where(
                                    accountsdetail.id == i.userid). values(amountToInvest=updatedValue))
                                db.session.execute(stmt)
                                db.session.commit()
            else:
                return make_response("error"), 400
            stmt1 = (update(memberinplots). where(and_(
                memberinplots.societyName == plotInfo['societyname'], memberinplots.sectorNo == plotInfo['sectorno'], memberinplots.plotid == plotInfo['plotno'])). values(saleOrNot="yes"))
            db.session.execute(stmt1)
            db.session.commit()
            salePaymentsAdd = salepaymentmethod(plotInfo="Ni", societyName=plotInfo["societyname"], sectorNo=plotInfo["sectorno"], plotNo=plotInfo["plotno"], amountInCash=amountInCash, chequeAmount=chequeAmount, noOfCheques=noOfCheques, chequeNo=chequeNo, chequeDescription=chequeDescription,
                                                payorderAmount=payorderAmount, noOfPayOrder=noOfPayOrder, payOrderNo=payOrderNo, payOrderDescription=payOrderDescription, profit=prof, remaningBalance=remBalance, completeOrNot=completeORNot,
                                                tokenAmount=tokenAmount, tokenDays=tokenDays, tokenDate=datetime.date.today(), tokenDescription=tokenDescription, taxAmount=taxAmount, taxDescription=taxDescription, onlineTransfer=onlineTransfer, onlineDescription=onlineDescription)
            db.session.add(salePaymentsAdd)
            db.session.commit()

            return make_response("add"), 200
        else:
            return make_response("access denied")


@app.route('/getAllSaleDetails', methods=['GET'])
def getAllDataFromSale():
    if (request.method == 'GET'):
        allData = []
        getAllData = salepaymentmethod.query.all()
        print(getAllData)
        if getAllData:
            for data in getAllData:
                dict = {"id": data.id,
                        "societyName": data.societyName,
                        "sectorNo": data.sectorNo,
                        "plotNo": data.plotNo,
                        "amountInCash": data.amountInCash,
                        "chequeAmount": data.chequeAmount,
                        "noOfCheques": data.noOfCheques,
                        "chequeNo": data.chequeNo,
                        "chequeDescription": data.chequeDescription,
                        "payorderAmount": data.payorderAmount,
                        "noOfPayOrder": data.noOfPayOrder,
                        "payOrderNo": data.payOrderNo,
                        "payOrderDescription": data.payOrderDescription,
                        "tokenAmount": data.tokenAmount,
                        "tokenDays": data.tokenDays,
                        "tokenDate": data.tokenDate,
                        "tokenDescription": data.tokenDescription,
                        "taxDescription": data.taxDescription,
                        "onlineTransfer": data.onlineTransfer,
                        "onlineDescription": data.onlineDescription,
                        "taxAmount": data.taxAmount,
                        "remaningBalance": data.remaningBalance,
                        "profit": data.profit}
                allData.append(dict)
            print(allData)
            plotAllDataJson = json.dumps(allData)
            return plotAllDataJson
        else:
            return make_response("No data Found"), 400
    else:
        return make_response("Request in error"), 400


# @app.route('/deletePaymentAddedPlot/<int:idd>', methods=['DELETE'])
# def deletePaymentAddedPlot(idd):
#     if (request.method == 'DELETE'):
#         # stmt = (delete(signup).where(signup.id == id))
#         # stmt = signup.query.get(id)
#         # db.session.delete(stmt)
#         # db.session.commit()
#         getData=payments.query.filter(payments.id==idd).all()
#         id=0
#         for i in getData:
#             id=i.id
#         print(id)
#         if getData:
#             stmt1 = payments.query.get(id)
#             db.session.delete(stmt1)
#             db.session.commit()
#         return make_response("ok"),200


# @app.route('/deleteSaleAddedPlots/<int:idd>', methods=['DELETE'])
# def deleteSaleAddedPlots(idd):
#     if (request.method == 'DELETE'):
#         # stmt = (delete(signup).where(signup.id == id))
#         # stmt = signup.query.get(id)
#         # db.session.delete(stmt)
#         # db.session.commit()
#         temp=[]
#         getData=salepaymentmethod.query.filter(salepaymentmethod.id==idd).all()
#         id=0
#         society=""
#         sector=""
#         plot=""
#         print(getData)
#         for i in getData:
#             id=i.id
#             society=i.societyName
#             sector=i.sectorNo
#             plot=i.plotNo
#             temp.append(i)
#         print(temp)
#         print(id)
#         # if getData:
#         #     stmt1 = salepaymentmethod.query.get(id)
#         #     db.session.delete(stmt1)
#         #     db.session.commit()
#         stmt = saleplotdetail.query.filter(saleplotdetail.societyname==society,saleplotdetail.sectorno==sector,saleplotdetail.plotno==plot)
#         db.session.delete(stmt)
#         db.session.commit()
#     return make_response("ok"),200

@app.route('/getAllSaleDetailsReview/<int:idd>', methods=['GET'])
def getAllSaleDetailsReview(idd):
    if (request.method == 'GET'):
        allData = []
        getAllData = salepaymentmethod.query.filter(
            salepaymentmethod.id == idd).all()
        print(getAllData)
        if getAllData:
            for data in getAllData:
                dict = {"id": data.id,
                        "societyName": data.societyName,
                        "sectorNo": data.sectorNo,
                        "plotNo": data.plotNo,
                        "amountInCash": data.amountInCash,
                        "chequeAmount": data.chequeAmount,
                        "noOfCheques": data.noOfCheques,
                        "chequeNo": data.chequeNo,
                        "chequeDescription": data.chequeDescription,
                        "payorderAmount": data.payorderAmount,
                        "noOfPayOrder": data.noOfPayOrder,
                        "payOrderNo": data.payOrderNo,
                        "payOrderDescription": data.payOrderDescription,
                        "tokenAmount": data.tokenAmount,
                        "tokenDays": data.tokenDays,
                        "tokenDate": data.tokenDate,
                        "tokenDescription": data.tokenDescription,
                        "taxDescription": data.taxDescription,
                        "onlineTransfer": data.onlineTransfer,
                        "onlineDescription": data.onlineDescription,
                        "taxAmount": data.taxAmount,
                        "remaningBalance": data.remaningBalance,
                        "profit": data.profit}
                allData.append(dict)
            print(allData)
            plotAllDataJson = json.dumps(allData)
            return plotAllDataJson
        else:
            return make_response("No data Found"), 400
    else:
        return make_response("Request in error"), 400


@app.route('/getAllPaymentsDetailsReview/<int:idd>', methods=['GET'])
def getAllPaymentsDetailsReview(idd):
    if (request.method == 'GET'):
        allData = []
        getAllData = payments.query.filter(payments.id == idd)
        print(getAllData)
        if getAllData:
            for data in getAllData:
                dict = {"id": data.id,
                        "plotid": data.plotid,
                        "societyName": data.societyName,
                        "sectorNo": data.sectorNo,
                        "plotNo": data.plotNo,
                        "amountInCash": data.amountInCash,
                        "chequeAmount": data.chequeAmount,
                        "noOfCheques": data.noOfCheques,
                        "chequeNo": data.chequeNo,
                        "chequeDescription": data.chequeDescription,
                        "payorderAmount": data.payorderAmount,
                        "noOfPayOrder": data.noOfPayOrder,
                        "payOrderNo": data.payOrderNo,
                        "payOrderDescription": data.payOrderDescription,
                        "tokenAmount": data.tokenAmount,
                        "tokenDays": data.tokenDays,
                        "tokenDate": data.tokenDate,
                        "tokenDescription": data.tokenDescription,
                        "taxDescription": data.taxDescription,
                        "onlineTransfer": data.onlineTransfer,
                        "onlineDescription": data.onlineDescription,
                        "taxAmount": data.taxAmount,
                        "remaningBalance": data.remaningBalance}
                allData.append(dict)
            print(allData)
            plotAllDataJson = json.dumps(allData)
            return plotAllDataJson
        else:
            return make_response("No data Found"), 400
    else:
        return make_response("Request in error"), 400


@app.route('/updateForPurchase', methods=['PUT'])
def updateAcc():
    return updateAccountDetailsAfterToken(payments)


@app.route('/updateForSale', methods=['PUT'])
def updateAccofSale():
    return updateAccountDetailsAfterToken(salepaymentmethod)


def updateAccountDetailsAfterToken(table):
    if request.method == 'PUT':
        salePaymentsAPI = request.get_json()
        idInPayment = salePaymentsAPI['id']
        obj = table.query.filter(table.id == idInPayment).all()
        for i in obj:
            societyName = i.societyName
            sectorName = i.sectorNo
            plotNo = i.plotNo
        # societyName = salePaymentsAPI["societyName"]
        # sectorName = salePaymentsAPI['sectorName']
        # plotNo = salePaymentsAPI['plotNo']
        amountInCash = salePaymentsAPI['amountInCash']
        chequeAmount = salePaymentsAPI['chequeAmount']
        noOfCheques = salePaymentsAPI['noOfCheques']
        chequeNo = salePaymentsAPI['chequeNo']
        chequeDescription = salePaymentsAPI['chequeDescription']
        payorderAmount = salePaymentsAPI['payorderAmount']
        noOfPayOrder = salePaymentsAPI['noOfPayOrder']
        payOrderNo = salePaymentsAPI['payOrderNo']
        payOrderDescription = salePaymentsAPI['payOrderDescription']
        onlineTransfer = salePaymentsAPI['onlineTransfer']

        getPaymentsWithToken = table.query.filter(
            and_(table.id == idInPayment, table.tokenAmount > 0)).all()
        getPartner = memberinplots.query.filter(and_(
            memberinplots.societyName == societyName, memberinplots.sectorNo == sectorName, memberinplots.plotid == plotNo)).all()
        print(getPaymentsWithToken)
        if getPaymentsWithToken:
            for i in getPaymentsWithToken:
                idd = i.id
                remBalance = i.remaningBalance
                aIc = i.amountInCash
                cA = i.chequeAmount
                pOa = i.payorderAmount
                nOc = i.noOfCheques
                nOp = i.noOfPayOrder
            if amountInCash or chequeAmount or payorderAmount or onlineTransfer:
                tOp = checkTotalOfPayments(
                    amountInCash, chequeAmount, payorderAmount, onlineTransfer)
            if(tOp != float(remBalance)):
                return make_response("added amount is greater or smaller than plot total remaning amount")
            for mem in getPartner:
                partnerAccId = mem.userid
                percentageInPlot = float(mem.percentageInPlot)
                account = accountsdetail.query.filter(
                    accountsdetail.id == partnerAccId).all()
                for i in account:
                    pInvestment = float(i.amountToInvest)
                remValue = float((percentageInPlot/100)*float(remBalance))
                if table == payments:
                    newInvest = float(pInvestment - remValue)
                else:
                    newInvest = float(pInvestment + remValue)
                stmt = (update(accountsdetail). where(
                    accountsdetail.id == partnerAccId). values(amountToInvest=newInvest))
                db.session.execute(stmt)
                db.session.commit()
                stmt1 = (update(table). where(
                    table.id == idd). values(tokenAmount=0, remaningBalance=0, tokenDays=0, completeOrNot="yes", amountInCash=amountInCash+aIc, noOfCheques=noOfCheques+nOc, chequeNo=chequeNo, chequeDescription=chequeDescription, chequeAmount=chequeAmount+cA,
                                             payorderAmount=payorderAmount+pOa, payOrderNo=payOrderNo, payOrderDescription=payOrderDescription, onlineTransfer=onlineTransfer, noOfPayOrder=noOfPayOrder+nOp))
                db.session.execute(stmt1)
                db.session.commit()
        else:
            return make_response("no record found!"), 400
        return {"Balance is": remBalance}


@app.route('/account/admin-partner/total-profit')
def total_profit_against_plot():
    dict = {}
    list_of_sale_plots = []
    plot_details = memberinplots.query.filter(
        memberinplots.saleOrNot == 'yes').all()
    for plot in plot_details:
        actual_price = plot_actual_price(
            plot.societyName, plot.sectorNo, plot.plotid)
        salePlotPrice = plot_sale_price(
            plot.societyName, plot.sectorNo, plot.plotid)
        profit_amount = float(salePlotPrice) - float(actual_price)
        amountPerPercentage = float(
            profit_amount) * float((float(plot.percentageInPlot)/100))
        dict = {
            'name': plot.names,
            'role': plot.role,
            'societyName': plot.societyName,
            'sectorNo': plot.sectorNo,
            'plotNo': plot.plotid,
            'amountInvested': float(plot.p_amounts) if float(plot.p_amounts) > 0 else float(plot.adm_amounts),
            'percentageInPlot': plot.percentageInPlot,
            'actualPrice': actual_price,
            'salePlotPrice': salePlotPrice,
            'profit_loss': amountPerPercentage
        }
        list_of_sale_plots.append(dict)
    return make_response(jsonify(list_of_sale_plots), 200)


def plot_actual_price(societyN, secN, plN):
    plot = plottopurchase.query.filter(plottopurchase.societyname == societyN,
                                       plottopurchase.sectorno == secN, plottopurchase.plotno == plN).first()
    return plot.plotamount


def plot_sale_price(societyN, secN, plN):
    plot = saleplotdetail.query.filter(saleplotdetail.societyname == societyN,
                                       saleplotdetail.sectorno == secN, saleplotdetail.plotno == plN).first()
    return plot.plotamount


@app.route('/saleInvoice/<id>', methods=['GET'])
def saleInvoice(id):
    if [request.method == 'GET']:
        plotlist = []
        temp = []
        # allplots = request.get_json()
        getData2 = salepaymentmethod.query.filter(and_(
            salepaymentmethod.id == id)).all()
        for plot in getData2:
            dict = {
                "plotno": plot.plotno,
                "societyName": plot.societyName,
                "sectorNo": plot.sectorNo
            }
            temp.append(dict)
        getData1 = payments.query.filter(and_(payments.sectorNo == ['sectorNo'],
                                              payments.societyName == ['societyName'], payments.plotNo == ['plotno'])).all()
        getData = saleplotdetail.query.filter(and_(saleplotdetail.sectorno == ['sectorNo'],
                                                   saleplotdetail.societyname == ['societyName'], saleplotdetail.plotno == ['plotno'])).all()
        for plot, plot1 in zip(getData, getData1):
            dict = {"id": plot.id,
                    "societyname": plot.societyname,
                    "sectorno": plot.sectorno,
                    "plotno": plot.plotno,
                    "plotamount": plot.plotamount,
                    "description1": plot1.description,
                    "plotownername": plot.plotownername,
                    "dateTime": plot.dateTime,
                    "plotsize": plot1.plotsize,
                    "plottype": plot1.plottype,
                    "description": plot1.description,
                    }
            plotlist.append(dict)
        plotpptJson = json.dumps(plotlist)
        return plotpptJson
    else:
        return make_response("Error"), 400


db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
