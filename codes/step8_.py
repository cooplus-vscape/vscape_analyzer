#coding:utf-8
from globalconfig import *
from DBatom import *
deletecollection(COOPPLUSDB,VCALLSITE+"_3")


vm2cl, vm2client = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_2")
vc2cl, vc2client = getdbhandler(COOPPLUSDB, VCALLSITE+"_2")
vc3cl,vc3client = getdbhandler(COOPPLUSDB,VCALLSITE+"_3")


mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = vm2cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])


mycount =1
for mid in contentlist:
    print mycount
    mycount+=1
    fi = {
        "_id":mid
    }

    doc=vm2cl.find_one(fi)
    myclass = doc["class"]
    objid=doc["vcallsiteid"]
    fii = {
        "_id":objid,
    }
    docc=vc2cl.find_one(fii)

    tarraw=docc["classregion"]
    newtar = []
    tar =[]
    addtar=[]
    colordict = {}
    for t in tarraw:
        color = t[1]
        if not colordict.has_key(str(color)):
            colordict[str(color)]=[]
            colordict[str(color)].append(t)
        else:
            colordict[str(color)].append(t)
        if len(t) ==3:
            tar.append(t)
    # print tar 
    # raw_input("((((((((")
    for i in tar:
        origincolor  = i[1]
        ii = myclass[i[0]]
        # print ii
        # raw_input("???")
        if type(ii) is list:
            newcolor = ii[0]
            print "newcolor="+str(newcolor)+"<=="
            if newcolor == origincolor:
                pass
            else:
                # print newcolor
                # print origincolor
                # print i[0]
                # raw_input("meet one ......")
                origin_colors = colordict[str(origincolor)]
                del colordict[str(origincolor)]
                newc=int(newcolor)
                if not colordict.has_key(str(newc)):
                    colordict[str(newc)] = origin_colors
                else:
                    colordict[str(newc)] = colordict[str(newc)] + origin_colors
            pass
        else:
            pass
    # upper ={
    #     "$set":{
    #         "vmethodid":mid,
    #         "colordict":colordict
    #     }
    # }
    docc["colordict"] = colordict
    docc["vmethodid"] = mid
    # print docc
    # print colordict


    vc3cl.insert(docc,check_keys=False)
    # vc3cl.update_one(fii,upper)
print "+__end_+_"


# vm2cl.find()


