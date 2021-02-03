#coding:utf-8

from globalconfig import *
from DBatom import *
from math import ceil

# GVTFlist 
deletecollection(COOPPLUSDB, GVTFlist)


vmcl, vmclient = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_af_w_double_reason")
cl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)

gf,gfclient = getdbhandler(COOPPLUSDB,GVTFlist)

mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = vmcl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []

for i in re:
    contentlist.append(i["_id"])
allre = []

for id in contentlist:
    fi = {
        "_id": id,
    }
    targetoffs = []
    doc = vmcl.find_one(fi)
    # print doc
    toffs = doc["targetoffs"]
    for i in toffs:
        allre.append(i)


def takeSecond(elem):
    return elem[1]

allre.sort(key=takeSecond)

ime = {"allre":allre}


for i in allre:
    mydict={}
    mydict["regionsize"] = i[1]
    mydict["affectoffset"]=i[0]
    mydict["GVTF_orgin"]=i[2]
    mydict["GVTF_overlap"]=i[3]
    mydict["interfacename"]=i[4]


    gf.insert(mydict,check_keys=False)



print "_end_"
