#coding:utf-8
from globalconfig import *
from DBatom import *
v2cl,v2client = getdbhandler(COOPPLUSDB,VCALLSITE+"_2")
wlcl,wlclient = getdbhandler(COOPPLUSDB,INTERFACEWHITELIST)



mypip = [
    {"$group": {"_id": "$interface_classname"}},
]



re = v2cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])


    
for icn in contentlist:

    fi = {
        "interfaceclassname":icn,
    }
    doc = wlcl.find_one(fi)

    fi = {
        "interface_classname": icn,
    }
    relists = v2cl.find(fi)

    objidlist = []
    for r in relists:

        objidlist.append(r["_id"])



    for objid in objidlist:

        fii ={
            "_id":objid,
        }
        up ={
            "$set":{
                "classtree":doc,#不知道能否插入集合
            }
        }

        v2cl.update_one(fii,up)
        # raw_input("stop me....")

v2client.close()
wlclient.close()
print "_end_"

