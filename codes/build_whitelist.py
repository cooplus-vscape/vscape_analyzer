#coding:utf-8
from pymongo import *
from globalconfig import *
from DBatom import *
import sys




vcallsitecl,vcallsiteclient = getdbhandler(COOPPLUSDB,VCALLSITE)
classlayoutcl,classlayoutclient = getdbhandler(COOPPLUSDB,CLASSLAYOUTRAW)
interfacecl,interfaceclient = getdbhandler(COOPPLUSDB,INTERFACEWHITELIST)

re = vcallsitecl.find({}, no_cursor_timeout=True)

mypip = [
    {"$group": {"_id": "$interface_classname"}},
]

re = vcallsitecl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)

content = []
for r in re:
    content.append(r)
    allnum = len(content)

print allnum


# sys.exit(-1)

co = 0


def add2dict(root,tmpdict):
    print "in add2dict"
    print root
    # print root
    tmpre = classlayoutcl.find({"classname": root})

    if tmpre.count()>1:

        print root

        baoliu = tmpre[0]

        delt = {
            "classname":root,
        }
        print tmpre.count()
        print "del repeated!"
        # raw_input("xxx--------")
        classlayoutcl.delete_many(delt)
        classlayoutcl.insert(baoliu,check_keys=False)
        tmpre = classlayoutcl.find({"classname": root})
    
    if tmpre.count()==0:
        return
    node = tmpre[0]
    # print node  

    if not node.has_key("child"):
        tmpdict[root]=[]
        return

    tmpdict[root]=node["child"]
    for mem in node["child"]:
        add2dict(mem,tmpdict)




deletecollection(COOPPLUSDB,INTERFACEWHITELIST)
countckx =0
for doc in content:
    countckx+=1;
    print "this is number: %d" % countckx


    tmpdict = dict()


    interface = doc["_id"]
    
    if interfacecl.find({"interfaceclassname":interface}).count()>0:
        me = interfacecl.find({"interfaceclassname": interface})[0]
        # -2 : 1 for object id， 1 for interfaceclassname
        interfacecl.update_one({"interfaceclassname": interface}, {"$set": {"nodenum":len(me.keys())-2}})
        # print len(me.keys())
        continue

    co =co+1
    print "======="
    print co
    print interface
    add2dict(interface,tmpdict)
    tmpdict["interfaceclassname"] = interface
    print tmpdict
    interfacecl.insert(tmpdict,check_keys=False)

    # if co >10:
    #     break


vcallsiteclient.close()
print "___end__"
