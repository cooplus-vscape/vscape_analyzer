#coding:utf-8
from globalconfig import *
from DBatom import *
global distributeID
global override_rela
global tmpIDnote
global maxdistributeID
v2cl, v2client = getdbhandler(COOPPLUSDB, VCALLSITE+"_2")

vfcl,vfclient = getdbhandler(COOPPLUSDB,VIRTUALFUNCTION)


def checkmethodone(item, root, methodname, rootdist_id=0,interface=False):
    # global distributeID
    global override_rela
    global maxdistributeID
    global tmpIDnote
    re = 0
    sc = {
        "itself": root,
        "methodname": methodname,
    }



    if not interface:
        con = vfcl.find_one(sc)
        # print con

        if not con:
            # print "notfound !"
            # print root
            # print ">>>>>>>>"
            override_rela.append([root, rootdist_id])
            tmpIDnote[root] = rootdist_id
            # return 0
        else:
            if con["parent"] != "->null<-":
                # distributeID +=1      
                maxdistributeID +=1
                rootdist_id = rootdist_id+1
                override_rela.append([root,maxdistributeID,con["parent"]])
                tmpIDnote[root]=maxdistributeID
                # up = {
                #     "$set":{
                #         "overrideclass":
                #     }
                # }
                # v2cl.update_one(fi,up)
                return 1
            else:


                override_rela.append([root, rootdist_id])
                tmpIDnote[root]=rootdist_id
    else:
        rootdist_id = 0
        override_rela = []
        override_rela.append([root, rootdist_id])
    return re





def checkmethodBFS(item, root, methodname, rootdist_id=0, interface=False):
    global override_rela
    global tmpIDnote
    global maxdistributeID
    # maxdistributeID = rootdist_id
    re = 0

    sc = {
        "itself": root,
        "methodname": methodname,
    }


    if interface:
        pass 
        # print "chuliziehn.,....."
        maxdistributeID = rootdist_id
        # if interface:
        rootdist_id = 0
        override_rela = []
        # print "tmpidnote clear"
        tmpIDnote={}
        tmpIDnote[root]=rootdist_id
        # print root
        override_rela.append([root, rootdist_id])
    # print "before loop"  
    for i in item[root]:
        # print root
        # print i
        # print tmpIDnote
        rep = checkmethodone(item, i, methodname, tmpIDnote[root])
        re = re | rep


    for i in item[root]:
        rep = checkmethodBFS(item, i, methodname, tmpIDnote[root])
        # if re == True:
        #     break
    return re




if __name__ =="__main__":

    



    mypip = [
        {"$group": {"_id": "$_id"}},
    ]


    re = v2cl.aggregate(mypip,allowDiskUse=True, maxTimeMS=9000000)
    idlist = []
    for i in re:
        idlist.append(i["_id"])

    print "all num is"
    print len(idlist)
    mycount = 1
    for oid in idlist:
        print mycount 
        fi = {
            "_id":oid,
        }
        doc = v2cl.find_one(fi)
        rel = doc["classtree"]
        checkmethodBFS(rel,rel["interfaceclassname"],doc["rawmethod"].split("::")[-1],0,True)
        # print override_rela
        upper = {
            "$set":{
                "classregion":override_rela
            }
        }
        print oid
        v2cl.update_one(fi,upper)
        mycount+=1
        # raw_input("stop me ....")
        

    print "__end___"
