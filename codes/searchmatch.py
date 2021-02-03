
from globalconfig import *
from DBatom import *
from math import ceil
import IPython


gf, gfclient = getdbhandler(COOPPLUSDB, GVTFlist)
abcl, abclclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW+"_stringrelate_all")

mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = abcl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []

for i in re:
    contentlist.append(i["_id"])




mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

def search_anwser(regionsize,vulofflist):
    result = []
    for i in vulofflist:
        ree=[]
        fi ={
            "regionsize":regionsize,
            "affectoffset":i,
        }
        re=gf.find(fi)
        # print "before appending ....."
        for it in re:
            # print "appending ....."
            # print it
            ree.append(it)
        if len(ree)>0:
            result.append([i,ree])
        else:
            print "not solve!"
            continue
        # IPython.embed()
    return result


cc = 0
for id in contentlist:
    cc += 1
    if cc % 100 == 0:
        print cc
    fi = {
        "_id": id,
    }

    doc = abcl.find_one(fi)

    rsz=doc["regionsize"]
    vulofflist=doc["vulofflist"]

    pott_gvtf = search_anwser(rsz,vulofflist)
    doc["pott_gvtf"] = pott_gvtf
    if len(pott_gvtf)!=0:
        flagme = True
    else:
        flagme = False

    up = {
        "$set":
        {
            "pott_gbtf": pott_gvtf,
            "is_solvable": flagme,
        },
    }
    abcl.update_one(fi, up)

