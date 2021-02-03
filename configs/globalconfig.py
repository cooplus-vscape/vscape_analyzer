#coding:utf-8
MONGODB_SERVER = '127.0.0.1'
MONGODB_PORT = 27017
PLAYERDB = 'playerDB'
COOPPLUSDB =  'motivation_example' #<===== modify here

CLASSLAYOUT= "classlayout"
CLASSLAYOUTRAW= "classlayoutraw"
VIRTUALFUNCTION = "virtualfunction"
VCALLSITE = "vcallsite"
ACCOUNTINFO = 'accountINFO'
INTERFACEWHITELIST = "interfacewhitelist"
INTERFACEWHITELIST_RE = "interfacewhitelist_re"
GVTFlist = "GVTFlist"
VMETHOD_TO_AN = "vmethodtoan"
TMPDB="tmpdb"
uri = "mongodb://admin:YOURPASSWORD@{serverip}:27017/?authSource=admin&authMechanism=SCRAM-SHA-1".format(serverip=MONGODB_SERVER)

connection_string = "mongodb://%s:%d" % (MONGODB_SERVER, MONGODB_PORT)
connection_string = uri


