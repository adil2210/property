from sqlalchemy.sql.expression import null
from werkzeug.security import generate_password_hash
from app import db
from flask_sqlalchemy import *

class signup(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    phoneno = db.Column(db.String(12), nullable=False)
    cnic = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    resetCode = db.Column(db.Integer,default=None, nullable=False)
    ralation = db.relationship(
        'addsocietydata', backref='signup', lazy='dynamic')
    ralation1 = db.relationship(
        'accountsdetail', backref='signup', lazy='dynamic')
    ralation2 = db.relationship(
        'permissions', backref='signup', lazy='dynamic')



class permissions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('signup.id'))
    Accounts = db.Column(db.Boolean, default=False, nullable=False)
    Purchase = db.Column(db.Boolean, default=False, nullable=False)
    Sale = db.Column(db.Boolean, default=False, nullable=False)
    Supper = db.Column(db.Boolean, default=False, nullable=False)




class addsocietydata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('signup.id'))
    societyname = db.Column(db.String(80), nullable=False)
    sectorno = db.Column(db.String(100), nullable=False)
    plotno = db.Column(db.String(100), nullable=False, unique=False)
    plotsize = db.Column(db.String(100), nullable=False)
    plottype = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    # sectormapimg = db.Column(db.String(100), nullable=True)


class plotimages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plotnum = db.Column(db.String(100))
    img = db.Column(db.String(100), nullable=True)


class plottopurchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    societyname = db.Column(db.String(100), nullable=False)
    sectorno = db.Column(db.String(100), nullable=False)
    plotno = db.Column(db.String(100), nullable=False)
    development = db.Column(db.Boolean, nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    plotamount = db.Column(db.String(1000), nullable=False)
    plotownername = db.Column(db.String(100), nullable=False)


class accountsdetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uid = db.Column(db.Integer, db.ForeignKey('signup.id'))
    name = db.Column(db.String(100), nullable=False)
    cnic = db.Column(db.String(100), nullable=False)
    contactNo = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    accName = db.Column(db.String(1000), nullable=False)
    bankName = db.Column(db.String(1000), nullable=False)
    accNo = db.Column(db.String(1000), nullable=False)
    amountToInvest = db.Column(db.Float, nullable=False)
    dateTime = db.Column(db.String(1000), nullable=False)
    amountInCash = db.Column(db.Float, default=None, nullable=False)
    chequeAmount = db.Column(db.Float, default=None, nullable=False)
    noOfCheques = db.Column(db.String(100), default=None, nullable=False)
    chequeNo = db.Column(db.String(100), default=None, nullable=False)
    chequeDescription = db.Column(
        db.String(1000), default=None, nullable=False)
    payorderAmount = db.Column(db.Float, default=None, nullable=False)
    noOfPayOrder = db.Column(db.String(100), default=None, nullable=False)
    payOrderNo = db.Column(db.String(100), default=None, nullable=False)
    payOrderDescription = db.Column(
        db.String(1000), default=None, nullable=False)
    onlineTransfer = db.Column(db.Float, default=None, nullable=False)
    onlineDescription = db.Column(db.String(100), default=None, nullable=False)


class memberinplots(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(1000), default=None, nullable=False)
    names = db.Column(db.String(1000), default=None, nullable=False)
    p_amounts = db.Column(db.String(1000), default=None, nullable=False)
    adm_amounts = db.Column(db.String(1000), default=None, nullable=False)
    percentageInPlot=db.Column(db.String(1000), default=None, nullable=False)
    role = db.Column(db.String(1000), default=None, nullable=False)
    societyName = db.Column(db.String(1000), default=None, nullable=False)
    sectorNo = db.Column(db.String(1000), default=None, nullable=False)
    plotid = db.Column(db.String(1000), default=None, nullable=False)
    saleOrNot= db.Column(db.String(1000), nullable=False)


class payments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    societyName = db.Column(db.String(1000), default=None, nullable=False)
    sectorNo = db.Column(db.String(1000), default=None, nullable=False)
    plotNo = db.Column(db.String(1000), default=None, nullable=False)
    amountInCash = db.Column((db.Float), default=None, nullable=False)
    chequeAmount = db.Column((db.Float), default=None, nullable=False)
    noOfCheques = db.Column((db.Float), default=None, nullable=False)
    chequeNo = db.Column(db.String(100), default=None, nullable=False)
    chequeDescription = db.Column(
        db.String(1000), default=None, nullable=False)
    payorderAmount = db.Column((db.Float), default=None, nullable=False)
    noOfPayOrder = db.Column((db.Float), default=None, nullable=False)
    payOrderNo = db.Column(db.String(100), default=None, nullable=False)
    payOrderDescription = db.Column(
        db.String(1000), default=None, nullable=False)
    tokenAmount = db.Column((db.Float), default=None, nullable=False)
    tokenDays = db.Column(db.String(100), default=None, nullable=False)
    tokenDate = db.Column(db.DateTime, default=None, nullable=False)
    tokenDescription = db.Column(db.String(100), default=None, nullable=False)
    taxAmount = db.Column((db.Float), default=None, nullable=False)
    taxDescription = db.Column(db.String(1000), default=None, nullable=False)
    onlineTransfer = db.Column((db.Float), default=None, nullable=False)
    onlineDescription = db.Column(db.String(1000), default=None, nullable=False)
    remaningBalance = db.Column(db.Float, default=None, nullable=False)
    completeOrNot = db.Column(db.String(100), default=None, nullable=False)


class saleplotdetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    societyname = db.Column(db.String(100), nullable=False)
    sectorno = db.Column(db.String(100), nullable=False)
    plotno = db.Column(db.String(100), nullable=False)
    withdevelopment = db.Column(db.Boolean, default=False, nullable=False)
    withDevelopDescrip=db.Column(db.String(1000),default=None, nullable=False)
    withoutdevelopment = db.Column(db.Boolean, default=False, nullable=False)
    withOutDevelopDescrip=db.Column(db.String(1000),default=None, nullable=False)
    plotdescription = db.Column(db.String(1000), nullable=False)
    plotamount = db.Column(db.String(1000), nullable=False)
    plotownername = db.Column(db.String(100), nullable=False)


class salepaymentmethod(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plotInfo=db.Column(db.String(1000), default=None, nullable=False)
    societyName = db.Column(db.String(1000), default=None, nullable=False)
    sectorNo = db.Column(db.String(1000), default=None, nullable=False)
    plotNo = db.Column(db.String(1000), default=None, nullable=False)
    amountInCash = db.Column((db.Float), default=None, nullable=False)
    chequeAmount = db.Column((db.Float), default=None, nullable=False)
    noOfCheques = db.Column((db.Float), default=None, nullable=False)
    chequeNo = db.Column(db.String(100), default=None, nullable=False)
    chequeDescription = db.Column(
        db.String(1000), default=None, nullable=False)
    payorderAmount = db.Column((db.Float), default=None, nullable=False)
    noOfPayOrder = db.Column((db.Float), default=None, nullable=False)
    payOrderNo = db.Column(db.String(100), default=None, nullable=False)
    payOrderDescription = db.Column(
        db.String(1000), default=None, nullable=False)
    tokenAmount = db.Column(db.Float, default=None, nullable=False)
    tokenDays = db.Column(db.String(100), default=None, nullable=False)
    tokenDate = db.Column(db.DateTime, default=None, nullable=False)
    tokenDescription = db.Column(db.String(100), default=None, nullable=False)
    taxAmount = db.Column((db.Float), default=None, nullable=False)
    taxDescription = db.Column(db.String(1000), default=None, nullable=False)
    onlineTransfer = db.Column((db.Float), default=None, nullable=False)
    onlineDescription = db.Column(db.String(1000), default=None, nullable=False)
    totalAmount = db.Column(db.Float, default=None, nullable=False)
    remaningBalance = db.Column(db.Float, default=None, nullable=False)
    completeOrNot = db.Column(db.String(100), default=None, nullable=False)


# Construction Module Tables
class constructionaccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    accountNo=db.Column(db.String(1000), default=None, nullable=False)
    name = db.Column(db.String(1000), default=None, nullable=False)
    amount = db.Column(db.Float, default=None, nullable=False)


class constructionaddplot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    societyName=db.Column(db.String(1000), default=None, nullable=False)
    plotNo=db.Column(db.String(1000), default=None, nullable=False)
    plotOwnerName=db.Column(db.String(1000), default=None, nullable=False)
    phoneNo=db.Column(db.String(1000), default=None, nullable=False)
    streetLocation=db.Column(db.String(1000), default=None, nullable=False)
    categories=db.Column(db.String(1000), default=None, nullable=False)
    totalStories=db.Column(db.String(1000), default=None, nullable=False)
    plotSqFeet=db.Column(db.Float, default=None, nullable=False)
    totalPlotSize=db.Column(db.String(1000), default=None, nullable=False)
    ratePerSqFeet=db.Column(db.Float, default=None, nullable=False)
    amount=db.Column(db.Float, default=None, nullable=False)
    pay=db.Column(db.Float, default=None, nullable=False)
    structure=db.Column(db.String(1000), default=None, nullable=False)
    material=db.Column(db.Boolean, nullable=False)
    status=db.Column(db.String(1000), default=None, nullable=False)
    
    
class constructionaddsupplier(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(1000),default=None,nullable=False)
    contact=db.Column(db.String(1000),default=None,nullable=False)
    cnic=db.Column(db.String(1000),default=None,nullable=False)
    address=db.Column(db.String(1000),default=None,nullable=False)
    filer=db.Column(db.Boolean,nullable=False)

class constructionpurchaseproduct(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    itemName=db.Column(db.String(1000),default=None,nullable=False)
    rate=db.Column(db.Float,default=None,nullable=False)
    unit=db.Column(db.String(1000),default=None,nullable=False)
    quantity=db.Column(db.String(1000),default=None,nullable=False)
    supplierName=db.Column(db.String(1000),default=None,nullable=False)
    


db.create_all()
