import pandas as pd
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"
    }


if __name__ == '__main__':

    url = "http://www.tianqihoubao.com/lishi/nanchang/month/202112.html"
    html = requests.get(url,headers = headers)
    soup = BeautifulSoup(html.content,'html.parser')
    df = pd.read_html(url, header=0,encoding ="gbk")[0]
    print(df)
    df.to_csv("气象.csv")
