import random
import re
from urllib import request
from userAgent import userAgents

list_url = r'https://www.biquke.com/bq/37/37868'
content_url = r'https://www.biquke.com/bq/37/37868/10576640.html'

# 1 获取列表 2 获取内容
state = 2


def getRandomUserAgent():
    return userAgents[random.randint(0, len(userAgents) - 1)]


def getPage(url):
    headers = {
        'User-Agent': getRandomUserAgent()
    }
    response = request.Request(url, headers=headers)
    return request.urlopen(response).read().decode('utf-8')


# 获取章节列表
def getListFromPage(page):
    pattern = re.compile('<dd><a.*?href="(.*?)".*?>(.*?)</a></dd>', re.S)
    results = re.findall(pattern, page)
    content = ''
    for item in results:
        content += item[0] + ',' + item[1] + '\n'
    createFile('/list.txt', content)


# 获取正文内容
def getPageCotent(page):
    title_pattern = re.compile('<div.*?class="bookname">.*?<h1>(.*?)</h1>.*?</div>', re.S)
    title = re.findall(title_pattern, page)[0]
    content_pattern = re.compile('<div.*?id="content".*?>(.*?)</div>', re.S)
    content = re.findall(content_pattern, page)[0]
    content = content.replace('<br/>', '\n').replace('&nbsp;', '')
    next_pattern = re.compile('<div.*?"bottem1">.*?章节列表.*?<a href="(.*?)">下一章</a>', re.S)
    nextUrl = re.findall(next_pattern, page)[0]
    string = title + '\n' + content + '\n下一章 ' + nextUrl
    createFile('/content.txt', string)


def createFile(path, content):
    f = open('./output' + path, 'w', encoding='utf-8')
    f.write(content)
    f.close()
    print('文件已创建')


def start():
    if state == 1:
        page = getPage(list_url)
        getListFromPage(page)
    else:
        page = getPage(content_url)
        getPageCotent(page)


start()
