
from globalconfig import *
from DBatom import *
from math import ceil


deletecollection(COOPPLUSDB, INTERFACEWHITELIST+"_mozilla_only")
iwcl, iwclient = getdbhandler(COOPPLUSDB, INTERFACEWHITELIST)
cl, clclient = getdbhandler(COOPPLUSDB, INTERFACEWHITELIST+"_mozilla_only")



mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = iwcl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])


for x in contentlist:
    fi = {
        "_id": x,
    }
    doc = iwcl.find_one(fi)
    ifn= doc["interfaceclassname"]
    if ifn.find("mozilla::dom")!=-1:
        cl.insert(doc,check_keys=False)
    
    # print doc

