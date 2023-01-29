from pymongo import MongoClient


class Database:

        client = MongoClient("mongodb://localhost:27017/")   # Подключение к хосту

        db = client.database

        posts = db.posts                                     # Создание коллекции


        #posts.delete_one({"first_name": ''}) Удаление по фильтру

        #print(posts.find_one()) Вывод одной записи

        a = posts.find()
        print("--------------------------------------Данные в БД ----------------------------------------")
        for i in a:
                print(i)
