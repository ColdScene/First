import os
import time
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#1. 初始化 Chrome 和 Selenium
service = Service(executable_path=r"C:\Users\lenovo\Desktop\iea脚本\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.implicitly_wait(5)  # 隐式等待
wait = WebDriverWait(driver, 10)

# 2. 打开起始页
driver.get("https://www.iea.org/policies?page=205")

# 3. 保存结果的文件
outfile = "policy1.txt"
if os.path.exists(outfile):
    os.remove(outfile)

# 4. 爬取第 1 页内容
html = driver.page_source
soup = BeautifulSoup(html, "html5lib")

def extract_and_save(soup, f):
    divs = soup.find_all('div',
        class_='m-policy-listing-item__col m-policy-listing-item__col--policy')
    for div in divs:
        a = div.find('a')
        if a:
            # 去除换行符，避免写入文件时断行
            text = a.get_text().replace("\n", " ").replace("\r", " ").strip()
            f.write(text + "\n")


'''
def extract_and_save(soup, f):
    divs = soup.find_all('div',
        class_='m-policy-listing-item__col m-policy-listing-item__col--policy')
    for div in divs:
        a = div.find('a')
        if a:
            f.write(a.get_text().strip() + "\n")
'''

with open(outfile, "a", encoding="utf-8") as f:
    extract_and_save(soup, f)

# 5. 循环点击第 2 到 370 页，并提取内容
for page in range(205, 335):
    try:
        # 点击页码
        link = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, str(page))))
        link.click()

        # 等待页面完全加载
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        time.sleep(0.5)

        # 再次等待第一个标题加载完毕
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,
            ".m-policy-listing-item__col--policy a")))

        # 提取 HTML 并写入文件
        html = driver.page_source
        soup = BeautifulSoup(html, "html5lib")
        with open(outfile, "a", encoding="utf-8") as f:
            extract_and_save(soup, f)

        print(f"第 {page} 页数据追加完成")
    except Exception as e:
        print(f"第 {page} 页处理失败:", e)
        continue

# 6. 结束并提示
driver.quit()
print(f"所有数据已保存至：{os.path.abspath(outfile)}")


