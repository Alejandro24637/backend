from pymongo import MongoClient


# base de datos local
#db_client = MongoClient().local

# base de datos remota 
db_client = MongoClient(
    "mongodb+srv://diego:diego@cluster0.dwddyj4.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0").diego