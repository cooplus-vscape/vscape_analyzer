#coding:utf-8
from globalconfig import *
from DBatom import *


deletecollection(COOPPLUSDB,  VMETHOD_TO_AN+"_3")

vm2cl, vm2client = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_2")
vm3cl, vm3client = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_3")

clcl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)

mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = vm2cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])

print len(contentlist)
mycount = 1
for mid in contentlist:
    print mycount
    mycount += 1
    fi = {
        "_id": mid
    }
    doc = vm2cl.find_one(fi)
    # print doc


# re = vm2cl.find({})

# mycount =1
# for i in re:

    newclass = {}    

    for classname in doc["class"]:
        newaccesslist=[]
        # print doc["class"]
        # print "xxxxx"
        # print classname
        # print doc["class"]
        if type(doc["class"][classname]) is list and len(doc["class"][classname]) == 2:
            accesslist=doc["class"][classname][1]
            fi = {
                "classname": classname,
            }
            c=clcl.find_one(fi)
            vlist=c["variablelist"]
            # print accesslist
            for item in accesslist:
                tarcn=item["classname"]
                offset = item["accessoffset"]
                foundoffset =False
                # print "offset first" + offset 
                # raw_input("----")
                for v in vlist:
                    if v["offset"] == int(offset):
                        
                        item["variablename"]=v["typename"] + " "+v["vname"]
                        if v["typename"].count("(*)(")>0:
                            doc["foundfuncpointer"]=1
                            print "found one!"
                            print doc["method"]
                            # print 
                            print item["variablename"]
                            with open ("yuqijieguo.txt","a") as f:
                                f.write("found one: "+doc["method"]+" | "+item["variablename"])
                                f.close()
                        foundoffset = True
                        break
                if not foundoffset:
                    # print "not found"
                    item["variablename"] = "variablename failed to find"
                    
                newaccesslist.append(item)
            
            newclass[classname] = doc["class"][classname]

            newclass[classname][1]=newaccesslist
        else:
            newclass[classname]=doc["class"][classname]
        # raw_input("=====")

    del doc["class"]
    doc["class"] = newclass
    vm3cl.insert(doc,check_keys=False)


