from selenium import webdriver
import chromedriver_binary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def crawler(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(1)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.LINK_TEXT, '賃貸物件')))
    a = driver.find_elements_by_link_text("賃貸物件")
    print(a)
    # search_box = driver.find_element_by_name("q")
    # search_box.send_keys('ChromeDriver')
    # search_box.submit()
    time.sleep(5)
    driver.quit()
