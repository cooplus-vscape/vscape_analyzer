
from globalconfig import *
from DBatom import *
from math import ceil


deletecollection(COOPPLUSDB, VCALLSITE+"_mozilla_only")
iwcl, iwclient = getdbhandler(COOPPLUSDB, VCALLSITE+"_4")
cl, clclient = getdbhandler(COOPPLUSDB, VCALLSITE+"_mozilla_only")


deletecollection(COOPPLUSDB, VMETHOD_TO_AN+"_mozilla_only")
vmcl, vmclclient = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_mozilla_only")
vm3cl, vm3clclient = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_3")

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
    ifn = doc["interface_classname"]
    tiaojian2=len(doc["colordict"].keys())>=2
    if ifn.find("mozilla::dom") != -1  and tiaojian2:
        cl.insert(doc, check_keys=False)

    # print doc








re = cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])


for x in contentlist:
    fi = {
        "_id": x,
    }
    doc=cl.find_one(fi)
    vmethodid=doc["vmethodid"]
    fi ={
        "_id":vmethodid
    }
    doc=vm3cl.find_one(fi)
    vmcl.insert(doc,check_keys=False)
    
