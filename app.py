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


#add the data
@app.route("/add_task", methods = ['POST'])
def add_task():
    try:
        data = json.loads(request.data)
        user_task = data['task']
        user_time = data['time']
        #last_seen = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        last_seen = datetime.datetime.utcnow()
        creation = datetime.datetime.utcnow()
        if user_task and user_time:
            status = db.Task.insert_one({
                "task" : user_task,
                "time": user_time,
                "ls": last_seen,
                "creation":creation
            })
        return dumps({'message' : 'SUCCESS'})
    except Exception, e:
        return dumps({'error' : str(e)})


#veiw all the data
@app.route("/get_all_task", methods = ['GET'])
def get_all_contact():
    try:
        tasks = db.Task.find()
        return dumps(tasks)
    except Exception, e:
        return dumps({'error' : str(e)})

#update the data, replacing and exisiting field
@app.route("/update_task", methods = ['POST'])
def update_task(task,time,**kwargs):
    try:
        '''data = json.loads(request.data)
        user_task = data['task']
        user_time = data['time']
        last_seen = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')'''
        user_task = task
        user_time = time
        if user_task and user_time:
            status = db.Task.replace_one(
             	{"task": user_task},
        		{"task" : user_task, "time" : user_time, "ls": datetime.datetime.utcnow()});
        #	return dumps({'message':'Already exists'})
        
        return dumps({"task_name":task,"message":"Updated Succesfully"})
    except Exception, e:
        return dumps({'error' : str(e)})

#update data, add extra field in the json

#get time interval and last updated time, compare the values with current time and do the process.

#get latest time interval

@app.route("/get_time_task", methods = ['GET'])
def get_time_task():
    try:
        tasks = db.Task.find().sort({'_id': -1}).limit(1) 

        return dumps(tasks)
    except Exception, e:
        return dumps({'error' : str(e)}) 

@app.route("/time_update")
def update_time():
    try:

        tasks=db.Task.find()
        for d in tasks:
            a = datetime.datetime.strptime(str(d['ls']), date_format)
            b = datetime.datetime.utcnow()
            b = datetime.datetime.strptime(str(b), date_format)
            delta = b - a
            delta=str(delta)
            delta=datetime.datetime.strptime(delta, "%H:%M:%S.%f")

            #print delta
            #print 
            #print "+++++++"
            ls_min = delta.strftime("%M")
            ls_min = int(ls_min)
            #print ls_min
            #print "*******"
            
            time = int(d['time'])
            #print time
            #print "--------"
            #print a
            if ls_min >= time:
                #print "Hello"
                update=update_task(d['task'],d['time'])
                return dumps(update)


        return dumps("SUCCESS")
    except Exception, e:
        return dumps({'error' : str(e)}) 


if __name__ == "__main__":
    app.run(host='127.0.0.1', port='5000',debug=True)