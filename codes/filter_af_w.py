#coding:utf-8

from globalconfig import *
from DBatom import *



deletecollection(COOPPLUSDB, VMETHOD_TO_AN+"_af_w")
vmcl, vmclient = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_af_w")


deletecollection(COOPPLUSDB, VCALLSITE+"_af_w")



vccl, vcclient = getdbhandler(COOPPLUSDB, VCALLSITE+"_af_w")


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
    if len(tar)>1:
        for it in tar[1]:

            print it["accesstype"]
            # raw_input("xxxx")
            if it["accesstype"].find("W")!=-1:
                # raw_input("====")
                offset = int(it["accessoffset"])

                return True

    return False
        



for id in contentlist:
    fi = {
        "_id": id,
    }

    doc = vmcl3.find_one(fi)
    # print doc


    redict=doc["class"]
    # newredict = {}
    foundflag = False
    interfacename = ""
    for i in redict.keys():
        # redict[i]
        print "\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"
        print redict[i]
        print type(redict[i])
        if type(redict[i])!=type([]):
            # raw_input("????")
            if redict[i] == 0:
                interfacename = i
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
        doc["interfacename"] = interfacename
        print "inserting. ..."
        vmcl.insert(doc,check_keys=False)

        # raw_input("xxxxxxxxxxx")
        




print "_end_"
