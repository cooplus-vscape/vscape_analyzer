#coding:utf-8
from sys import path
path.append("../")
from globalconfig import *
from DBatom import *


databasecl, client = getdbhandler(COOPPLUSDB, CLASSLAYOUT)


fi= {
    "child":{"$exists":True}
}
con = databasecl.find(fi,no_cursor_timeout=True)


count=0
for i in con:
    count=count+1
    f2={
        "classname":i['classname']
    }
    num=databasecl.find(f2).count()
    print "count:num = %d : %d"%(count,num)
    # print num
    if num>1:
        print i["classname"]
