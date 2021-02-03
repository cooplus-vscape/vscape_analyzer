
from globalconfig import *
from DBatom import *


deletecollection(COOPPLUSDB, CLASSLAYOUTRAW+"_stringrelate")


deletecollection(COOPPLUSDB, CLASSLAYOUTRAW+"_stringrelate_all")

cl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)
bcl, bclclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW+"_stringrelate")


abcl, abclclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW+"_stringrelate_all")
scl, sclclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW+"_stringclass")

mypip = [
    {"$group": {
        "_id": "$classname"
    }}
]

re = scl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
stringclslist = []

for i in re:
    stringclslist.append(i["_id"])


stringclslist.append("char")


mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)

idlist = []
for i in re:
    idlist.append(i["_id"])







def check(doc):
    vl=doc["variablelist"]
    for i in vl:
        tn=i["typename"]
        if tn in stringclslist:
            return True
    return False




againlist=[]

ii = 0
for id in idlist:
    ii += 1
    if ii % 10000 == 0:
        print ii
    # if ii% 30000==0:
    #     break

    fi = {
        "_id": id,
    }

    doc = cl.find_one(fi)

    if not check(doc):
        continue
    else:
        bcl.insert(doc, check_keys=False)
        againlist.append(id)



def insertchilds(namelist):

    # for item in doc:
    if len(namelist)==0:
        # if bcl.find_one()
        return 
    else:
        for it in namelist:
            fi = {
                "classname": it,
            }
            doc=cl.find_one(fi)

            if doc.has_key("child"):
                insertchilds(doc["child"])
                try:
                    # print "add happen"
                    abcl.insert(doc,check_keys=False)
                except:
                    pass
            else:
                insertchilds([])
                try:
                    abcl.insert(doc,check_keys=False)
                except:
                    pass

        



ii = 0
c=0
for id in againlist:
    ii += 1
    if ii % 100 == 0:
        print ii

    fi = {
        "_id": id,
    }

    doc = cl.find_one(fi)
    if doc.has_key("child"):
        print doc["classname"]
        insertchilds(doc["child"])
    try:
        abcl.insert(doc,check_keys=False)
        pass
    except:
        pass








print "===end=="
