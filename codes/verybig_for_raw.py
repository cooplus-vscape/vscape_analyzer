#coding:utf-8
from globalconfig import *
from DBatom import *


from threading import Thread
import threading
import time


def processitems(content, rangenum, rangenumend, tid):
    for cc in range(rangenum, rangenumend):
        # print cc
        tmp = databasecl.find_one({"classname": content[cc]["_id"]})
        # print tmp
        rawcl.insert_one(tmp, bypass_document_validation=True)
        content[cc]["has_processed"] = True
        print content[cc]
    print "thread %d done " % tid
    pass


if __name__ == "__main__":

    # deletecollection(COOPPLUSDB, CLASSLAYOUTRAW)
    dbcount = int(sys.argv[1])
    bigdict={}
    allsearch=0
    rawcl, rawclient = getdbhandler(
        COOPPLUSDB, CLASSLAYOUTRAW)
    mypip = [
        {"$group": {"_id": "$classname"}},
        # {"$count": "tongji"},
    ]
    re = rawcl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)


    for r in re:
        bigdict[r["_id"]]=1
    
    for i in range(dbcount+1):
        
        databasecl, client = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW+"_"+str(i))
        mypip = [
            {"$group": {"_id": "$classname"}},
            # {"$count": "tongji"},
        ]
        re = databasecl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
        content = []
        for r in re:
            content.append(r)

        for r in content:

            allsearch+=1
            # print r["_id"]
            if bigdict.has_key(r["_id"]):
                continue
            else:
    
                bigdict[r["_id"]]=1
                fi = {
                    "classname":r["_id"],
                }
                jie=databasecl.find_one(fi)
                rawcl.insert(jie,check_keys=False)

            




        # allnum = len(content)
        print len(bigdict)
        print "---->"+str(allsearch)


    print "__end__"
