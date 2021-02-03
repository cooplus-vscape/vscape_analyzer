#coding:utf-8
from globalconfig import *
from DBatom import *





deletecollection(COOPPLUSDB, VCALLSITE+"_2")

vcallsitecl2, vcallsiteclient = getdbhandler(COOPPLUSDB, VCALLSITE+"_2")
vcallsitecl1, vcallsiteclient1 = getdbhandler(COOPPLUSDB, VCALLSITE+"_1")
whitelistcl, whitelistclient = getdbhandler(COOPPLUSDB, INTERFACEWHITELIST)
vfcl,vfclient=getdbhandler(COOPPLUSDB,VIRTUALFUNCTION+"_2")

con = vcallsitecl1.find({}, no_cursor_timeout=True)


mypip = [
    {"$group": {"_id": "$full_vcallname"}},
]

re = vcallsitecl1.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)


contentlist = []
for i in re:
    contentlist.append(i["_id"])




def checkmethod(item, root, methodname, interface=False):
    re = 0
    
    
    sc={
        "itself":root,
        "methodname":methodname
    }
    con=vfcl.find_one(sc)

    if not con:
        return 0 #<====== ISSUE
    if not interface:
        if con["parent"]!="->null<-":
            return 1
    
        
    for i in item[root]:
        rep = checkmethod(item,i,methodname)
        re = re | rep
        if re == True:
            break
    return re
        
        #     /* 2 * /
        # {
            #     "_id": ObjectId("5d51241bf3fadda8ed5b4d52"),
            #     "rawmethod": "::~GMPLoader",
            #     "interface classname": "mozilla::gmp::GMPLoader",
            #     "src loc": "NULL",
            #     "full vcallname": "mozilla::gmp::GMPLoader::~GMPLoader"
            # }


mycount = 0
for r in contentlist:
    mycount+=1
    print mycount
    fi = {
        "full_vcallname":r,
    }
    item = vcallsitecl1.find_one(fi)
    iname = item["interface_classname"]
    iitem = whitelistcl.find_one({"interfaceclassname": iname})
    methodname = item["rawmethod"].split("::")[-1]
    res = checkmethod(iitem,iname,methodname,True)
    if res:
        vcallsitecl2.insert(item, check_keys=False)


vcallsiteclient.close()
vcallsiteclient1.close()
whitelistclient.close()

print "__end__"
