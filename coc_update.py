#同步tool工具代码给amadeus
import os
import file_ctrl
from multiprocessing import Process as p
import time


src_makise = {
'dir_src':r"E:\Program Files\Python\Python38\works\\tool\\",
'backup_config_worker02':r"E:\Program Files\Python\Python38\works\\tool\\backup_worker02\\",
'backup_config_worker01':r"E:\Program Files\Python\Python38\works\\tool\\backup_worker01\\",
'Coclog_src':r'E:\Program Files\Python\Python38\works\\tool\\coclog.txt',
'configpath_src':r"E:\Program Files\Python\Python38\works\tool\Config.ini",
'ddpath_src':r'D:\Program Files\DundiEmu\DunDiEmu.exe',
'resourceids':r"x for x in resourceids_work01"
}

dest_worker02 = {
'dir_dest':r"\\worker02\\tool\\",
'Coclog_dest':r'D:\Program Files\Python38\works\tool\\coclog.txt',
'configpath_dest':r"D:\Program Files\Python38\works\tool\\Config.ini",
'ddpath_dest':r'D:\Program Files\DundiEmu\\DunDiEmu.exe',
'resourceids':r"x for x in resourceids_work02"
}

dest_worker01 = {
'dir_dest':r"\\worker01\\tool\\",
'Coclog_dest':r'D:\Program Files\Python38\works\tool\\coclog.txt',
'configpath_dest':r"D:\Program Files\Python38\works\tool\\Config.ini",
'ddpath_dest':r'D:\Program Files\DundiEmu\\DunDiEmu.exe',
'resourceids':r"x for x in resourceids_work01"
}




#获取目录下文件
def get_files(dir):
    file_list = os.listdir(dir)
    print(file_list)
    return (file_list)

def update(src,dest):
    filelist = get_files(src['dir_src'])
    #复制文件并覆盖源文件
    for filename in filelist:
        if ("py" in filename) and ("pyc" not in filename):#以py结尾的文件
            file_ctrl.copy_file(filename,src['dir_src'],dest['dir_dest'])
    os.chdir(dest['dir_dest'])#切换到目标目录

    file_ctrl.replace_utf8(src['resourceids'],dest['resourceids'],'coc_script.py')
    file_ctrl.replace_utf8(src['resourceids'],dest['resourceids'],'coc.py')

    file_ctrl.copy_file('coc_customer.csv',src['dir_src'],dest['dir_dest'])
    file_ctrl.copy_file('stock_info.csv',src['dir_src'],dest['dir_dest'])
    os.chdir(src['dir_src'])#返回原始目录

def backup_config(src,dest_dir):
    file_ctrl.copy_file('Config.ini',src['dir_dest'],dest_dir)
    os.chdir(src_makise['dir_src'])#返回原始目录

    
def start():
    update(src_makise,dest_worker02)
    update(src_makise,dest_worker01)
    backup_config(dest_worker02,src_makise['backup_config_worker02'])
    backup_config(dest_worker01,src_makise['backup_config_worker01'])
