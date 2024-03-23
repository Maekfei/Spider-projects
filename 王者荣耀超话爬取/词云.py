import jieba.posseg as psg
import pandas
from wordcloud import WordCloud
from PIL import Image
from numpy import array
import matplotlib.pyplot as plt

import openpyxl

# 读取 Excel 文件
workbook = openpyxl.load_workbook(r'C:\Users\11579\Desktop\爬虫接单\王者荣耀超话爬取\data\上官婉儿.xlsx')
worksheet = workbook.active

# 读取一列数据并拼接成长字符串
column_data = [str(cell.value) for cell in worksheet['A']]
s = ''.join(column_data)

result=psg.cut(s)  #利用jieba库进行分词
text_split = []
ban_list = ["儿"]

for x in result:
    if x.flag =="n" or x.flag == "adj":
        if len(x.word)>1:
            text_split.append(x.word)
text_split = pandas.Series(text_split)
articleDict = dict(text_split.value_counts())
print([i for i in articleDict.items()][:8])  #输出出现次数前8的关键词名称及其具体次数


pic = Image.open("王者荣耀.jpeg")  #打开蒙版图片
picarray = array(pic)
word = WordCloud(background_color="white",
                 width=800,  #设置宽度
                 height=800,  #设置长度
                 font_path='msyh.ttf',  #字体文件
                 max_words=100,  #词云中显示的词汇书数量
                 mask=picarray,  #蒙版
                 ).generate_from_frequencies(articleDict)
word.to_file('上官婉儿.png')
print("词云图片已保存")
plt.figure(figsize=(10, 10))
# 展示图片
plt.imshow(word)  # 使用plt库显示图片
plt.axis("off")
plt.show()
