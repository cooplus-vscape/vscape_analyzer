#coding:utf-8

from sys import path
path.append("../")

from DBatom import *
from globalconfig import *
from pprint import pprint
COOPPLUSDB ='QT-1'
clcl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUT)
vccl, vcclient = getdbhandler(COOPPLUSDB,VCALLSITE+"_4")

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

re = vccl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist_1 = []
contentlist = []
for i in re:
    contentlist_1.append(i["_id"])

for c in contentlist_1:
    fi = {
        "_id": c,
    }
    i = vccl.find_one(fi)

    uvcname = i["interface_classname"]+i["rawmethod"]
    # if uvcname in mytargetdict:
    contentlist.append(i["vmethodid"])
print (len(contentlist))

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

    # print mycount
    fi = {
        "_id": c,
    }
    doc = v2cl.find_one(fi)
    obj = doc["class"]
    for item in obj:
        size = getclasssize(item)
        if size:
            if size >=128 or True:
                #命中
                qualified_base.append((item,size))
    # print qualified_base
    # print obj
    for item,size in qualified_base:
        # print("\n"*8)
        # pprint (obj)
        # print obj[item]
        if type(obj[item]) == type([]):
            if len(obj[item])>1:
                for mv in obj[item][1]:
                    if mv["accesstype"].find("W")!=-1: 
                        offset = mv["accessoffset"]
                        if int(offset)%8 > 1: 
                            vn = mv["variablename"].lower()
                            if vn.find("ptr")==-1: 
                                print "append offset ", offset
                                qualified_counterfeit.append((item,offset))
    
    for item,size in qualified_base:
        pair_dict[item]=[]
        for counterfeit_class,offset in qualified_counterfeit:
            if offset >=size:
                if counterfeit_class not in pair_dict[item]:
                    pair_dict[item].append(counterfeit_class)
                    pair_count=pair_count+1
                    pair_count_in_uvc=pair_count_in_uvc+1
                    print ("hit the:",offset)
                    # print("hit one")
    
    if pair_count_in_uvc >0:
        uvc_count = uvc_count+1


    print("\n")
    
    print("uvc_count:%d / %d"%(uvc_count,mycount))
    print("pair_count:%d"%pair_count)

    
    