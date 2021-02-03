from pymongo import *
from globalconfig import *
from DBatom import *


deletecollection(COOPPLUSDB, VCALLSITE+"_1")

vcallsitecl, vcallsiteclient = getdbhandler(COOPPLUSDB, VCALLSITE)
vcallsitecl1,vcallsiteclient1=getdbhandler(COOPPLUSDB,VCALLSITE+"_1")
whitelistcl, whitelistclient = getdbhandler(COOPPLUSDB, INTERFACEWHITELIST)



con = vcallsitecl.find({},no_cursor_timeout=True)


for item in con:

#     /* 2 * /
# {
#     "_id": ObjectId("5d51241bf3fadda8ed5b4d52"),
#     "rawmethod": "::~GMPLoader",
#     "interface classname": "mozilla::gmp::GMPLoader",
#     "src loc": "NULL",
#     "full vcallname": "mozilla::gmp::GMPLoader::~GMPLoader"
# } 
    iname=item["interface_classname"]

    iitem=whitelistcl.find({"interfaceclassname":iname})[0]
    try:
        if len(iitem[iname])==0:
            # print "found one no childs"
            # print iname
            continue
    except:
        # print "found one no items"
        # print iname
        continue

    vcallsitecl1.insert(item,check_keys=False)




vcallsiteclient.close()
vcallsiteclient1.close()
whitelistclient.close()

print "__end__"
