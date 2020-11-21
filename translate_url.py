import re
import easygui as g
import subprocess

def writelist(list,file):
    for line in list:
        #只保留前面的字符，如果一行中有空格，确保把后面字符去掉
        file.write( line.split()[0] + '\n')

def start():
    path = g.fileopenbox(msg='打开需要提取链接的文件',title='提取迅雷链接')
    #names = re.findall(r'\d+',path)#获取链接中数字
    #name = names[-1]#获取最后一个数字
    #print(name)
    name = '提取链接文件'
    file = name + '.txt'
    r = open(file,'w')#用来存储结果的
    with open(path,'r') as f:
        result_thunder = []
        result_http = []
        result_baidu = []
        for line in f:
            try:
                # 提取迅雷链接
                result_thunder.append(re.findall(r'magnet:.+',line)[0]) #re返回的链接是list
            except IndexError as reason:
                print('未匹配到迅雷结果:' + str(reason))
                try:
                    # 提取http链接
                    result_http.append(re.findall(r'http.+', line)[0])  # re返回的链接是list
                except IndexError as reason:
                    print('未匹配到http结果:' + str(reason))
                    try:
                        # 提取百度链接
                        result_baidu.append(re.findall(r'pan.+', line)[0])  # re返回的链接是list
                    except IndexError as reason:
                        print('未匹配到任何链接:' + str(reason))
        writelist(result_thunder,r)
        writelist(result_http,r)
        writelist(result_baidu,r)

    r.close()#关闭
    #打开链接文件
    subprocess.Popen(file, shell=True)
