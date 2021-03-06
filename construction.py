from datetime import datetime
from sqlalchemy.orm import query
import database
from sqlalchemy import and_, or_, not_, update, func
import datetime
from flask import make_response
from flask import *
import app

construction = Blueprint('construction', __name__)
# constructionAddPlot= Blueprint('constructionAddPlotApi', __name__)
# constructionAddSupplier=Blueprint('constructionAddSupplierApi',__name__)
# productInventory=Blueprint('productInventoryApi',__name__)
# productInventory=Blueprint('productInventoryApi',__name__)


# add account for construction start up
@construction.route('/constructionAmount', methods=['POST'])
def addConstructionAccountDetails():
    try:
        constructionDetailsApi = request.get_json()
        accountNo = constructionDetailsApi["accountNo"]
        name = constructionDetailsApi['name']
        amount = constructionDetailsApi['amount']
        construction = database.constructionaccount(
            accountNo=accountNo, name=name, amount=amount)
        app.db.session.add(construction)
        app.db.session.commit()
        return make_response("added"), 200
    except Exception as e:
        return e


@construction.route('/getConstructionAccountData', methods=['GET'])
def getConstructionAccountData():
    if (request.method == 'GET'):
        allData = []
        getAllData = database.constructionaccount.query.all()
        print(getAllData)
        if getAllData:
            for data in getAllData:
                dict = {"id": data.id,
                        "accountNo": data.accountNo,
                        "name": data.name,
                        "amount": data.amount}
                allData.append(dict)
            print(allData)
            accountData = json.dumps(allData)
            return accountData
        else:
            return make_response("No data Found"), 400
    else:
        return make_response("Request in error"), 400


@construction.route('/updateConstructionAccount', methods=['PUT'])
def updateConstructionAccount():
    if (request.method == 'PUT'):
        updateObj = request.get_json()
        obj = database.constructionaccount.query.filter(
            database.constructionaccount.id == updateObj['id']).all()
        for i in obj:
            amn = i.amount
        if amn > 0:
            newAmn = float(amn)+float(updateObj['amount'])
        stmt = (update(database.constructionaccount).where(database.constructionaccount.id == updateObj['id']).values(
            accountNo=updateObj['accountNo'], name=updateObj['name'], amount=newAmn))
        app.db.session.execute(stmt)
        app.db.session.commit()
        q = database.constructionaccount.query.filter_by(
            id=updateObj['id']).all()
        for i in q:
            dict = {
                "accountNo": i.accountNo,
                "name": i.name,
                "amount": i.amount,
            }
        return dict
    else:
        return make_response('using put method for update!'), 400


@construction.route('/deleteConstructionAccount/<int:idd>', methods=['DELETE'])
def deleteUdeleteConstructionAccountser(idd):
    if (request.method == 'DELETE'):
        # stmt = (delete(signup).where(signup.id == id))
        # stmt = signup.query.get(id)
        # db.session.delete(stmt)
        # db.session.commit()
        getData = database.constructionaccount.query.filter(
            database.constructionaccount.id == idd).all()
        id = 0
        for i in getData:
            id = i.id
        print(id)
        if getData:
            stmt = database.constructionaccount.query.get(idd)
            app.db.session.delete(stmt)
            app.db.session.commit()
        return make_response("ok"), 200


@construction.route('/addPlot', methods=['POST'])
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
    pay = addPlotApi['pay']
    structure = addPlotApi['structure']
    material = addPlotApi['material']
    checkPlotSociety = database.constructionaddplot.query.filter(and_(database.constructionaddplot.plotNo == plotNo,
                                                                      database.constructionaddplot.societyName == societyName)).first()
    if checkPlotSociety:
        return make_response("Plot already exists in this society"), 400
    else:
        totalAmount = plotSqFeet*ratePerSqFeet
        if pay == totalAmount:
            s = "complete"
        else:
            s = "not complete"
        remBalance = totalAmount-pay
        consAcc = database.constructionaccount.query.all()
        amn = 0
        for i in consAcc:
            amn = i.amount
        stmt = (update(database.constructionaccount).values(amount=amn+pay))
        app.db.session.execute(stmt)
        app.db.session.commit()
        addPlot = database.constructionaddplot(societyName=societyName, plotNo=plotNo, sectorNo=sector, remainingBalance=remBalance, plotOwnerName=plotOwnerName, phoneNo=phoneNo, amount=totalAmount, pay=pay, status=s,
                                               streetLocation=streetLocation, categories=categories, totalStories=totalStories, plotSqFeet=plotSqFeet, totalPlotSize=totalPlotSize, ratePerSqFeet=ratePerSqFeet, structure=structure, material=material)
        app.db.session.add(addPlot)
        app.db.session.commit()
        return make_response("added"), 200


@construction.route('/getConstructionAddPlotData', methods=['GET'])
def getConstructionAddPlotData():
    if (request.method == 'GET'):
        allData = []
        getAllData = database.constructionaddplot.query.all()
        print(getAllData)
        if getAllData:
            for data in getAllData:
                dict = {"id": data.id,
                        "societyName": data.societyName,
                        "plotNo": data.plotNo,
                        "sectorNo": data.sectorNo,
                        "plotOwnerName": data.plotOwnerName,
                        "phoneNo": data.phoneNo,
                        "streetLocation": data.streetLocation,
                        "categories": data.categories,
                        "totalStories": data.totalStories,
                        "plotSqFeet": data.plotSqFeet,
                        "totalPlotSize": data.totalPlotSize,
                        "ratePerSqFeet": data.ratePerSqFeet,
                        "amount": data.amount,
                        "remainingBalance": data.remainingBalance,
                        "pay": data.pay,
                        "structure": data.structure,
                        "material": data.material,
                        "status": data.status
                        }
                allData.append(dict)
            print(allData)
            constructionPlotData = json.dumps(allData)
            return constructionPlotData
        else:
            return make_response("No data Found"), 400
    else:
        return make_response("Request in error"), 400


@construction.route('/updateConstructionPlotData', methods=['PUT'])
def updateConstructionPlotData():
    if (request.method == 'PUT'):
        updateObj = request.get_json()
        obj = database.constructionaddplot.query.filter(
            database.constructionaddplot.id == updateObj['id']).all()
        for i in obj:
            p = i.pay
            amn = i.amount
        prev = p+float(updateObj['pay'])
        remBalance = amn-prev
        if p > 0:
            pay = float(p)+float(updateObj['pay'])
        stmt = (update(database.constructionaddplot).where(database.constructionaddplot.id == updateObj['id']).values(societyName=updateObj['societyName'], plotNo=updateObj['plotNo'], sectorNo=updateObj['sectorNo'], plotOwnerName=updateObj['plotOwnerName'], phoneNo=updateObj['phoneNo'], streetLocation=updateObj[
                'streetLocation'], categories=updateObj['categories'], totalStories=updateObj['totalStories'], plotSqFeet=updateObj['plotSqFeet'], totalPlotSize=updateObj['totalPlotSize'], ratePerSqFeet=updateObj['ratePerSqFeet'], amount=amn, pay=pay, remainingBalance=remBalance, structure=updateObj['structure'], material=updateObj['material']))
        app.db.session.execute(stmt)
        app.db.session.commit()
        q = database.constructionaddplot.query.filter_by(
            id=updateObj['id']).all()
        for data in q:
            dict = {
                "societyName": data.societyName,
                "plotNo": data.plotNo,
                "sectorNo": data.sectorNo,
                "plotOwnerName": data.plotOwnerName,
                "phoneNo": data.phoneNo,
                "streetLocation": data.streetLocation,
                "categories": data.categories,
                "totalStories": data.totalStories,
                "plotSqFeet": data.plotSqFeet,
                "totalPlotSize": data.totalPlotSize,
                "ratePerSqFeet": data.ratePerSqFeet,
                "amount": data.amount,
                "pay": data.pay,
                "structure": data.structure,
                "material": data.material,
                "status": data.status
            }
        return dict
    else:
        return make_response('using put method for update!'), 400


@construction.route('/deleteConstructionAddPlot/<int:idd>', methods=['DELETE'])
def deleteConstructionAddPlot(idd):
    if (request.method == 'DELETE'):
        # stmt = (delete(signup).where(signup.id == id))
        # stmt = signup.query.get(id)
        # db.session.delete(stmt)
        # db.session.commit()
        getData = database.constructionaddplot.query.filter(
            database.constructionaddplot.id == idd).all()
        id = 0
        for i in getData:
            id = i.id
        print(id)
        if getData:
            stmt = database.constructionaddplot.query.get(idd)
            app.db.session.delete(stmt)
            app.db.session.commit()
        else:
            print("Not such id in database"), 400
        return make_response("ok"), 200


# add supplier account
@construction.route('/addSupplier', methods=['Post'])
def addSupplier():
    addSupplierApi = request.get_json()
    name = addSupplierApi['name']
    contact = addSupplierApi['contact']
    cnic = addSupplierApi['cnic']
    address = addSupplierApi['address']
    filer = addSupplierApi['filer']
    checkSupplier = database.constructionaddsupplier.query.filter(or_(
        database.constructionaddsupplier.contact == contact, database.constructionaddsupplier.cnic == cnic)).all()
    if checkSupplier:
        return make_response("contact no or cnic already exists"), 400
    else:
        supplierAdd = database.constructionaddsupplier(
            name=name, contact=contact, cnic=cnic, address=address, filer=filer)
        app.db.session.add(supplierAdd)
        app.db.session.commit()
        return make_response("added"), 200


@construction.route('/getConstructionAddSupplierData', methods=['GET'])
def getConstructionAddSupplierData():
    if (request.method == 'GET'):
        allData = []
        getAllData = database.constructionaddsupplier.query.all()
        print(getAllData)
        if getAllData:
            for data in getAllData:
                dict = {"id": data.id,
                        "name": data.name,
                        "contact": data.contact,
                        "cnic": data.cnic,
                        "address": data.address,
                        "filer": data.filer
                        }
                allData.append(dict)
            print(allData)
            constructionSupplierData = json.dumps(allData)
            return constructionSupplierData
        else:
            return make_response("No data Found"), 400
    else:
        return make_response("Request in error"), 400


@construction.route('/updateConstructionAddSupplier', methods=['PUT'])
def updateConstructionAddSupplier():
    if (request.method == 'PUT'):
        editSupp = request.get_json()
        stmt = (update(database.constructionaddsupplier).where(database.constructionaddsupplier.id == editSupp['id']).values(
            name=editSupp['name'], contact=editSupp['contact'], cnic=editSupp['cnic'], address=editSupp['address'], filer=editSupp['filer']))
        app.db.session.execute(stmt)
        app.db.session.commit()
        return make_response('edited successfully!'), 200


@construction.route('/deleteConstructionAddSupplier/<int:idd>', methods=['DELETE'])
def deleteConstructionAddSupplier(idd):
    if (request.method == 'DELETE'):
        # stmt = (delete(signup).where(signup.id == id))
        # stmt = signup.query.get(id)
        # db.session.delete(stmt)
        # db.session.commit()
        getData = database.constructionaddsupplier.query.filter(
            database.constructionaddsupplier.id == idd).all()
        id = 0
        for i in getData:
            id = i.id
        print(id)
        if getData:
            stmt = database.constructionaddsupplier.query.get(idd)
            app.db.session.delete(stmt)
            app.db.session.commit()
        else:
            print("Not such id in database"), 400
        return make_response("ok"), 200


@construction.route('/getAllSuppliers', methods=['GET'])
def getAllSupplier():
    temp = []
    getSupplier = database.constructionaddsupplier.query.all()
    for i in getSupplier:
        dict = {
            "id": i.id,
            "name": i.name,
            "contact": i.contact,
            "cnic": i.cnic,
            "address": i.address,
            "filer": i.filer
        }
        temp.append(dict)
    supp = json.dumps(temp)
    return supp


@construction.route('/getSupplierName', methods=['GET'])
def getSupplierName():
    temp = []
    getSupplier = database.constructionaddsupplier.query.all()
    for i in getSupplier:
        dict = {
            "id": i.id,
            "name": i.name
        }
        temp.append(dict)
    supp = json.dumps(temp)
    return supp


#  purchase products
@construction.route('/purchaseProduct', methods=['POST'])
def purchaseProduct():
    purchaseProductApi = request.get_json()
    itemName = purchaseProductApi['itemName']
    rate = purchaseProductApi['rate']
    unit = purchaseProductApi['unit']
    quantity = purchaseProductApi['quantity']
    supplierName = purchaseProductApi['supplierName']
    pay = purchaseProductApi['pay']
    paymentMethod = purchaseProductApi['paymentMethod']
    itemName = itemName.lower()

    total = quantity*rate
    remBalance = total-pay
    objCa = database.constructionaccount.query.all()
    totalAmount = 0
    for i in objCa:
        totalAmount = i.amount
    totalAmount = totalAmount-pay
    if pay > 0:
        stmt = (update(database.constructionaccount).values(amount=totalAmount))
        app.db.session.execute(stmt)
        app.db.session.commit()
    if pay == total:
        paid = True
    else:
        paid = False
    checkItem = database.productInventory.query.filter(
        and_(database.productInventory.itemName == itemName)).all()
    if checkItem:
        for i in checkItem:
            idd = i.id
            quan = i.quantity
        stmt = (update(database.productInventory).where(
            database.productInventory.id == idd).values(unit=unit, rate=rate, quantity=quan+quantity))
        app.db.session.execute(stmt)
        app.db.session.commit()
        add = database.allPurchaseProductAndSup(itemName=itemName, unit=unit, rate=rate, totalAmount=total, quantity=quantity,
                                                paymentMethod=paymentMethod, pay=pay, paid=paid, supplierName=supplierName, remainingBalance=remBalance)
        app.db.session.add(add)
        app.db.session.commit()
        return make_response("added"), 200
    else:
        add = database.allPurchaseProductAndSup(itemName=itemName, unit=unit, rate=rate, totalAmount=total, quantity=quantity,
                                                paymentMethod=paymentMethod, pay=pay, paid=paid, supplierName=supplierName, remainingBalance=remBalance)
        app.db.session.add(add)
        app.db.session.commit()
        purchaseProduct = database.productInventory(
            itemName=itemName, unit=unit, rate=rate, quantity=quantity)
        app.db.session.add(purchaseProduct)
        app.db.session.commit()
        return make_response("added"), 200


@construction.route('/getConstructionPurchaseProducts', methods=['GET'])
def getConstructionPurchaseProducts():
    if (request.method == 'GET'):
        allData = []
        getAllData = database.allPurchaseProductAndSup.query.all()
        print(getAllData)
        if getAllData:
            for data in getAllData:
                dict = {
                    "id": data.id,
                    "itemName": data.itemName,
                    "rate": data.rate,
                    "unit": data.unit,
                    "quantity": data.quantity,
                    "supplierName": data.supplierName,
                    "totalAmount": data.totalAmount,
                    "paid": data.paid,
                    "pay": data.pay,
                    "remainingBalance": data.remainingBalance,
                    "paymentMethod": data.paymentMethod,
                    "dateOfPurchase": data.dateOfPurchase
                }
                allData.append(dict)
            print(allData)
            constructionPurchaseProductData = json.dumps(allData)
            return constructionPurchaseProductData
        else:
            return make_response("No data Found"), 400
    else:
        return make_response("Request in error"), 400


@construction.route('/updateConstructionPurchaseProduct', methods=['PUT'])
def updateInventory():
    if (request.method == 'PUT'):
        edit_inventory = request.get_json()
        r = edit_inventory['rate']
        q = edit_inventory['quantity']
        itemName = edit_inventory['itemName']
        itemName = itemName.lower()
        total = r*q
        p = 0
        num = float(edit_inventory['pay'])
        obj = database.allPurchaseProductAndSup.query.filter(
            database.allPurchaseProductAndSup.id == edit_inventory['id']).all()
        for i in obj:
            p = i.pay
        print(p)
        pa = p+float(num)
        remBalance = float(total)-pa
        if num == total:
            paid = True
        else:
            paid = False
        objCa = database.constructionaccount.query.all()
        totalAmount = 0
        for i in objCa:
            totalAmount = i.amount
        totalAmount = totalAmount-float(num)
        if num > 0:
            stmt = (update(database.constructionaccount).values(
                amount=totalAmount))
            app.db.session.execute(stmt)
            app.db.session.commit()
        if float(num) == float(total):
            paid = True
        else:
            paid = False
        stmt = (update(database.allPurchaseProductAndSup).where(database.allPurchaseProductAndSup.id == edit_inventory['id']).values(itemName=itemName, rate=edit_inventory['rate'], unit=edit_inventory[
                'unit'], quantity=edit_inventory['quantity'], supplierName=edit_inventory['supplierName'], totalAmount=total, paid=paid, pay=pa, paymentMethod=edit_inventory['paymentMethod'], remainingBalance=remBalance))
        app.db.session.execute(stmt)
        app.db.session.commit()
        stmt1 = (update(database.productInventory).where(database.productInventory.itemName == edit_inventory['itemName']).values(
            rate=edit_inventory['rate'], unit=edit_inventory['unit'], quantity=edit_inventory['quantity']))
        app.db.session.execute(stmt1)
        app.db.session.commit()
        return make_response('edited successfully!'), 200


@construction.route('/deleteConstructionPurchaseProduct/<int:idd>', methods=['DELETE'])
def deleteConstructionPurchaseProduct(idd):
    if (request.method == 'DELETE'):
        # stmt = (delete(signup).where(signup.id == id))
        # stmt = signup.query.get(id)
        # db.session.delete(stmt)
        # db.session.commit()
        getData = database.allPurchaseProductAndSup.query.filter(
            database.allPurchaseProductAndSup.id == idd).all()
        id = 0
        for i in getData:
            id = i.id
        print(id)
        if getData:
            stmt = database.allPurchaseProductAndSup.query.get(idd)
            app.db.session.delete(stmt)
            app.db.session.commit()
        else:
            print("Not such id in database"), 400
        return make_response("ok"), 200


@construction.route('/allPlot', methods=['GET'])
def allPlotsForConstruction():
    allPlotObj = database.constructionaddplot.query.all()
    plist = []
    for plot in allPlotObj:
        dict = {
            "plotId": plot.id,
            "societyName": plot.societyName,
            "sectorNo": plot.sectorNo,
            "plotNo": plot.plotNo
        }
        plist.append(dict)
    newls = json.dumps(plist)
    return newls


@construction.route('/allItems', methods=['GET'])
def getAllItemName():
    temp = []
    getSupplier = database.productInventory.query.all()
    for i in getSupplier:
        dict = {
            "id": i.id,
            "name": i.itemName,
            "rate": i.rate,
            "unit": i.unit,
            "quantity": i.quantity,
        }
        temp.append(dict)
    supp = json.dumps(temp)
    return supp


@construction.route('/materialAssigned', methods=['POST'])
def materialAssignedToPlot():
    if (request.method == 'POST'):
        materialAssigned = request.get_json()
        plotId = materialAssigned['plotId']
        itemName = materialAssigned['itemName']
        quantity = materialAssigned['quantity']
        quantityType = materialAssigned['quantityType']
        supplierName = materialAssigned['supplierName']
        inventObj = database.productInventory.query.filter(
            itemName == itemName).all()
        for prod in inventObj:
            rate = prod.rate
        amount = quantity * rate
        print(amount)
        checkSupWithItem = database.allPurchaseProductAndSup.query.filter(
            supplierName == supplierName).all()
        itm = 0
        for i in checkSupWithItem:
            if i.itemName == itemName:
                itm = i.itemName
        print(itm)
        if itm == itemName:
            prodObj = database.productInventory.query.filter(
                itemName == itemName).all()
            for i in prodObj:
                quan = i.quantity
            n = quan
            print(n)
            if quantity > quan:
                return make_response('inventory Fails quantity Entered is higher!'), 400
            objMa = database.materiaAssingedToPlot(
                plotId=plotId, itemName=itemName, totalAmount=amount, quantity=quantity, supplierName=supplierName, quantityType=quantityType)
            app.db.session.add(objMa)
            app.db.session.commit()
            stmt = (update(database.productInventory).where(
                database.productInventory.itemName == itemName).values(quantity=n-quantity))
            app.db.session.execute(stmt)
            app.db.session.commit()
            return make_response('material Assigned!'), 200
        else:
            return make_response('this '+itemName+' was not purchased by this '+supplierName), 400


@construction.route('/getConstructionMaterialAssignedPlot', methods=['GET'])
def getConstructionMaterialAssignedPlot():
    material_obj = database.materiaAssingedToPlot.query.all()
    allPlots = []  # list of dictionaries
    plot_list = []
    temp = []
    for i in material_obj:
        # allPlots.append(i.plotId)
        if i.plotId not in plot_list:
            plot_list.append(i.plotId)
            dict = {
                "id": i.id,
                "plotId": i.plotId
            }
            allPlots.append(dict)
    for i in allPlots:
        getData = database.constructionaddplot.query.filter(
            database.constructionaddplot.id == i['plotId']).all()
        for n in getData:
            dict = {
                "id": n.id,
                "societyName": n.societyName,
                "sectorNo": n.sectorNo,
                "plotNo": n.plotNo
            }
            temp.append(dict)
    material = json.dumps(temp)
    return material


@construction.route('/getMaterialAgainstPlotId/<int:idd>', methods=['GET'])
def getMaterialAgainstPlotId(idd):
    temp = []
    material_obj = database.materiaAssingedToPlot.query.filter(
        database.materiaAssingedToPlot.plotId == idd).all()
    for i in material_obj:
        dict = {
            "id": i.id,
            "itemName": i.itemName,
            "quantity": i.quantity,
            "quantityType": i.quantityType,
            "supplierName": i.supplierName,
            "totalAmount": i.totalAmount
        }
        temp.append(dict)
    material = json.dumps(temp)
    return material


@construction.route('/deleteConstructiongetMaterialAgainstPlot/<int:idd>', methods=['DELETE'])
def deleteConstructiongetMaterialAgainstPlot(idd):
    if (request.method == 'DELETE'):
        # stmt = (delete(signup).where(signup.id == id))
        # stmt = signup.query.get(id)
        # db.session.delete(stmt)
        # db.session.commit()
        getData = database.materiaAssingedToPlot.query.filter(
            database.materiaAssingedToPlot.plotId == idd).all()
        id = 0
        for i in getData:
            id = i.id
            if getData:
                stmt = database.materiaAssingedToPlot.query.get(id)
                app.db.session.delete(stmt)
                app.db.session.commit()
            else:
                print("Not such id in database"), 400
        return make_response("ok"), 200


@construction.route('/getAllPlot', methods=['GET'])
def getAllPlotsForConstruction():
    allPlotObj = database.constructionaddplot.query.all()
    plist = []
    for plot in allPlotObj:
        dict = {
            "plotId": plot.id,
            "societyName": plot.societyName,
            "sectorNo": plot.sectorNo,
            "plotNo": plot.plotNo,
            "streetLocation": plot.streetLocation
        }
        plist.append(dict)
    newls = json.dumps(plist)
    return newls


allWorkName = {
    "1": "Demarcation of Site",
    "2": "STANDARED PROTECTOR COMPACTION TEST & FDT TEST",
    "3": "Layout of Foundation",
    "4": "Foundation Basement & Columns & Waterproofing Plot",
    "5": "Retaining Walls/ Stair Case",
    "6": "Water Proofing",
    "7": "Basement Lintels",
    "8": "Basement Slabs and Beams",
    "9": "Layout of Foundation Ground Floorwith Set Back",
    "10": "Construction Of Boundary Wall Upto D.P.C",
    "11": "Foundation Ground Floor Columns and stair case",
    "12": "Plint Beams",
    "13": "D.P.C level with set back Porch Level",
    "14": "Under Ground Water Tank",
    "15": "Foundation Ground Floor Lintels Beams (Door & Window)",
    "16": "Car Porch Slab and Beams",
    "17": "Fround Floor Slab & Beams, Projection & Stair Case",
    "18": "Layout of First Floor",
    "19": "First Floor Lintels Beams (Doors and Windows)	",
    "20": "First Floor Slab, Beams, Projection & Stairs",
    "21": "First Floor Parapet Wall",
    "22": "OverHeaad water Tank",
    "23": "Top Floor Water Proofing",
    "24": "Ramp 3 'High From Road Level & lying of 3' Dia Three Pipes",
    "25": "Septic Tanks",
    "26": "Internal Drainage(for Rain Water) should be connected to road/drain",
    "27": "Gate and Boundary Wall and Plot Measuring",
    "28": "In Case of Corner Plot Boundary wall should be Chamfered	",
    "29": "********* Finishing (Material/ Colour)",
    "30": "Gas/ Electric Meters",
    "31": "Site Clearance"
}


@construction.route('/constructionManagment', methods=['POST'])
def constructionManagment():
    constructionManagmentApi = request.get_json()
    for i in constructionManagmentApi:
        supervisor = i['supervisor']
        dateStart = str(i['dateStart'])
        dateFinish = str(i['dateFinish'])
        plotId = i['plotId']
        toDoId = i['toDoId']
        comment = i['comment']
        violation = i['violation']
        name = i['name']
        getData = database.plotConstructionManagment.query.filter(and_(
            database.plotConstructionManagment.plotId == plotId, database.plotConstructionManagment.toDoId == toDoId)).all()
        print(getData)
        if getData:
            stmt = (update(database.plotConstructionManagment).where(and_(database.plotConstructionManagment.plotId == plotId, database.plotConstructionManagment.toDoId == toDoId)).values(
                supervisor=supervisor, dateStart=dateStart, dateFinish=dateFinish, plotId=plotId, toDoId=toDoId, comment=comment, violation=violation, name=name))
            app.db.session.execute(stmt)
            app.db.session.commit()
        else:
            pCm = database.plotConstructionManagment(supervisor=supervisor, dateStart=dateStart, dateFinish=dateFinish,
                                                     plotId=plotId, toDoId=toDoId, comment=comment, violation=violation, name=name)
            app.db.session.add(pCm)
            app.db.session.commit()
    return make_response("ok"), 200


@construction.route('/toDoGet/<int:idd>', methods=['GET'])
def toDoGet(idd):
    # id=request.get_json()
    # pid=id["pid"]
    getData = database.plotConstructionManagment.query.filter(
        database.plotConstructionManagment.plotId == idd).all()
    n = []
    temp = []
    print(idd)
    for i in getData:
        toId = i.toDoId
        name = allWorkName[str(toId)]
        print(name)
        print(toId)
        # valueAgainstId=database.plotConstructionManagment.query.filter(database.plotConstructionManagment.toDoId==toId).all()
        # print(valueAgainstId)
        for j in getData:
            if j.toDoId not in temp:
                temp.append(j.toDoId)
                dict = {
                    "toDoId": j.toDoId,
                    "descName": name,
                    "com": j.comment,
                    "vio": j.violation,
                    "name": j.name,
                    "date": j.dateOfPurchase
                }
                n.append(dict)
    data = json.dumps(n)
    return data


@construction.route('/getPlotForConstructionManagment', methods=['GET'])
def getPlotForConstructionManagment():
    managmentPlot = database.plotConstructionManagment.query.all()
    allPlots = []  # list of dictionaries
    plot_list = []
    temp = []
    for i in managmentPlot:
        # allPlots.append(i.plotId)
        if i.plotId not in plot_list:
            plot_list.append(i.plotId)
            dict = {
                "id": i.id,
                "plotId": i.plotId,
                "supervisor": i.supervisor
            }
            allPlots.append(dict)
    print(allPlots)
    for i in allPlots:
        getData = database.constructionaddplot.query.filter(
            database.constructionaddplot.id == i['plotId']).all()
        getData1 = database.plotConstructionManagment.query.filter(
            database.plotConstructionManagment.supervisor == i['supervisor']).all()
        print(getData1)
        print("adil")
        print(getData)
        for n, n1 in zip(getData, getData1):
            print(n)
            dict = {
                "plotId": n.id,
                "societyName": n.societyName,
                "sectorNo": n.sectorNo,
                "plotNo": n.plotNo,
                "supervisor": n1.supervisor,
                "dateStart": n1.dateStart,
                "dateFinish": n1.dateFinish
            }
            temp.append(dict)
    material = json.dumps(temp)
    return material
