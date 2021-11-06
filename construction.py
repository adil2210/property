import database
from sqlalchemy import and_, or_, not_, update,func
from flask import make_response
from flask import *
import app

construction = Blueprint('construction', __name__)
# constructionAddPlot= Blueprint('constructionAddPlotApi', __name__)
# constructionAddSupplier=Blueprint('constructionAddSupplierApi',__name__)
# constructionPurchaseProduct=Blueprint('constructionPurchaseProductApi',__name__)
# constructionPurchaseProduct=Blueprint('constructionPurchaseProductApi',__name__)



# add account for construction start up
@construction.route('/constructionAmount' ,methods=['POST'])
def addConstructionAccountDetails():
    constructionDetailsApi = request.get_json()
    accountNo = constructionDetailsApi["accountNo"]
    name = constructionDetailsApi['name']
    amount = constructionDetailsApi['amount']
    construction=database.constructionaccount(accountNo=accountNo,name=name,amount=amount)
    app.db.session.add(construction)
    app.db.session.commit()
    return make_response("added"),200

# add plot for construction
@construction.route('/addPlot' ,methods=['POST'])
def addPlot():
    addPlotApi = request.get_json()
    societyName = addPlotApi["societyName"]
    plotNo = addPlotApi['plotNo']
    sector = addPlotApi['sector']
    plotOwnerName = addPlotApi['plotOwnerName']
    phoneNo = addPlotApi['phoneNo']
    streetLocation = addPlotApi['streetLocation']
    categories = addPlotApi['categories']
    totalStories = addPlotApi['totalStories']
    plotSqFeet = addPlotApi['plotSqFeet']
    totalPlotSize = addPlotApi['totalPlotSize']
    ratePerSqFeet = addPlotApi['ratePerSqFeet']
    pay=addPlotApi['pay']
    structure = addPlotApi['structure']
    material = addPlotApi['material']
    checkPlotSociety = database.constructionaddplot.query.filter(and_(database.constructionaddplot.plotNo == plotNo,
                                                                database.constructionaddplot.societyName == societyName)).first()
    if checkPlotSociety:
        return make_response("Plot already exists in this society"),400
    else:
        totalAmount=plotSqFeet*ratePerSqFeet
        if pay==totalAmount:
            s="complete"
        else:
            s="not complete"
        consAcc=database.constructionaccount.query.all()
        amn=0
        for i in consAcc:
            amn=i.amount
        stmt = (update(database.constructionaccount).values(amount=amn+pay))
        app.db.session.execute(stmt)
        app.db.session.commit()
        addPlot=database.constructionaddplot(societyName=societyName,plotNo=plotNo,sector=sector,plotOwnerName=plotOwnerName,phoneNo=phoneNo,amount=totalAmount,pay=pay,status=s,
                                                streetLocation=streetLocation,categories=categories,totalStories=totalStories,plotSqFeet=plotSqFeet,totalPlotSize=totalPlotSize,ratePerSqFeet=ratePerSqFeet,structure=structure,material=material)
        app.db.session.add(addPlot)
        app.db.session.commit()
        return make_response("added"),200

# add supplier account
@construction.route('/addSupplier',methods=['Post'])
def addSupplier():
    addSupplierApi=request.get_json()
    name=addSupplierApi['name']
    contact=addSupplierApi['contact']
    cnic=addSupplierApi['cnic']
    address=addSupplierApi['address']
    filer=addSupplierApi['filer']
    checkSupplier=database.constructionaddsupplier.query.filter(or_(database.constructionaddsupplier.contact==contact ,database.constructionaddsupplier.cnic==cnic)).all()
    if checkSupplier:
        return make_response("contact no or cnic already exists"),400
    else:
        supplierAdd=database.constructionaddsupplier(name=name,contact=contact,cnic=cnic,address=address,filer=filer)
        app.db.session.add(supplierAdd)
        app.db.session.commit()
        return make_response("added"),200


@construction.route('/getSupplierName',methods=['GET'])
def getSupplierName():
    temp=[]
    getSupplier=database.constructionaddsupplier.query.all()
    for i in getSupplier:
        dict={
            "name":i.name,
            "contact":i.contact
        }
        temp.append(dict)
    supp = json.dumps(temp)
    return supp


#  purchase products
@construction.route('/purchaseProduct',methods=['POST'])
def purchaseProduct():
    purchaseProductApi=request.get_json()
    itemName=purchaseProductApi['itemName']
    rate=purchaseProductApi['rate']
    unit=purchaseProductApi['unit']
    quantity=purchaseProductApi['quantity']
    supplierName=purchaseProductApi['supplierName']
    pay=purchaseProductApi['pay']
    total=quantity*rate
    if pay==total:
        paid=True
    else:
        paid=False
    checkItem=database.constructionpurchaseproduct.query.filter(and_(database.constructionpurchaseproduct.itemName==itemName)).all()
    if checkItem:
        for i in checkItem:
            idd=i.id
            totall=i.totalAmount
            quan=i.quantity
        
        stmt = (update(database.constructionpurchaseproduct).where(database.constructionpurchaseproduct.id==idd).values(itemName=itemName, unit=unit,rate=rate,totalAmount=totall+total,quantity=quan+quantity))
        app.db.session.execute(stmt)
        app.db.session.commit()
        
        return make_response("added"),200
    else:
        purchaseProduct=database.constructionpurchaseproduct(itemName=itemName, unit=unit,rate=rate,totalAmount=total,quantity=quantity,pay=pay,paid=paid,supplierName=supplierName)
        app.db.session.add(purchaseProduct)
        app.db.session.commit()
        return make_response("added"),200
        
    