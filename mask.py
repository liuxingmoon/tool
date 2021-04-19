import tkinter as tk
import subprocess as pcs
import re
import math

#用于开启临时热点
def start():
    try:
        def getinfo():
            ip = ip_entry.get()
            mask = mask_entry.get()
            return (ip,mask)
        def tranMask():
            ip = getinfo()[0]
            mask = getinfo()[1]
            masks = re.findall(r'\d+\.\d+\.\d+\.\d+',mask)[0]
            if masks != "":
                masks.split('.')
            elif mask.isdigit():#如果该字符全是数字
                prefix = mask
                if prefix >= 24 and prefix <=32:
                    mask='255.255.255'
                    math
                mask = []


        def stopWifi():
            pcs.Popen(r'netsh wlan stop hostednetwork')

        root = tk.Tk()
        root.title('掩码转换')

        ip_entry = tk.Entry(root)
        ip_entry.insert(0,'ip')#插入初始化文本
        ip_entry.grid(row=0, column=1,width=10)
        mask_entry = tk.Entry(root)
        mask_entry.insert(0,'掩码')#插入初始化文本
        mask_entry.grid(row=0, column=2,width=5)
        mask_start_bt = tk.Button(root,text='转换掩码', width=10, command=tranMask)
        mask_start_bt.grid(row=1,column=2)


        root.mainloop()
    except:
        root.destroy()