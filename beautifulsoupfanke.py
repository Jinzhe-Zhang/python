import requests
import re
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import csv
import time
import random

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
        items = soup.find('ul',id=re.compile('list_con'))
        for div in items.find_all('li',class_=re.compile('job_item')):
            labellist=div.find('div',class_=re.compile('job_wel')).find_all('span')
            labelist=[]
            labelistext=''
            for label in labellist:
                label=label.text
                labelist.append(label)
            yield {
                '名称':div.find('span',class_=re.compile('name')).text,
                #'Type': div.find('dd', class_=re.compile('size')).contents[1].text,#tag的 .contents 属性可以将tag的子节点以列表的方式输出
                #'Area':div.find('dd',class_=re.compile('size')).contents[5].text,
                #'Towards':div.find('dd',class_=re.compile('size')).contents[9].text,
                #'Floor':div.find('dd',class_=re.compile('size')).contents[13].text.replace('\n',''),
                #'Decorate':div.find('dd',class_=re.compile('size')).contents[17].text,
                '薪酬':div.find('p',class_=re.compile('job_salary')).text,
                '地址':div.find('span',class_=re.compile('address')).text,
                '公司':div.find('a',class_=re.compile('fl')).text,
                '标签':','.join(labelist),
                '职业方向':div.find('span',class_=re.compile('cate')).text,
                '学历':div.find('span',class_=re.compile('xueli')).text,
                '经验':div.find('span',class_=re.compile('jingyan')).text#,
                #'Price':div.find('div',class_=re.compile('time')).text
            }
        #有一些二手房信息缺少部分信息，如：缺少装修信息，或者缺少楼层信息，这时候需要加个判断，不然爬取就会中断。
        if div[\
        '名称'#, #'Type', 'Area', 'Towards', 'Floor', 'Decorate', \
        '地址', '薪酬', '标签','公司','职业方向','学历','经验'\
        #, 'Price'\
        ] == None:
                return None
    except Exception:
        return None

def main():
    with open(r'D:\QQ\294103703\FileRecv\Data2.csv', "r+") as f:
        f.truncate()
    flag=True
    for i in range(1,51):
        url = 'https://dl.58.com/tech/pn{}/'.format(i)
        print (url)
        content = get_one_page(url)
        print('第{}页抓取完毕'.format(i))
        for div in parse_one_page(content):
            print(div)
        with open(r'D:\QQ\294103703\FileRecv\Data2.csv', 'a', newline='') as f:  # Data.csv 文件存储的路径,如果默认路径就直接写文件名即可。
            #if(flag)
                #f.truncate()
                #flag=True
            fieldnames = [\
        '名称', #'Type', 'Area', 'Towards', 'Floor', 'Decorate', \
        '地址', '薪酬', '标签','公司','职业方向','学历','经验'\
        #, 'Price'\
        ]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in parse_one_page(content):
                writer.writerow(item)
        time.sleep(random.random()*2+2)#设置爬取频率，一开始我就是爬取的太猛，导致网页需要验证。

if __name__=='__main__':
    main()