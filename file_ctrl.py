#用于处理文件
import os


def copy_file(filename,src_dir,dest_dir):
    try:
        #切换到目的目录
        os.chdir(dest_dir)
    except NotADirectoryError as reason:
        #不是目录，写的是文件名字，过滤掉最后的文件名作为路径目录
        dest_dir = dest_dir.split('\\')
        dest_dir.pop(-1)
        dest_dir = ",".join(dest_dir).replace(',','\\')#将列表连接为str
        #切换到目的目录
        os.chdir(dest_dir)
    except FileNotFoundError as reason:
        #没有目录，直接新建
        os.mkdir(dest_dir)
        #切换到目的目录
        os.chdir(dest_dir)
    #获取文件名
    #file_name = src_file.split('\\')[-1]
    #备份目的目录文件
    if filename in os.listdir():
        try:
            os.rename(filename,"%s.bak" % (filename)) #文件备份
        except FileExistsError as reason:
            #如果已有备份，就删掉以前备份，重新备份
            os.remove("%s.bak" %(filename))
            os.rename(filename,"%s.bak" % (filename)) #文件备份
    #复制源文件到目的目录,路径必须用双引号括起来，应该是cmd的格式要求
    #os.system('copy /y "%s" "%s"' %(src_file,dest_dir))
    src_path = src_dir + os.sep + filename
    dest_path = dest_dir + os.sep + filename
    #方法一：使用os的拷贝
    #os.system('copy /y "%s" "%s"'%(src_path , dest_path))
    #方法二：使用python拷贝文件，更通用各个平台
    with open(src_path,"rb") as src_file:
        with open(dest_path,"wb") as dest_file:
            while True:
                #循环读取源文件到目标文件
                data = src_file.read(1024)#一次只读1024字节
                if data:#如果存在数据，不是空，就写入到目标文件
                    dest_file.write(data)
                else:
                    break# 空文件跳过
    
    
#恢复
def resume(filename,dest_dir):    
    try:
        #切换到目的目录
        os.chdir(dest_dir)
    except NotADirectoryError as reason:
        #不是目录，写的是文件名字，过滤掉最后的文件名作为路径目录
        dest_dir = dest_dir.split('\\')
        dest_dir.pop(-1)
        dest_dir = ",".join(dest_dir).replace(',','\\')#将列表连接为str
        #切换到目的目录
        os.chdir(dest_dir)
    try:
        os.rename("%s.bak"%(filename),filename) #文件备份
    except FileExistsError as reason:
        #如果已有备份，就删掉以前备份，重新备份
        os.remove(filename)
        os.rename("%s.bak"%(filename),filename) #文件备份

def replace(old_text,new_text,file_name):
    f=open(file_name,'r',encoding='utf-8')
    new_file=open('%s.tmp' % file_name,'w',encoding='utf-8')#临时文件
    for line in f.readlines():#f.readlines()返回一个文件迭代器，每次只从文件（硬盘）中读一行
        new_file.write(line.replace(old_text,new_text))#把读出来的行经过替换后直接写入到新的文件
    f.close()
    new_file.close()
    try:
        os.rename(file_name,'%s.bak' % (file_name)) #源文件备份
    except FileExistsError as reason:
        #如果已有备份，就删掉以前备份，重新备份
        os.remove('%s.bak' %(file_name))
        os.rename(file_name,'%s.bak' % (file_name)) #源文件备份
    os.rename('%s.tmp' % (file_name),file_name) #把新文件重命名为源文件
    print('已替换源文件 %s' %(file_name))
