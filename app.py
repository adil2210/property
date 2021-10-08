from sqlalchemy import and_, or_, not_, update,func
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
from flask_mail import Mail,Message
import random

import sqlite3 as sql
from flask_marshmallow import Marshmallow
import os


pymysql.install_as_MySQLdb()


app = Flask(__name__)

CORS(app)
mail= Mail(app)
app.secret_key = 'ghjc'

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True
# app.config['SQLALCHEMY_POOL_SIZE'] = 1000
# app.config['SQLALCHEMY_POOL_TIMEOUT'] = 3000
# app.config['SECRET_KEY'] = 'JustDemonstrating'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://a7ad9e_pmsdb:Asdf#123@mysql5027.site4now.net:330'
db = SQLAlchemy(app)
from database import *
db.create_all()
from construction import constructionAmount,constructionAddPlot,constructionAddSupplier
# construction file importsad
app.register_blueprint(constructionAmount)
app.register_blueprint(constructionAddPlot)
app.register_blueprint(constructionAddSupplier)


UPLOAD_FOLDER = 'images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PLOT_FOLDER = 'plotimg'
app.config['PLOT_FOLDER'] = PLOT_FOLDER
app.config['SECRET_KEY'] = 'JustDemonstrating'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'adil22108@gmail.com'
app.config['MAIL_PASSWORD'] = 'adil4329156457'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False

# const PORT =process.env.PORT||


mail = Mail(app)


@app.route("/" ,methods=['POST'])
def deploy():
    return make_response("badar")


@app.route("/email")
def index():
   msg = Message('Hello cake', sender =app.config['MAIL_USERNAME'], recipients = ['badarbaig21@gmail.com'])
   msg.body = "Hello Flask message sent from Flask-Mail"
   mail.send(msg)
   return "Sent"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def checkPermission(userid,name):
    checkP = db.session.query(permissions).filter(permissions.uid == userid).all()
    print(checkP)
    for i in checkP:
        if i.Supper and name=="Supper":
            return True
        elif i.Sale and name=="Sale":
            return True
        elif i.Accounts and name=="Accounts":
            return True
        elif i.Purchase and name=="Purchase":
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
        checkEmail = signup.query.filter_by(email=email).first()
        checkphone = signup.query.filter_by(phoneno=phoneno).first()
        checkcnic = signup.query.filter_by(cnic=cnic).first()
        if checkEmail != None and checkphone != None and checkcnic != None:
            return make_response("Email or Phone No or CNIC both already exists"), 400
        else:
            if checkEmail == None:
                if checkphone == None:
                    if checkcnic==None:
                        newUser = signup(username=username, email=email,
                                        password=hashed, phoneno=phoneno, cnic=cnic, role=role,resetCode=0)
                        db.session.add(newUser)
                        db.session.commit()
                        getId = signup.query.all()
                        n=0
                        for i in getId:
                            n=i.id
                        addPerm = permissions(uid=n, Accounts=Accounts, Purchase=Purchase,
                                            Sale=Sale, Supper=Supper)
                        db.session.add(addPerm)
                        db.session.commit()
                        return make_response("added"), 200
                    else:
                        return make_response("CNIC already exist"), 400
                else:
                    return make_response("Phone-NO already exist"), 400
            else:
                return make_response("Email already exist"), 400


@app.route('/reset', methods=['POST'])
def resetPassword():
    if (request.method == 'POST'):
        resetApi=request.get_json()
        email=resetApi['email']
        randNo=random.randint(100000,999999)
        print(randNo)
        msg = Message('Hello cake', sender = app.config['MAIL_USERNAME'], recipients = ['badarbaig21@gmail.com'])
        msg.body = randNo
        mail.send(msg)
        stmt = (update(signup). where(
                    signup.email == email). values(resetCode=randNo))
        db.session.execute(stmt)
        db.session.commit()
        return make_response("Code has sent on your email"),200
    else:
        return make_response("error")


@app.route('/checkCode', methods=['POST'])
def checkCodee():
    if (request.method == 'POST'):
        codeCheckApi=request.get_json()
        code=codeCheckApi['code']
        check=signup.query.filter(signup.resetCode==code).all()
        if check==None:
            return make_response("Enter Code is wrong"),400
        else:
            return make_response("correct code"),200

@app.route('/newPassword', methods=['POST'])
def newPassword():
    if (request.method == 'POST'):
        newPassApi=request.get_json()
        code=newPassApi['code']
        password=newPassApi['password']
        confirmPass=newPassApi['confirmPass']
        check=signup.query.filter(signup.resetCode==code).all()
        if check==None:
            return make_response("Enter Code is wrong"),400
        else:
            if(password==confirmPass):
                hashed = pbkdf2_sha256.hash(password)
                stmt = (update(signup). where(
                    signup.resetCode == code). values(password=hashed))
                db.session.execute(stmt)
                db.session.commit()
            return make_response("correct code"),200





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
        user = signup.query.filter(signup.email==email).all()
        if not user:
            return 'User Not Found!', 404
        #session["uid"] = user.id
        for i in user:
            idd=i.id
            passs=i.password
            name=i.username
            emaill=i.email
            role=i.role
        getPermissions=permissions.query.filter(permissions.uid==idd).all()
        print(getPermissions)
        for n in getPermissions:
            acc=n.Accounts
            pur=n.Purchase
            s=n.Sale
            su=n.Supper

        if pbkdf2_sha256.verify(password,passs):
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
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
            }
            token = (jwt.encode(data, app.config['SECRET_KEY']))
            temp=[token]
            obj=json.dumps(temp)
            return obj
        else:
            return 'Invalid Login Info!', 400


@app.route('/addsociety', methods=['POST'])
def addsocietydataa():
    if (request.method == 'POST'):
        if checkPermission(getUserId(),"Supper"):
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
            return make_response("Access Denied"),400


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
    allplots = request.get_json()
    sectorno = allplots['sectorno']
    societyname = allplots['societyname']
    getplots = addsocietydata.query.filter(and_(addsocietydata.sectorno == sectorno,
                                                addsocietydata.societyname == societyname)).all()
    for plot in getplots:
        plotlist.append(plot.plotno)
    plotJson = json.dumps(plotlist)
    return plotJson


@app.route('/plottopurchase', methods=['POST'])
def addPlotToPurchase():
    if (request.method == 'POST'):
        if checkPermission(getUserId(),"Supper"):
            plotToPurchaseApi = request.get_json()
            societyname = plotToPurchaseApi['societyname']
            sectorno = plotToPurchaseApi['sectorno']
            plotno = plotToPurchaseApi['plot']
            development = bool(plotToPurchaseApi['development'])
            description = plotToPurchaseApi['description']
            plotamount = float(plotToPurchaseApi['plotamount'])
            plotownername = plotToPurchaseApi['plotownername']
            dev=bool(development)
            addtoPurchase = plottopurchase(societyname=societyname, sectorno=sectorno, plotno=plotno, development=development,
                                        description=description, plotamount=plotamount, plotownername=plotownername)
            db.session.add(addtoPurchase)
            db.session.commit()
            return make_response("ok"), 200
        else:
            return make_response("Access Denied")


#  get all data from plot to purchase table

@app.route('/getalldata', methods=['GET'])
def getAllDataFromPlotToPurchase():
    if (request.method == 'GET'):
        allData = []
        getAllData = plottopurchase.query.all()
        print(getAllData)
        if getAllData:
            for data in getAllData:
                dict = {"id": data.id,
                        "societyname": data.societyname,
                        "sectorno": data.sectorno,
                        "plotno": data.plotno,
                        "development": data.development,
                        "description": data.description,
                        "plotamount": data.plotamount,
                        "plotownername": data.plotownername}
                allData.append(dict)
            print(allData)
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
    allSocietyData = plottopurchase.query.all()
    for name in allSocietyData:
        if name.societyname not in societiesName:
            societiesName.append(name.societyname)
    print("all society names ", societiesName)
    societyNamePPTJson = json.dumps(societiesName)
    return societyNamePPTJson


# get sector no for purchase ppt module

@app.route('/getsectorsforppt', methods=['GET'])
def getAllSectorsForppt():
    sectorlist = []
    allsectors = request.get_json()
    societyname = allsectors['societyname']
    getSectors = plottopurchase.query.filter(
        (plottopurchase.societyname == societyname)).all()
    for sector in getSectors:
        if sector.sectorno not in sectorlist:
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
                    "withdevelopment": plot.withdevelopment,
                    "withoutdevelopment": plot.withoutdevelopment,
                    "description": plot.description,
                    "plotamount": plot.plotamount,
                    "plotownername": plot.plotownername}
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
    aIc=(aIc)
    cA=(cA)
    pOa=(pOa)
    ot=(ot)
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
        if checkPermission(getUserId() , "Accounts"):
            accountsApi = request.get_json()
            #name = accountsApi['name']
            #contactNo = accountsApi['contactNo']
            uid = accountsApi['uid']
            user = signup.query.filter_by(id = uid).all()
            for use in user:
                print('adil')
                cnic = use.cnic
                role = use.role
                name = use.username
                contactNo = use.phoneno
            #cnic = accountsApi['cnic']
            #role = accountsApi['role']
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
            accDetails=accountsdetail.query.filter(accountsdetail.uid==uid).all()
            print(accDetails)
            if accDetails:
                print('already have account')
                return make_response('user already exist!'),400
            else:
                if  chequeAmount or payorderAmount or onlineTransfer or amountInCash:
                    tOp = checkTotalOfPayments(amountInCash,chequeAmount, payorderAmount , onlineTransfer)
                    print(tOp)
                    if(tOp != float(amountToInvest)):
                        return make_response("added amount of is greater or smaller than total investment"),400
                    else:
                        if(accDetails):
                            return make_response("user already exists"),400
                        else:
                            accounts = accountsdetail(uid=uid,name=name,cnic=cnic,contactNo=contactNo,role=role,accName=accName, bankName=bankName, accNo=accNo, amountToInvest=amountToInvest,
                                            dateTime=datetime.datetime.now(), amountInCash=amountInCash, chequeAmount=chequeAmount, noOfCheques=noOfCheques, chequeNo=chequeNo, chequeDescription=chequeDescription,
                                            payorderAmount=payorderAmount, noOfPayOrder=noOfPayOrder, payOrderNo=payOrderNo, payOrderDescription=payOrderDescription, onlineTransfer=onlineTransfer, onlineDescription=onlineDescription)
                            db.session.add(accounts)
                            db.session.commit()
                            return make_response("added"), 200
        else:
            return make_response("Access Denied")

@app.route('/updateaccount', methods=['POST'])
def updateAccountsData():
    if (request.method == 'POST'):
        accountUpdateApi=request.get_json()
        uid=accountUpdateApi['uid']
        amount = accountUpdateApi['amount']
        try:
            stmt = (update(accountsdetail). where(
            accountsdetail.uid == uid). values(amountToInvest=amount))
            db.session.execute(stmt)
            db.session.commit()
        except Exception as e:
            return make_response('cannot update') , 400
    else:
        return make_response('method error!')


# get all users from accounts table

@app.route('/accountalldata', methods=['GET'])
def getsAccountsData():
    if (request.method == 'GET'):
        accountslist = []
        accountsUsers = accountsdetail.query.all()
        for user in accountsUsers:
            dict = {"id": user.id,
                    "name": user.name,
                    "amountToInvest": user.amountToInvest}

            accountslist.append(dict)
        accountslist = json.dumps(accountslist)
        return accountslist
    else:
        return make_response("Error"), 400


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




# all the payments are handling in this route

@app.route('/payments', methods=['POST'])
def paymentsDetails():
    if (request.method == 'POST'):
        print(getUserId())
        if checkPermission(getUserId(),"Payments"):
            jwtToken = request.headers.get('Authorization')
            cleared_header = jwtToken[7:]
            print("token is:", cleared_header)
            decodedToken = jwt.decode(
                cleared_header, app.config['SECRET_KEY'], algorithms=["HS256"])
            print("decode token id is : ", decodedToken["id"])

            paymentsAPI = request.get_json()

            # member in plots objects
            userid = paymentsAPI['userid']
            adm_amounts = paymentsAPI['adm_amounts']

            # payments objects
            societyName = paymentsAPI['societyName']
            sectorNo = paymentsAPI['sectorNo']
            plotNo = paymentsAPI['plotNo']
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

            getTotalPlotAmount = plottopurchase.query.filter(
                plottopurchase.societyname == societyName, plottopurchase.sectorno == sectorNo, plottopurchase.plotno == plotNo).first()
            totalAmount = getTotalPlotAmount.plotamount
            remBalance = 0
            if tokenAmount:
                completeOrNot = "not"
                remBalance = float(totalAmount)-tokenAmount
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
                        return make_response("added amount of token is greater or smaller than plot total amount")
                else:
                    if amountInCash or chequeAmount or payorderAmount or onlineTransfer:
                        tOp = checkTotalOfPayments(
                            amountInCash, chequeAmount, payorderAmount, onlineTransfer)
                    if(tOp != float(totalAmount)):
                        return make_response("added amount is greater or smaller than plot total amount")
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
                        accountsdetail.uid == decodedToken["id"]).all()
                    for i in adminaccount:
                        adInvestment = int(i.amountToInvest)
                        adName = i.name

                    if (int(adm_amounts) > adInvestment):
                        return make_response("Added amount is greater than total investment of " + adName), 400

                    if tokenAmount:
                        if amountInCash or chequeAmount or payorderAmount or onlineTransfer:
                            tOp = checkTotalOfPayments(
                                amountInCash, chequeAmount, payorderAmount,onlineTransfer)
                        if(tOp > float(tokenAmount)):
                            return make_response("added amount greater than plot total amount")

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
                            accountsdetail.uid == decodedToken["id"]).all()
                        temp = []
                        for i in acc:
                            dict = {"id": i.id}
                            temp.append(dict)
                        stmt = (update(accountsdetail). where(
                            accountsdetail.id == temp[0]['id']). values(amountToInvest=adnewInvest))
                        db.session.execute(stmt)
                        db.session.commit()
                        partnerAmountAgainstPLot = memberinplots(
                            userid=temp[0]['id'], names=adName, adm_amounts=adm_amounts, p_amounts="0", percentageInPlot=percInPlotadm, plotid=plotNo, role="admin", societyName=societyName, sectorNo=sectorNo , saleOrNot="No")
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
                            accountsdetail.uid == decodedToken["id"]).all()
                        print(acc)
                        temp = []
                        for i in acc:
                            dict = {"id": i.id}
                            temp.append(dict)
                        print(temp)
                        stmt = (update(accountsdetail). where(
                            accountsdetail.id == temp[0]['id']). values(amountToInvest=adnewInvest))
                        db.session.execute(stmt)
                        db.session.commit()
                        partnerAmountAgainstPLot = memberinplots(
                            userid=temp[0]['id'], names=adName, adm_amounts=adm_amounts, p_amounts="0", percentageInPlot=percInPlotadm, plotid=plotNo, role="admin", societyName=societyName, sectorNo=sectorNo , saleOrNot="No")
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
                        return make_response("added amount of token is greater or smaller than plot total amount")
                else:
                    if amountInCash or chequeAmount or payorderAmount:
                        tOp = checkTotalOfPayments(
                            amountInCash, chequeAmount, payorderAmount)
                    if(tOp != float(totalAmount)):
                        return make_response("added amount is greater or smaller than plot total amount")

                if tokenAmount:
                    print("chutti ker")
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
                            userid=partner['id'], names=partner['name'], p_amounts=partner['amount'], adm_amounts="0", percentageInPlot=percInPlotPart, plotid=plotNo, role="partner", societyName=societyName, sectorNo=sectorNo , saleOrNot="No")
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
                    accountsdetail.uid == decodedToken["id"]).all()
                for i in adminaccount:
                    adInvestment = int(i.amountToInvest)
                    adName = i.name
                if (int(adm_amounts) > adInvestment):
                    return make_response("Added amount is greater than total investment of " + adName), 400

                # check the total sum of cheque amount , amount in cash or payorder amount is equal to plot total amount
                if tokenAmount:
                    if amountInCash or chequeAmount or payorderAmount:
                        tOp = checkTotalOfPayments(
                            amountInCash, chequeAmount, payorderAmount)
                    if(tOp != float(tokenAmount)):
                        return make_response("added amount of token is greater or smaller than plot total amount")
                else:
                    if amountInCash or chequeAmount or payorderAmount:
                        tOp = checkTotalOfPayments(
                            amountInCash, chequeAmount, payorderAmount)
                    if(tOp != float(totalAmount)):
                        return make_response("added amount is greater or smaller than plot total amount")

                if tokenAmount:
                    adminaccount = accountsdetail.query.filter(
                        accountsdetail.uid == decodedToken["id"]).all()
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
                        accountsdetail.uid == decodedToken["id"]).all()
                    print(acc)
                    temp = []
                    for i in acc:
                        dict = {"id": i.id}
                        temp.append(dict)
                    print(temp)
                    stmt = (update(accountsdetail). where(
                        accountsdetail.id == temp[0]['id']). values(amountToInvest=adnewInvest))
                    db.session.execute(stmt)
                    db.session.commit()
                    partnerAmountAgainstPLot = memberinplots(
                        userid=temp[0]['id'], names=adName, adm_amounts=adm_amounts, p_amounts="0", percentageInPlot=percInPlotadm, plotid=plotNo, role="admin", societyName=societyName, sectorNo=sectorNo, saleOrNot="No")
                    db.session.add(partnerAmountAgainstPLot)
                    db.session.commit()
                else:
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
                        accountsdetail.uid == decodedToken["id"]).all()
                    print(acc)
                    temp = []
                    for i in acc:
                        dict = {"id": i.id}
                        temp.append(dict)
                    print(temp)
                    stmt = (update(accountsdetail). where(
                        accountsdetail.id == temp[0]['id']). values(amountToInvest=adnewInvest))
                    db.session.execute(stmt)
                    db.session.commit()
                    partnerAmountAgainstPLot = memberinplots(
                        userid=temp[0]['id'], names=adName, adm_amounts=adm_amounts, p_amounts="0", percentageInPlot=percInPlotadm, plotid=plotNo, role="admin", societyName=societyName, sectorNo=sectorNo, saleOrNot="No")
                    db.session.add(partnerAmountAgainstPLot)
                    db.session.commit()

            paymentsAdd = payments(societyName=societyName, sectorNo=sectorNo, plotNo=plotNo, amountInCash=amountInCash, chequeAmount=chequeAmount, noOfCheques=noOfCheques, chequeNo=chequeNo, chequeDescription=chequeDescription,
                                   payorderAmount=payorderAmount, noOfPayOrder=noOfPayOrder, payOrderNo=payOrderNo, payOrderDescription=payOrderDescription, remaningBalance=remBalance, completeOrNot=completeOrNot,
                                   tokenAmount=tokenAmount, tokenDays=tokenDays, tokenDate=datetime.date.today(), tokenDescription=tokenDescription, taxAmount=taxAmount, taxDescription=taxDescription, onlineTransfer=onlineTransfer, onlineDescription=onlineDescription)
            db.session.add(paymentsAdd)
            db.session.commit()
            return make_response("add")
        else:
            return make_response("access denied")


# return indication if token days less than or equal to 3

@app.route('/checkTokenofPurchase', methods=['GET', 'Post'])
def checkToken():
    return tokenForPurchase(payments)


@app.route('/checkTokenofSale', methods=['GET', 'Post'])
def checkTokenofSale():
    return tokenForPurchase(salepaymentmethod)


def tokenForPurchase(tableName):
    if request.method == 'GET':
        tokendict = {}
        tokenlist = []
        tokenobj = tableName.query.all()
        print(tokenobj)
        for i in tokenobj:
            print("640 ", i.tokenAmount)
            day = int(i.tokenDays)
            if i.tokenAmount:
                tokenExp = i.tokenDate + datetime.timedelta(days=day)
                remDays = tokenExp-i.tokenDate
                if remDays.days <= 3:
                    tokendict = {
                        'plotNo':  i.plotNo,
                        'societyName':  i.societyName,
                        'tokenAmount':  i.tokenAmount,
                        'color': 'red'
                    }
                    tokenlist.append(tokendict)
                else:
                    tokendict = {
                        'plotNo':  i.plotNo,
                        'societyName':  i.societyName,
                        'tokenAmount':  i.tokenAmount,
                        'color': 'black'
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
        plotlist = []
        allInfo = []
        getplots = payments.query.all()

        for plot in getplots:
            dict = {"societyName": plot.societyName,
                    "sectorNo": plot.sectorNo,
                    "plotNo": plot.plotNo}
            plotlist.append(dict)
        #print("682" , plotlist)
        for i in plotlist:
            info = plottopurchase.query.filter(and_(
                plottopurchase.societyname == i['societyName'], plottopurchase.sectorno == i['sectorNo'], plottopurchase.plotno == i['plotNo']))
            for plot in info:
                dict = {"id": plot.id,
                        "societyname": plot.societyname,
                        "sectorno": plot.sectorno,
                        "plotno": plot.plotno,
                        "withdevelopment": plot.withdevelopment,
                        "withoutdevelopment": plot.withoutdevelopment,
                        "description": plot.description,
                        "plotamount": plot.plotamount,
                        "plotownername": plot.plotownername
                        }
                #print("697 ",dict)
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
            info = plottopurchase.query.filter(and_(
                plottopurchase.societyname == i.societyName, plottopurchase.sectorno == i.sectorNo, plottopurchase.plotno == i.plotNo))
            for plot in info:
                dict = {"id": plot.id,
                        "societyname": plot.societyname,
                        "sectorno": plot.sectorno,
                        "plotno": plot.plotno,
                        "withdevelopment": plot.withdevelopment,
                        "withoutdevelopment": plot.withoutdevelopment,
                        "description": plot.description,
                        "plotamount": plot.plotamount,
                        "plotownername": plot.plotownername}
                if dict not in allInfo:
                    allInfo.append(dict)
        allInfoJson = json.dumps(allInfo)
        return allInfoJson
    else:
        return make_response("Error"), 400


@app.route('/saleplotdetails', methods=['GET'])
def salePlotDetails():
    if (request.method == 'GET'):
        if checkPermission(getUserId() , "Sale"):
            plotDesc = []
            plotToPurchaseApi = request.get_json()
            societyname = plotToPurchaseApi['societyname']
            sectorno = plotToPurchaseApi['sectorno']
            plotno = plotToPurchaseApi['plotno']
            withdevelopment = plotToPurchaseApi['withdevelopment']
            withDevelopDescrip = plotToPurchaseApi['withDevelopDescrip']
            withoutdevelopment = plotToPurchaseApi['withoutdevelopment']
            withOutDevelopDescrip = plotToPurchaseApi['withOutDevelopDescrip']
            plotamount = plotToPurchaseApi['plotamount']
            plotownername = plotToPurchaseApi['plotownername']
            getPlotDesc = plottopurchase.query.filter(
                plottopurchase.societyname == societyname, plottopurchase.sectorno == sectorno, plottopurchase.plotno == plotno)
            for i in getPlotDesc:
                dict = {"description": i.description}
                if dict not in plotDesc:
                    plotDesc.append(dict)
            print(plotDesc)
            addtoPurchase = saleplotdetail(societyname=societyname, sectorno=sectorno, plotno=plotno, withdevelopment=withdevelopment, withDevelopDescrip=withDevelopDescrip,
                                           withoutdevelopment=withoutdevelopment, withOutDevelopDescrip=withOutDevelopDescrip, plotdescription=plotDesc[0]['description'], plotamount=plotamount, plotownername=plotownername)
            db.session.add(addtoPurchase)
            db.session.commit()
            return make_response("ok"), 200
        else:
            return make_response("access denied")


@app.route('/salepayments', methods=['POST'])
def SalePaymentsDetails():
    if (request.method == 'POST'):
        if checkPermission(getUserId(), "Sale"):
            salePaymentsAPI = request.get_json()
            plotInfo = salePaymentsAPI["plotInfo"]
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
            if tokenAmount:
                completeORNot = "not"
            else:
                completeORNot = "yes"
            updatedValue = 0
            remBalance = 0
            getPartner = memberinplots.query.filter(and_(
                memberinplots.societyName == plotInfo['societyname'], memberinplots.sectorNo == plotInfo['sectorNo'], memberinplots.plotid == plotInfo['plotNo'])).all()
            # check the total sum of cheque amount , amount in cash or payorder amount is equal to plot total amount
            if tokenAmount:
                if amountInCash or chequeAmount or payorderAmount or onlineTransfer:
                    tOp = checkTotalOfPayments(
                        amountInCash, chequeAmount, payorderAmount, onlineTransfer)
                if(tOp != float(tokenAmount)):
                    return make_response("added amount of token is greater or smaller than plot total amount")
            else:
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
                                print(plotInfo['sectorNo'])
                                print(plotInfo['plotNo'])
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
                return make_response("error"),400
            stmt1 = (update(memberinplots). where(and_(
                memberinplots.societyName == plotInfo['societyname'], memberinplots.sectorNo == plotInfo['sectorNo'], memberinplots.plotid == plotInfo['plotNo'])). values(saleOrNot="yes"))
            db.session.execute(stmt1)
            db.session.commit()
            salePaymentsAdd = salepaymentmethod(plotInfo="Ni", societyName=plotInfo["societyname"], sectorNo=plotInfo["sectorNo"], plotNo=plotInfo["plotNo"], amountInCash=amountInCash, chequeAmount=chequeAmount, noOfCheques=noOfCheques, chequeNo=chequeNo, chequeDescription=chequeDescription,
                                                payorderAmount=payorderAmount, noOfPayOrder=noOfPayOrder, payOrderNo=payOrderNo, payOrderDescription=payOrderDescription, totalAmount=plotInfo[
                                                    "plotAmount"], remaningBalance=remBalance, completeOrNot=completeORNot,
                                                tokenAmount=tokenAmount, tokenDays=tokenDays, tokenDate=datetime.date.today(), tokenDescription=tokenDescription, taxAmount=taxAmount, taxDescription=taxDescription, onlineTransfer=onlineTransfer, onlineDescription=onlineDescription)
            db.session.add(salePaymentsAdd)
            db.session.commit()

            return make_response("add"),200
        else:
            return make_response("access denied")





@app.route('/updateForPurchase', methods=['PUT'])
def updateAcc():
    return updateAccountDetailsAfterToken(payments)


@app.route('/updateForSale', methods=['PUT'])
def updateAccofSale():
    return updateAccountDetailsAfterToken(salepaymentmethod)


def updateAccountDetailsAfterToken(table):
    if request.method == 'PUT':
        salePaymentsAPI = request.get_json()
        societyName = salePaymentsAPI["societyName"]
        sectorName = salePaymentsAPI['sectorName']
        plotNo = salePaymentsAPI['plotNo']
        amountInCash = salePaymentsAPI['amountInCash']
        chequeAmount = salePaymentsAPI['chequeAmount']
        noOfCheques = salePaymentsAPI['noOfCheques']
        chequeNo = salePaymentsAPI['chequeNo']
        chequeDescription = salePaymentsAPI['chequeDescription']
        payorderAmount = salePaymentsAPI['payorderAmount']
        noOfPayOrder = salePaymentsAPI['noOfPayOrder']
        payOrderNo = salePaymentsAPI['payOrderNo']
        payOrderDescription = salePaymentsAPI['payOrderDescription']

        getPaymentsWithToken = table.query.filter(and_(
            table.societyName == societyName, table.sectorNo == sectorName, table.plotNo == plotNo, table.tokenAmount > 0)).all()
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
            if amountInCash or chequeAmount or payorderAmount:
                tOp = checkTotalOfPayments(
                    amountInCash, chequeAmount, payorderAmount)
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
                                             payorderAmount=payorderAmount+pOa, payOrderNo=payOrderNo, payOrderDescription=payOrderDescription, noOfPayOrder=noOfPayOrder+nOp))
                db.session.execute(stmt1)
                db.session.commit()
        else:
            return make_response("no record found!"), 400
        return {"Balance is": remBalance}



db.create_all()

if __name__ == '__main__':
    app.run()
