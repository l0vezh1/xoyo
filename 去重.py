import os

userdata=[]
def read_CSV():
    for line in open("成功用户数据.csv", encoding='UTF-8'):
        data = line.strip('\n').split(',')
        if not data in userdata:
            userdata.append(data)
    
def write_CSV():
    file = open("成功用户数据.csv", 'w',encoding='UTF-8')
    for data in userdata:
        file.write('{},{},{},{}\n'.format(data[0], data[1], data[2], data[3]))
    file.close()


if __name__ == "__main__":
    read_CSV()
    write_CSV()
    print("完成 按任意键退出")
    input()