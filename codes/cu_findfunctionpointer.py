#coding:utf-8
from globalconfig import *
from DBatom import *

# deletecollection(COOPPLUSDB, VMETHOD_TO_AN+"_1")
# vmcl, vmclient = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN)
# vmcl1, vmclient1 = getdbhandler(COOPPLUSDB, VMETHOD_TO_AN+"_1")
# vfcl, vfclient = getdbhandler(COOPPLUSDB, VIRTUALFUNCTION)
clcl, clclient = getdbhandler(COOPPLUSDB, CLASSLAYOUTRAW)
re=clcl.distinct("variablelist")

with open("cushai","w") as f:
    sys.stdout = f
    print re
    # print "ok"
    f.close()
