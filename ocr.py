# coding=utf-8
import sys
import json
import base64
import easygui as g
import win32clipboard
import win32gui
from win32.lib import win32con
import configparser

# 保证兼容python2以及python3
IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

# 防止https证书校验不正确
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#配置文件路径
configpath = r"Config.ini"
config = configparser.ConfigParser()
config.read(configpath, encoding="utf-8")
#启动id范围
APP_ID = config.get("ocr", "APP_ID")
API_KEY = config.get("ocr", "API_KEY")
SECRET_KEY = config.get("ocr", "SECRET_KEY")
OCR_URL = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic'
"""  TOKEN start """
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'
'''
OCR_URL = config.get("ocr", "SECRET_KEY")
TOKEN_URL = config.get("ocr", "SECRET_KEY")
APP_ID = '24192605'
API_KEY = '006FMhOUkFsgMVcDnzYFc0nH'
SECRET_KEY = '0dU16pxoGsogXXAdV0GfoAVspotht1U2'
'''


def send_msg_to_clip(type_data, msg):
    """
    操作剪贴板分四步：
    1. 打开剪贴板：OpenClipboard()
    2. 清空剪贴板，新的数据才好写进去：EmptyClipboard()
    3. 往剪贴板写入数据：SetClipboardData()
    4. 关闭剪贴板：CloseClipboard()

    :param type_data: 数据的格式，
    unicode字符通常是传 win32con.CF_UNICODETEXT
    :param msg: 要写入剪贴板的数据
    """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(type_data, msg)
    win32clipboard.CloseClipboard()
    
"""
    获取token
"""
def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print(err)
    if (IS_PY3):
        result_str = result_str.decode()
    result = json.loads(result_str)

    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not 'brain_all_scope' in result['scope'].split(' '):
            print ('please ensure has check the  ability')
            exit()
        return result['access_token']
    else:
        print ('please overwrite the correct API_KEY and SECRET_KEY')
        exit()

"""
    读取文件
"""
def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')
        return f.read()
    except:
        print('read image file fail')
        return None
    finally:
        if f:
            f.close()


"""
    调用远程服务
"""
def request(url, data):
    req = Request(url, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()
        if (IS_PY3):
            result_str = result_str.decode()
        return result_str
    except  URLError as err:
        print(err)

def start(image):
    # 获取access token
    token = fetch_token()

    # 拼接通用文字识别高精度url
    image_url = OCR_URL + "?access_token=" + token
    text = ""

    # 读取书籍页面图片
    file_content = read_file(image)

    # 调用文字识别服务
    result = request(image_url, urlencode({'image': base64.b64encode(file_content)}))

    # 解析返回结果
    result_json = json.loads(result)
    for words_result in result_json["words_result"]:
        text = text + words_result["words"]
    text = text.replace(';',';\n').replace('。','。\n')#有分号和句号换行
    if text != '':#如果识别到文字，弹出文字识别窗口
        # 打印文字
        g.msgbox(msg=text,title='文字识别')
        send_msg_to_clip(win32con.CF_UNICODETEXT, text)
    else:
        print('没有识别到文字')

