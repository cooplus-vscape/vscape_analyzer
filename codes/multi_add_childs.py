#coding:utf-8
from globalconfig import *
from DBatom import *
from threading import Thread
import threading
import time

global processedcount


def addtoparent(child, parent):
    cs = {
        "classname": parent,
    }

    # print "on searching .... "+parent
    con = databasecl.find(cs)
    connum = con.count()
    if connum > 1:

        print "parent class is "+parent
        print "count  > 1!!!"
        raise Exception

    elif connum == 1:
        result = con[0]
    else:
        # print "not found: "+parent
        return

    if result.has_key("child"):
        prechild = result["child"]
        # print "prechild .......)))))))"
        # print prechild
        newchildlist = prechild
        if prechild.count(child) > 0:
            return
        else:
            # print child
            newchildlist.append(child)

        # print newchildlist
        up = {
            "$set":
            {
                "child": newchildlist,
            },
        }
    else:
        # print child
        if child == "":
            print "child is null"
            raise Exception
        childlist = [child]
        up = {
            "$set":
            {
                "child": childlist,
            },
        }

    # if parent == "X":
    #     print up
    #     raw_input("fenxi ....")
    fi = {"classname": parent}

    databasecl.update_one(fi, up)
    # databasecl.update(cs)





def processitems(content,tid):


    global processedcount
    myid = 0
    while True:
        myid = myid+1
        print myid
        try:
            c = content[0]
        except:
            # print cc
            # print c
            # client.close()
            break

        if c.has_key("has_processed"):
            # print "has_processed"
            # print c["classname"]
            continue
        else:
            # print "no processed"
            pass

        # print "----------------------------||||||||"
        # print "class: " + c["classname"]
        for base in c["baseclasslist"]:
            # print base["baseclassname"]
            addtoparent(c["classname"], base["baseclassname"])

        noteone = {
            "$set":
            {
                "has_processed": True,
            },
        }
        fi = {
            "classname": c["classname"],
            '_id': c["_id"],
        }
        databasecl.update_one(fi, noteone)
    print "tid %d done and idx is %d" % (tid,myid)
    processedcount = processedcount+myid
    print "processed count reach %d"%processedcount



















if __name__ == "__main__":
    NWORKERS = 40
    threads=[]


    databasecl, client = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)

    fi = {
        "has_processed": {"$exists": False}
    }
    content = databasecl.find(fi, no_cursor_timeout=True)
    allnum= content.count()


    stepnum=allnum/NWORKERS
    yu=0
    if stepnum*NWORKERS<allnum:
        yu = allnum - stepnum*NWORKERS


    contentlist =[]

    processedcount=0
    for n in range(NWORKERS):
        cont=databasecl.find(fi, no_cursor_timeout=True).skip(n*stepnum).limit(stepnum)
        contentlist.append(cont)
    if yu > 0:
        cont=databasecl.find(fi, no_cursor_timeout=True).skip(NWORKERS*stepnum).limit(yu)
        contentlist.append(cont)

    print "contentlist size if %d"%len(contentlist)
    for i in contentlist:

        t = Thread(target=processitems,args=(i,n))
        t.daemon = True  #设置成守护进程，ctrl+c杀死mainthread的时候，childthread一起销毁
        #但是daemon以后不能配合join()使用
        # print "%d is started" % n
        t.start()
        threads.append(t)

    while True:
        time.sleep(10)
        pass
    client.close()
    print "__end__"
