from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests
import re
import pymysql
from wordcloud import WordCloud

headers = {
    "Referer": "https://pvp.qq.com/web201605/herolist.shtml",
     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1"
}
resp=requests.get('https://pvp.qq.com/web201605/herolist.shtml')  #����һ����ҳ

soup=BeautifulSoup(resp.content,"html.parser") #����bs4������ҳ

def sum():
    qu=[]
    for k in soup.select('ul.herolist.clearfix a'):
        a = "https://pvp.qq.com/web201605/" + k.get("href") #���ÿһ��Ӣ�۵�������
        qu.append(a)

    name = []  #����Ӣ�����б�
    skill1 = []  #����Ӣ�ۼ����б�
    beidong = [] #����Ӣ�ۼ��ܱ����б�
    coat1 = []  #����Ӣ��Ƥ�����б�
    form1 = [] #����Ӣ���ٻ�ʦ�����б�
    number = []  #����Ӣ������ֵ�б�
    for link in qu:
        hero_link = requests.get(link)

        bea = BeautifulSoup(hero_link.content, "html.parser")

        name1 = bea.find_all("h2")[0].text

        print(name1)
        name.append(name1)

        for skill in bea.find('p', class_='skill-desc'): #������ҳ�ṹ�ҵ�class����Ϊ��skill-desc��
            skill = skill.text[3:]  #ƥ�似������
            skill1.append(skill)
            print(skill)
            break


        for type in bea.select('span.herodetail-sort i'):  #ƥ�䱻����������
            # print(type.get("class"))
            beidong.append(type.get("class"))
            # Ƥ��
        for coat in bea.find_all('ul', class_='pic-pf-list pic-pf-list3'): #ƥ��Ƥ������
            coat = coat['data-imgname']
            coat1.append(coat)


        for form in bea.find_all('p', class_='sugg-name sugg-name3'): #ƥ���ٻ�ʦ����
            form = form.text[5:]
            form1.append(form)

        for width in bea.find_all('i', class_='ibar'):  #ƥ��Ӣ������
            width = width['style'][6:]
            number.append(width)
    life=number[::4]  #��ȡ����ֵ����
    hurt=number[1::4] #��ȡ�˺�����
    show=number[2::4] #��ȡ����Ч������
    hard=number[3::4] #��ȡ�����Ѷ�����

    reserve(name, skill1, coat1, form1, life, hurt, show, hard)
    present(name, life, hurt, show, hard)


def reserve(name, skill, coat, form, life, hurt, show, hard):
    db = pymysql.connect(host='localhost', user='root', password='123456', port=3306, db='wangzhe', autocommit=True)
    cursor = db.cursor()
    for i in range(len(name)):
        sql = """INSERT INTO wangzhe(name,
                     skill,coat,form,life,hurt,show1,hard)
                     VALUES(%s , %s, %s, %s , %s, %s , %s, %s )"""
        data = (name[i], skill[i], coat[i], form[i], life[i], hurt[i], show[i], hard[i])
        cursor.execute(sql, data)
        db.commit()
    cursor.close()
    db.close()
    print("���ڼ���")


def present(name,life,hurt,show,hard):
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    name_list = name
    name_list1 = []
    name_list2 = []
    name_list3 = []
    name_list4 = []
    name_list5 = []
    for i in name_list:
        name_list1.append(i)

    for i in name_list:
        name_list2.append(i)

    for i in name_list:
        name_list3.append(i)

    for i in name_list:
        name_list4.append(i)

    for i in name_list:
        name_list5.append(i)

    num_list = life
    num_list_1 = []
    for i in num_list:
        str1 = i[0:2]
        str2 = int(str1)/100
        num_list_1.append(str2)

    num_list1 = hurt
    num_list_2 = []
    for i in num_list1:
        str1 = i[0:2]
        str2 = int(str1)/100
        num_list_2.append(str2)


    num_list2 = show
    num_list_3 = []
    for i in num_list2:
        str1 = i[0:2]
        str2 = int(str1) / 100
        num_list_3.append(str2)


    num_list3 = hard
    num_list_4 = []
    for i in num_list3:
        str1 = i[0:2]
        str2 = int(str1) / 100
        num_list_4.append(str2)

    num_list_5 = []
    for i in range(len(name_list)):
        num_list_5.append((num_list_1[i]+num_list_2[i]+num_list_3[i]+num_list_4[i])/4)

    for i in range(1, len(num_list_5)):
        for j in range(0, len(num_list_5) - i):
            if num_list_5[j] > num_list_5[j + 1]:
                num_list_5[j], num_list_5[j + 1] = num_list_5[j + 1], num_list_5[j]
                name_list5[j], name_list5[j + 1] = name_list5[j + 1], name_list5[j]

    for i in range(1, len(num_list_1)):
        for j in range(0, len(num_list_1) - i):
            if num_list_1[j] > num_list_1[j + 1]:
                num_list_1[j], num_list_1[j + 1] = num_list_1[j + 1], num_list_1[j]
                name_list1[j], name_list1[j + 1] = name_list1[j + 1], name_list1[j]

    for i in range(1, len(num_list_2)):
        for j in range(0, len(num_list_2) - i):
            if num_list_2[j] > num_list_2[j + 1]:
                num_list_2[j], num_list_2[j + 1] = num_list_2[j + 1], num_list_2[j]
                name_list2[j], name_list2[j + 1] = name_list2[j + 1], name_list2[j]

    for i in range(1, len(num_list_3)):
        for j in range(0, len(num_list_3) - i):
            if num_list_3[j] > num_list_3[j + 1]:
                num_list_3[j], num_list_3[j + 1] = num_list_3[j + 1], num_list_3[j]
                name_list3[j], name_list3[j + 1] = name_list3[j + 1], name_list3[j]

    for i in range(1, len(num_list_4)):
        for j in range(0, len(num_list_4) - i):
            if num_list_4[j] > num_list_4[j + 1]:
                num_list_4[j], num_list_4[j + 1] = num_list_4[j + 1], num_list_4[j]
                name_list4[j], name_list4[j + 1] = name_list4[j + 1], name_list4[j]
    fig = plt.figure(figsize=(50, 10))
    plt.bar(name_list1, num_list_1, label='����', fc='g')
    plt.legend()
    plt.savefig("Ӣ�ۡ�������.png")
    plt.show()

    plt.figure(figsize=(50, 10))
    x = num_list_2
    plt.pie(x)
    plt.pie(x, labels=name_list2)
    plt.savefig("Ӣ�ۡ����˺�.png")
    plt.show()

    plt.figure(figsize=(50, 10))
    x_axis_data = name_list3
    y_axis_data = num_list_3
    plt.plot(x_axis_data, y_axis_data, 'b*--', alpha=0.5, linewidth=1, label='acc')
    plt.legend()  # ��ʾ�����label
    plt.xlabel('Ӣ����')  # x_label
    plt.ylabel('����Ч��')  # y_label
    plt.savefig("Ӣ�ۡ�������Ч��.png")
    plt.show()

    fig = plt.figure(figsize=(50, 10))
    plt.bar(name_list4, num_list_4, label='�����Ѷ�', fc='grey')
    plt.legend()
    plt.savefig("Ӣ�ۡ��������Ѷ�.png")
    plt.show()

    fig = plt.figure(figsize=(50, 10))
    plt.bar(name_list5, num_list_4, label='Ӣ��ƽ��ֵ', fc='pink')
    plt.legend()
    plt.savefig("Ӣ�ۡ�������ƽ��ֵ.png")
    plt.show()

    articleDict = {}
    for i in name_list5:
        articleDict[i] = name_list5.count(i)

    word = WordCloud(background_color="white",
                     width=800,  # ���ÿ��
                     height=800,  # ���ó���
                     font_path='msyh.ttf',  # �����ļ�
                     max_words=100,  # ��������ʾ�Ĵʻ�������
                     ).generate_from_frequencies(articleDict)
    word.to_file('����.png')
    print("����ͼƬ�ѱ���")
    plt.figure(figsize=(10, 10))
    plt.imshow(word)  # ʹ��plt����ʾͼƬ
    plt.axis("off")
    plt.show()


if __name__ == '__main__':
    sum()
