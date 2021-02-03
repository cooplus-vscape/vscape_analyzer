


#coding:utf-8
import sys
sys.path.append("../")
from globalconfig import *
from DBatom import *
import z3


def getbanner_info():
    clcl,clclient=getdbhandler(COOPPLUSDB,CLASSLAYOUTRAW)
    con=clcl.find({"classname":"banner"},no_cursor_timeout=True)

    re=[]
    for i in con:
        re.append(i)

    if len(re)>1:
        raise Exception("wrong... more than one banner")

    bannerinfo=re[0]
    bannerstructsize=bannerinfo['size']
    for key in bannerinfo['variablelist']:
        if key['vtype']=='ptr':
            ptroffset=key['offset']
            break
    clclient.close()
    return bannerstructsize,ptroffset

def get_useful_oob_info():
    vm3cl,vm3client=getdbhandler(COOPPLUSDB,VMETHOD_TO_AN+"_3")

    re=vm3cl.find({"method":"::render"})
    clss=re[0]["class"]
    relist =[]
    victim_obj_list=[]
    for shape in clss:
        if shape not in victim_obj_list:
            victim_obj_list.append(shape)
        if type(clss[shape])==list:
            for it in clss[shape][1]:
                if it["variablename" ].find("param_")!=-1:
                    relist.append( (shape,int(it['accessoffset'])))
                    break
    redict ={}
    for it in relist:
        if redict.__contains__(it[1]):
            redict[it[1]].append(it[0])
        else:
            redict[it[1]]=[it[0]]
    vm3client.close()
    return redict,victim_obj_list

def get_struct_size(structname):
    clcl,clclient=getdbhandler(COOPPLUSDB,CLASSLAYOUTRAW)
    con=clcl.find({"classname":structname},no_cursor_timeout=True)
    for r in con:
        clclient.close()
        return r["size"]
        # if r["classname"].find("shape")!=0:
            # shape
    
def get_struct_cache_size(structname):
    return get_cache_size2(get_struct_size(structname))
# def get_victim_objs():
#     vm3cl,vm3client=getdbhandler(COOPPLUSDB,VMETHOD_TO_AN+"_3")




# def get_shape_info():
    # shape0

def get_cache_size(thesize):
    if thesize <=8:
        return 8
    elif thesize <=128:
        return thesize-(thesize%16)+16
    elif thesize <=256:
        return thesize-(thesize%32)+32
    elif thesize<=512:
        return thesize-(thesize%64)+64
    else:
        raise Exception("to do")
        return -1

def get_jemalloc_cache_sizes():
    return [8]+[16, 32, 48, 64, 80, 96, 112, 128]+[160, 192, 224, 256]+[320, 384, 448, 512]+[640, 768, 896, 1024]+[1280, 1536, 1792, 2048]
def get_cache_size2(thesize):
    alist=get_jemalloc_cache_sizes()
    for idx,value in enumerate(alist):
        if value>=thesize:
            return alist[idx]
    raise Exception("out of consideration")


# def gen_perspective_pair()


ckxsolver=z3.Solver()
sym_oob_offset = z3.Int("sym_oob_offset")
sym_victim_cache_size  = z3.Int("sym_victim_cache_size")
sym_ptr_offset = z3.Int("sym_ptr_offset")
checkme1 = sym_oob_offset - sym_victim_cache_size == sym_ptr_offset
ckxsolver.add(checkme1)

solvers = []

vulnerable_obj_cache_size = 160

if __name__ =="__main__":
    minimalbannersize,ptroffset=getbanner_info()
    offsetdict,victim_obj_list=get_useful_oob_info()
    count=0
    for obj in victim_obj_list:
        thevictim_size=get_struct_cache_size(obj)
        for oob_offset in offsetdict:
            count+=1
            print (count)
            ckxsolver=z3.Solver()
            sym_oob_offset = z3.Int("sym_oob_offset")
            sym_victim_cache_size  = z3.Int("sym_victim_cache_size")
            sym_ptr_offset = z3.Int("sym_ptr_offset")
            checkme1 = sym_oob_offset - sym_victim_cache_size == sym_ptr_offset
            ckxsolver.add(checkme1)
            checkme2 = sym_victim_cache_size > minimalbannersize
            ckxsolver.add(checkme2)
            checkme3 = sym_victim_cache_size == vulnerable_obj_cache_size
            ckxsolver.add(checkme3)
            ckxsolver.add(thevictim_size==sym_victim_cache_size)
            ckxsolver.add(ptroffset==sym_ptr_offset)
            ckxsolver.add(oob_offset==sym_oob_offset)
            # print ckxsolver
            print "%d - %d=%d ?= %d"%(oob_offset,thevictim_size,oob_offset-thevictim_size,ptroffset)
            # if oob_offset==88 and thevictim_size==48:
                # import IPython
                # IPython.embed()
            if z3.sat==ckxsolver.check():
                import os
                import sys
                print("find one .....")
                print offsetdict[oob_offset]
                print obj
                sys.exit(-1)
                # result.append()

    print("not found !")

    # print get_cache_size(109)
    # first_size=get_cache_size2(minimalbannersize)
    # alist=get_jemalloc_cache_sizes()
    # idx_start=alist.find(first_size)
    # for iii in alist[idx_start:]:
    #     alist[iii]=alist


    