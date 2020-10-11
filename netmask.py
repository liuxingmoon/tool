import tkinter as tk
import math
import easygui as g
import ssl
import urllib.request

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
                prefix = int(info)
                bin_arr = ['0' for i in range(32)]
                for i in range(prefix):
                    bin_arr[i] = '1'
                    tmpmask = [''.join(bin_arr[i * 8:i * 8 + 8]) for i in range(4)]
                    tmpmask = [str(int(tmpstr, 2)) for tmpstr in tmpmask]
                    mask = '.'.join(tmpmask)
                g.msgbox(msg=mask)


            else:#如果返回不全是数字（掩码）
                mask = info.split('.')
                len = 0
                x = 0
                #计算掩码长度
                for x in range(4):
                    mask[x] = int(mask[x])#转换成int
                    if (255 & mask[x]) == 255:#如果结果为255，说明这8位全为1，掩码长度加8
                        len += 8
                    else:#如果不为255，说明此8位不是全为1，255-maxk[x] +1= 256-maxk[x]，计算以2为底的log值，用8减去log值，就是此8位1的个数
                        len += (8-math.log(256-mask[x],2))
                g.msgbox(msg=int(len))

        root = tk.Tk()
        root.title('掩码计算+公网ip地址地理分析')

        netmask_label = tk.Label(root, text='掩码或者公网ip地址')
        netmask_label.grid(row=0, column=1, sticky='w')  # 左对齐
        netmask_entry = tk.Entry(root)
        netmask_entry.insert(0,'255.255.255.0')#插入初始化文本
        netmask_entry.grid(row=0, column=2)

        ipPos_bt = tk.Button(root,text='查询ip地址', width=10, command=ipPos_query)
        ipPos_bt.grid(row=1,column=1)
        netmaak_bt = tk.Button(root,text='计算掩码', width=10, command=netMask_calc)
        netmaak_bt.grid(row=1, column=2)

        root.mainloop()
    except:
        root.destroy()