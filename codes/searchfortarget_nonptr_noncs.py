
from globalconfig import *
from DBatom import *


deletecollection(COOPPLUSDB, CLASSLAYOUTRAW+"_base_c_s")
cl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)
bcl, bclclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW+"_base_c_s")


mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []

for i in re:
    contentlist.append(i["_id"])



def check(me):
    if len(me["baseclasslist"])>0:
        return False
    if len(me["variablelist"])==0:
        return False
    for item in me["variablelist"]:
        if item["vtype"]=="c/s" or item["vtype"]=="ptr":
            return False
        
    return True

ii = 0
for id in contentlist:
    ii+=1
    if ii%10000==0:
        print ii

    fi = {
        "_id": id,
    }

    doc = cl.find_one(fi)

    if not check(doc):
        continue
    else:
        bcl.insert(doc,check_keys=False)

print "===end=="





