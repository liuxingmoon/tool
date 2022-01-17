#用于处理文件
import os
import win32com
from win32com.client import Dispatch

# 处理Word文档的类
class RemoteWord:
    def __init__(self, filename=None):
        self.xlApp = win32com.client.Dispatch('Word.Application') # 此处使用的是Dispatch，原文中使用的DispatchEx会报错
        self.xlApp.Visible = 0 # 后台运行，不显示
        self.xlApp.DisplayAlerts = 0  #不警告
        if filename:
            self.filename = filename
            if os.path.exists(self.filename):
                self.doc = self.xlApp.Documents.Open(filename)
            else:
                self.doc = self.xlApp.Documents.Add()  # 创建新的文档
                self.doc.SaveAs(filename)
        else:
            self.doc = self.xlApp.Documents.Add()
            self.filename = ''
  
    def add_doc_end(self, string):
        '''在文档末尾添加内容'''
        rangee = self.doc.Range()
        rangee.InsertAfter('\n' + string)
  
    def add_doc_start(self, string):
        '''在文档开头添加内容'''
        rangee = self.doc.Range(0, 0)
        rangee.InsertBefore(string + '\n')
  
    def insert_doc(self, insertPos, string):
        '''在文档insertPos位置添加内容'''
        rangee = self.doc.Range(0, insertPos)
        if (insertPos == 0):
            rangee.InsertAfter(string)
        else:
            rangee.InsertAfter('\n' + string)
  
    def replace_doc(self, string, new_string):
        '''替换文字'''
        self.xlApp.Selection.Find.ClearFormatting()
        self.xlApp.Selection.Find.Replacement.ClearFormatting()
        #(string--搜索文本,
        # True--区分大小写,
        # True--完全匹配的单词，并非单词中的部分（全字匹配）,
        # True--使用通配符,
        # True--同音,
        # True--查找单词的各种形式,
        # True--向文档尾部搜索,
        # 1,
        # True--带格式的文本,
        # new_string--替换文本,
        # 2--替换个数（全部替换）
        self.xlApp.Selection.Find.Execute(string, False, False, False, False, False, True, 1, True, new_string, 2)
  
    def replace_docs(self, string, new_string):
        '''采用通配符匹配替换'''
        self.xlApp.Selection.Find.ClearFormatting()
        self.xlApp.Selection.Find.Replacement.ClearFormatting()
        self.xlApp.Selection.Find.Execute(string, False, False, True, False, False, False, 1, False, new_string, 2)
    def save(self):
        '''保存文档'''
        self.doc.Save()
  
    def save_as(self, filename):
        '''文档另存为'''
        self.doc.SaveAs(filename)
  
    def close(self):
        '''保存文件、关闭文件'''
        self.save()
        self.xlApp.Documents.Close()
        self.xlApp.Quit()
  
  
#重命名文件
def rename(filename_last,filename_new):
    try:
        os.rename(filename_last,filename_new)
    except FileExistsError as reason:
        #如果已有备份，就删掉以前备份，重新备份
        print("已存在文件:%s"%(filename_new))
    
#拷贝文件
def copy_file(filename,src_dir,dest_dir):
    curdir = os.getcwd()#当前目录
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
    os.chdir(curdir)#返回原始目录
    
    
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
    f=open(file_name,'r')
    new_file=open('%s.tmp' % file_name,'w')#临时文件
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
    
def replace_utf8(old_text,new_text,file_name):
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
