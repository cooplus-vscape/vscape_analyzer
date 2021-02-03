#coding:utf-8
from globalconfig import *
from DBatom import *

import time


def addtoparent(child,parent):
    cs = {
        "classname":parent,
    }

    print "on searching .... "+parent
    con=databasecl.find(cs)
    connum = con.count()
    if connum>1:
        print "parent class is "+parent
        print "count  > 1!!!"
        raise Exception
        # raw_input("count > 1")
        # return 
    elif connum==1:
        result=con[0]
    else:
        print "not found: "+parent
        return


    if result.has_key("child") :
        prechild = result["child"]
        # print "prechild .......)))))))"
        # print prechild
        newchildlist=prechild
        if prechild.count(child)>0:
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
        if child=="":
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
    fi = {"classname":parent}

    databasecl.update_one(fi,up)
    # databasecl.update(cs)




if __name__ =="__main__":


    fi = {
        "has_processed": {"$exists": False}
    }


    databasecl, client = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)
    content = databasecl.find(fi, no_cursor_timeout=True)
    contentnum = content.count()
    print "search content num: " + str(contentnum)
#     search content num: 3
# nsStylePadding
# mozilla::RemoveReference<class mozilla::PlatformDecoderModule *&> (empty)
# mozilla::detail::PointerType<class mozilla::SdpGroupAttributeList, class mozilla::DefaultDelete<class mozilla::SdpGroupAttributeList> > (empty)
# no processed
# ----------------------------||||||||
# class: nsStylePadding
# no processed
# ----------------------------||||||||
# class: mozilla::detail::PointerType<class mozilla::SdpGroupAttributeList, class mozilla::DefaultDelete<class mozilla::SdpGroupAttributeList> > (empty)
# 2
# {u'classname': u'mozilla::detail::PointerType<class mozilla::SdpGroupAttributeList, class mozilla::DefaultDelete<class mozilla::SdpGroupAttributeList> > (empty)', u'baseclasslist': [], u'_id': ObjectId('5d5526176e717a5ba8be3d2a'), u'variablelist': [], u'size': 1}
# Traceback (most recent call last):
#   File "add_childs.py", line 118, in <module>
# raise Exception






    # for cc in range(contentnum):
    #     print content[cc]["classname"]

    myid=0
    while True:
        myid=myid+1
        print myid
        try:
            c=content[0]
        except:
            # print cc
            # print c
            client.close()
            break

        if c.has_key("has_processed"):
            print "has_processed"
            print c["classname"]
            continue
        else:
            print "no processed"
            pass


        print "----------------------------||||||||"
        print "class: "+ c["classname"]
        for base in c["baseclasslist"]:
            # print base["baseclassname"]
            addtoparent(c["classname"],base["baseclassname"])

        noteone = {
            "$set":
            {
                "has_processed": True,
            },
        }
        fi = {
            "classname":c["classname"],
            '_id':c["_id"],
        }
        databasecl.update_one(fi,noteone)

    client.close()
    print "\n\n loop end\n\n"
    # time.sleep(5)
    # print c

    print "__end__"







