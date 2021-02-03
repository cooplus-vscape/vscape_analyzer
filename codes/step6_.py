#coding:utf-8
from globalconfig import *
from DBatom import *
deletecollection(COOPPLUSDB,VMETHOD_TO_AN+"_1")
vmcl,vmclient = getdbhandler(COOPPLUSDB,VMETHOD_TO_AN)
vmcl1, vmclient1 = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_1")
vfcl,vfclient = getdbhandler(COOPPLUSDB,VIRTUALFUNCTION)
clcl,clclient = getdbhandler(COOPPLUSDB,CLASSLAYOUTRAW)



ones = vmcl.find({})

mycount=1
for one in ones:
    # print mycount
    foundflag = False
    mycount+=1
    m=one["method"].split("::")[-1]

    for cn in one["class"]:
        fi ={
            "itself":cn,
            "methodname":m,
        }
        # print fi
        doc = vfcl.find_one(fi)
        # print doc
        if len(doc["accesslist"])>0:
            del doc["_id"]
            # print one
            vmcl1.insert(one,check_keys=False)
            foundflag=True
            break
    if not foundflag:
        print one
        print doc
print "_end_"

# {
#     "itself": "mozilla::net::SpdyPushedStream31",
#     "methodname": "ReadSegments",
# }






