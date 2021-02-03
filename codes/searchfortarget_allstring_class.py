
from globalconfig import *
from DBatom import *


deletecollection(COOPPLUSDB, CLASSLAYOUTRAW+"_stringclass")
cl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)
bcl, bclclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW+"_stringclass")
}}
]

re = cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []

for i in re:
    contentlist.append(i["_id"])


def check(me):
    cln=me["classname"]
    cln=cln.lower()
    if int(me["size"])>32:
        return False
    if cln.find("string")==-1:
        return False

    if cln.find("<")!=-1 and cln.find(">")!=-1:
        return False
    if cln.find("string_")!=-1:
        return True

    if cln.endswith("string"):
        return True
    else:
        return False



ii = 0
for id in contentlist:
    ii += 1
    if ii % 10000 == 0:
        print ii

    fi = {
        "_id": id,
    }

    doc = cl.find_one(fi)

    if not check(doc):
        continue
    else:
        bcl.insert(doc, check_keys=False)

print "===end=="
