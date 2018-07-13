# coding=utf-8

#这段代码主要使用selenium模块，使用Firefox里的geckodriver来打开一个网页，并截图

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys

#如果需要在没有界面的后台运行，在webdriver.firefox()时，需要加上参数环境
from selenium.webdriver import FirefoxOptions
opts = FirefoxOptions()
opts.add_argument("-headless")
#driver = webdriver.Firefox()
driver = webdriver.Firefox(firefox_options=opts)

driver.get("http://www.96369.net")

#assert "百度" in driver.title
#elem = driver.find_element_by_name("wd")
#elem.send_keys("Eastmount")
#elem.send_keys(Keys.RETURN)
#assert "No resultes found" in driver.title


StrTime=time.strftime("%Y%m%d_%H_%M_%S",time.localtime(time.time()))
fileName="..\..\Pic_"+StrTime+".png"

driver.save_screenshot(fileName)
driver.close()
#driver.quit()