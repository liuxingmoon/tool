#同步tool工具代码给amadeus
import os
import file_ctrl

src_file = r"E:\Program Files\Python\Python38\works\\tool\*.py"
dest_dir = r"\\Amadeus\\tool\\"
#coc_script
Coclog_src = r'E:\Program Files\Python\Python38\works\tool\coclog.txt'
configpath_src = r"E:\Program Files\Python\Python38\works\tool\Config.ini"
ddpath_src = r'D:\Program Files\DundiEmu\DunDiEmu.exe'

Coclog_dest = r'D:\Program Files\Python38\works\tool\\coclog.txt'
configpath_dest = r"D:\Program Files\Python38\works\tool\\Config.ini"
ddpath_dest = r'D:\Program Files\DundiEmu\\DunDiEmu.exe'

def start():
    #复制文件并覆盖源文件
    file_ctrl.copy(src_file,dest_dir)
    #替换
    file_ctrl.replace(Coclog_src,Coclog_dest,'coc_script.py')
    file_ctrl.replace(configpath_src,configpath_dest,'coc_script.py')
    file_ctrl.replace(ddpath_src,ddpath_dest,'coc_script.py')
    file_ctrl.replace(configpath_src,configpath_dest,'coc_template.py')
