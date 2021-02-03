#coding:utf-8




from globalconfig import *

from config import *
import pymongo


def getdbhandler(dbname, collectionname):
    client = pymongo.MongoClient(connection_string)
    db = client[dbname]
    cl = db[collectionname]
    return cl,client


def dropdatabase(dbname):
    client = pymongo.MongoClient(connection_string)
    client.drop_database(dbname)
    
    

def deletecollection(dbname,collectionname):
    client = pymongo.MongoClient(connection_string)
    db = client[dbname]
    db.drop_collection(collectionname)
    # cl = db[collectionname]
    

def createDB(dbname):
    print connection_string
    client = pymongo.MongoClient(connection_string)
    # c = pymongo.MongoClient("mongodb: // localhost: 27017")
    db = client[dbname]
    client.close()


def insertONEinMongo(dbname, collectionname, insertdict):
    client = pymongo.MongoClient(connection_string)
    db = client[dbname]
    cl = db[collectionname]
    cl.insert_one(insertdict)
    client.close()


def findinMongo(dbname, collectionname, checksentence):
    print connection_string

    client = pymongo.MongoClient(connection_string)
    db = client[dbname]
    cl = db[collectionname]
    client.close()
    return cl.find(checksentence)


def updateinMongo(dbname, collectionname, findsentence, newsentence):
    print connection_string

    client = pymongo.MongoClient(connection_string)
    db = client[dbname]
    cl = db[collectionname]
    cl.update_one(findsentence, newsentence)
    client.close()
    return True


if __name__ == "__main__":
    createDB("ckxtest")
