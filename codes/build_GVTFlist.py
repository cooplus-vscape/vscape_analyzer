#coding:utf-8

from globalconfig import *
from DBatom import *
from math import ceil


deletecollection(COOPPLUSDB, GVTFlist+"_tmp")
vmcl, vmclient = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_af_w")
cl, clclient = getdbhandler(COOPPLUSDB, GVTFlist+"_tmp")


mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]


re = vmcl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])


mycount = 1
for mid in contentlist:
    print mycount
    mycount += 1
    fi = {
        "_id": mid
    }
    doc = vmcl.find_one(fi)

    virtualmethodname=doc["method"]
    classdict=doc["class"]
    indexme = doc["_id"]
    for i in classdict:
        newdoc={}
        newdoc["function_name"] = i+virtualmethodname
        newdoc["index"] = indexme
        cl.insert_one(newdoc,bypass_document_validation=True)
        print "inserted"
        


