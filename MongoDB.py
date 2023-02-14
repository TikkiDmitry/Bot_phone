from pymongo import MongoClient
import xlsxwriter

class Database:

        client = MongoClient("mongodb://localhost:27017/")   # Подключение к хосту

        db = client.database

        posts = db.posts                                     # Создание коллекции


        #posts.delete_one({"first_name": ""})               Удаление по фильтру

        #print(posts.find_one()) Вывод одной записи

        a = posts.find()

        # workbook = xlsxwriter.Workbook('database.xlsx')
        # worksheet = workbook.add_worksheet()
        # worksheet.write(f'A{1}', "id")
        # worksheet.write(f'B{1}', "from")
        # worksheet.write(f'C{1}', "first_name")
        # worksheet.write(f'D{1}', "phone_number")
        # worksheet.write(f'E{1}', "date/time")

        print(a)
        print("--------------------------------------Данные в БД ----------------------------------------")
        for k in a:
            print(k)
        # col = 0
        # row = 2
        # for i in a:
        #         print(i)
        #         print(i.values())
        #         for data in enumerate(i.values()):
        #                 for j in data:
        #                         worksheet.write(row, col, str(j))
        #                 col+=1
        #         row+=1
        #         col = 0
        #
        # workbook.close()

