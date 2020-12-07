import tkinter as tk
import math
import easygui as g
import ssl
import urllib.request


#用于将prefix换算为ip数和掩码
def tran_pfx(prefix):
    bin_arr = ['0' for i in range(32)]
    prefix = int(prefix)
    for i in range(prefix):
        bin_arr[i] = '1'
        tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
        tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
        mask = '.'.join(tmpmask)
    n = 32 - prefix
    ip_nums = int(math.pow(2,n))
    ip_nums_useable = ip_nums - 2
    ip_nums_useable_ali = ip_nums - 4
    return (prefix,mask,ip_nums,ip_nums_useable,ip_nums_useable_ali)

#计算ip,返回一个endip
def ip_calc(ip,ip_nums):
    ips = ip.split('.')#将ip切分为4段列表
    ip = [int(x) for x in ips]#转换列表元素为int
    ip[-1] += ip_nums
    #从后往前依次计算ip地址4个网段，进位递归加1
    for n in [-1,-2,-3]:
        up = ip[n] // 256
        if up >= 1:#进位
            ip[n-1] += up
            ip[n] = (ip[n] % 256)
            ip = [str(x) for x in ip]#转换列表元素为str
            ip = ','.join(ip).replace(',','.')#将列表中所有str元素连接在一起转换为str
            return (ip_calc(ip,0))#递归
    ip = [str(x) for x in ip]  # 转换列表元素为str
    ip = ','.join(ip).replace(',', '.')  # 将列表中所有str元素连接在一起转换为str
    return (ip)


#用于计算掩码
def start():
    try:
        def getinfo():
            info = netmask_entry.get()
            return (info)
        def ipPos_query():
            ipquery = getinfo()
            host = 'https://jisuip.market.alicloudapi.com'
            path = '/ip/location'
            method = 'GET'
            appcode = 'ad4f8f46057e479a97476f3a4357272a'
            # print(query)
            querys = 'ip=' + str(ipquery)
            bodys = {}
            url = host + path + '?' + querys
            request = urllib.request.Request(url)
            request.add_header('Authorization', 'APPCODE ' + appcode)
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            response = urllib.request.urlopen(request, context=ctx)
            content = response.read().decode('utf-8')
            g.msgbox(msg=content)

        def netMask_calc():
            info = getinfo()
            if info.isdigit():#如果返回字符全是数字
                info = tran_pfx(info)
                (prefix,mask,ip_nums,ip_nums_useable,ip_nums_useable_ali) = info
                g.msgbox(msg='%d位\n掩码为：%s\n占用ip数为%d\n可用ip数为%d\n阿里云可用ip数为%d' %(prefix,mask,ip_nums,ip_nums_useable,ip_nums_useable_ali))
            elif '/' not in info:#如果返回没有'/'，纯掩码
                mask = info.split('.')
                length = 0
                x = 0
                #计算掩码长度
                for x in range(4):
                    mask[x] = int(mask[x])#转换成int
                    if (255 & mask[x]) == 255:#如果结果为255，说明这8位全为1，掩码长度加8
                        length += 8
                    else:#如果不为255，说明此8位不是全为1，255-maxk[x] +1= 256-maxk[x]，计算以2为底的log值，用8减去log值，就是此8位1的个数
                        length += (8-math.log(256-mask[x],2))
                n = 32 - int(length)
                ip_nums = int(math.pow(2, n))
                ip_nums_useable = ip_nums - 2
                ip_nums_useable_ali = ip_nums - 4
                g.msgbox(msg='%d位\n掩码为：%s\n占用ip数为%d\n可用ip数为%d\n阿里云可用ip数为%d' % (int(length),info,ip_nums,ip_nums_useable, ip_nums_useable_ali))
            elif '/' in info:#如果返回有'/',格式是IP/prefix
                info = info.split('/')
                #计算掩码
                prefix = info[-1]
                result = tran_pfx(prefix)
                (prefix, mask, ip_nums, ip_nums_useable, ip_nums_useable_ali) = result
                #计算ip
                ip_start = info[0]
                ip_end = ip_calc(ip_start,ip_nums)
                g.msgbox(msg='%d位\nIP地址从 %s 到 %s \n掩码为：%s\n占用ip数为%d\n可用ip数为%d\n阿里云可用ip数为%d' % (
                prefix,ip_start,ip_end, mask, ip_nums, ip_nums_useable, ip_nums_useable_ali))

                #g.msgbox(msg=int(length))

        root = tk.Tk()
        root.title('掩码计算+公网ip地址地理分析')

        netmask_label = tk.Label(root, text='掩码或者公网ip地址')
        netmask_label.grid(row=0, column=1, sticky='w',padx=10,pady=10)  # 左对齐
        netmask_entry = tk.Entry(root)
        netmask_entry.insert(0,'192.168.0.0/24')#插入初始化文本
        netmask_entry.grid(row=0, column=2,padx=10,pady=10)

        ipPos_bt = tk.Button(root,text='查询ip地址', width=10, command=ipPos_query)
        ipPos_bt.grid(row=1,column=1)
        netmaak_bt = tk.Button(root,text='计算掩码', width=10, command=netMask_calc)
        netmaak_bt.grid(row=1, column=2)

        root.mainloop()
    except:
        root.destroy()