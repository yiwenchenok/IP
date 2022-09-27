import csv
import os
import time
import random

import requests
from lxml import etree

urlha = 'https://www.kuaidaili.com/free/inha/{}/'  # 快代理高匿代理池
urltr = 'https://www.kuaidaili.com/free/intr/{}/'  # 快代理普通代理池
url66ip = 'http://www.66ip.cn/{}.html'  # 66ip代理获取
urlyun = 'http://www.ip3366.net/?stype=1&page={}'  # 云ip代理获取
urlqiyun='https://proxy.ip3366.net/free/?action=china&page={}'# 齐云ip获取
urlkaixinha = 'http://www.kxdaili.com/dailiip/1/{}.html'  # 开心高匿ip代理获取
urlkaixintr = 'http://www.kxdaili.com/dailiip/2/{}.html'  # 开心普通ip代理获取
url89 = 'https://www.89ip.cn/index_{}.html'  # 89ip代理获取


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15"

}
# 建立一个user-Agent池防屏蔽
user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Opera/8.0 (Windows NT 5.1; U; en)',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) '
]


def get_url(url):
    user_agent = random.choice(user_agents)
    headers.update({"User-Agent": user_agent})
    response = requests.get(url=url, headers=headers)
    html = response.text.encode(response.encoding).decode(response.apparent_encoding)
    return html


def get_data(html):
    selector = etree.HTML(html)
    all = selector.xpath('//*[@id="list"]/table/tbody/tr') or selector.xpath(
        '//*[@id="main"]/div[1]/div[2]/div[1]/table/tr') or selector.xpath(
        '//div[2]/table//tr') or selector.xpath(
        '//div[1]/table//tr') or selector.xpath('//*[@id="content"]/section/div[2]/table//tr')

    list = []
    for iplist in all:
        try:
            ip = iplist.xpath('./td[1]/text()')[0].strip() # .strip()两边去空
            local = iplist.xpath('./td[2]/text()')[0].strip()
            ipaddresss = ip + ':' + local
            list.append(ipaddresss)
        except Exception as e:
            pass

    return list


def save_data(list):
    if os.path.exists('ip地址.csv'):
        os.remove('ip地址.csv')
    with open('ip地址.csv', 'a', encoding="utf-8", newline="") as file:
        write = csv.writer(file)
        write.writerow(['ip地址'])
        for i in list:
            write.writerow([i])


def read_csv():  # 读取csv文件
    with open('ip地址.csv') as file:
        iplist = []
        read = csv.reader(file)
        next(read)  # 使得file文件从第二行开始读取
        for line in read:
            iplist.append(line[0])
        return iplist


def visit(iplist):  # 访问itrun.xyz
    succeed = 0
    fail = 0
    for i in iplist:
        ip = str(i)
        try:
            response = requests.get(url='http://itrun.xyz', headers=headers, proxies={"http": ip}, timeout=10)
            time.sleep(1)
            if response.status_code == 200:
                print(ip + '--访问成功')
                succeed += 1
        except Exception:
            print(ip + '--访问失败')
            fail += 1
    print('总共访问了' + str(len(iplist)) + '条数据' + '，成功' + str(succeed) + '次' + ',失败' + str(fail) + '次')


def circulate():
    list = []
    for page in range(1, 3):
        html = get_url(urlha.format(page))  # 高匿代理爬取
        time.sleep(1)
        list += get_data(html)

        html = get_url(urltr.format(page))  # 普通代理爬取
        time.sleep(1)
        list += get_data(html)

        html = get_url(url66ip.format(page))  # 66ip代理爬取
        time.sleep(1)
        list += get_data(html)

        html = get_url(urlyun.format(page))  # 云ip代理爬取
        time.sleep(1)
        list += get_data(html)

        html = get_url(urlqiyun.format(page))  # 齐云ip代理爬取
        time.sleep(1)
        list += get_data(html)

        html = get_url(urlkaixinha.format(page))  # 开心高匿ip代理获取
        time.sleep(1)
        list += get_data(html)

        html = get_url(urlkaixintr.format(page))  # 开心普通ip代理获取
        time.sleep(1)
        list += get_data(html)

        html = get_url(url89.format(page))  # 89ip代理获取
        time.sleep(1)
        list += get_data(html)
    return list


if __name__ == '__main__':
    print('开始爬取数据，等待20秒...')
    save_data(circulate())
    print('保存ip地址数据成功，开始访问...')
    visit(read_csv())
    print('访问结束')
