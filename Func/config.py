import configparser




config = configparser.ConfigParser()   # 创建对象
config.read("config.ini", encoding="utf-8")  # 读取配置文件，如果配置文件不存在则创建

def getKeysValue(section):
    return config.items(section)

def getsystemIndex():
    return int(config.get('system', 'index'))  # 获取指定节点的指定key的value

def setsystemIndex(index):
    if isinstance(index,int):
        config.set("system", "index", str(index))
        config.write(open('config.ini', 'w'))
