#coding:utf-8
from globalconfig import *
from DBatom import *


from threading import Thread
import threading
import time

deletecollection(COOPPLUSDB,CLASSLAYOUTRAW)
databasecl, client = getdbhandler(COOPPLUSDB, CLASSLAYOUT)
rawcl,rawclient = getdbhandler(COOPPLUSDB,CLASSLAYOUTRAW)



# for r in re:


    
#     # print r[]
#     print r["_id"]
#     fi ={"classname":r["_id"]}

#     # tmp=databasecl.find_one(fi)

#     # insertlists.append(tmp)

#     # if len(insertlists)==100:

#     #     rawcl.insert_many(insertlists)
#     #     insertlists = []

#     # print tmp
#     # rawcl.insert_one(tmp,bypass_document_validation=True)
#     print count
#     count = count+1

# print re.count()
# print re[0]


def processitems(content, rangenum, rangenumend, tid):
    for cc in range(rangenum, rangenumend):
        # print cc
        tmp = databasecl.find_one({"classname":content[cc]["_id"]})
        # print tmp
        rawcl.insert_one(tmp,bypass_document_validation=True)
        content[cc]["has_processed"]=True
        print content[cc]
    print "thread %d done " % tid
    pass




if __name__ == "__main__":
    NWORKERS = 70
    threads = []

    # deletecollection(COOPPLUSDB,CLASSLAYOUTRAW)
    mypip = [
        {"$group": {"_id": "$classname"}},
        # {"$count": "tongji"},
    ]


    re = databasecl.aggregate(mypip,allowDiskUse=True,maxTimeMS=9000000)
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
        print "allnum is %d"%allnum
        print "laststart is %d"%laststart
        processitems(content,laststart,allnum,0)
    # raw_input("xxxxxx")

    while True:
        tongji = True
        for t in threads:
            tongji = tongji & (not t.is_alive())
        if tongji:
            break
    client.close()
    print "__end__"



