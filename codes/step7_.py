#coding:utf-8
from globalconfig import *
from DBatom import *

deletecollection(COOPPLUSDB, VMETHOD_TO_AN+"_2")
v2cl,v2client = getdbhandler(COOPPLUSDB,VCALLSITE+"_2")

vm1cl, vm1client = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_1")

vm2cl, vm2client = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_2")
vfcl, vfclient = getdbhandler(COOPPLUSDB, VIRTUALFUNCTION+"_2")
clcl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)


mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = vm1cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])


def find_parent(doc,item):
    classtree = doc["classtree"]


    # print doc
    # print classtree
    # raw_input("<<<<<<,")

    for i in classtree:
        if type(classtree[i]) is not list:
            continue
        if classtree[i].count(item)>0:
            return i
            # break


def checkbaseoffset(sub,bse):
    fi = {
        "classname":sub,
    }
    doc=clcl.find_one(fi)
    bcl=doc["baseclasslist"]
    for bc in bcl:
        if bc["baseclassname"]==base:
            return bc["offset"]
    return -1

def getaccesslist(classsname,auxiliaryfunction):
    fi = {
        "itself":classsname,
        "methodname":auxiliaryfunction,
    }
    doc=vfcl.find_one(fi)
    return doc["accesslist"]
def getclasssize(classname):
    fi = {
        "classname":classname,
    }
    doc = clcl.find_one(fi)
    return doc["size"] 

def checkGVTF(sub,base,auxiliaryfunction):
    baseoffset = checkbaseoffset(sub,base)
    basesize = getclasssize(base)
    if baseoffset==-1:
        return -1
    accesslist = getaccesslist(sub,auxiliaryfunction)
    GVTFlist =[]
    for item in accesslist:
        accessoffset = item["accessoffset"]
        accessoffset = int(accessoffset)
        related_offset = accessoffset - baseoffset
        if related_offset >= basesize:
            GVTFlist.append(item)

    if len(GVTFlist)>0:
        return GVTFlist
    else:
        return False

def getparentcolor(doc,classname):
    parentname=find_parent(doc,classname)
    # print classname
    # print parentname
    # print doc["classregion"]
    # raw_input(">>>>>>>>>")
    l=doc["classregion"]
    for i in l:
        if i[0] == parentname:
            return i[1]
    return -1



mycount = 1

for c in contentlist:
    print mycount
    mycount+=1
    fi = {
        "_id":c,
    }
    doc = vm1cl.find_one(fi)
    objid = doc["vcallsiteid"]
    # print fi
    # print doc
    # print objid
    # raw_input("xxxx")
    d = v2cl.find_one({
        "_id":objid,
    })
    tar = doc["class"]
    for t in tar:
        if tar[t]==0:
            continue
        base = find_parent(d,t)
        re = checkGVTF(t,base,doc["method"].split("::")[-1])
        if not re:
            tar[t]=[getparentcolor(d,t)+0.5]
        else:
            GVFlist = re
            tar[t]=[tar[t],GVFlist]
    del doc["class"]
    doc["class"] = tar
    vm2cl.insert(doc,check_keys=False)


        



# ones = vmcl1.find({})

# mycount = 1
# for one in ones:
#     print mycount
#     mycount += 1
#     m = one["method"].split("::")[-1]

#     for cn in one["class"]:
#         fi = {
#             "itself": cn,
#             "methodname": m,
#         }
#         print fi
#         doc = vfcl.find_one(fi)
#         # print doc
#         if len(doc["accesslist"]) > 0:
#             del doc["_id"]
#             print one
#             vmcl1.insert(one, check_keys=False)
#             break
print "_end_"
