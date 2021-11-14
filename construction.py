from sqlalchemy.orm import query
import database
from sqlalchemy import and_, or_, not_, update,func
from flask import make_response
from flask import *
import app

construction = Blueprint('construction', __name__)
# constructionAddPlot= Blueprint('constructionAddPlotApi', __name__)
# constructionAddSupplier=Blueprint('constructionAddSupplierApi',__name__)
# productInventory=Blueprint('productInventoryApi',__name__)
# productInventory=Blueprint('productInventoryApi',__name__)



# add account for construction start up
@construction.route('/constructionAmount' ,methods=['POST'])
def addConstructionAccountDetails():
    try:
        constructionDetailsApi = request.get_json()
        accountNo = constructionDetailsApi["accountNo"]
        name = constructionDetailsApi['name']
        amount = constructionDetailsApi['amount']
        construction=database.constructionaccount(accountNo=accountNo,name=name,amount=amount)
        app.db.session.add(construction)
        app.db.session.commit()
        return make_response("added"),200
    except Exception as e:
        return e

# add plot for construction
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
    ratePerSqFeet = float(addPlotApi['ratePerSqFeet'])
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
        addPlot=database.constructionaddplot(societyName=societyName,plotNo=plotNo,sectorNo=sector,plotOwnerName=plotOwnerName,phoneNo=phoneNo,amount=totalAmount,pay=pay,status=s,
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

@construction.route('/editsupplier',methods=['Post'])
def editsupplier():
    try:
        editSupp = request.get_json()
        stmt = (update(database.constructionaddsupplier).where(database.constructionaddsupplier.id==editSupp['id']).values(name = editSupp['name'] , contact = editSupp['contact'] , cnic = editSupp['cnic'] , address = editSupp['address'] , filer = editSupp['filer']))
        app.db.session.execute(stmt)
        app.db.session.commit()
        return make_response('edited successfully!'),200
    except Exception as e:
        return make_response(e),400

@construction.route('/getAllSuppliers',methods=['GET'])
def getAllSupplier():
    temp=[]
    getSupplier=database.constructionaddsupplier.query.all()
    for i in getSupplier:
        dict={
            "id":i.id,
            "name":i.name,
            "contact":i.contact,
            "cnic":i.cnic,
            "address":i.address,
            "filer":i.filer
        }
        temp.append(dict)
    supp = json.dumps(temp)
    return supp


@construction.route('/getSupplierName',methods=['GET'])
def getSupplierName():
    temp=[]
    getSupplier=database.constructionaddsupplier.query.all()
    for i in getSupplier:
        dict={
            "id":i.id,
            "name":i.name
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
    paymentMethod=purchaseProductApi['paymentMethod']

    total=quantity*rate
    objCa = database.constructionaccount.query.all()
    for i in objCa:
        totalAmount = i.amount
    totalAmount = totalAmount-pay
    if pay > 0:
        stmt = (update(database.constructionaccount).values(amount = totalAmount))
        app.db.session.execute(stmt)
        app.db.session.commit()
    if pay==total:
        paid=True
    else:
        paid=False
    checkItem=database.productInventory.query.filter(and_(database.productInventory.itemName==itemName)).all()
    if checkItem:
        for i in checkItem:
            idd=i.id
            totall=i.totalAmount
            quan=i.quantity
        stmt = (update(database.productInventory).where(database.productInventory.id==idd).values(unit=unit,rate=rate,totalAmount=totall+total,quantity=quan+quantity))
        app.db.session.execute(stmt)
        app.db.session.commit()
        add = database.allPurchaseProductAndSup(itemName=itemName, unit=unit,rate=rate,totalAmount=total,quantity=quantity ,paymentMethod=paymentMethod, pay = pay , paid = paid,supplierName=supplierName)
        app.db.session.add(add)
        app.db.session.commit()
        return make_response("added"),200
    else:
        add = database.allPurchaseProductAndSup(itemName=itemName, unit=unit,rate=rate,totalAmount=total,quantity=quantity ,paymentMethod=paymentMethod, pay = pay , paid = paid,supplierName=supplierName)
        app.db.session.add(add)
        app.db.session.commit()
        purchaseProduct=database.productInventory(itemName=itemName, unit=unit,rate=rate,totalAmount=total,quantity=quantity)
        app.db.session.add(purchaseProduct)
        app.db.session.commit()
        return make_response("added"),200


@construction.route('/allPlot',methods=['GET'])
def allPlotsForConstruction():
    allPlotObj = database.constructionaddplot.query.all()
    plist = []
    for plot in allPlotObj:
        dict = {
            "plotId":plot.id,
            "societyName": plot.societyName,
            "sectorNo":plot.sectorNo,
            "plotNo":plot.plotNo
        }
        plist.append(dict)
    newls = json.dumps(plist)
    return newls
    
@construction.route('/allItems',methods=['GET'])
def getAllItemName():
    temp=[]
    getSupplier=database.productInventory.query.all()
    for i in getSupplier:
        dict={
            "name":i.itemName,
            "rate":i.rate
        }
        temp.append(dict)
    supp = json.dumps(temp)
    return supp


@construction.route('/materialAssigned',methods=['POST'])
def materialAssignedToPlot():
    try:
        materialAssigned = request.get_json()
        plotId=materialAssigned['plotId']
        itemName=materialAssigned['itemName']
        quantity=materialAssigned['quantity']
        quantityType=materialAssigned['quantityType']
        supplierName=materialAssigned['supplierName']
        inventObj = database.productInventory.query.filter(itemName == itemName ).all()
        for prod in inventObj:
            rate = prod.rate
        amount = quantity * rate
        print(amount)
        checkSupWithItem = database.allPurchaseProductAndSup.query.filter(supplierName == supplierName).all()
        itm  = 0
        for i in checkSupWithItem:
            itm = i.itemName
        if itm:
            prodObj = database.productInventory.query.filter(itemName == itemName).all()
            for i in prodObj:
                quan = i.quantity
            if quantity > quan:
                return make_response('inventory Fails quantity Entered is higher!'),400
            try:
                objMa = database.materiaAssingedToPlot(plotId = plotId , itemName = itemName, totalAmount=amount,quantity=quantity,supplierName = supplierName,quantityType=quantityType )
                app.db.session.add(objMa)
                app.db.session.commit()
            except Exception as e:
                return make_response(e),400
            try:
                stmt = (update(database.productInventory).where(database.productInventory.itemName==itemName).value(quantity=quan-quantity))
                app.db.session.execute(stmt)
                app.db.session.commit()
            except Exception as e:
                return make_response(e),400
            return make_response('material Assigned!'),200
        else:
            return make_response('this '+itemName+' was not purchased by this '+supplierName),400
    except Exception as e:
        print (e)
        return make_response("Error during material assigned"),400

