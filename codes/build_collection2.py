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

    def __init__(self, classname=None, accesstype=None, accessoffset=None, variablename=None,parentfield=None):
        self.classname = classname
        self.accesstype = accesstype
        self.accessoffset = accessoffset
        self.variablename = variablename
        self.parentfield = parentfield

    def build(self, dct):
        self.build_default(dct)
        return dct

    def parse(self, dct):
        self.parse_default(dct)
        return self

    def set_variablename(self):
        self.variablename = "wait to pad"
        # print "this is vari:"
        # try:
        #     # print cc[self.classname].offsetdict[self.accessoffset]

        #     self.variablename = cc[self.classname]["offsetdict"][self.accessoffset]
        # except KeyError:
        #     self.variablename = "not found classname"

    def __repr__(self):
        return "[%s,%s,%s]" % (self.accesstype, self.accessoffset, self.variablename)


def generate_overridevfs_collection(databasecl):

    def unitwork(objectunitbuffer, databasecl):
        # print "one complete!----------------"
        # ov = overridvf()
        unitdict = {}

        # print objectunitbuffer
        objectunitbuffer = dropuntil(
            objectunitbuffer, "Virtual function name: \n")
        tmpob = rud(objectunitbuffer, "\n")
        vfname = tmpob.split("\t")[-1]
        # subclassname = vfname.split("::")[0]

        # ckx_b::padding(JSContext*, JS::Rooted<JSString*>*)



        # coop.out.vf 改版了， 去掉了参数的括号项目，所以进行一定修改
        # vfname_raw = vfname[:vfname.rfind("(")]
        vfname_raw = vfname

        methodename = vfname_raw.split("::")[-1]

        subclassname = "::".join(vfname_raw.split("::")[:-1])
        # print "goooo"
        # print vfname_raw
        # print subclassname
        # print methodename
        # print "donnn"
        ob = dropuntil(objectunitbuffer, "Overridden functions:\n")

        # print ob
        nextline = rud(ob, "\n")

        # print nextline
        if "Access fields:" not in nextline:
            # print "trigger ..."
            target = nextline.split("\t")[-1]

            # print target
            # mozilla::GetUserMediaStreamRunnable::Run()::LocalTrackSource::~LocalTrackSource()
            # basevf = target.split("(")[0]

            basevf = target[:target.rfind("(")]
            

            baseclassname = "::".join(basevf.split("::")[:-1]).split("++  ")[-1]

        else:
            
            baseclassname = "->null<-"
            
            pass
        ovf = overridevf(methodename, baseclassname, subclassname)

        accessfields = rud(
            dropuntil(ob, "Access fields:\n"), "Virtual function Finish:")
        # print accessfields
        # IPython.embed()
        offlist = []
        for line in accessfields.split("\n"):
            if line == "":
                continue
            # print "aaa"
            # tokenlist = line.split("\t")
            r = re.compile('[ \t\n\r:]+')
            [a, accesstype, offset, d] = r.split(line)
            offset = str(int(offset))

            # print "re content ...."
            # print a
            # print accesstype
            # print offset
            # print d
            parentfield = "NULL"
            pf =""

            if d.find("|||")!=-1:
                pf=d.split("|||")[-2]
                # print pf
                parentfield = pf
            # print "pa\n"
            # print "gooo"
            # print parentfield
            # print "\n\n"
            # parentfield
            af = accessfield(subclassname, accesstype, offset,parentfield=parentfield)
            af.set_variablename()
            tmp = af.build({})
            ovf.accesslist.append(tmp)
            # print "re done...."
            # if offset not in offlist:
            #     offlist.append((offset))

        # ovf.set_accessname()
        tmpdict = ovf.build({})

        # print tmpdict
        databasecl.insert_one(tmpdict)
        # raw_input("tsp")
        # ovfc.overridevfdict.update({vfname: tmpdict})



        # print ">>>>>>>>>>>>>>"

    logging.info("=== generate_overridevfs_collection : start ===")
    TARGETNAME = "coop.out.vf.me"
    TARGETNAME = "coop.out.vf"
    startflag = False
    finishflag = False
    objectunitbuffer = ""
    resultdict = {}
    # print "start parsing vf ...\n"
    targetname = TARGETNAME
    # if len(sys.argv) >1:
    #     targetname = sys.argv[1]
    # else:
    #     targetname = TARGETNAME

    startflag = False
    finishflag = False

    with open(targetname) as file:
        i = 0
        for line in file:
            if "Virtual function LOC:" in line:
                startflag = True
            if startflag and "\n" == line:
                finishflag = True

            if startflag and not finishflag:
                objectunitbuffer = objectunitbuffer + line
            elif finishflag:

                # print i
                i += 1
                unitwork(objectunitbuffer, databasecl)
                # if i >100:
                #     break
                objectunitbuffer = ""
                finishflag = False
                startflag = False

    if startflag == True or finishflag == True:
        unitwork(objectunitbuffer, databasecl)
        objectunitbuffer == ""
        finishflag = False
        startflag = False

    # print "\n == vf complete =="
    logging.info("=== generate_overridevfs_collection : complete ===")

    return resultdict


if __name__ == "__main__":

    
    for i in filelist:
        if not os.path.exists(i):
            logging.info('\tfile %s does not exist' % i)
            sys.exit(-1)

    
    # ovfc = overridevfcollection()

    deletecollection(COOPPLUSDB, VIRTUALFUNCTION)
    databasecl, client = getdbhandler(COOPPLUSDB, VIRTUALFUNCTION)

    generate_overridevfs_collection(databasecl)

    client.close()

    



    print "____end____"
