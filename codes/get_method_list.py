#coding:utf-8

from globalconfig import *
from DBatom import *
from math import ceil




cl, clclient = getdbhandler(COOPPLUSDB, GVTFlist+"_tmp")

mypip = [
    {"$group": {
        "_id": "$function_name"
    }}
]

re = cl.aggregate(mypip, allowDiskUse=True, maxTimeMS=9000000)
contentlist = []


for i in re:
    contentlist.append(i["_id"])


for i in contentlist:
    print i
