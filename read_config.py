import socket,os
from config_ctrl import *

#当前服务器名
servername = socket.gethostname()
configpath = r'\\%s\\tool\\Config.ini' %(servername)
if os.path.isfile(configpath) == False:#如果tool没有在网络路径上（未分享）
    configpath = r"D:\\Program Files\\Python38\\works\\tool\\Config.ini"
minid = int(config_read(configpath,"coc","minid"))
maxid = max([int(x.strip('dundi').rstrip('.rar')) for x in os.listdir(r'D:\Program Files\DundiEmu\DundiData\avd\\') if x != 'vboxData'])
QQlists = config_read(configpath,"coc", "QQlists").split()
baidulists = config_read(configpath,"coc", "baidulists").split()
kunlunlists = config_read(configpath,"coc", "kunlunlists").split()

def get_resourceids(server_name):
    #server_name = [ 'server01','server02','server03' ]
    try:
        resourceids = config_read(r'\\%s\\tool\\Config.ini'%(server_name),'coc','resourceids').split()
    except:
        resourceids = []
    return (resourceids)
