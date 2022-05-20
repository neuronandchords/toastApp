from flask import Flask, render_template, request, url_for, redirect

import pymongo
from pymongo import MongoClient

app = Flask(__name__)

# cluster = MongoClient("mongodb+srv://toastapp:arun%40toastapp@cluster0.6eh69.mongodb.net/?retryWrites=true&w=majority")

# app.config["MONGO_URI"] = "mongodb://localhost:27017/roytuts"
# mongo = PyMongo(app)
connection_url ="mongodb+srv://toastapp:arun%40toastapp@cluster0.6eh69.mongodb.net/?retryWrites=true&w=majority"

client=pymongo.MongoClient(connection_url)
print(client.list_database_names())

# db = connection.test
# names = db.items
# menu = db.menu

# print ('names',names)

@app.route('/', methods=('GET','POST'))
def index():
    collection = db["Menu"]
    return ("hello world!")

@app.route('/addItem', methods=['POST'])
def add_item():
        _json = request.json
        item_id = _json['item_id']
        name = _json['name']
        desc = _json['desc']
        price = _json['price']
        existsOrNot = client.toastApp.items.find_one({"item_id":item_id})
        if(not existsOrNot):
            try:
                insert= client.toastApp.items.insert_one({'item_id': item_id, 'name': name, '': desc, 'price': price})
                print(str(insert))
                return ("Item added")
            except Exception as e:
                return (str(e))
        return ("already exists")

@app.route('/getItem', methods=['GET'])
def view_item():
    items = []
    results = client.toastApp.items.find({})
    for doc in results: 
        items.append(doc)
    return(str(items))

@app.route('/addItem', methods=['POST'])
def add_item_to_menu():
        _json = request.json
        item_id = _json['item_id']
        try:
            insert= client.toastApp.menu.insert_one({'item_id': item_id})
            return ("User created")
        except Exception as e:
            return (str(e))




#working on the orders part, basically maintaing a list of items and stroing it in DB. Please allow me some time to complete this I have a call at 5 after that I'll complete this. 
@app.route('/addOrder', methods=['POST'])
def add_item():
        _json = request.json
        order_id = _json['order_id']
        payment_mode = _json['payment_mode']
        billValue = _json['billValue']
        items = _json['items']
        existsOrNot = client.toastApp.orders.find_one({"item_id":order_id})
        if(not existsOrNot):
            try:
                insert= client.toastApp.items.insert_one({'item_id': item_id, 'name': name, '': desc, 'price': price})
                print(str(insert))
                return ("Item added")
            except Exception as e:
                return (str(e))
        return ("new item")

@app.route('/getItem', methods=['GET'])
def view_item():
    items = []
    results = client.toastApp.items.find({})
    for doc in results: 
        items.append(doc)
    return(str(items))