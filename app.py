import os
import json
 
from flask import Flask, jsonify
from pymongo import MongoClient                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
from flask import request
from pymongo.errors import ConnectionFailure
 
app = Flask(__name__)

uri ='mongodb+srv://test1:Sam2255@cluster0.lf672.mongodb.net/todo?retryWrites=true&w=majority'

client=MongoClient(uri)
try:
   client.admin.command('ismaster')
except ConnectionFailure:
   print("Server not available")

db = client['todo']
collection = db['tasks']
todo = db.todo


@app.route('/')
def hello_world():
    return 'Welcome to your To-Do list'
 
@app.route("/CreateTask", methods=['POST'])
def insert_document():
    print("inserting document")
    req_data = request.get_json()
    collection.insert_one(req_data).inserted_id
    return ('Task created successfully', 200)
 
@app.route("/FetchAll", methods=['GET'])
def get():
    print("fetching documents")
    documents = collection.find()
    print(format(documents))
    response=tostring(documents)
    return (response)

@app.route("/ByTaskID/<task_id>", methods=['GET'])
def search_document(task_id):
    print("searching document by task_id")
    print(format(task_id))
    documents=collection.find({'task_id':str(task_id)})
    response=tostring(documents)
    print("Printing found document")
    return (response)

@app.route("/ByPriority/<priority>", methods=['GET'])
def query_strings(priority):
    print("searching by query")
    print(format(priority))
    documents=collection.find({'priority':str(priority)})
    response=tostring(documents)
    print("Showing documents with this priority")
    return (response)  

@app.route("/SortByPriority", methods=['GET'])
def sort_by_priority():
    print("sorting documents by priority")
    priority=request.args.get('priority')
    documents=collection.find({'priority':str(priority)})
    response=tostring(documents)
    return (response)  

@app.route("/SortByTask_id", methods=['GET'])
def sort_by_taskID():
    print("sorting documents by taskID")
    task_id=request.args.get('task_id')
    documents=collection.find({'task_id':str(task_id)})
    response=tostring(documents)
    return (response)      

@app.route("/Update/<task_id>", methods=['PATCH'])
def update(task_id):
    print("updating document")
    req_data = request.get_json()
    print("ReqData: "+format(req_data))
    print("Priority: ",req_data['priority'])
    collection.update_one({'task_id':task_id},{'$set':{'priority':req_data['priority']}})
    return ('The task has been updated', 200)
    
@app.route("/Delete/<task_id>", methods=['DELETE'])
def delete(task_id):
    print("deleting document")
    print(format(task_id))
    documents=collection.delete_one({'task_id':str(task_id)})
    return ('The task has been deleted', 200)

def tostring(documents):
    response=[]
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
        print(format(response))
    return jsonify(response)  

if __name__ == '__main__':
    app.run(debug=True, port=5000)
