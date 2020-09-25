from app import app
from flask import request, jsonify
from database import db
import requests
from bson.json_util import dumps
import random
import pymongo
from datetime import datetime

def lab_already_in_db(collection, lab_prefix):
    result = collection.find_one({"Lab": lab_prefix})
    return result is not None and len(result) > 0

def insert_lab(collection, lab_prefix):
    new_lab = {
        "Lab": lab_prefix
    }

    result = collection.insert_one(new_lab)
    return {"_id": str(result.inserted_id)}

@app.route("/lab/create/<lab_prefix>")
def create_lab(lab_prefix):
    """
    This function creates a specified lab in our database, and it returns 
    the object id of the lab.
    """
    collection = db.labs
    
    if lab_already_in_db(collection,lab_prefix):
        return f"{lab_prefix} ya existe en la base de datos."
    else:
        return insert_lab(collection,lab_prefix)
    
    return "No se ha guardado el lab en la base de datos. Problema desconocido"
    

@app.route("/lab/<lab_prefix>/search")
def searchLab(lab_prefix):
    """
    Purpose: Search student submissions on specific lab
    Params: lab_prefix
    Returns: Number of open PR
            Number of closed PR
            Percentage of completeness (closed vs open)
            List number of missing pr from students
            The list of unique memes used for that lab
            Instructor grade time in hours: (pr_close_time-last_commit_time)
"""
        
    
    opened_pr=db.pulls.find({"$and":[{"Lab":lab_prefix},{"State": "open"}]}).count()
    closed_pr=db.pulls.find({"$and":[{"Lab":lab_prefix},{"State": "closed"}]}).count()
    percentage=round(closed_pr/(opened_pr+closed_pr)*100,2)

    totalpr = db.pulls.find({"$and":[{"Lab":lab_prefix}]}).count()
    totalusers = db.users.find().count()
    missing_pr= abs(totalpr - totalusers)
    
    #memes=list(db.labs.find({"$and":[{"Lab":lab_prefix},{"Meme":{"$nin":["null"]}}]}))   
    #projection = {"_id":0,'Meme':1}
    #memes = list(db.pulls.find({"Lab": lab_prefix}, projection))
    
    projection = {'Instructor':1,'_id':0, 'Creado':1, 'Cerrada':1}
    for x in db.pulls.find({'$and':[ {'Lab':lab_prefix} , {'State':'closed'} ]},projection):
        close_time = datetime.strptime(x.get('Cerrada'), "%Y-%m-%dT%H:%M:%SZ")
        open_time = datetime.strptime(x.get('Creado'), "%Y-%m-%dT%H:%M:%SZ")
        queue_time = (close_time-open_time).total_seconds()/3600
        
        
    
    
    result={'-The number of opened PR is': opened_pr,
    '-The number of closed PR is': closed_pr,
    'The percentage of completeness is': percentage,
    'Number of missing PR is': missing_pr,
    'The instructor grade time in hours is': queue_time
    
    }
  
    return dumps(result)


@app.route("/lab/randomeme/<lab_prefix>")
def random_meme(lab_prefix):
    result=db.pulls.aggregate([
        { "$match":  {"Lab": lab_prefix} },
        { "$sample": {"size": 1} },
        { "$project" : { "Meme" : 1, "_id": 0}}
      ])
    return dumps(result)    