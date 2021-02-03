#coding:utf-8

from globalconfig import *
from DBatom import *
from math import ceil

deletecollection(COOPPLUSDB, VMETHOD_TO_AN+"_af_string_ptr_cs")
vmcl, vmclient = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_af_string_ptr_cs")


cl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)




vmcl3, vmclient3 = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_3")


mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = vmcl3.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])


# print contentlist

def checkwrite(tar):
    print "-------------"
    print tar
    # if
    if len(tar) > 1:
        for it in tar[1]:

            print it["accesstype"]
            vn=it["variablename"]
            vn = vn.lower()
            if vn.find("string")!=-1:
            
                return True

    return False


for id in contentlist:
    fi = {
        "_id": id,
    }

    doc = vmcl3.find_one(fi)
    # print doc

    redict = doc["class"]
    # newredict = {}
    foundflag = False
    # interfacename = ""
    affectoffset = []
    classsizelist = []

    for i in redict.keys():
        # redict[i]
        print "\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"
        print redict[i]
        print type(redict[i])

        classname = i

        fi = {
            "classname": classname,
        }
        d = cl.find_one(fi)
        sz = d["size"]
        regionsz = int(ceil(sz/16.0))*16
        classsizelist.append((classname, regionsz))

        if type(redict[i]) != type([]):
            # raw_input("????")
            if redict[i] == 0:
                # interfacename = i
                pass
            continue
        if checkwrite(redict[i]):
            foundflag = True
            pass
        else:
            del redict[i]
            pass
    if not foundflag:
        pass
    else:
        del doc["class"]
        doc["class"] = redict
        doc["affectoffset"] = affectoffset
        doc["regionsizelist"] = classsizelist

        print "inserting. ..."
        vmcl.insert(doc, check_keys=False)

        # raw_input("xxxxxxxxxxx")


print "_end_"
