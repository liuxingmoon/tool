#用于打包py文件为exe
import os
import easygui as g
from file_ctrl import copy_file

def start():
    pack_path = g.fileopenbox(msg='选择需要打包的py执行文件',title='打包py文件')
    result = pack_path.rpartition("\\")#将结果切分为3段
    pack_dir = result[0]#打包文件目录
    pack_file = result[-1]#打包文件
    pack_ico = g.fileopenbox(msg='选择ico图标文件',title='打包py文件')
    pack_ico = pack_ico.rpartition("\\")
    pack_ico_dir = pack_ico[0]#图标目录
    pack_ico_file = pack_ico[-1]#图标文件
    copy_file(pack_ico_file,pack_ico_dir,pack_dir)#拷贝图标到py文件目录
    os.chdir(pack_dir)#切换到py文件目录
    os.system("pyinstaller -Fwi %s %s" %(pack_ico_file,pack_file))
    
