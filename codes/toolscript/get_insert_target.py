#coding:utf-8
from sys import path
path.append("../")
from globalconfig import *
from DBatom import *


# databasecl, client = getdbhandler(COOPPLUSDB, CLASSLAYOUT)

print("before")
print MONGODB_SERVER
databasecl,client = getdbhandler(COOPPLUSDB,VCALLSITE+"_4")


fi= {}
con = databasecl.find(fi,no_cursor_timeout=True)

f=open("atemp_qt","w")

count=0
for i in con:
    count=count+1
    target=i["full_vcallname"]
    # print(target)
    aline = "\""+target+"\""+",\n"
    print(aline)
    f.write(aline)


