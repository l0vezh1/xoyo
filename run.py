import os
from Func.process import process
import Func.config


userdata = []


def writeStatus(data, code):
    file = None
    if code == 0:
        file = open("成功用户数据.csv", 'a',encoding='UTF-8')
        pass
    if code == 1:
        file = open("失败用户数据.csv", 'a',encoding='UTF-8')
        pass
    if code == 2:
        file = open("失败用户数据.csv", 'a',encoding='UTF-8')
        pass
    if code == 3:
        file = open("未知错误用户数据.csv", 'a',encoding='UTF-8')
        pass
    file.write('{},{},{},{}\n'.format(data[0], data[1], data[2], data[3]))
    file.close()


def read_CSV():
    for line in open("userdata.csv", encoding='UTF-8'):
        data = line.strip('\n').split(',')
        userdata.append(data)


if __name__ == "__main__":
    '''
    Chrome version = 79
    '''
    read_CSV()

    p = process()

    index = Func.config.getsystemIndex()
    while index < len(userdata):
        data = userdata[index]
        os.system('cls')
        print("验证码剩余点数: {}".format(process.Captchaclient.get_left_point()))
        print("当前第 {} / {} 账号: {} 密码: {} 姓名： {} ID ：{}".format(
            index+1,len(userdata), data[0], data[1], data[2], data[3]))
        p.run(data[0], data[1], data[2], data[3])

        # 显示记录
        # 写入文件 Index
        writeStatus(data, p.code)
        Func.config.setsystemIndex(index)

        index += 1
    
    print("完成 按任意键退出")
    input()
