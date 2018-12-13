import requests
import re
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import csv
import time

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}

def get_one_page(url):
    try:
        response = requests.get(url,headers = headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

def parse_one_page(content):
    try:
        soup = BeautifulSoup(content,'html.parser')
        items = soup.find('div',class_=re.compile('js-tips-list'))
        for div in items.find_all('div',class_=re.compile('ershoufang-list')):
            yield {
                #'Name':div.find('a',class_=re.compile('js-title')).text,
                #'Type': div.find('dd', class_=re.compile('size')).contents[1].text,#tag的 .contents 属性可以将tag的子节点以列表的方式输出
                #'Area':div.find('dd',class_=re.compile('size')).contents[5].text,
                #'Towards':div.find('dd',class_=re.compile('size')).contents[9].text,
                #'Floor':div.find('dd',class_=re.compile('size')).contents[13].text.replace('\n',''),
                #'Decorate':div.find('dd',class_=re.compile('size')).contents[17].text,
                'Address':div.find('span',class_=re.compile('address')).text#,
                #'TotalPrice':div.find('span',class_=re.compile('js-price')).text+div.find('span',class_=re.compile('yue')).text,
                #'Price':div.find('div',class_=re.compile('time')).text
            }
        #有一些二手房信息缺少部分信息，如：缺少装修信息，或者缺少楼层信息，这时候需要加个判断，不然爬取就会中断。
        if div[\
        #'Name', 'Type', 'Area', 'Towards', 'Floor', 'Decorate', \
        'Address'\
        #, 'TotalPrice', 'Price'\
        ] == None:
                return None
    except Exception:
        return None

def main():
    for i in range(1,3):
        url = 'https://dl.58.com/tech/pn{}/'.format(i)
        content = get_one_page(url)
        print('第{}页抓取完毕'.format(i))
        for div in parse_one_page(content):
            print(div)
        with open(r'D:\QQ\294103703\FileRecv\Data2.csv', 'a', newline='') as f:  # Data.csv 文件存储的路径,如果默认路径就直接写文件名即可。
            fieldnames = [\
            #'Name', 'Type', 'Area', 'Towards', 'Floor', 'Decorate', \
            'Address'\
            #, 'TotalPrice', 'Price'\
            ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in parse_one_page(content):
                writer.writerow(item)
        time.sleep(3)#设置爬取频率，一开始我就是爬取的太猛，导致网页需要验证。

if __name__=='__main__':
    main()