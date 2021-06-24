#²Ù×÷config
import configparser

#¶Á
def config_read(configpath,tag,key):
    config = configparser.ConfigParser()
    config.read(configpath, encoding="utf-8")
    values = config.get(tag, key)
    return (values)
#Ð´    
def config_write(configpath,tag,key,values):
    config = configparser.ConfigParser()
    config.read(configpath, encoding="utf-8")
    config.set(tag, key, flag_reboot, values)
    config.write(open(configpath, "w",encoding='utf-8'))