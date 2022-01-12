#读写config配置
import configparser

#读
def config_read(configpath,tag,key):
    config = configparser.ConfigParser()
    config.read(configpath, encoding="utf-8")
    values = config.get(tag, key)
    return (values)
#写
def config_write(configpath,tag,key,values):
    config = configparser.ConfigParser()
    config.read(configpath, encoding="utf-8")
    config.set(tag, key, values)
    config.write(open(configpath, "w",encoding='utf-8'))