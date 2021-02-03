#coding:utf-8
from sys import path
path.append("../")

from DBatom import *
from globalconfig import *
from pprint import pprint

clcl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUT)
def getclasssize(classname):
    fi = {
        "classname":classname,
    }
    doc = clcl.find_one(fi)
    if doc.__contains__("size"):
        return doc["size"]
    else:
        return None

v2cl, v2client = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_3")


mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = v2cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])


allnum=0
loglist =[]
mycount=0
pair_count = 0
pair_count_in_uvc = 0
uvc_count = 0


for c in contentlist:
    pair_dict= {}
    qualified_base = []
    qualified_counterfeit = []
    pair_count_in_uvc = 0
    mycount += 1
    fi = {
        "_id": c,
    }
    doc = v2cl.find_one(fi)
    obj = doc["class"]
    for item in obj:
        size = getclasssize(item)
        if size:
            if size >=128:
                qualified_base.append((item,size))
    for item,size in qualified_base:
        if type(obj[item]) == type([]):
            if len(obj[item])>1:
                for mv in obj[item][1]:
                    if mv["accesstype"].find("W")!=-1: # Write COND
                        offset = mv["accessoffset"] 
                        vn = mv["variablename"].lower()
                        if vn.find("ptr")==-1: # NonPtr COND
                            qualified_counterfeit.append((item,offset))
    
    for item,size in qualified_base:
        pair_dict[item]=[]
        for counterfeit_class,offset in qualified_base:
            if offset >=size:
                if counterfeit_class not in pair_dict[item]:
                    pair_dict[item].append(counterfeit_class)
                    pair_count=pair_count+1
                    pair_count_in_uvc=pair_count_in_uvc+1
                    # print("hit one")
    
    if pair_count_in_uvc >0:
        uvc_count = uvc_count+1


    print("\n")
    
    print("uvc_count:%d / %d"%(uvc_count,mycount))
    print("pair_count:%d"%pair_count)

    
    


    # print obj






