#coding:utf-8
from globalconfig import *
from DBatom import *

global allbasetype

deletecollection(COOPPLUSDB, VIRTUALFUNCTION+"_2")

vfcl, vfclient = getdbhandler(COOPPLUSDB, VIRTUALFUNCTION)

vf2cl, vf2client = getdbhandler(COOPPLUSDB, VIRTUALFUNCTION+"_2")

clraw, client = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)

mypip = [
    {"$group": {"_id": "$_id"}},
]

re = vfcl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)


contentlist = []
for i in re:
    contentlist.append(i["_id"])



def addtobasetype(tc):
    global allbasetype
    allbasetype.append(tc)
    sc = {
        "classname": tc,
    }
    ddoc = clraw.find_one(sc)
    # print ddoc
    if ddoc is not None:
        for item in ddoc["baseclasslist"]:
            # print item
            bname = item["baseclassname"]
            # print bname
            # allbasetype.append(bname)
            addtobasetype(bname)
            


def check_base(cs):
    if cs in allbasetype:
        return True
    return False

for myid in contentlist:
    sc = {
        "_id": myid,
    }
    doc=vfcl.find_one(sc)
    newdoc=doc
    itselfname = doc["itself"]
    allbasetype = []
    addtobasetype(itselfname)
    new_aclist = []
    delete_offset_list=[]

    sc = {
        "classname": itselfname,
    }
    thislayout = clraw.find_one(sc)
    if thislayout is None:
        continue
    # print "xxxxxxxxxxxxxxxxxxx"
    # print itselfname
    # print thislayout
    thissize=thislayout["size"]

    for item in doc["accesslist"]:
        if int(item["accessoffset"])>thissize:
            delete_offset_list.append(item["accessoffset"])
            # if item["parentfield"] !="NULL":
            #     re=check_base(item["parentfield"])
            #     if (not re):
    
    
    for item in doc["accesslist"]:
        if item["accessoffset"] in delete_offset_list:
            pass
        else:
            new_aclist.append(item)

    del newdoc["accesslist"]
    newdoc["accesslist"] = new_aclist
    vf2cl.insert_one(newdoc, bypass_document_validation=True)



    # sc = {
    #     "classname": itselfname,
    # }


    # ddoc=clraw.find_one(sc)
    # baseclasslist=ddoc['baseclasslist']
    # for item in baseclasslist:


