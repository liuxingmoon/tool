import re
import easygui as g

def start():
	path = g.fileopenbox(msg='打开需要提取链接的文件，生成的链接文件在桌面',title='提取迅雷链接')
	names = re.findall(r'\d+',path)#获取链接中数字
	name = names[-1]#获取最后一个数字
	#print(name)
	file = r'C:\Users\Administrator\Desktop\\' + str(name) + '.txt'
	r = open(file,'w')#用来存储结果的
	with open(path,'r') as f:
		for line in f:
			result = re.findall(r'magnet:.+',line)#返回的链接是list
			try:#有空行，会出现空list
				r.write(result[0] + '\n')
			except IndexError as reason:
				print('有空行:' + str(reason))
				continue
	r.close()#关闭
