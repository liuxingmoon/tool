# coding: utf8
# @Author: 郭 璞
# @File: capture.py
# @Time: 2017/7/24
# @Contact: 1064319632@qq.com
# @blog: http://blog.csdn.net/marksinoberg
# @Description: 根据鼠标移动进行划屏截图
import pyHook
import pythoncom
import win32gui
from PIL import Image, ImageGrab
from win32api import GetSystemMetrics as gsm
# 提前绑定鼠标位置事件
old_x, old_y = 0, 0
new_x, new_y = 0, 0
def hotkey(key=None):
  """绑定热键，开始进行划屏截图操作"""
  pass
def on_mouse_event(event):
  global old_x, old_y, new_x, new_y, full, hm
  if event.MessageName == "mouse left down":
    old_x, old_y = event.Position
  if event.MessageName == "mouse left up":
    new_x, new_y = event.Position
    # 解除事件绑定
    hm.UnhookMouse()
    hm = None
  # 划屏
  if full:
    image = ImageGrab.grab((0, 0, gsm(0), gsm(1)))
  else:
    image = ImageGrab.grab((old_x, old_y, new_x, new_y))
  image.show()
full = False
hm = None
def capture():
  hm = pyHook.HookManager()
  hm.SubscribeMouseAll(on_mouse_event)
  hm.HookMouse()
  pythoncom.PumpMessages()
capture()