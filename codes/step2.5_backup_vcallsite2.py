from pymongo import *
from globalconfig import *
from DBatom import *


# vcallsitecl, vcallsiteclient = getdbhandler(COOPPLUSDB, VCALLSITE)
deletecollection(COOPPLUSDB, VCALLSITE+"_2_bak")

v2cl,v2client = getdbhandler(COOPPLUSDB,VCALLSITE+"_2")
v2bcl,v2bclient = getdbhandler(COOPPLUSDB,VCALLSITE+"_2_bak")




mypip = [
    {"$group": {"_id": "$_id"}},
]

re = v2cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)


contentlist = []
for doc in re:
    tmp = doc["_id"]
    contentlist.append(tmp)

for i in contentlist:
    fi = {
        "_id":i,
    }
    tmp = v2cl.find_one(fi)
    v2bcl.insert(tmp,check_keys=False)


v2client.close()
v2bclient.close()


print "__end__"
