import chardet #需要下载该模块
 
def readFile(file_path):
    with open(file_path, 'rb') as f:
        cur_encoding = chardet.detect(f.read())['encoding']
        #print (cur_encoding) #当前文件编码
 
    #用获取的编码读取该文件而不是python3默认的utf-8读取。
    with open(file_path,encoding=cur_encoding) as file:
         fileData = file.readlines()
    return (fileData)