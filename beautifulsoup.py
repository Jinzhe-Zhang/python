import requests
from bs4 import  BeautifulSoup
import xlwt
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.75 Safari/537.36'
}
def get_html():
    k=1 #参数k代表存储到excel的行数
    wb = xlwt.Workbook()  # 创建工作簿
    f = wb.add_sheet("招聘信息")  # 创建工作表
    '''
    下方的循环是将Excel表格中第一行固定
    Excel表第一行的前五列分别对应 职位、公司、工作地点、薪水、发布日期
    '''
    raw = ['职位', '公司', '工作地点', '薪水', '发布日期']
    for i in range(len(raw)):
        f.write(0, i, raw[i])
        '''
        write函数中第一个参数表示存储到多少行
        第二各参数存储到多少列表，第三个参数代表存储到对应行列的值
        '''
    url='https://search.51job.com/list/000000,000000,0000,00,9,99,%2520,2,{}.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare='
    try:
        for page in range(12):#解析前11页
            res = requests.get(url.format(page))
            res.encoding = 'gbk'
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'lxml')
                t1 = soup.select('.t1 span a')
                t2 = soup.select('.t2 a')
                t3 = soup.select('.t3')
                t4 = soup.select('.t4')
                t5 = soup.select('.t5')
                for i in range(len(t2)):
                    job = t1[i].get('title')#获取职位
                    href = t2[i].get('href')#获取链接
                    company = t2[i].get('title')#获取公司名
                    location = t3[i+1].text#获取工作地点
                    salary = t4[i+1].text#获取薪水
                    date = t5[i+1].text#获取发布日期
                    print(job + " " + company + " " + location + " " + salary + " " + date + " " + href)
                    f.write(k,0,job)
                    f.write(k,1,company)
                    f.write(k,2,location)
                    f.write(k,3,salary)
                    f.write(k,4,date)
                    k+=1#每存储一行 k值加1
        wb.save('D:/招聘.csv')#写完后掉用save方法进行保存
    except TimeoutError:
        print("请求失败")
        return  None
if __name__=='__main__':
    get_html()