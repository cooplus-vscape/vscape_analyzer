#coding:utf-8

def dropuntil(longstring, keyword):
    assert longstring.find(keyword) >= 0
    idx = longstring.find(keyword) + len(keyword)
    return longstring[idx:]

def ru(longstring, keyword):
    assert longstring.find(keyword) >= 0
    idx = longstring.find(keyword) + len(keyword)
    return longstring[:idx]
    
def rud(longstring, keyword):
    assert longstring.find(keyword) >= 0
    idx = longstring.find(keyword)
    return longstring[:idx]
