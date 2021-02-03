# coding:utf-8
class ToFileStdOut(object):
    def __init__(self,outfilename):
        self.outfile = open(outfilename, "a")
        # self.outfile = open("./tmp.output", "a")

    def write(self, text):
        self.outfile.write(text)
    def flush(self):
        self.outfile.flush()
    def isatty(self):
        return False
    def __del__(self):
        self.outfile.close()


from sys import path
path.append("../")
from globalconfig import *
from DBatom import *
import sys

vcallsitecl,client = getdbhandler(COOPPLUSDB,VCALLSITE+"_4")
vmethod_cl,client1 = getdbhandler(COOPPLUSDB,VMETHOD_TO_AN+"_3")
layout_cl,client2 = getdbhandler(COOPPLUSDB,CLASSLAYOUTRAW)

def get_oob_offsets(counterfeit_classname,vmethodid):
    fi = {"_id":vmethodid}
    # vmethode_cl1.find()
    con = vmethod_cl.find(fi,no_cursor_timeout=True)
    item = next(con)
    adict= item["class"]
    if not adict.__contains__(counterfeit_classname):
        raise Exception("counterfeit class not found in class dict")
    # print(adict[counterfeit_classname])
    if len(adict[counterfeit_classname])<2:
        return [-1]
    # print("++++++")
    ooblist=adict[counterfeit_classname][1]
    resultlist = []
    for it in ooblist:
        offset = int(it["accessoffset"])
        if offset not in resultlist:
            resultlist.append(offset)


    return resultlist


def is_offset_toward_ptr_or_struct(aunit):
    classname = aunit[1]
    offset = aunit[2]
    # layout_cl.find()
    fi = {
        "classname":classname,
    }
    con = layout_cl.find(fi,no_cursor_timeout=True)
    item = next(con)
    alist = item["variablelist"]
    for it in alist:
        if it["offset"]==offset:
            # if it["vtype"] == "ptr":# or it["vtype"]=="c/s":
            if it["vtype"] == "ptr":
                aunit.append("ptr")
                return it["vname"]
            
            elif it["vtype"]=="c/s":
                aunit.append("c/s")
                return it["vname"]
                # return True
            else:
                return False
    print (aunit)
    raise Exception("not found offset type")



# vcallsitecl, client = getdbhandler(COOPPLUSDB, CLASSLAYOUT)

print("before")
print MONGODB_SERVER



# sys.stdout = ToFileStdOut("./tmpt.out")

fi= {}
con = vcallsitecl.find(fi,no_cursor_timeout=True)

# f=open("atemp_qt","w")

count=0
resultlist = []
filtered_result_list = []
for i in con:
    count=count+1
    # target=i["full_vcallname"]
    interface_functionname = i["full_vcallname"]
    colordict = i["colordict"]
    vmethodid =i["vmethodid"]
    rawmethod = i["rawmethod"]
    # if i["rawmethod"]!="::Draw3DTransformedSurface":
    #     continue
    
    for item in colordict.keys():
        if item!="0":
            for aunit in colordict[item]:
                if len(aunit)==3:
                    # 主要关注实现重载的方法就行了
                    counterfeit_classname = aunit[0]
                    # print (vmethodid)
                    offsetlist = get_oob_offsets(counterfeit_classname,vmethodid)
                    for offset in offsetlist:
                        if offset !=-1:
                            taskunit = [interface_functionname,counterfeit_classname,offset,rawmethod]
                            # print(taskunit)
                            resultlist.append(taskunit)
                            try:
                                # vname = is_offset_toward_ptr_or_struct(taskunit)
                                vname = True
                                if vname:
                                    taskunit.append(vname)

                                    # print(taskunit)
                
                                    # filtered_result_list.append(taskunit)
                                else:
                                    # print("not ptr or c/s")
                                    pass
                            except Exception:
                                pass



# for result in resultlist:
#     if is_offset_toward_ptr_or_struct(result):
#         filtered_result_list.append(result)



                # counterfeit_classname = aunit[0]

    # print(target)
    # aline = "\""+target+"\""+",\n"
    # print(aline)
    # f.write(aline)



print(len(taskunit))