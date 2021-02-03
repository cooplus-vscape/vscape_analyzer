#coding:utf-8

# from globalconfig import *
# from DBatom import *


# deletecollection(COOPPLUSDB, VMETHOD_TO_AN+"_af_w_bool_mod8")
# vmcl, vmclient = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_af_w_bool_mod8")


# vccl, vcclient = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN +"_af_w")




# mypip = [
#     {"$group": {
#         "_id": "$_id"
#     }}
# ]

# re = vccl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
# contentlist = []
# for i in re:
#     contentlist.append(i["_id"])


# # print contentlist

# def checkwrite(tar):
#     print "-------------"
#     print tar
#     # if
#     if len(tar) > 1:
#         for it in tar[1]:

#             # print it["accesstype"]
           
#             # raw_input("xxxx")
#             if it["accesstype"].find("W") != -1:
#                 vn=it["variablename"]
#                 vn = vn.lower()
#                 if vn.find("bool")!=-1:
#                     offset = int(it["accessoffset"])
#                     yu = offset % 8
#                     if yu >= 4:
#                         if offset>144:
#                             return True

#     return False


# for id in contentlist:
#     fi = {
#         "_id": id,
#     }

#     doc = vccl.find_one(fi)
#     # print doc

#     redict = doc["class"]
#     # newredict = {}
#     foundflag = False
#     interfacename = ""
#     for i in redict.keys():
#         # redict[i]
#         print "\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"
#         print redict[i]
#         print type(redict[i])
#         if type(redict[i]) != type([]):
#             # raw_input("????")
#             if redict[i] == 0:
#                 interfacename = i
#             continue
#         if checkwrite(redict[i]):
#             foundflag = True
#             pass
#         else:
#             del redict[i]
#             pass
#     if not foundflag:
#         pass
#     else:
#         del doc["class"]
#         doc["class"] = redict
#         doc["interfacename"] = interfacename
#         print "inserting. ..."
#         vmcl.insert(doc, check_keys=False)

#         # raw_input("xxxxxxxxxxx")


# print "_end_"






#coding:utf-8

from globalconfig import *
from DBatom import *
from math import ceil


deletecollection(COOPPLUSDB, VMETHOD_TO_AN+"_af_w_bool_mod8")
vmcl, vmclient = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_af_w_bool_mod8")



cl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)



vmcl_w, vmclient_w = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_af_w")


mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = vmcl_w.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])


global affectoffset
global classsizelist

def checkwrite(tar):
    global affectoffset
    print "-------------"
    print tar
    # if
    if len(tar) > 1:
        for it in tar[1]:
            if it["accesstype"].find("W") != -1:
                vn = it["variablename"]
                vn = vn.lower()
                if vn.find("bool") != -1:
                    offset = int(it["accessoffset"])
                    yu = offset % 8
                    if yu >= 1:
                        if offset > 144:
                            affect = it["accessoffset"]
                            affect = int(affect)
                            if (it["classname"], affect) not in affectoffset:
                                affectoffset.append((it["classname"], affect))
                            return True


    return False





for id in contentlist:
    fi = {
        "_id": id,
    }

    doc = vmcl_w.find_one(fi)
    # print doc

    redict = doc["class"]
    # newredict = {}
    foundflag = False
    # interfacename = ""
    affectoffset=[]
    classsizelist=[]

    for i in redict.keys():
        # redict[i]
        print "\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"
        print redict[i]
        print type(redict[i])

        classname=i

        fi = {
            "classname": classname,
        }
        d=cl.find_one(fi)
        sz=d["size"]
        regionsz = int(ceil(sz/16.0))*16
        classsizelist.append((classname,regionsz))


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
        doc["regionsizelist"]=classsizelist

        print "inserting. ..."
        vmcl.insert(doc, check_keys=False)

        # raw_input("xxxxxxxxxxx")


print "_end_"
