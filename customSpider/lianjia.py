from bs4 import BeautifulSoup
import requests
import json
import pandas as pd

url = "https://hz.lianjia.com/ershoufang/"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html.parser")
result = soup.find('div', {'data-role': 'ditiefang'})
content = result.find_all('a')

def get_key (dict, value):
    return [k for k, v in dict.items() if v == value]

line_metro = {}             #储存每条地铁线对应的url  例： {一号线:url}
line_name = []
for items in content:
    link = "https://hz.lianjia.com" + items['href']
    line = items.text
    line_metro[line] = link
    line_name.append(line)

metro_station = {}        #储存每个地铁站对应的url  例：{人民广场:url}
line_station = {}
for item in line_name:
    url_line = line_metro[item]
    page_line = requests.get(url_line)
    soup_line = BeautifulSoup(page_line.text,"html.parser")
    result_line = soup_line.find('div',{'data-role':'ditiefang'})
    content = result_line.find_all('a')

    for items in content:
        link = items['href']
        station = items.text
        metro_station[station] = link
        line_station[station] = item
        if station in line_name:
            metro_station.pop(station)
        else:
            pass

lst=[]                                                      #将所有提取的二手房信息全部储存到lst中
for value in metro_station.values():
    url_stn="https://hz.lianjia.com"+value
    page_stn=requests.get(url_stn)
    soup_stn=BeautifulSoup(page_stn.text, "html.parser")
    try:                                                     #如果有多页数据，提取页码
        number=json.loads(soup_stn.find('div', {'class':'page-box house-lst-page-box'})['page-data'])['totalPage']
    except:
        number=1
        print('Number Error')
    
    stn_name = ''.join(get_key(metro_station, value))
    ln_name = line_station[stn_name]

    print('正在爬取' + stn_name)

    for i in range(1, number+1):
        pg=""
        if i > 1:
            pg = "pg" + str(i)
        pg = requests.get(url_stn+pg)
        soup_dtl = BeautifulSoup(pg.text, "html.parser")
        result_dtl = soup_dtl.find('ul', {'class': 'sellListContent'})
        try:
            first_result_dtl = result_dtl.find_all('li')   #有些地铁站没有二手房信息，所以遇到这种情况程序需要自动跳过，否则会报错
        except:
            print('无二手房信息')
            continue
        
        for item in first_result_dtl:
            house=item.find('div',{'class':'houseInfo'})   
            rsd=house.text                                        
            condition=item.find('div',{'class':'positionInfo'})    
            age=condition.text                                     
            Pr=item.find('div',{'class':'unitPrice'})
            price=Pr.text
            Tlpr=item.find('div',{'class':'totalPrice'})
            ttlprice=Tlpr.text
            lst.append((ln_name,stn_name,rsd,age,price,ttlprice))
    print(len(lst))


df=pd.DataFrame(lst, columns=['line','station','residence','year','price/sqm','ttl price'])
df.to_csv('Lianjia_project.csv',index=False,encoding='utf-8')