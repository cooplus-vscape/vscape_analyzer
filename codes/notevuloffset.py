
from globalconfig import *
from DBatom import *
from math import ceil






cl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)
bcl, bclclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW+"_stringrelate")


abcl, abclclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW+"_stringrelate_all")
scl, sclclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW+"_stringclass")
mypip = [
    {"$group": {
        "_id": "$classname"
    }}
]

re = scl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
stringclslist = []

for i in re:
    stringclslist.append(i["_id"])


stringclslist.append("char")


mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re =bcl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)

idlist = []
for i in re:
    idlist.append(i["_id"])





def collect_vuloffset(doc):
    vulofflist=[]
    for item in doc["variablelist"]:
        if item["typename"] in stringclslist:
            vulofflist.append(item["offset"])
    return vulofflist


def insertchilds(namelist,doc):

    # for item in doc:
    if len(namelist) ==0:
        # if bcl.find_one()
        return
    else:
        for it in namelist:
            fi = {
                "classname": it,
            }
            d = abcl.find_one(fi)
            parent = doc["classname"]
            for i in d["baseclasslist"]:
                if i["baseclassname"] ==parent:
                    boff=i["offset"]
            vulofflist = []
            for x in doc["vulofflist"]:
                vulofflist.append(x+boff)
            d["vulofflist"]=vulofflist
            # regionsize 
            sz = d["size"]
            if sz <= 1280:
                regionsize = int(ceil(sz/16.0))*16
            else:
                regionsize = -1
            d["regionsize"]=regionsize

            up = {
                "$set":
                {
                    "vulofflist": vulofflist,
                    "regionsize": regionsize,
                    "raw_origin": 0,
                },
            }
            abcl.update_one(fi, up)

            if d.has_key("child"):
                insertchilds(d["child"],d)

            else:
                pass


cc = 0
for id in idlist:
    cc+=1
    if cc %100==0:
        print cc
    fi = {
        "_id": id,
    }

    doc = bcl.find_one(fi)


    vulofflist=collect_vuloffset(doc)
    sz=doc["size"] 
    if sz<=1280:
        regionsize=int(ceil(sz/16.0))*16
    else:
        regionsize = -1

        
    doc["vulofflist"] = vulofflist
    up = {
        "$set":
        {
            "vulofflist": vulofflist,
            "regionsize": regionsize,
            "raw_origin":1,
        },
    }
    abcl.update_one(fi,up)



    if doc.has_key("child"):
        insertchilds(doc["child"],doc)
