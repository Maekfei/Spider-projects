import time

from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from xlrd import open_workbook
from xlutils.copy import copy

url_search = 'http://117.161.154.157:7011/dc/jsp/dc/industry/query/fooddrug/spschz_info_list.jsp'


#调用selenium工具
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])

driver = webdriver.Chrome(executable_path=r"", options=options)

driver.get(url_search)
#定义一个函数，用来求一个长字符串中 位于某一个字符和另一个字符之间的字符串
def get_data(start,end,text):
    # 找到第一个起始字符的位置
    start_index = text.find(start)

    # 如果找到了起始字符
    if start_index != -1:
        # 找到第一个结束字符的位置
        end_index = text.find(end, start_index + 1)

        # 如果找到了结束字符
        if end_index != -1:
            # 提取子字符串
            substring = text[start_index + 1:end_index]
            #print(substring)
            return substring
count= 0
link = []
for i in range(1,200):
    element1 = driver.find_element_by_css_selector("#taskGrid_next > a:nth-child(1)")
    driver.execute_script("arguments[0].click();", element1)
input()
for i in range(200,504):
    # count += 1
    # print(count)
    # elements1 = driver.find_elements_by_css_selector("tr.odd > td:nth-child(2) > a:nth-child(1)")
    # elements2 = driver.find_elements_by_css_selector("tr.even > td:nth-child(2) > a:nth-child(1)")
    # elements = elements1 + elements2
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    for k in soup.select("tbody tr td.center a"):
        link1 = "http://117.161.154.157:7011/dc/jsp/dc/industry/query/fooddrug/spschz_info_detail.jsp?id="+get_data("('", "')", k.get("href"))[1:]
        print(link1)
        link.append(link1)
    element1 = driver.find_element_by_css_selector("#taskGrid_next > a:nth-child(1)")
    driver.execute_script("arguments[0].click();", element1)


for link2 in link:
    content = []
    driver.get(link2)
    time.sleep(1)
    n = driver.find_elements_by_css_selector("td.fieldInput")
    for i in n:
        if i.text != None:
            content.append(i.text)
        else:
            content.append("无")
    print(content)
    r_xls = open_workbook("内蒙古.xlsx")  # 读取excel文件
    row = r_xls.sheets()[0].nrows  # 获取已有的行数
    excel = copy(r_xls)  # 将xlrd的对象转化为xlwt的对象
    worksheet = excel.get_sheet(0)  # 获取要操作的sheet
    # 对excel表追加一行内容
    for i in range(len(content)):
        worksheet.write(row, i, content[i])  # 括号内分别为行数、列数、内容

    excel.save("内蒙古.xlsx")  # 保存并覆盖文
