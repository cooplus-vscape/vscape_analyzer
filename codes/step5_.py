#coding:utf-8
from globalconfig import *
from DBatom import *


# step5 filter according to access fields

deletecollection(COOPPLUSDB,VMETHOD_TO_AN)
v2cl,v2client = getdbhandler(COOPPLUSDB,VCALLSITE+"_2")
vmcl,vmclient = getdbhandler(COOPPLUSDB,VMETHOD_TO_AN)

mypip = [
    {"$group":{
        "_id":{
            "interface_classname":"$interface_classname",
            "rawmethod":"$rawmethod",
            "classregion":"$classregion",
            "_id":"$_id"
            }
    }}
]
# mypip = [
#     {"$group": {"_id": "$_id"}},
# ]


re = v2cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append([i["_id"]["rawmethod"],i["_id"]["classregion"],i["_id"]["interface_classname"],i["_id"]["_id"]])

    # print i
    # raw_input("-------  ")

tmpre = ""

mycount = 1
for r in contentlist:
    print mycount
    mycount+=1
    tmpdict= {}
    method = r[0]
    cr = r[1]
    for c in cr:
        suc =False
        biaoji = -1
        if len(c)==3:
            if c[2].startswith(" "):
                c[2]=c[2][1:]
            if c[2] == r[2]:
                suc = True
                biaoji = 0
            if not suc:
                for ii in c[2]:
                    if ii[0] == c[2]:

                        biaoji = ii[1]
                        # print "biaoji"+str(biaoji)
                        suc = True
                        break
            if not suc:
                print c[2]
                print r[2]
                print c
                print method
                # print cr
                # raw_input("found one alone")
                tmpdict[c[0]] = c[1]
            if suc:
                tmpdict[c[2]]=biaoji
                tmpdict[c[0]]=c[1]
    waittoan=[method,tmpdict]
    # print r[3]
    waitdict = {
        "method":method,
        "class":tmpdict,
        "class_count":len(tmpdict.keys()),
        "vcallsiteid":r[3],
    }
    # print waittoan
    vmcl.insert(waitdict,check_keys=False)
    
    
    # tmpre = tmpre + str(len(waittoan[1]))
    # print len(waittoan[1])
    # print tmpre
    # raw_input("-------")
print "__end__"




