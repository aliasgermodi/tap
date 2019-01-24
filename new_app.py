from flask import Flask
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
import json
import datetime
import time
client = MongoClient('localhost:27017')
db = client.TaskDB

app = Flask(__name__)
#app.config["MONGODB_DATABASE"]="user"
ts = time.time()

date_format = "%Y-%m-%d %H:%M:%S.%f"



@app.route("/add_customer", methods = ['POST'])
def add_customer():
    try:
        data = json.loads(request.data)

        #user_task = data['task']
        #user_time = data['time']
        #last_seen = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #last_seen = datetime.datetime.utcnow()
        creation = datetime.datetime.utcnow()
        #if user_task and user_time:
        status = db.Customer.insert({
                "customer_id" : data['customer_id'],
                "plan_name" : data['plan_name'],
                "price":{"amount":data['amount'],"currency":data['currency']},
                #"time": user_time,
                #"ls": last_seen,
                "creation":creation
            })
        return dumps({'message' : 'SUCCESS'})
    except Exception, e:
        return dumps({'error' : str(e)})


@app.route("/add_features", methods = ['POST'])
def add_features():
    try:
        data = json.loads(request.data)
        #print data

        #user_task = data['task']
        #user_time = data['time']
        #last_seen = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        #last_seen = datetime.datetime.utcnow()
        creation = datetime.datetime.utcnow()
        #if user_task and user_time:
        status = db.Feature.insert({
                "customer_id" : data['customer_id'],
                "feature_type" : data['feature_type'],
                "limit":{"amount":data['limit_amount'],"unit":data['limit_unit'],"balance":data['limit_balance']},
                "extraCharge":{"amount":data['extra_charge_amount'],"currency":data['extra_charge_currency'],"unit":data['extra_charge_unit']},
                #"time": user_time,
                #"ls": last_seen,
                "creation":creation
            })
        return dumps({'message' : 'SUCCESS'})
    except Exception, e:
        return dumps({'error' : str(e)})




#veiw all the data
@app.route("/get_all_info", methods = ['POST'])
def get_all_contact():#customer_id,**kwargs):
    try:
        data = json.loads(request.data)
        customer = db.Customer.find({"customer_id":data['customer_id']})
        #customer= 'Customer':list(customer)
        print customer
        features = db.Feature.find({"customer_id":data['customer_id']})
        features = list(features)
        print list(features)
        info=[]
        info.extend([customer,features])
        print info
        return dumps({"plan":customer,"Feature":features})
    except Exception, e:
        return dumps({'error' : str(e)})

@app.route("/update_customer",methods=['POST'])
def update_customer():
    try:
        data=json.loads(request.data)
        print data
        creation = datetime.datetime.utcnow()
        '''status=db.Customer.replace_one(
            {"customer_id":data['customer_id']},
            {"plan_name":data['plan_name'],"amount":data['amount'],"currency":data['currency']})'''
        user = db.Customer.update({
                                "customer_id" : data['customer_id']
                                },{                                
                                "$set": {
                                        "plan_name":data['plan_name'],
                                        "price":{"amount":data['amount'],"currency":data['currency']},
                                        "creation":creation
                                    }
                                })
        return dumps({"message":"Updated Succesfully"})
    except Exception, e:
        return dumps({"error":str(e)})


@app.route("/update_features",methods=['POST'])
def update_features():
    try:
        data=json.loads(request.data)
        print data
        creation = datetime.datetime.utcnow()
        '''status=db.Customer.replace_one(
            {"customer_id":data['customer_id']},
            {"plan_name":data['plan_name'],"amount":data['amount'],"currency":data['currency']})'''
        user = db.Feature.update({
                                "customer_id" : data['customer_id'],"feature_type" : data['feature_type']
                                },{                                
                                "$set": {                                
                                        "limit":{"amount":data['limit_amount'],"unit":data['limit_unit'],"balance":data['limit_balance']},
                                        "extraCharge":{"amount":data['extra_charge_amount'],"currency":data['extra_charge_currency'],"unit":data['extra_charge_unit']},
                                        "creation":creation
                                    }
                                })
        return dumps({"message":"Updated Succesfully"})
    except Exception, e:
        return dumps({"error":str(e)})



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000,debug=True)
