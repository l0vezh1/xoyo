from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np
import math
import random
def click_locxy(dr,element,xy):
    if xy=='':
        return
    data=xy.split(',')
    x=int(data[0])
    y=int(data[1])
    ActionChains(dr).move_to_element_with_offset(element,x,y).click().perform()



def drag(dr,element,xy):
    data=xy.split(',')
    x=int(data[0])
    y=int(data[1])
    '''0 太右
    45 太左
    '''
    distance=x-38
    track_list = get_track(distance)
    time.sleep(2)
    
    ActionChains(dr).move_to_element_with_offset(element,7,203).click_and_hold().perform()
    time.sleep(0.2)
    for track in track_list:
        ActionChains(dr).move_by_offset(xoffset=track,yoffset=0).perform()
    time.sleep(random.randint(2,5)/10)
    x=random.randint(1,5)
    '''
    # 模拟人工滑动超过缺口位置返回至缺口的情况，数据来源于人工滑动轨迹，同时还加入了随机数，都是为了更贴近人工滑动轨迹
    ActionChains(dr).move_by_offset(xoffset=-x-2, yoffset=0).perform() 
    time.sleep(random.randint(6,10)/10)
    ActionChains(dr).move_by_offset(xoffset=x, yoffset=0).perform()
    '''
    # 放开圆球
    ActionChains(dr).pause(random.randint(6,14)/10).release().perform()
    time.sleep(2)




def get_track(distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 0.7
        # 计算间隔
        t = 0.1
        # 初速度
        v = 0

        while current < distance:
            if current < mid:
                # 加速度为正2
                a = 40
            else:
                # 加速度为负3
                a = -24
            # 初速度v0
            v0 = v
            # 当前速度v = v0 + at
            v = v0 + a * t
            # 移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
            #print('forword', current, distance)

        v = 0

        print(current,distance)
        move = distance - current
        # 加入轨迹
        track.append(round(move))


        return track
'''
def get_track(distance):
    track=[]
    current=0
    mid=distance*3/4
    t=random.randint(2,4)/10
    v=0
    while current<distance:
          if current<mid:
             a=2
          else:
             a=-3
          v0=v
          v=v0+a*t
          move=v0*t+1/2*a*t*t
          current+=move
          track.append(round(move))
    return track
'''
