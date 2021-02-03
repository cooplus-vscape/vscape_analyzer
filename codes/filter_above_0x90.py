#coding:utf-8
from globalconfig import *
from DBatom import *

deletecollection(COOPPLUSDB, VCALLSITE+"_0x90")


vc4cl, vc4client = getdbhandler(COOPPLUSDB, VCALLSITE+"_4")
vc5cl, vc5client = getdbhandler(COOPPLUSDB, VCALLSITE+"_0x90")


clcl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)


mypip = [
    {"$group": {
        "_id": "$interface_classname"
    }}
]

re = vc4cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])


mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = vc4cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
idlist = []
for i in re:
    idlist.append(i["_id"])

mycount = 1

relist=[]
print len(contentlist)
for mid in contentlist:
    # print mycount
    mycount += 1
    fi = {
        "classname": mid
    }
    doc = clcl.find_one(fi)
    sz = doc["size"]
    if sz >= 0x90:
        relist.append(mid)

mycount = 1
for i in idlist:
    mycount += 1
    fi = {
        "_id":i,
    }
    doc=vc4cl.find_one(fi)
    # print doc
    if doc["interface_classname"] in relist:
        vc5cl.insert(doc, check_keys=False)

print "_end_"
