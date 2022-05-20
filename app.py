from flask import Flask, render_template, request, url_for, redirect
from flask import Response
import json

import pymongo
from pymongo import MongoClient
from flask import jsonify

app = Flask(__name__)
connection_url ="mongodb+srv://toastapp:arun%40toastapp@cluster0.6eh69.mongodb.net/?retryWrites=true&w=majority"

client=pymongo.MongoClient(connection_url)
print(client.list_database_names())

@app.route('/', methods=('GET','POST'))
def index():
    return ("hello arun welcome to toastApp!")

#MENU OPERATIONS 

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
        return ("item ID already exists")

@app.route('/getMenu', methods=['GET'])
def view_items():
    items = []
    results = client.toastApp.items.find({}, {'_id': 0})
    for doc in results : 
        items.append(doc)
    print(items)
    return Response(json.dumps(items),  mimetype='application/json')

@app.route('/deleteItem', methods=['POST'])
def delete_item():
        _json = request.json
        item_id = _json['item_id']
        query={'item_id':item_id}
        existsOrNot = client.toastApp.items.find_one({"item_id":item_id})
        print(existsOrNot)
        if(existsOrNot is not None):
            try:
                delete= client.toastApp.items.delete_one({'item_id': item_id})
                return ("Item deleted")
            except:
                return ("Some error occured in deleting item")
        return ("Item does not exist")

@app.route('/updateItem', methods=['POST'])
def update_item():
        _json = request.json
        item_id = _json['item_id']
        name = _json['name']
        price = _json['price']
        desc = _json['desc']
        filter = {'item_id': item_id}
        newValues = { "$set": {'name': name, 'price': price, 'desc': desc}}
        print(filter, newValues)
        existsOrNot = client.toastApp.items.find_one({'item_id':item_id})
        if(existsOrNot is not None):
            try:
                insert= client.toastApp.items.update_one(filter, newValues)
                return ("Item updated")
            except Exception as e:
                return (str(e))
        return ("Item not found")

#ORDER OPERATIONS 

@app.route('/addOrder', methods=['POST'])
def add_order():
        _json = request.json
        order_id = _json['order_id']
        payment_mode = _json['payment_mode']
        items = _json['items']
        user_id = ''
        try:
            user_id = _json['user_id']
        except:
            user_id = -1
        bill =0
        existsOrNot = client.toastApp.orders.find_one({"order_id":order_id})
        if(not existsOrNot):
            for item in items:
                priceItem = client.toastApp.items.find_one({"item_id":item})
                bill+=priceItem['price']
                if user_id != -1:
                    bill = bill - (0.10 * bill)  # 10% discount for already existing user
                order = client.toastApp.orders.insert_one({'order_id': order_id, 'payment_mode': payment_mode, 'items': items, 'user_id': user_id, 'bill': bill})
                print(order)
                return ("order created")
        return ("order ID already exists")


@app.route('/getOrders', methods=['GET'])
def view_orders():
        items = []
        results = client.toastApp.orders.find({}, {'_id': 0})
        for doc in results: 
            items.append(doc)
        return Response(json.dumps(items),  mimetype='application/json')

@app.route('/deleteOrder', methods=['POST'])
def delete_order():
        _json = request.json
        order_id = _json['order_id']
        query={'order_id':order_id}
        existsOrNot = client.toastApp.orders.find_one({"order_id":order_id})
        print(existsOrNot)
        if(existsOrNot is not None):
            try:
                delete= client.toastApp.orders.delete_one({'order_id': order_id})
                return ("Order deleted")
            except:
                return ("Some error occured in deleting order")
        return ("Order does not exist")

@app.route('/updateOrder', methods=['POST'])
def update_order():
        _json = request.json
        order_id = _json['order_id']
        payment_mode = _json['payment_mode']
        items = _json['items']
        user_id = ''
        try:
            user_id= _json['user_id']
        except:
            user_id = -1
        filter = {'order_id': order_id}
        newValues = { "$set": {'payment_mode': payment_mode, 'items': items, 'user_id': user_id}}
        print(filter, newValues)
        existsOrNot = client.toastApp.orders.find_one({'order_id':order_id})
        if(existsOrNot is not None):
            try:
                insert= client.toastApp.orders.update_one(filter, newValues)
                return ("Order updated")
            except Exception as e:
                return (str(e))
        return ("Order not found")


#USER OPERATIONS:


@app.route('/addUser', methods=['POST'])
def add_user():
        _json = request.json
        user_id = _json['user_id']
        name = _json['name']
        email = _json['email']
        phone = _json['phone']
        existsOrNot = client.toastApp.users.find_one({"email":email})
        if(not existsOrNot):
            try:
                insert= client.toastApp.users.insert_one({'user_id': user_id, 'name': name, 'email': email, 'phone': phone})
                return ("User created")
            except Exception as e:
                return (str(e))
        return ("User already exists")

@app.route('/getUsers', methods=['GET'])
def view_users():
        items = []
        results = client.toastApp.users.find({}, {'_id': 0})
        for doc in results: 
            items.append(doc)
        return Response (json.dumps(items),  mimetype='application/json')

@app.route('/deleteUser', methods=['POST'])
def delete_users():
        _json = request.json
        user_id = _json['user_id']
        query={'user_id':user_id}
        existsOrNot = client.toastApp.users.find_one({"user_id":user_id})
        print(existsOrNot)
        if(existsOrNot is not None):
            try:
                delete= client.toastApp.users.delete_one({'user_id': user_id})
                return ("User deleted")
            except:
                return ("Some error occured in deleting user")
        return ("User does not exist")

@app.route('/updateUser', methods=['POST'])
def update_user():
        _json = request.json
        user_id = _json['user_id']
        name = _json['name']
        email = _json['email']
        phone = _json['phone']
        filter = {'user_id': user_id}
        newValues = { "$set": {'name': name, 'email': email, 'phone': phone}}
        print(filter, newValues)
        existsOrNot = client.toastApp.users.find_one({'user_id':user_id})
        if(existsOrNot is not None):
            try:
                insert= client.toastApp.users.update_one(filter, newValues)
                return ("User updated")
            except Exception as e:
                return (str(e))
        return ("User not found")

