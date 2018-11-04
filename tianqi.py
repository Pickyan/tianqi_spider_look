#encoding:utf-8

import requests
from bs4 import BeautifulSoup
from pyecharts import Bar


DATA = []

def parser_page(url):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    response = requests.get(url,headers=headers)
    html = response.content.decode('utf-8')
    #使用html5lib兼容性比lxml要好
    soup = BeautifulSoup(html,'html5lib')
    soup = soup.find('div',attrs={'class':'conMidtab'})
    tables = soup.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index,tr in enumerate(trs):  #enumerate(list/...) for循环遍历list/...时返回角标给index。
            tds = tr.find_all('td')
            city = tds[0]
            if index==0:
                city = tds[1]

            city = list(city.stripped_strings)[0] #取出city里的文字信息，并去除空格换行，list一列表形式返回。

            min_temp = tds[-2]
            min_temp = list(min_temp.stripped_strings)[0]
            # print({'city':city,'min_temp':min_temp})
            DATA.append({'city':city,'min_temp':int(min_temp)})


def main():
    base_url = 'http://www.weather.com.cn/textFC/'
    areas = ['hb.shtml','db.shtml','hd.shtml','hz.shtml','hn.shtml','xb.shtml','xn.shtml','gat.shtml']
    for area in areas:
        url = base_url + area
        parser_page(url)

    DATA.sort(key=lambda data:data['min_temp'])  #sort()函数根据min_temp的值进行排序
    look(DATA[0:10])


#可视化
def look(data):
    cities = list(map(lambda x: x['city'], data))  # map(func,list)函数第一个参数是函数，第二个是列表，map函数会遍历list并传入fanc中。
    min_temp = list(map(lambda x: x['min_temp'], data))
    #可视化工具pyecharts
    chart = Bar("中国最低温度前十城市")
    chart.add('',cities,min_temp)
    chart.render('temp_look.html')


if __name__ == '__main__':
    main()

