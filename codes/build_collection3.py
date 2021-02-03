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
    
        self.variablename = "wait to pad"
        # print "this is vari:"
        # try:
        #     # print cc[self.classname].offsetdict[self.accessoffset]

        #     self.variablename = cc[self.classname]["offsetdict"][self.accessoffset]
        # except KeyError:
        #     self.variablename = "not found classname"

    def __repr__(self):
        return "[%s,%s,%s]" % (self.accesstype, self.accessoffset, self.variablename)


def generate_vcallsite_collection(databasecl):

    def unitwork(objectunitbuffer, databasecl):
        # print "one complete!----------------"
        # ov = overridvf()
        unitdict = {}

        # print objectunitbuffer


        # print objectunitbuffer
        objectunitbuffer = dropuntil(objectunitbuffer, "Call site LOC:\n\t")
        srcloc = rud(objectunitbuffer,"\n")
        # print objectunitbuffer
        # try:
        allvcall = dropuntil(objectunitbuffer, "\t")

        # except AssertionError:
        #     print srcloc
        #     print objectunitbuffer
        #     raw_input("xxx")


        # allvcall = dropuntil(allvcall, ", ")
        # print "xxx"
        vcall = rud(allvcall, "\n")
        # print allvcall

        tc = dropuntil(allvcall, "\t")

        clsname = rud(tc,"\n")

        rawmethod = vcall[vcall.find(clsname)+len(clsname):]
        # rawmethod = vcall.split(clsname)[1]
        # print rawmethod
        # print srcloc
        # print vcall
        # print clsname



        unitdict.update({
            "rawmethod":rawmethod,
            "interface_classname":clsname,
            "full_vcallname": vcall,
            "srcloc":srcloc,
        })

        databasecl.insert_one(unitdict)


        # raw_input("xxx")


    logging.info("=== generate_vfcallsite_collection : start ===")
    TARGETNAME = "coop.out.callsite"
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
            if "Call site LOC:" in line:
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
    logging.info("=== generate_vcallsite_collection : complete ===")

    return resultdict


if __name__ == "__main__":

    for i in filelist:
        if not os.path.exists(i):
            logging.info('\tfile %s does not exist' % i)
            sys.exit(-1)

    ovfc = overridevfcollection()

    deletecollection(COOPPLUSDB, VCALLSITE)
    databasecl, client = getdbhandler(COOPPLUSDB, VCALLSITE)

    generate_vcallsite_collection(databasecl)

    client.close()

    print "____end____"
