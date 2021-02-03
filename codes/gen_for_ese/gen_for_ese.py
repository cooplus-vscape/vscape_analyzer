#coding:utf-8

from sys import path
path.append("../")

from globalconfig import *
from DBatom import *
import os


# deletecollection(COOPPLUSDB, VMETHOD_TO_AN+"_2")


v3cl, v3lient = getdbhandler(COOPPLUSDB, VCALLSITE+"_3")


mypip = [
    {"$group": {
        "_id": "$_id"
    }}
]

re = v3cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []
for i in re:
    contentlist.append(i["_id"])


# def


os.system("rm functions_to_break.txt")

f = open("functions_to_break.txt","a")


# tp = (a,)
def addtobreaklist(a,b):
    aline = a+b+"\n"
    f.write(aline)



allnum = 0
loglist = []
mycount = 0
for c in contentlist:
    # mycount += 1
    # if mycount==10:
    #     break
    # print mycount
    fi = {
        "_id": c,
    }
    doc = v3cl.find_one(fi)
    obj = doc["colordict"]
    methodname = doc["rawmethod"]

    for i in obj:
        for ii in obj[i]:
            addtobreaklist(ii[0],methodname)

f.close()

#     # print obj
#     mydict = extractpairs(obj)
#     mylist = zip(mydict.keys(), mydict.values())
#     candi_num = cal_num(mylist)
#     # print mydict
#     print candi_num
#     if candi_num > 10000:
#         loglist.append(doc["method"])
#         continue

#     allnum += candi_num
#     # if mycount==10:
#     #     break
#     # print fi

# print "all num is:"
# print allnum

# print loglist
