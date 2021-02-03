#coding:utf-8
from globalconfig import *
from DBatom import *

from threading import Thread
import threading
import time


def processitems(content, rangenum, rangenumend, tid):
    for cc in range(rangenum, rangenumend):
        try:
            try:
                print content[cc]
            except:
                continue
            fs = {
                "classname": content[cc]["classname"]
            }
            baoliu = content[cc]
            databasecl.delete_many(fs)
            # databasecl.insert(baoliu,check_keys=False)
            databasecl.insert(baoliu, check_keys=False)
        except:
            continue

    print "thread %d done " % tid
    pass



if __name__ == "__main__":

    NWORKERS = 40
    threads = []

    databasecl, client = getdbhandler(COOPPLUSDB, CLASSLAYOUT)

    fi={}
    content = databasecl.find(fi, no_cursor_timeout=True)
    # num = content.count()


    allnum = content.count()
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

    # raw_input("xxxxxx")
    while True:
        time.sleep(10)
        pass
    client.close()
    print "__end__"
