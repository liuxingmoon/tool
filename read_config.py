import socket

#当前服务器名
servername = socket.gethostname()
configpath = r'\\%s\\tool\\Config.ini' %(servername)
