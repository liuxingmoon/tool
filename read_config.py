import socket
from config_ctrl import *

#当前服务器名
servername = socket.gethostname()
configpath = r'\\%s\\tool\\Config.ini' %(servername)


def get_resourceids(server_name):
    #server_name = [ 'server01','server02','server03' ]
    try:
        resourceids = config_read(r'\\%s\\tool\\Config.ini'%(server_name),'coc','resourceids').split()
    except:
        resourceids = []
    return (resourceids)
