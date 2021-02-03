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

    dbcount = int(sys.argv[1])
    databasecl, client = getdbhandler(COOPPLUSDB, CLASSLAYOUT+"_"+str(dbcount))
    rawcl, rawclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW+"_"+str(dbcount))


    NWORKERS = 2
    threads = []

    deletecollection(COOPPLUSDB, CLASSLAYOUTRAW+"_"+str(dbcount))
    mypip = [
        {"$group": {"_id": "$classname"}},
        # {"$count": "tongji"},
    ]

    re = databasecl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
    content = []
    for r in re:
       content.append(r)
    allnum = len(content)


    stepnum = allnum/NWORKERS

    rangenum = 0
    rangenumend = 0
    for n in range(NWORKERS):
        rangenum = rangenumend
        rangenumend = rangenum+stepnum
        t = Thread(target=processitems, args=(
            content, rangenum, rangenumend, n,))
        t.daemon = True 
        # print "%d is started" % n
        t.start()
        threads.append(t)

    laststart = allnum/NWORKERS*NWORKERS
    if laststart < allnum:
        print "allnum is %d" % allnum
        print "laststart is %d" % laststart
        processitems(content, laststart, allnum, 0)
    # raw_input("xxxxxx")
    while True:
        time.sleep(10)
        pass
    client.close()
    print "__end__"
