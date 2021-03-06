import subprocess as sub
import tkinter as tk

def poweroff_time():
    value = int(listbox.get(listbox.curselection())*3600)  # 选择光标的值
    print(value)
    sub.Popen(r'shutdown -f -s -t %s' %(value),shell=True)

def cancelpoweroff_time():
    sub.Popen(r'shutdown -a',shell=True)

def getcmd():
    cmd = cmdbox.get()  # 获取到输入框的信息
    if cmd == "":
        cmd = r'shutdown /f /s /t 00'
    return (cmd)

def poweroff_time1(cmd):
    timebox = editbox.get()#获取到输入框的信息
    w1,w2,w3,w4,w5,w6,w7 = "","","","","","",""#初始化为空
    flagsID = []
    for n in flags:
        flagsID.append(n.get())
    print(flagsID)
    if (flagsID[0] == 1):
        if(flagsID[1] == flagsID[2] == flagsID[3] == flagsID[4] == flagsID[5] ==flagsID[6] == 0):
            w1 = "M"
        else:
            w1 = "M,"
    if flagsID[1] == 1:
        if(flagsID[2] == flagsID[3] == flagsID[4] == flagsID[5] ==flagsID[6] == 0):
            w2 = "T"
        else:
            w2 = "T,"
    if flagsID[2] == 1:
        if(flagsID[3] == flagsID[4] == flagsID[5] ==flagsID[6] == 0):
            w3 = "w"
        else:
            w3 = "w,"
    if flagsID[3] == 1:
        if(flagsID[4] == flagsID[5] ==flagsID[6] == 0):
            w4 = "Th"
        else:
            w4 = "Th,"
    if flagsID[4] == 1:
        w5 = "F"
        if(flagsID[5] ==flagsID[6] == 0):
            w5 = "F"
        else:
            w5 = "F,"
    if flagsID[5] == 1:
        if(flagsID[6] == 0):
            w6 = "S"
        else:
            w6 = "S,"
    if flagsID[6] == 1:
        w7 = "Su"            
    
    print(timebox,w1,w2,w3,w4,w5,w6,w7)
    #删掉所有未更改的日期
    weekday = [w1,w2,w3,w4,w5,w6,w7]
    for n in weekday:
        if n == "":
            weekday.remove(n)
    days = len(weekday)
    
    if cmd == 'shutdown':
        sub.Popen(r'at %s /every:%s shutdown -f -s -t 00' % (timebox, w1 + w2 + w3 + w4 + w5 + w6 + w7), shell=True)
    elif cmd == 'restart':
        sub.Popen(r'at %s /every:%s shutdown -f -r -t 00' % (timebox, w1 + w2 + w3 + w4 + w5 + w6 + w7), shell=True)
    else:
        sub.Popen(r'at %s /every:%s %s' % (timebox, w1 + w2 + w3 + w4 + w5 + w6 + w7,cmd), shell=True)

def cancelpoweroff_time1():
    sub.Popen(r'at /yes /delete',shell=True)
    

def start():
    global listbox
    root = tk.Toplevel()
    root.title('定时关机')
    title = tk.Label(root,text='定时关机').grid(row=0,column=2)

    #延时关机
    time_text = tk.Label(root,
                    text = '延时关机',
                    justify='left',#左对齐
                    padx=5,
                    pady=5,
                    compound='left',width=15)
    time_text.grid(row=1,column=1,padx=10,pady=10)

    timelist_frame = tk.Frame(root)
    timelist_frame.grid(row=1,column=2,padx=10,pady=10)
    timebt_frame = tk.Frame(root)
    timebt_frame.grid(row=1,column=3,padx=10,pady=10)

    #滚动条
    time_scrollerbar = tk.Scrollbar(timelist_frame)
    time_scrollerbar.pack(side='right',fill='y')#靠右填充

    listbox = tk.Listbox(timelist_frame,selectmode='single',#多选
                         height=5,  # 默认只有10行，如果选项大于10项会被遮蔽
                         yscrollcommand=time_scrollerbar.set)#设置启用滚动条，可以滚轮滚动列表
    for item in range(0,49,1):
        listbox.insert('end',0.5*item)#每次插入到最后一个index
    listbox.pack(side='left',fill='both')
    time_scrollerbar.config(command=listbox.yview)#绑定滚动条给列表框的y轴view（可以鼠标点击拉动滚动条）

    timeoff_bt = tk.Button(timebt_frame,text='延时关机',command=poweroff_time,width=15)
    timeoff_bt.pack()
    timecancel_bt = tk.Button(timebt_frame,text='取消延时关机',command=cancelpoweroff_time,width=15)
    timecancel_bt.pack()

    #定时周期性关机
    timelist_frame1 = tk.Frame(root)
    timelist_frame1.grid(row=3,column=1,columnspan=2,padx=10)
    timebox_frame1 = tk.Frame(root)
    timebox_frame1.grid(row=3,column=3,padx=10)
    timebt_frame1 = tk.Frame(root)
    timebt_frame1.grid(row=4,column=1,columnspan=3,padx=10,pady=10)

    timeoff_text = tk.Label(root,
                    text = '定时周期性关机',
                    justify='left',#左对齐
                    padx=5,
                    compound='left',width=15)
    timeoff_text.grid(row=2,column=1,columnspan=3)

    global timebox,editbox,flags,cmdbox
    #时间框
    editbox = tk.Entry(timebox_frame1)
    editbox.pack(padx=10)
    editbox.delete(0,'end')#删除输入框的内容
    editbox.insert(0,'00:00')#插入文本
    timebox = editbox.get()#获取到输入框的信息

    #命令框
    cmdbox = tk.Entry(timebox_frame1)
    cmdbox.pack(padx=10)
    cmdbox.delete(0,'end')#删除输入框的内容
    cmdbox.insert(0,'shutdown /f /s /t 00')#插入文本
    timebox = cmdbox.get()#获取到输入框的信息

    flags=[]#未选中为0，选中为1
    timelist1 = ['星期一','星期二','星期三','星期四','星期五','星期六','星期日']
    for timelist in timelist1:
        flags.append(tk.IntVar())#每个检查框实例化前，先实例化int值
        checkboxs = tk.Checkbutton(timelist_frame1,text=timelist,variable=flags[-1])
        checkboxs.pack(side='left', anchor='center')  # 横向排列，居中显示

    timeoff_bt1 = tk.Button(timebt_frame1,text='定时周期性关机',command=lambda :poweroff_time1('shutdown'),width=15)
    timeoff_bt1.pack(side='left',padx=15,anchor='center')
    timerestart_bt = tk.Button(timebt_frame1,text='定时周期性重启',command=lambda :poweroff_time1('restart'),width=15)
    timerestart_bt.pack(side='left',padx=15, anchor='center')
    cmd_bt = tk.Button(timebt_frame1,text='定时执行命令',command=lambda :poweroff_time1(getcmd()),width=15)
    cmd_bt.pack(side='left',padx=15, anchor='center')
    timecancel_bt1 = tk.Button(timebt_frame1,text='取消所有定时命令',command=cancelpoweroff_time1,width=15)
    timecancel_bt1.pack(side='left',padx=15, anchor='center')

    root.mainloop()







