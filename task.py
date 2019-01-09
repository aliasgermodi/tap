from flask import Flask
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
import json
import datetime
import time
client = MongoClient('localhost:27017')
db = client.TaskDB

#app = Flask(__name__)
#app.config["MONGODB_DATABASE"]="user"
ts = time.time()

date_format = "%Y-%m-%d %H:%M:%S.%f"


while 1:

    tasks=db.Task.find()
    #print list(tasks)
    for d in list(tasks):
        #print "time"
        a = datetime.datetime.strptime(str(d['ls']), date_format)
        b = datetime.datetime.utcnow()
        b = datetime.datetime.strptime(str(b), date_format)
        delta = b - a
        delta=str(delta)
        delta=datetime.datetime.strptime(delta, "%H:%M:%S.%f")

        ls_min = delta.strftime("%M")
        ls_min = int(ls_min)
        #print "====="
        #print ls_min
                
                
        time = int(d['time'])
        #print "+++++++"
        #print time
        if ls_min >= time:
            #print "Hello"
            update=db.Task.replace_one(
                    {"task": d['task']},
                    {"task" : d['task'] , "time" : d['time'], "ls": datetime.datetime.utcnow()});
            print d['task'] + " with time interval" +" "+ str(d['time']) + " min updated successfully"
                


 
