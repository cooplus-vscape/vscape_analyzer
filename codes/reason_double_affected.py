#coding:utf-8

from globalconfig import *
from DBatom import *
from math import ceil


deletecollection(COOPPLUSDB, VMETHOD_TO_AN+"_af_w_double_reason")
vmcl, vmclient = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_af_w_double_reason")
cl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)

# deletecollection(COOPPLUSDB, VCALLSITE+"_af_w_double_reason")


vmcl_w, vmclient_w = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_af_w_double")


mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = vmcl_w.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])

for id in contentlist:
    fi = {
        "_id": id,
    }
    targetoffs=[]
    doc = vmcl_w.find_one(fi)
    # print doc
    rl = doc["regionsizelist"]
    aset = doc["affectoffset"]
    for r in rl:
        for a in aset:
            if r[1]>=a[1]:
                continue
            toff=a[1]%r[1]
            toffunit = (toff,r[1],r[0],a[0],doc["interfacename"],doc["method"])
            targetoffs.append(toffunit)
    doc["targetoffs"] = targetoffs
            


    print "inserting. ..."
    vmcl.insert(doc, check_keys=False)

        # raw_input("xxxxxxxxxxx")


print "_end_"
