import pymongo
import json

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
def view_collectionnames(db):
    for item in myclient[db].list_collection_names():
        print(item)
view_collectionnames("MyBankCardsManagerDB2")
Original = myclient["MyBankCardsManagerDB"]["Original"]
SuperOriginal = myclient["MyBankCardsManagerDB2"]["SuperOriginal"]
# SuperOriginal.drop()
# exit()

with open('original.json') as json_file:
    o = json.load(json_file)
with open('superoriginal.json') as json_file:
    so = json.load(json_file)

# print(type(o[1]))
# inserting the data in the database
# for i in o:
try:
    rec = Original.insert_many(o)
except:
    pass
try:
    rec = SuperOriginal.insert_many(so)
except:
    pass
for i in Original.find():
    print(i)
print("IMPORT DONE ORIGINAL")
for i in SuperOriginal.find():
    print(i)
print("IMPORT DONE SUPERORIGINAL")





