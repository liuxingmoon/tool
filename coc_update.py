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
'Coclog_src':r'E:\Program Files\Python\Python38\works\tool\coclog.txt',
'configpath_src':r"E:\Program Files\Python\Python38\works\tool\Config.ini",
'ddpath_src':r'D:\Program Files\DundiEmu\DunDiEmu.exe'
}

dest_worker02 = {
'dir_dest':r"\\worker02\\tool\\",
'Coclog_dest':r'D:\Program Files\Python38\works\tool\\coclog.txt',
'configpath_dest':r"D:\Program Files\Python38\works\tool\\Config.ini",
'ddpath_dest':r'D:\Program Files\DundiEmu\\DunDiEmu.exe'
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
    #替换
    file_ctrl.replace(src['Coclog_src'],dest['Coclog_dest'],'coc_script.py')
    file_ctrl.replace(src['configpath_src'],dest['configpath_dest'],'coc_script.py')
    file_ctrl.replace(src['ddpath_src'],dest['ddpath_dest'],'coc_script.py')
    file_ctrl.replace(src['configpath_src'],dest['configpath_dest'],'coc_template.py')
    os.chdir(src['dir_src'])#返回原始目录

    
def start():
    update(src_makise,dest_worker02)

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