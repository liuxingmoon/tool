#同步tool工具代码给amadeus
import os
import file_ctrl
from multiprocessing import Process as p
import time




#coc_scriptdir_src = r"E:\Program Files\Python\Python38\works\\tool\\"
#src_file = r"E:\Program Files\Python\Python38\works\\tool\*.py"
'''
dir_src = r"E:\Program Files\Python\Python38\works\\tool\\"
Coclog_src = r'E:\Program Files\Python\Python38\works\tool\coclog.txt'
configpath_src = r"E:\Program Files\Python\Python38\works\tool\Config.ini"
ddpath_src = r'D:\Program Files\DundiEmu\DunDiEmu.exe'

dir_dest = r"\\Amadeus\\tool\\"
Coclog_dest = r'D:\Program Files\Python38\works\tool\\coclog.txt'
configpath_dest = r"D:\Program Files\Python38\works\tool\\Config.ini"
ddpath_dest = r'D:\Program Files\DundiEmu\\DunDiEmu.exe'

dest_old_dir = r"\\oldman\\tool\\"
Coclog_old_dest = r'C:\Program Files\Python38\project\tool\\coclog.txt'
configpath_old_dest = r"C:\Program Files\Python38\project\tool\\Config.ini"
ddpath_old_dest = r'C:\Program Files\DundiEmu\\DunDiEmu.exe'
'''

src_makise = {
'dir_src':r"E:\Program Files\Python\Python38\works\\tool\\",
'backup_config_worker02':r"E:\Program Files\Python\Python38\works\\tool\\backup_worker02\\",
'backup_config_worker03':r"E:\Program Files\Python\Python38\works\\tool\\backup_worker03\\",
'Coclog_src':r'E:\Program Files\Python\Python38\works\\tool\\coclog.txt',
'configpath_src':r"E:\Program Files\Python\Python38\works\tool\Config.ini",
'ddpath_src':r'D:\Program Files\DundiEmu\DunDiEmu.exe',
'resourceids':r"resourceids = [x for x in resourceids_work01 if x not in donateids_for_paid]"
}

dest_worker02 = {
'dir_dest':r"\\worker02\\tool\\",
'Coclog_dest':r'D:\Program Files\Python38\works\tool\\coclog.txt',
'configpath_dest':r"D:\Program Files\Python38\works\tool\\Config.ini",
'ddpath_dest':r'D:\Program Files\DundiEmu\\DunDiEmu.exe',
'resourceids':r"resourceids = [x for x in resourceids_work02 if x not in donateids_for_paid]"
}

dest_worker03 = {
'dir_dest':r"\\worker03\\tool\\",
'Coclog_dest':r'D:\Program Files\Python38\works\tool\\coclog.txt',
'configpath_dest':r"D:\Program Files\Python38\works\tool\\Config.ini",
'ddpath_dest':r'D:\Program Files\DundiEmu\\DunDiEmu.exe',
'resourceids':r"resourceids = [x for x in resourceids_work03 if x not in donateids_for_paid]"
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
    #替换
    file_ctrl.replace(src['Coclog_src'],dest['Coclog_dest'],'coc_script.py')
    file_ctrl.replace(src['configpath_src'],dest['configpath_dest'],'coc_script.py')
    file_ctrl.replace(src['ddpath_src'],dest['ddpath_dest'],'coc_script.py')
    file_ctrl.replace(src['resourceids'],dest['resourceids'],'coc_script.py')
    file_ctrl.replace(src['resourceids'],dest['resourceids'],'coc.py')
    file_ctrl.replace(src['configpath_src'],dest['configpath_dest'],'coc_template.py')
    file_ctrl.replace(src['configpath_src'],dest['configpath_dest'],'ocr.py')
    #更新coc_customer.csv stock_info.csv到各个机器
    file_ctrl.copy_file('coc_customer.csv',src['dir_src'],dest['dir_dest'])
    file_ctrl.copy_file('stock_info.csv',src['dir_src'],dest['dir_dest'])
    os.chdir(src['dir_src'])#返回原始目录

def backup_config(src,dest_dir):
    file_ctrl.copy_file('Config.ini',src['dir_dest'],dest_dir)
    os.chdir(src_makise['dir_src'])#返回原始目录

    
def start():
    update(src_makise,dest_worker02)
    update(src_makise,dest_worker03)
    backup_config(dest_worker02,src_makise['backup_config_worker02'])
    backup_config(dest_worker03,src_makise['backup_config_worker03'])

    '''
    filelist = get_files(dir_src)
    #复制文件并覆盖源文件
    for filename in filelist:
        if ("py" in filename) and ("pyc" not in filename):#以py结尾的文件
            #process_copy = p(target=file_ctrl.copy_file,args=(filename,dir_src,dir_dest))
            #process_copy.start()
            file_ctrl.copy_file(filename,dir_src,dir_dest)
            #file_ctrl.copy_file(filename,dir_src,dest_old_dir)
    #替换
    file_ctrl.replace(src['Coclog_src'],Coclog_dest,'coc_script.py')
    file_ctrl.replace(src['configpath_src'],configpath_dest,'coc_script.py')
    file_ctrl.replace(src['ddpath_src'],ddpath_dest,'coc_script.py')
    file_ctrl.replace(src['configpath_src'],configpath_dest,'coc_template.py')
    os.chdir(dir_src)#返回原始目录

    file_ctrl.replace(Coclog_src,Coclog_old_dest,'coc_script.py')
    file_ctrl.replace(configpath_src,configpath_old_dest,'coc_script.py')
    file_ctrl.replace(ddpath_src,ddpath_old_dest,'coc_script.py')
    file_ctrl.replace(configpath_src,configpath_old_dest,'coc_template.py')
    os.chdir(dir_src)#返回原始目录
    '''