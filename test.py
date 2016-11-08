import re
import xlwt
from pip._vendor import requests
from bs4 import BeautifulSoup

def getPage(html):      #获取总页数
    soup = BeautifulSoup(html)
    str = soup.select('span[class="total-page"]')[0].get_text()
    reg = r'[0-9]*'
    re.compile(reg)
    pageTotal = re.findall(reg, str)
    return pageTotal[1]

def getMessage(html, row):   #获取表格内容
    soup = BeautifulSoup(html)
    line, flag = 0, 0
    for message in soup.find("tbody", id="tbody").find_all("td"):
        if flag == 0:
            line += 1
            if line > 10:
                line = 0
                flag = 1
            continue
        if 4 <= line <= 6:
            line += 1
        elif line < 4:
            if message.string == None:
                worksheet.write(row, line, message.get_text().strip())
            else:
                worksheet.write(row, line, message.string)
            line += 1
        elif 6 < line < 10:
            if message.string == None:
                worksheet.write(row, line-3, message.get_text().strip())
            else:
                worksheet.write(row, line-3, message.string)
            line += 1
        else:
            line = 0
            row += 1
    return row

html = requests.get('http://www.jc.net.cn/market/list_11_210.html')
pageTotal = getPage(html.text)
workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('My Worksheet')

i = 1
pageTotal = int(pageTotal)
row= 0
while i <= pageTotal:
    url = r'http://www.jc.net.cn/market/search.html?keys=&area_name=&province=0&city=0' +\
        '&t1=%E9%97%A8%E7%AA%97%E5%8F%8A%E6%A5%BC%E6%A2%AF%E5%88%B6%E5%93%81' +\
        '&t2=%E5%BD%A9%E9%92%A2%E9%97%A8%E7%AA%97&st=&jgjs=&pno='
    html= requests.get(url + str(i))
    row = getMessage(html.text, row)
    print("进度：%d%%" % (i/pageTotal*100))
    i += 1

workbook.save('test.xls')







