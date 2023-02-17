from pymongo import MongoClient
import xlsxwriter

class Database:

        client = MongoClient("mongodb://localhost:27017/")

        db = client.database

        posts = db.posts

        a = posts.find()
