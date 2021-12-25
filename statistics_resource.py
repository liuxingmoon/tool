#农信统计故障设备
import easygui as g
import re,os

def start():
    resource_info = g.textbox(msg='输入需要统计的资源信息',title='资源信息统计')
    cpu_info = re.findall("\d.*核",resource_info)
    cpu_info = [ int(x.strip('核')) for x in cpu_info]
    cpu_info = sum(cpu_info)#统计cpu数量
    
    mem_info = re.findall("/\d.*[g,G]",resource_info)
    mem_info = [ int(x.strip('[/,g,G]')) for x in mem_info]
    mem_info = sum(mem_info)#统计内存大小
    
    if cpu_info == mem_info == 0:
        disk_info = re.findall("\d.*",resource_info)
        disk_info = [ int(x) for x in disk_info]
        disk_info = sum(disk_info)
    else:
        disk_info = 0

    with open('report_resource.txt','w') as rp:
        rp.write("cpu核数：" + str(cpu_info) + '\n' + "内存大小：" + str(mem_info) + '\n' + "磁盘大小：" + str(disk_info) )
    os.system('report_resource.txt')