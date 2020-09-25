from app import app
from flask import request, jsonify
from database import db
import requests

@app.route('/')
def welcome():
    return {
        "message":'Welcome to the ApIronhack!',
        "available_endpoints":{"/student/create/<student_name>":{"input":"A student's name",
                                                                                "output": "The object ID assigned to that student",
                                                                                "extra" : "If the student is already created, a message will pop up clarifying it."},
                                            "/student/all": {"input" : "No input required",
                                                            "Ouput": "A list with all the students in this bootcamp",
                                                            "extra" : "Id from each student is removed to make the list cleaner"},
                                            "/lab/create/<lab_prefix>":{"input" : "A lab's name",
                                                                                "Ouput": "The object ID assigned to that student",
                                                                                "extra" : "If the student is already created, a message will pop up clarifying it."},
                                            "/lab/<lab_prefix>/search":{"input" : "A lab's name",
                                                                        "Ouput": "Lab analysis",
                                                                        "extra" : "Error 404 : List of distinct memes was not found"},
                                            "/lab/randomeme/<lab_prefix>":{"input" : "A lab's name",
                                                                            "Ouput": "A random meme URL from that specific lab",
                                                                            "extra" : "No Id included for cleaner output"}

                                                    }
                               

                                                    }

def user_already_in_db(collection, username):
    """
    This function checks if the inserted user is already stored in the database, in that case, 
    it will let you know with a message.
    """
    result = collection.find_one({"name": username})
    return result is not None and len(result) > 0


def insert_student(collection, name):
    """
    This function inserts the specified student in the mongo database.
    """
    new_student = {
        "name": name
    }

    result = collection.insert_one(new_student)
    return {"_id": str(result.inserted_id)}


@app.route("/student/create/<student_name>")
def create_student(student_name):
    '''
    This function receives a student name and creates a new entry in our database, returning the
    student id 
    It also validates if it exists in github and if it is created already in our DB
    '''
    collection = db.users

    if user_already_in_db(collection, student_name):
        return f"{student_name} ya existe en la base de datos."
    else:
        return insert_student(collection, student_name)

    return "No se ha guardado el alumno en la base de datos. Problema desconocido"

@app.route("/student/all")
def search_students():
    '''
    This function returns a json with all the student names in our db.
    '''
    collection = db.users

    # El campo _id es un objeto y no podemos convertirlo a json, por lo que lo quitamos
    cursor = collection.find({}, {'_id': False})

    return(jsonify(list(cursor)))

    