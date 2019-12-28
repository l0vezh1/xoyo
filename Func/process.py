import platform
import time
import json
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from Func.captcha import Chaoren
from Func.controller import *
from fake_useragent import UserAgent


class process():

    Captchaclient = Chaoren()

    def __init__(self):
        self.options = Options()
        # self.options.add_argument('--headless')

        self.options.add_argument('disable-infobars')
        self.options.add_argument("--incognito")
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('user-agent=' + UserAgent().random)
        self.driver = self.getWebDrive()
        self.driver.set_window_size(1024, 960)
        self.driver.get("https://www.baidu.com")

        self.username = None
        self.passwd = None
        self.name = None
        self.ID = None
        self.Success = True

    def getWebDrive(self):
        sys = platform.system()
        if sys == "Windows":
            print("OS is Windows!!!")
            return webdriver.Chrome('./chromedriver.exe', chrome_options=self.options)

        elif sys == "Linux":
            print("OS is Linux!!!")
            return webdriver.Chrome('./chromedriver', chrome_options=self.options)
        else:
            pass

    def run(self, account, pwd, name, id):
        self.username = account
        self.passwd = pwd
        self.name = name
        self.ID = id
        # 0登录成功 1 登陆失败 2 实名失败 3 未知失败
        self.Success = True
        self.code = 0

        self.Openpage()
        self.checkCaptchaType()
        self.isLoginSuccess()
        self.antiAddiction()
        self.issubmitSuccess()
        self.close()

    def close(self):
        self.driver.delete_all_cookies()
        self.driver.close()
        self.driver.switch_to_window(self.driver.window_handles[0])

    def Openpage(self):
        try:
            print("打开登录页面")

            newwindow = 'window.open("https://passport.xoyo.com/signin")'
            self.driver.execute_script(newwindow)
            self.driver.switch_to_window(self.driver.window_handles[1])
            time.sleep(5)
            self.driver.find_element_by_id(
                'sigin_account').send_keys(self.username)
            self.driver.find_element_by_id(
                'sigin_pwd').send_keys(self.passwd)

            # 定位到要悬停的元素
            # 对定位到的元素执行鼠标悬停操作
            print("等待2秒 点击登录按钮")
            time.sleep(0.5)
            submit_button = self.driver.find_element_by_id('sigin_login')
            submit_button.click()
            time.sleep(2)
        except Exception as e:
            self.Success = False
            self.code = 3
            print(e)

    def getResultofCaptcha(self):
        imgdata = open('captcha.png', 'rb').read()
        res = process.Captchaclient.recv_byte(imgdata)
        print(res[u'result'])  # 识别结果
        return res

    def isLoginSuccess(self):
        if '登录' in self.driver.title:
            captchaBox = self.driver.find_element_by_xpath(
                '/html/body/div[3]/div[2]')
            if captchaBox.size['height'] != 0:
                self.code = 3
                self.Success = False
                captchaBox.screenshot(
                    "Log\Failed\{}.png".format(self.username))
                return False
            if captchaBox.size['height'] == 0:
                self.code = 1
                self.Success = False
                return False
        return True

    def text(self):

        newwindow = 'window.open("https://www.geetest.com/demo/slide-bind.html")'
        self.driver.execute_script(newwindow)
        # 移动句柄，对新打开页面进行操作
        self.driver.switch_to_window(self.driver.window_handles[1])
        submit_button = self.driver.find_element_by_id('btn')
        submit_button.click()
        time.sleep(2)
        captchaBox = self.driver.find_element_by_xpath('/html/body/div/div[2]')
        captchaBox.screenshot('captcha.png')
        result = self.getResultofCaptcha()
        data = json.loads(json.dumps(result))
        data = data['result']
        data = data.split(';')
        for i in data:
            if i == '':
                data.remove(i)
        print("验证码{}".format(data))
        if len(data) == 1:
            drag(self.driver, captchaBox, data[0])

        if len(data) != 1:
            for vars in data:
                print("等待1秒 点击{}".format(vars))
                time.sleep(1)
                click_locxy(self.driver, captchaBox, vars)

            print("等待1秒 点击提交按钮")
            time.sleep(1)
            summitButton = self.driver.find_element_by_xpath(
                '/html/body/div[3]/div[2]/div[6]/div/div/div[3]/a/div')
            summitButton.click()

        time.sleep(2)

    def checkCaptchaType(self):
        try:
            if not self.Success:
                return

            print("等待2秒 等待生成验证码")
            time.sleep(2)
            if '个人中心' in self.driver.title:
                return 0

            captchaBox = self.driver.find_element_by_xpath(
                '/html/body/div[3]/div[2]')
            captchaBox.screenshot('captcha.png')
            result = self.getResultofCaptcha()
            jsondata = json.loads(json.dumps(result))
            data = jsondata['result']
            data = data.split(';')
            for i in data:
                if i == '':
                    data.remove(i)
            print("验证码{}".format(data))

            # 点击验证码
            if "请在下图依次点击" in captchaBox.text:
                if len(data) != 1:
                    for vars in data:
                        print("等待1秒 点击{}".format(vars))
                        time.sleep(1)
                        click_locxy(self.driver, captchaBox, vars)

                    print("等待1秒 点击提交按钮")
                    time.sleep(1)
                    summitButton = self.driver.find_element_by_xpath(
                        '/html/body/div[3]/div[2]/div[6]/div/div/div[3]/a/div')
                    summitButton.click()
            else:
                # 滑动验证码
                if len(data) == 1:
                    drag(self.driver, captchaBox, data[0])
                if len(data) != 1:
                    self.Success = False
                    self.code = 3
                    process.Captchaclient.report_err(jsondata['imgId'])
                    print("滑动验证码 识别错误 上报")
                    return

            time.sleep(2)

        except Exception as e:
            self.Success = False
            self.code = 3
            print(e)

    def antiAddiction(self):
        try:
            if not self.Success:
                return

            print("打开防沉迷页面")
            self.driver.get("https://i.xoyo.com/anti-addiction")

            if '登录' in self.driver.title:
                self.Success = False
                return 0

            # 未实名
            element = self.driver.find_element_by_xpath(
                '//*[@id="app"]/section/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[7]')

            if '您已经提交了防沉迷信息' in element.text:
                element.screenshot('Log\Success\{}.png'.format(self.username))
                return 0

            if '提交' in element.text:
                print("填入 姓名 : {}".format(self.name))
                self.driver.find_element_by_xpath(
                    '//*[@id="app"]/section/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[7]/section[1]/form/div[1]/div/div/input').send_keys(self.name)
                print("填入 ID : {}".format(self.ID))
                time.sleep(1)
                self.driver.find_element_by_xpath(
                    '//*[@id="app"]/section/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[7]/section[1]/form/div[2]/div/div[1]/input').send_keys(self.ID)
                print("等待1秒 点击提交")
                time.sleep(0.5)
                submit_button = self.driver.find_element_by_xpath(
                    '//*[@id="app"]/section/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[7]/section[1]/form/div[3]/div/button')
                submit_button.click()
                time.sleep(2)

        except Exception as e:
            self.Success = False
            self.Success = 3
            print(e)

    def issubmitSuccess(self):
        try:
            if not self.Success:
                return

            print("打开防沉迷页面")
            self.driver.get("https://i.xoyo.com/anti-addiction")

            if '登录' in self.driver.title:
                self.Success = False
                return 0

            # 获取element
            element = self.driver.find_element_by_xpath(
                '//*[@id="app"]/section/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[7]')

            if '您已经提交了防沉迷信息' in element.text:
                element.screenshot(
                    'Log\Success\{}.png'.format(self.username))
                return 0

            if '提交' in element.text:
                element.screenshot(
                    'Log\Failed\{}.png'.format(self.username))
                self.Success = False
                self.code = 2

        except Exception as e:
            self.Success = False
            self.Success = 3
            print(e)
