import urllib.request
import urllib.parse#用于编码data
import json#用于解析json
import time
import easygui as g
#import zlib
'''
data = {
    'from': 'zh',
    'to': 'en',
    'query': '爬虫',
    'transtype': 'translang',
    'simple_means_flag': '3',
    'sign': '253813.474180',
    'token': '444fe02f6bf65d9b8a1158b0a41d3893',
    'domain': 'common'
    }




data = urllib.parse.urlencode(data).encode('utf-8')#编码
url = 'https://fanyi.baidu.com/v2transapi?from=zh&to=en'
try:
    response = urllib.request.urlopen(url,data)
    html = response.read().decode('utf-8')
except urllib.error.HTTPError as error:
    print(zlib.decompress(error.read()))
#返回401错误，百度要登录授权
    '''


'''
#防隐藏方法一 ,User-Agent
header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    }
'''
def start():
    while True:
        content = g.textbox(msg='请输入需要翻译的内容',title='翻译')
        if content == '':
            break
        data = {
            'i': content,
            'from':'AUTO',
            'to':'AUTO',
            'smartresult':'dict',
            'client':'fanyideskweb',
            'salt':'15865082095429',
            'sign':'0bb7901b4fdce48e90ac89ef5e1d1e96',
            'ts':'1586508209542',
            'bv':'52e219b107829df251d81c3ece9b6c69',
            'doctype':'json',
            'version':'2.1',
            'keyfrom':'fanyi.web',
            'action':'FY_BY_CLICKBUTTION'
            #'typoResult':'false'
            }
        data = urllib.parse.urlencode(data).encode('utf-8')#编码
        #url = 'http://fanyi.youdao.com/translate_0?smartresult=dict&smartresult=rule'
        #_o反爬虫，去掉后可以读取
        url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
        req = urllib.request.Request(url,data)
        #防屏蔽方法二
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36')
        try:
            response = urllib.request.urlopen(req)
            html = response.read().decode('utf-8')
            result = json.loads(html)
            g.msgbox(msg=result['translateResult'][0][0]['tgt'])
        except urllib.error.HTTPError as error:
            print(error.read())
            time.sleep(5)


