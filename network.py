from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

server = Server("D:\\Program Files\\Python38\\works\\tools\\browsermob-proxy-2.1.4\\bin\\browsermob-proxy.bat")
server.start()
proxy = server.create_proxy()

chrome_options = Options()
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))

driver = webdriver.Chrome(chrome_options=chrome_options)
# 要访问的地址
base_url = "https://3a119.com/play/7696-1-1.html"
proxy.new_har("ht_list2", options={'captureContent': True})

driver.get(base_url)
# 此处最好暂停几秒等待页面加载完成，不然会拿不到结果
time.sleep(3)
result = proxy.har

for entry in result['log']['entries']:
    _url = entry['request']['url']
    print(_url)
    # # 根据URL找到数据接口,这里要找的是 http://git.liuyanlin.cn/get_ht_list 这个接口

    _response = entry['response']
    _content = _response['content']
    # 获取接口返回内容
    print(_response)

server.stop()
