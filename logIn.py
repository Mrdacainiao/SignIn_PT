from selenium import webdriver
import time
import json
import logging
import ddddocr

from downloadPicture import download_pic
from signIn import sign_in

username = 'zxftx'
password = '11111111h'
urlPic = 'yzm.png'


def browser_initial():
    browser = webdriver.Chrome()
    url = 'http://pterclub.com/index.php'
    return url, browser


# 手动登录获取cookie
def get_cookies(url, browser):
    browser.get(url)
    time.sleep(30)
    dictCookies = browser.get_cookies()
    jsonCookies = json.dumps(dictCookies)
    with open('cookies', 'a') as f:
        f.write(jsonCookies)
    print('cookie save success：' + url)
    # logging.info('cookie save success：' + url)


def add_cookie(browser):
    with open('cookies', 'r', encoding='utf8') as f:
        listCookies = json.loads(f.read())

    for cookie in listCookies:
        cookie_dict = {
            'path': cookie.get('path'),
            'domain': cookie.get('domain'),
            # 'expiry': cookie.get('expiry'),
            'secure': cookie.get('secure'),
            'httpOnly': cookie.get('httpOnly'),
            'name': cookie.get('name'),
            'value': cookie.get('value')
        }
        browser.add_cookie(cookie_dict)
    browser.refresh()
    return browser

def log_in_with_cookie():
    url, browser = browser_initial()
    browser.get(url)
    browser = add_cookie(browser)
    return browser
    # browser.refresh()


def log_in(url, browser):
    # assert isinstance(browser, webdriver.Chrome())
    browser.get(url)
    time.sleep(5)
    browser.find_element_by_name('username').send_keys(username)
    time.sleep(1)
    browser.find_element_by_name('password').send_keys(password)
    time.sleep(1)

    # 输入验证码
    # 获取验证码图片URL
    yzmUrl = browser.find_element_by_xpath('//*[@id="nav_block"]/form[2]/table/tbody/tr[3]/td[2]/img').get_attribute(
        'src')
    # 下载图片
    download_pic(yzmUrl)
    # 识别验证码图片
    yzm = deal_picture(urlPic)
    # 输入验证码
    browser.find_element_by_name('imagestring').send_keys(yzm)
    time.sleep(1)
    # 登录
    browser.find_element_by_xpath('//*[@id="nav_block"]/form[2]/table/tbody/tr[10]/td/input[1]').click()

def deal_picture(url_pic):
    ocr = ddddocr.DdddOcr(old=True)
    with open(url_pic, 'rb') as f:
        image_bytes = f.read()
    res = ocr.classification(image_bytes)
    return res


def log_in_with_password():
    url, browser = browser_initial()
    log_in(url, browser)
    return browser





if __name__ == '__main__':
    browser = log_in_with_cookie()
    # browser = log_in_with_password()
    sign_in(browser)
    time.sleep(10)