import time
from bs4 import BeautifulSoup
from selenium import webdriver
from xlrd import open_workbook
from xlutils.copy import copy
import eventlet#导入eventlet这个模块
#调用selenium工具
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])
driver = webdriver.Chrome(executable_path=r"chromedriver.exe", options=options)

base_url = "https://s.weibo.com/weibo?q=%E7%8E%8B%E8%80%85%E8%8D%A3%E8%80%80%E8%B6%85%E8%AF%9D%E4%BC%A0%E7%BB%9F%E6%96%87%E5%8C%96&page="


count = 0
driver.get("https://weibo.com/p/100808ccb61d96c8f867d4f6c412e95c4f173a/super_index?current_page=3&since_id=4878245637659820&page=2#1678548112338")
driver.delete_all_cookies()
cookies ={}
for cookie in cookies:
    cookie_dict = {
    'domain': '.weibo.com',
'name': cookie.get('name'),
'value': cookie.get('value'),
"expires": cookie.get('value'),
'path': '/',
'httpOnly': False,
'HostOnly': False,
'Secure': False}
    driver.add_cookie(cookie_dict)
driver.refresh()
for i in range(1,100): #第一页到第100页
    chuantong = []
    temp_height = 0
    url = base_url+str(i) #控制翻页
    driver.get(url)
    time.sleep(5)
    eventlet.monkey_patch()  # 必须加这条代码
    with eventlet.Timeout(10, False):  # 设置超时时间为20秒
        while True:
            # 循环将滚动条下拉
            driver.execute_script("window.scrollBy(0,1000)")
            # sleep一下让滚动条反应一下
            time.sleep(0.05)
            # 获取当前滚动条距离顶部的距离
            check_height = driver.execute_script(
                "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            # 如果两者相等说明到底了
            if check_height >9000:
                break

    elements = driver.find_elements_by_css_selector(
        "div.content p.txt a")
    for i in  elements:
        if "展开" in i.text:
            driver.execute_script("arguments[0].click()",i)

    time.sleep(5)
    html = driver.page_source
    soup = BeautifulSoup(html, "lxml")
    count1 = 0
    for k in soup.select('div.content p.txt'):
        d = k.text
        if "传统文化" in d:
            chuantong.append(d)
            count+=1
            print(d)

        else:
            pass

    r_xls = open_workbook(r"帖子内容.xlsx")  # 读取excel文件
    row = r_xls.sheets()[0].nrows  # 获取已有的行数
    excel = copy(r_xls)  # 将xlrd的对象转化为xlwt的对象
    worksheet = excel.get_sheet(0)  # 获取要操作的sheet
    # 对excel表追加一行内容
    for i in range(len(chuantong)):
        worksheet.write(row, 0, chuantong[i])  # 括号内分别为行数、列数、内容

        row += 1
    excel.save(r"帖子内容.xlsx")  # 保存并覆盖文