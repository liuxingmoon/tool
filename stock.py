# -*-coding:utf-8-*-
import ssl
import urllib.request
import easygui as g

def start():
    host = 'http://stock.market.alicloudapi.com'
    path = '/sz-sh-stock-history'
    method = 'GET'
    appcode = 'ad4f8f46057e479a97476f3a4357272a'
    query = g.multenterbox(msg='输入需要查询的时间和股票代码',title='股票K线查询',fields=['股票代码','开始时间','结束时间'],values=['','',''])
    querys = 'begin=%s&code=%s&end=%s' %(query[1],query[0],query[2])
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


