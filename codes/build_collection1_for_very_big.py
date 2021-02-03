#!/usr/bin/python
#coding:utf-8


import logging
import os
import re
import sys
from stringtool import *
from json import dumps
from classrepr import *
import pprint
import json
import argparse
import importlib
from globalconfig import *
from DBatom import *
mycount =0
dbcount =0 
global databasecl
global client

# print "xxx"


filelist = ["coop.out.vf", "coop.out.callsite", "coop.out.layout"]
# global cl

# class collection
global cc

# virtual function collection
global vfc


class basedecl(Default):
    def __init__(self, typename, variablename):
        self.typename = typename
        self.variablename = variablename

    def build(self, dct):
        self.build_default(dct)
        return dct

    def parse(self, dct):
        self.parse_default(dct)
        return self

    def __repr__(self):
        return "[\"%s\",\"%s\"]" % (self.typename, self.variablename)


class accessfield(Default):

    def __init__(self, classname=None, accesstype=None, accessoffset=None, variablename=None):
        self.classname = classname
        self.accesstype = accesstype
        self.accessoffset = accessoffset
        self.variablename = variablename

    def build(self, dct):
        self.build_default(dct)
        return dct

    def parse(self, dct):
        self.parse_default(dct)
        return self

    def set_variablename(self):
        # print "this is vari:"
        try:
            # print cc[self.classname].offsetdict[self.accessoffset]

            self.variablename = cc[self.classname]["offsetdict"][self.accessoffset]
        except KeyError:
            self.variablename = "not found classname"

    def __repr__(self):
        return "[%s,%s,%s]" % (self.accesstype, self.accessoffset, self.variablename)


def generate_structure_layouts_collection():
    global databasecl
    global client
    global mycount
    global dbcount

    def unitwork(objectunitbuffer):
        global databasecl
        global client
        global mycount
        global dbcount

        # print "one complete!"

        # print objectunitbuffer
        objectunitbuffer = dropuntil(objectunitbuffer, "Class name: \n\t")
        # classname = rud(objectunitbuffer, "\n")

        ob = dropuntil(objectunitbuffer, "Class layout:\n")
        try:
            ob_end = dropuntil(ob, "| [")
        except AssertionError:
            print ob
            # raw_input("xxx")
            return
        ob = rud(ob, "| [")
        oblist = ob.split("\n")
        # print ob
        # print "\\\\\\"
        try:
            clsize = int(
                ob_end[ob_end.find("sizeof=")+len("sizeof="):ob_end.find(",")])
        except:
            print "error happen!"
            print ob
            return

        baseclasslist = []
        variablelist = []
        thisclassname = ""
        for line in oblist:
            try:
                print "--------"
                print line
                if len(line.split(" | ")) < 2:
                    continue
                col1 = line.split(" | ")[0]
                col2 = line.split(" | ")[1]
                try:
                    offset = int(col1)
                except ValueError:
                    offset = int(col1.split(":")[0])

                # print "col2 is ..............."
                # print col2
                # print "line is ////"
                print "col2"
                print repr(col2)
                if col2 == "" or col2 == " " or col2 == "  ":
                    # 4|
                    continue
                if col2[0] != " ":
                    # print "col2[0]!="
                    if col2.startswith("class"):
                        thisclassname = col2[6:]
                    elif col2.startswith("struct"):
                        thisclassname = col2[7:]

                    # elif col2.startswith("union"):
                    #     thisclassname = col2[6:]
                    else:
                        return
                    print "this classname: "+thisclassname
                    continue

                try:
                    if col2[:2] == "  " and col2[3] != " ":
                        print "direct variable: " + col2

                    else:
                        # print "not direct xxxx : "+col2
                        continue
                except:
                    continue

                if col2.find("(primary base)") != -1 or col2.find("(base)") != -1:
                    print "find a baseclass begin"
                    tmpclassname = col2[2:]
                    classname = tmpclassname.split(" (primary base)")[0]
                    classname = classname.split(" (base)")[0]

                    if classname.startswith("struct"):
                        classname = classname[7:]
                    elif classname.startswith("class "):
                        classname = classname[6:]

                    # {
                    #     offset:offset
                    #     classname:classname,
                    # }

                    subunit = {
                        "offset": offset,
                        "baseclassname": classname,
                    }
                    # print classname
                    baseclasslist.append(subunit)
                else:
                    # {
                        # offset:""
                        # vtype: "ptr" / "variable" /"class/struct"
                        # typename:
                        # vname:""
                    # }
                    tmptn = col2[2:]
                    tokens = tmptn.split(" ")
                    if len(tokens) < 2:
                        continue
                    vname = tokens[-1]
                    if tokens[-2] == "*":

                        print "find a pointer"
                        vtype = "ptr"
                        if tokens[0] == "class" or tokens[0] == "struct":
                            # class ckxclass * ckxptr
                            typename = " ".join(tokens[1:][:-2])

                        else:
                            # int * ckxptr
                            typename = " ".join(tokens[:-2])

                    elif tokens[0] == "class" or tokens[0] == "struct":
                        # class ckxclass ckxvname
                        vtype = "c/s"
                        typename = " ".join(tokens[:-1][1:])
                    else:
                        # int ckx
                        vtype = "variable"
                        typename = " ".join(tokens[:-1])

                    vunit = {
                        "offset": offset,
                        "vtype": vtype,
                        "typename": typename,
                        "vname": vname,
                    }

                    print "find a type + name"
                    print vunit
                    variablelist.append(vunit)
                if thisclassname == "":
                    print thisclassname
                    print "kkk"
                    print objectunitbuffer
                    raise Exception
            except:
                continue

        cl = classlayout()
        print ">>>>"
        print thisclassname
        print variablelist
        cl.classname = thisclassname
        cl.variablelist = variablelist
        cl.baseclasslist = baseclasslist
        cl.size = clsize

        tmpdict = {}
        tmpdict = cl.build(tmpdict)
        tmpdict2 = tmpdict

        # ckx: 数据库嵌入

        # 插入

        # print tmpdict
        # raw_input("tmp stop")

        # cc.update({cl.classname: tmpdict})
        # cc.update({cl.classname:cl})
        # continue

        # try:
        mycount+=1
        if mycount%1000000 == 0:
            dbcount+=1
            deletecollection(COOPPLUSDB, CLASSLAYOUT+"_"+str(dbcount))
            databasecl,client = getdbhandler(COOPPLUSDB,CLASSLAYOUT+"_"+str(dbcount))
        databasecl.insert(tmpdict, check_keys=False)
        # except:
        # print tmpdict2
        # raw_input("xxx")

        return cl


# Class name:
# 	sub
# Class layout:
#          0 | class sub
#          0 |   class base (primary base)
#          0 |     (base vtable pointer)
#          8 |     class intra intraname
#          8 |       int ii
#         12 |       int ccd
#         16 |       char hchar
#         20 |     int mem1
#         24 |     int mem2
#         32 |   class base2 (base)
#         32 |     (base2 vtable pointer)
#         40 |     class basebase (base)
#         40 |       int kk
#         44 |       int pp
#         48 |     int mem1
#         52 |     int mem2
#         56 |   int sub_mem1
#         60 |   int sub_mem2
#            | [sizeof=64, dsize=64, align=8,
#            |  nvsize=64, nvalign=8]
        # IPython.embed()

    TARGETNAME = "coop.out.layout.me"
    TARGETNAME = "coop.out.layout"
    startflag = False
    finishflag = False
    objectunitbuffer = ""
    alldict = {}
    logging.info("=== generate_-structure_layouts_collectio : begin")
    # print "start parsing ...\n"

    startflag = False
    finishflag = False

    # cc = classcollections();

    with open(TARGETNAME) as file:
        count = 0
        for line in file:

            if "Class name:" in line:
                startflag = True
            if startflag and "\n" == line:
                finishflag = True

            if startflag and not finishflag:
                objectunitbuffer = objectunitbuffer + line
            elif finishflag:

                # cc.update({cl.classname:unitwork(objectunitbuffer)})
                unitwork(objectunitbuffer)
                objectunitbuffer = ""
                finishflag = False
                startflag = False

                # count+=1
                # if count > 10:
                #     break

    if startflag == True or finishflag == True:
        # cc.update({cl.classname: unitwork(objectunitbuffer)})
        unitwork(objectunitbuffer)
        objectunitbuffer == ""
        finishflag = False
        startflag = False

    # print "\n == mission complete =="
    logging.info("=== generate_structure_layouts_collectio : complete")
    # print alldict
    # return cc


if __name__ == "__main__":


    for i in filelist:
        if not os.path.exists(i):
            logging.info('\tfile %s does not exist' % i)
            sys.exit(-1)

    cc = classcollections()

    logging.info("generate_collection")

    deletecollection(COOPPLUSDB, CLASSLAYOUT+"_0")
    # suffix = range(1,29)
    # databasecllist=[]
    # clientlist=[]
    # for su in suffix:
    # databasecl, client = getdbhandler(COOPPLUSDB, CLASSLAYOUT+"_"+str(su))
    databasecl,client = getdbhandler(COOPPLUSDB,CLASSLAYOUT+"_0")

    generate_structure_layouts_collection()

    client.close()

    print "____end____"
