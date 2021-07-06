import base64
import easygui as g
import tkinter as tk
from clip_ctrl import clip

def encode_base64():
    msg = text1.get('1.0','end')
    code = msg.encode('utf-8')
    code = base64.b64encode(code)
    clip(code.decode('utf-8'))
    g.msgbox(msg=code)

def encode_file():
    path = g.fileopenbox(msg='选择需要编码的文件',title='打开文件')
    f = open(path,"rb")
    code = base64.b64encode(f.read())
    clip(code.decode('utf-8'))
    g.msgbox(msg=code)

def decode_base64():
    msg = text1.get('1.0','end')
    code = msg.encode('utf-8')
    code = base64.b64decode(code)
    clip(code.decode('utf-8'))
    g.msgbox(msg=code)
    
def start():    
    try:
        root = tk.Tk()#实例化一个Tkinter
        root.title('编码解码base64')
        w1 = tk.Message(root, text='请在下方输入需要转码的内容', width=500)
        w1.pack(side='top',pady=10)
        global text1
        text1 = tk.Text(root, width=150, height=20)  # 宽100字符，高20行
        text1.pack(side='top')
        encode_bt = tk.Button(root,text='编码base64',width=20,command=encode_base64)
        encode_bt.pack(side='left',padx=50,pady=10)
        encode_file_bt = tk.Button(root,text='从文件编码',width=20,command=encode_file)
        encode_file_bt.pack(side='left',padx=50,pady=10)
        decode_bt = tk.Button(root,text='解码base64',width=20,command=decode_base64)
        decode_bt.pack(side='left',padx=50,pady=10)
        cancel_bt = tk.Button(root,text='退出',width=20,command=root.destroy)
        cancel_bt.pack(side='right',padx=50,pady=10)
        root.mainloop()
    except:
        root.destroy()
        