# -*- coding: utf-8 -*-
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import keyboard as key
from user import user
import easygui as g
from user import user

pos = {
  'username':[917,475],
  'passwd':[914,547],
  'submit':[944,705]
  }


def click(x,y):
    key.mouse_click(x,y)
    time.sleep(2)

def text(t):
    for n in t:
        key.press_key(n)
    time.sleep(1)

    #B站刷抽奖
def bili(username,password):
    driver = webdriver.Chrome()#模拟浏览器打开网站
    driver.get(curl)
    driver.maximize_window() #将窗口最大化
    time.sleep(2)#延时加载


    try:
     #登录
     driver.find_element_by_css_selector("#chat-control-panel-vm > div > div.chat-input-ctnr.p-relative > div > p > span").click()
     time.sleep(2)#延时加载
     click(pos['username'][0],user['username'][1])
     text(username)
     click(pos['passwd'][0],user['passwd'][1])
     text(password)
     click(pos['submit'][0],user['submit'][1])
     time.sleep(10)#延时加载
     
     '''
     driver.find_element_by_id("content").click()
     driver.find_element_by_id('login-username').send_keys(username)
     driver.find_element_by_id("login-passwd").send_keys(password)
     time.sleep(2)#延时加载
     driver.find_element_by_id("login-submit").click()
     '''
     
    except:
     print('登录失败')
     #刷弹幕
    while True:
        try:
         driver.find_element_by_css_selector("#chat-control-panel-vm > div > div.chat-input-ctnr.p-relative > div > textarea").send_keys(keyword)
         driver.find_element_by_css_selector("#chat-control-panel-vm > div > div.bottom-actions.p-relative > div.right-action.p-absolute.live-skin-coloration-area > button").click()
        except:
         print('刷弹幕失败')

    #企鹅电竞刷抽奖
def tencent(username,password):
    driver = webdriver.Chrome()#模拟浏览器打开网站
    driver.get(curl)
    driver.maximize_window() #将窗口最大化
    time.sleep(2)#延时加载

    try:
     #登录
     driver.find_element_by_css_selector("#__layout > div > div.gui-navbar.gui-navbar-bg > div > div.gui-navbar-fr > a.gui-navbar-login > span").click()
     time.sleep(2)#延时加载
     #再来登录一次保险
     driver.find_element_by_css_selector("#__layout > div > div.gui-navbar.gui-navbar-bg > div > div.gui-navbar-fr > a.gui-navbar-login > span").click()
     time.sleep(2)#延时加载
     #切换登录框
     driver.switch_to.frame("_egame_login_frame_qq_")#切换登录框
     time.sleep(2)#延时加载
     driver.switch_to.frame("ptlogin_iframe")#切换登录框
     time.sleep(2)#延时加载
     #QQ密码登录
     driver.find_element_by_css_selector("#switcher_plogin").click()
     time.sleep(2)#延时加载
     #账号
     driver.find_element_by_id('u').send_keys(username)
     #密码
     driver.find_element_by_id("p").send_keys(password)
     #登录按钮
     driver.find_element_by_id("login_button").click()
     time.sleep(2)#延时加载
     driver.switch_to.default_content()#切换到最上层
    except:
     print('登录失败')
     #刷弹幕
    while True:
        try:
         driver.find_element_by_css_selector("#live-right-chat > div.chat.has-color-panel > div.chat-inputbox-wrap.has-guard > div.chat-inputbox > input[type=text]").send_keys(keyword)
         driver.find_element_by_css_selector("#live-right-chat > div.chat.has-color-panel > div.chat-inputbox-wrap.has-guard > div.chat-inputbox > i.icon-send").click()
         time.sleep(6)#延时加载
        except:
         print('刷弹幕失败')

def start():
    global keyword,curl
    keyword = g.textbox(msg='请输入抽奖口令！')
    curl = g.textbox(msg='请输入抽奖网页地址！')
    if (curl.split('/')[2] == 'live.bilibili.com'):
        bili(user['bili_phone'][0],user['bili_phone'][1])
    elif (curl.split('/')[2] == 'egame.qq.com'):
        tencent(user['qq1'][0],user['qq1'][1])









    
