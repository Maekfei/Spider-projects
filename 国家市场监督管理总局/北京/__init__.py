import time

from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from xlrd import open_workbook
from xlutils.copy import copy

url_search = 'http://scjgj.beijing.gov.cn/cxfw/'


#调用selenium工具
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(executable_path=r"", options=options)

driver.get(url_search)
while True:
    elements = driver.find_elements_by_css_selector("a.cxxx.huxi")
    for element in elements:
        content = []
        driver.execute_script("arguments[0].click();", element)
        time.sleep(3)
        driver.switch_to.window(driver.window_handles[-1])
        url = driver.current_url
        print(url)

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")
        for k in soup.select("div.container table.table_sjcx tbody tr"):
            content.append(k.text)
            print(k.text)
        r_xls = open_workbook("北京.xlsx")  # 读取excel文件
        row = r_xls.sheets()[0].nrows  # 获取已有的行数
        excel = copy(r_xls)  # 将xlrd的对象转化为xlwt的对象
        worksheet = excel.get_sheet(0)  # 获取要操作的sheet
        # 对excel表追加一行内容
        for i in range(len(content)):
            worksheet.write(row, i, content[i])  # 括号内分别为行数、列数、内容

        excel.save("北京.xlsx")  # 保存并覆盖文
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    element1 = driver.find_element_by_css_selector("#pagestart > a:nth-child(1)")
    driver.execute_script("arguments[0].click();", element1)
