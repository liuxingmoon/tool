#同步tool工具代码给amadeus
import os
import file_ctrl
from multiprocessing import Process as p
import time

src_dir = r"E:\Program Files\Python\Python38\works\\tool\\"
src_file = r"E:\Program Files\Python\Python38\works\\tool\*.py"
dest_dir = r"\\Amadeus\\tool\\"
dest_old_dir = r"\\oldman\\tool\\"
#coc_script
Coclog_src = r'E:\Program Files\Python\Python38\works\tool\coclog.txt'
configpath_src = r"E:\Program Files\Python\Python38\works\tool\Config.ini"
ddpath_src = r'D:\Program Files\DundiEmu\DunDiEmu.exe'

Coclog_dest = r'D:\Program Files\Python38\works\tool\\coclog.txt'
configpath_dest = r"D:\Program Files\Python38\works\tool\\Config.ini"
ddpath_dest = r'D:\Program Files\DundiEmu\\DunDiEmu.exe'

Coclog_old_dest = r'C:\Program Files\Python38\project\tool\\coclog.txt'
configpath_old_dest = r"C:\Program Files\Python38\project\tool\\Config.ini"
ddpath_old_dest = r'C:\Program Files\DundiEmu\\DunDiEmu.exe'


#获取目录下文件
def get_files(dir):
    file_list = os.listdir(dir)
    print(file_list)
    return (file_list)
    
def start():
    filelist = get_files(src_dir)
    #复制文件并覆盖源文件
    for filename in filelist:
        if ("py" in filename) and ("pyc" not in filename):#以py结尾的文件
            #process_copy = p(target=file_ctrl.copy_file,args=(filename,src_dir,dest_dir))
            #process_copy.start()
            file_ctrl.copy_file(filename,src_dir,dest_dir)
            #file_ctrl.copy_file(filename,src_dir,dest_old_dir)
    #替换
    file_ctrl.replace(Coclog_src,Coclog_dest,'coc_script.py')
    file_ctrl.replace(configpath_src,configpath_dest,'coc_script.py')
    file_ctrl.replace(ddpath_src,ddpath_dest,'coc_script.py')
    file_ctrl.replace(configpath_src,configpath_dest,'coc_template.py')
    os.chdir(src_dir)#返回原始目录
    '''
    file_ctrl.replace(Coclog_src,Coclog_old_dest,'coc_script.py')
    file_ctrl.replace(configpath_src,configpath_old_dest,'coc_script.py')
    file_ctrl.replace(ddpath_src,ddpath_old_dest,'coc_script.py')
    file_ctrl.replace(configpath_src,configpath_old_dest,'coc_template.py')
    os.chdir(src_dir)#返回原始目录
    '''