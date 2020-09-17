# -*-coding:utf-8-*-
import ssl
import urllib.request
import easygui as g

def start():
    host = 'https://jisuip.market.alicloudapi.com'
    path = '/ip/location'
    method = 'GET'
    appcode = 'ad4f8f46057e479a97476f3a4357272a'
    query = g.textbox(msg='请输入ip地址',title='IP地址查询')
    #print(query)
    querys = 'ip=' + str(query)
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


