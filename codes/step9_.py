#coding:utf-8
from globalconfig import *
from DBatom import *

deletecollection(COOPPLUSDB,VCALLSITE+"_4")
vc4cl, vc4client = getdbhandler(COOPPLUSDB, VCALLSITE+"_4")
vc3cl,vc3client = getdbhandler(COOPPLUSDB,VCALLSITE+"_3")


mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = vc3cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])

import math

def nCr(n,r):
    f = math.factorial
    return f(n) / f(r) / f(n-r)


mycount =1
for mid in contentlist:
    print mycount
    mycount+=1
    fi = {
        "_id":mid
    }
    doc=vc3cl.find_one(fi)

    mydict=doc["colordict"]
    if len(mydict)>1:
        colornum = len(mydict)
        doc["colorcount"] = colornum
        doc["paircount"]=nCr(colornum,2)
        vc4cl.insert(doc,check_keys= False)

print "_end_"


