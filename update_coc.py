#同步tool工具代码给amadeus
import os

src_dir = r"E:\Program Files\Python\Python38\works\\tool\\"
dest_dir = r"\\Amadeus\\tool\\"
#dest_dir = "D:\\"

def start():
    os.chdir(src_dir)
    os.system('copy /y coc_script.py %s' %(dest_dir))
    '''
    #切换目录
    os.system('cd %s' %dest_dir)
    file = []
    with open(r'coc_script.py','r',encoding='utf-8') as f:
        file = f.readlines()
        file_index = file.index('#日志路径\n')
        file[file_index + 1] = "Coclog = r'D:\Program Files\Python38\works\\tool\coclog.txt'"
        file[file_index + 2] = "configpath = r'D:\Program Files\Python38\works\\tool\Config.ini'"'
        file[file_index + 3] = "ddpath = r'D:\Program Files\DundiEmu\DunDiEmu.exe'"
        f.write(file)
    '''