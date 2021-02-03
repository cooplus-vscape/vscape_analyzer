from pymongo import *
from globalconfig import *
from DBatom import *


deletecollection(COOPPLUSDB, INTERFACEWHITELIST_RE)
whitelistcl, whitelistclient = getdbhandler(COOPPLUSDB, INTERFACEWHITELIST)
whitelistclre, whitelistclientre = getdbhandler(
    COOPPLUSDB, INTERFACEWHITELIST_RE)

mypip = [
    {"$group": {"_id": "$interfaceclassname"}},
]

re = whitelistcl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
re = whitelistcl.find({})

contentlist = []
for doc in re:
    tmp = {
        "_id": doc["_id"],
        "interfaceclassname": doc["interfaceclassname"]
    }
    contentlist.append(tmp)

for i in contentlist:
    whitelistclre.insert(i)


whitelistclient.close()
whitelistclientre.close()


print "__end__"
