from selenium import webdriver
from identify import get_predict
import pytesseract as pt
from PIL import Image
import time as t
import cv2

# 設定
account = "f130481519" # 請輸入自己的帳密
password = "h82836103"
pt.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

date = ""
time = ""
url = ['https://bwd.xuanen.com.tw/wd02.aspx?module=login_page&files=login&PT=1',
       'https://scr.cyc.org.tw/TP07.aspx?module=login_page&files=login&PT=1',
       'https://scr.cyc.org.tw/tp10.aspx?module=login_page&files=login&PT=1']
login = ['https://bwd.xuanen.com.tw/wd02.aspx?module=net_booking&files=booking_place&PT=1',
         'https://scr.cyc.org.tw/TP07.aspx?module=net_booking&files=booking_place&PT=1',
         'https://scr.cyc.org.tw/tp10.aspx?module=net_booking&files=booking_place&PT=1']
name = ['大同運動中心', '蘆洲運動中心', '永和運動中心']

def accept_alert():
    try:
        while True:
            alert = driver.switch_to.alert
            alert.accept()
    except:
        return

def crawler(index):
    driver.get(url[index])
    accept_alert()
    t.sleep(1)
    element = driver.find_element_by_id("ContentPlaceHolder1_loginid")
    element.send_keys(account)
    element = driver.find_element_by_id("loginpw")
    element.send_keys(password)
    driver.save_screenshot("screenshot.png")

    while True:
        img = cv2.imread('screenshot.png', cv2.IMREAD_GRAYSCALE)
        h, w = img.shape
        text = get_predict(img[343:376, 850:930])

        element = driver.find_element_by_id("ContentPlaceHolder1_Captcha_text")
        element.send_keys(text)
        element = driver.find_element_by_id("login_but")
        element.click()
        t.sleep(1)

        # 如果驗證碼判斷錯誤，那就重跑登入流程
        try:
            accept_alert()
            driver.refresh()
            accept_alert()
            element = driver.find_element_by_id("ContentPlaceHolder1_loginid")
            element.send_keys(account)
            element = driver.find_element_by_id("loginpw")
            element.send_keys(password)
            driver.save_screenshot("screenshot.png")
        except:
            break

    driver.get(login[index])
    get_onclick(driver, index)

def get_onclick(driver, index):
    try:
        driver.find_element_by_xpath(f".//img[contains(@onclick, '{date}')]").click()
        driver.find_element_by_xpath(f"//img[contains(@onclick, '{time}')]")
        print(f"{name[index]}\n")
    except:
        s = ""
        link = list(driver.current_url)
        link[-1] = '2'
        for i in link:
            s = s+i
        driver.get(s)
        try:
            driver.find_element_by_xpath(f"//img[contains(@onclick, '{time}')]")
            print(f"{name[index]}\n")
        except:
            s = ""
            link = list(driver.current_url)
            link[-1] = '3'
            for i in link:
                s = s+i
            driver.get(s)
            try:
                driver.find_element_by_xpath(f"//img[contains(@onclick, '{time}')]")
                print(f"{name[index]}\n")
            except:
                return

date = input("請輸入日期:")

time = input("請輸入時間:")

print()

for i in range(len(name)):
    crawler(i)
driver.quit()
