import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://toastapp:arun%40toastapp@cluster0.6eh69.mongodb.net/?retryWrites=true&w=majority")

db = cluster["toastApp"]
menu = db["Menu"]
orders = db["Orders"]
users = db["Users"]