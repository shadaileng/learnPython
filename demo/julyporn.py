#!usr/bin/python3
#-*- coding: utf-8 -*-

from urllib import request, parse
from bs4 import BeautifulSoup
import re, requests, os, sqlite3, sys, random

from time import sleep
import functools

def process_(func):
    @functools.wraps(func)
    def wrapper(*args, **kw):
        total = kw.get('total', 0)
        index = kw.get('index', 0)
        result = ''
        _stdout = sys.stdout
        Len = 50
        desc = kw.get('desc', '')
        for i in range(index, total):
            cur = int(i / total * Len)
            cur_ = (Len - cur)
            kw['index'] = i
            kw['desc'] = desc % (i + 1)
            result = func(*args, **kw)
            _stdout.write(f'\rprograss: {int(i / total * 100):0>2d}%|{cur * "#":s}{cur_ * " ":s}|{i + 1} in {total} |{desc % (i + 1)}')
        _stdout.flush()
        print('\rprograss: %s|%s' % (100, Len * '#'))
#        return result
    return wrapper

def random_ip():
    a=random.randint(1,255)
    b=random.randint(1,255)
    c=random.randint(1,255)
    d=random.randint(1,255)
    return(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))

def random_Agent():
    agents = [
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)",
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'
    ]
    return random.choice(agents)

def add_header():
    return {"Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7", "Proxy-Connection": "keep-alive", 'User-Agent': random_Agent(), 'X-Forwarded-For':random_ip()
#    , 'Accept-Encoding': 'gzip, deflate, br' 
    }



@process_
def catch_requests(baseurl, uri, node, node_condition, index = 0, total = 0, dir_ = 'res', desc = 'julyporn'):
    url_ = '%s%s=%s' % (baseurl, uri, str(index))
    rep = requests.get(url_, allow_redirects=True, headers=add_header())
#    print('status: %s, reason: %s' % (rep.status_code, rep.reason))
    if rep.status_code == 200:
        data = rep.content.decode('utf-8')
        soup = BeautifulSoup(data, features='html.parser')
        items = soup.find_all(node, node_condition)
#        print('colVideoList size: %s' % len(items))
        buf = ''
        for item in items:
            v = item.find('a', {'class': 'display'})
            i = v.find_all('div', {'class': 'img'})[0]['style']
            t = item.find('a', {'class': 'title'})
            if t == None or t['href'][:4] == 'http': continue
            buf += '[text: %s, href: %s%s, img: %s]\n' % (t.string, baseurl, v['href'], 'https:%s' % i.split("'", 1)[1].rsplit("'", 1)[0])
        res = '%s/%s' % (os.getcwd(), dir_)
        os.makedirs(res, exist_ok = True)
        filename = '%s/%s.txt' % (res, desc)
        with open(filename, 'a') as file:
            file.write(buf)

@process_
def download_m3u8(url, index = 0, total = 0, desc = '第%s页', unknow = True, tss = []):
    download_path = '%s/%s' % (os.getcwd(), 'm3u8')
    os.makedirs(download_path, exist_ok = True)
    rep = requests.get(url, allow_redirects=True, headers=add_header())
    print('status: %s, reason: %s' % (rep.status_code, rep.reason))
    if rep.status_code == 200:
        data = rep.content.decode('utf-8')
        print(data)
        
#    print(all_content)
#    file_line = all_content.split("\n")    # 读取文件里的每一行
#    # 通过判断文件头来确定是否是M3U8文件
#    if file_line[0] != "#EXTM3U":
#        raise BaseException("非M3U8的链接")
#    else:
#        total = all_content.count('EXTINF')
#        baseurl = url.rsplit("/", 1)[0]
#        for index, line in enumerate(file_line):
#            if "EXTINF" in line:
#                unknow = False
#                # 拼出ts片段的URL
#                tss.append(file_line[index + 1])
##                pd_url = url.rsplit("/", 1)[0] + "/" + file_line[index + 1]
##                res = requests.get(pd_url)
##                c_fule_name = str(file_line[index + 1])
##                with open(download_path + "/" + c_fule_name, 'ab') as f:
##                    f.write(res.content)
##                    f.flush()
#        if unknow:
#            raise BaseException("未找到对应的下载链接")
#        else:
#            print("下载完成")

def download_by_m3u8(url, filename, tss = []):
    buf = ''
    with open(filename, 'r') as file:
        buf = file.read()
    file_line = buf.split("\n")
    if file_line[0] != "#EXTM3U":
        raise BaseException("非M3U8的链接")
    else:
        total = buf.count('EXTINF')
        baseurl = url.rsplit("/", 1)[0]
        unknow = True
        for index, line in enumerate(file_line):
            if "EXTINF" in line:
                unknow = False
                # 拼出ts片段的URL
                tss.append('%s/%s' % (baseurl, file_line[index + 1]))
        if unknow:
            raise BaseException("未找到对应的下载链接")
        else:
#            print(tss)
            print('开始下载...')
            for pd_url in tss:
                res = requests.get(pd_url)
                with open(download_path + "/tmp.mp4", 'ab') as f:
                    f.write(res.content)
                    f.flush()
        print('下载完成')

if __name__ == '__main__':
    catch_requests('https://7.f39.xyz/videos', '/all/free?page', 'div', {'class': 'colVideoList'}, total = 115, desc = '第%s页', dir_ = 'res2')

#    download_m3u8('https://m.slxstatic.com/k-aafd5572d8ef63532180d5d1c62b937e/e-1581856396/28/28-Ybx2kokXmPB8uFLUrhHk.m3u8', total = 115, desc = '第%s页')
#    download_by_m3u8('https://m.slxstatic.com/k-aafd5572d8ef63532180d5d1c62b937e/e-1581856396/28/28-Ybx2kokXmPB8uFLUrhHk.m3u8', '28-Ybx2kokXmPB8uFLUrhHk.m3u8')
