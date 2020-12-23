#同步tool工具代码给amadeus
import os
import file_ctrl


src_dir = r"E:\Program Files\Python\Python38\works\\tool\\"
src_file = r"E:\Program Files\Python\Python38\works\\tool\*.py"
dest_dir = r"\\Amadeus\\tool\\"
#coc_script
Coclog_src = r'E:\Program Files\Python\Python38\works\tool\coclog.txt'
configpath_src = r"E:\Program Files\Python\Python38\works\tool\Config.ini"
ddpath_src = r'D:\Program Files\DundiEmu\DunDiEmu.exe'

Coclog_dest = r'D:\Program Files\Python38\works\tool\\coclog.txt'
configpath_dest = r"D:\Program Files\Python38\works\tool\\Config.ini"
ddpath_dest = r'D:\Program Files\DundiEmu\\DunDiEmu.exe'


#获取目录下文件
def get_files(dir):
    file_list = os.listdir(dir)
    print(file_list)
    return (file_list)
    
def start():
    os.chdir(src_dir)#返回原始目录
    filelist = get_files(src_dir)
    #复制文件并覆盖源文件
    for filename in filelist:
        if ("py" in filename) and ("pyc" not in filename):#以py结尾的文件
            file_ctrl.resume(filename,dest_dir)
    #替换
    os.chdir(src_dir)#返回原始目录