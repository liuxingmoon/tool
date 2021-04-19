# -*- coding: utf-8 -*- 
#SVN的目录有中文 
#svn的命令传英文路径没有问题，中文路径由于编码问题会出现乱码 
#中文路径是utf-8的编码，传给SVN会出现乱码，识别不了 
#windows的中文编码是gbk. svn的中文路径需要转化为gbk的编码才能识别 
#cmd_gbk=cmd.encode("gbk") 

import time 
import os
import svnconfig
import easygui as g



closeOption = svnconfig.setting['closeOption']

def update(dist):
    cmd = 'TortoiseProc.exe /command:update /path '+ dist + ' /notempfile' + closeOption
    result = os.system(cmd)
    if result == 0:
        print('svn update success')
    else:
        g.msgbox(title='SVN更新',msg="svn update fail")
        
def add(dist):
    cmd = 'TortoiseProc.exe /command:add /path '+ dist + ' /notempfile' + closeOption
    result = os.system(cmd)
    if result == 0:
        print('svn add success')
    else:
        g.msgbox(title='SVN提交',msg="svn add fail")

def commit(dist):
    cmd = 'TortoiseProc.exe /command:commit /path '+ dist + ' /notempfile' + closeOption
    result = os.system(cmd)
    if result == 0:
        print('svn commit success')
    else:
        g.msgbox(title='SVN提交',msg="svn commit fail")