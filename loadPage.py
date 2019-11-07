import random
import re
from urllib import request
from userAgent import userAgents
from urls import list_url, content_url
import gzip

# 1 获取列表 2 获取内容
state = 2


def ungzip(data):
    try:
        data = gzip.decompress(data)
    except:
        pass
    return data


def getRandomUserAgent():
    return userAgents[random.randint(0, len(userAgents) - 1)]


def getPage(url):
    print('start...')
    headers = {
        'User-Agent': getRandomUserAgent()
    }
    response = request.Request(url, headers=headers)
    content = ungzip(request.urlopen(response).read()).decode('utf-8')
    return content


# 获取章节列表
def getListFromPage(page):
    pattern = re.compile('<dd>.*?<a.*?href="(.*?)".*?>(.*?)</a></dd>', re.S)
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
    content = content.replace('<br>', '\n').replace('<br/>', '\n').replace('&nbsp;', '')
    # content_filter = re.compile('<p.*?</p>', re.S)
    # content = content_filter.sub('', content).strip()
    next_pattern = re.compile('<div.*?class="bottem1">.*?章节列表.*?<a href="(.*?)".*?>下一[章|页]</a>', re.S)
    nextUrl = re.findall(next_pattern, page)[0]
    string = title + '\n' + content
    createFile('/content.txt', string)
    if list_url.find(nextUrl) > -1:
        print('这是最后一章')
    else:
        reWriteUrl(nextUrl.split('/')[-1])


def createFile(path, content):
    f = open('./output' + path, 'w', encoding='utf-8')
    f.write(content)
    f.close()
    print('文件已创建')


# 重写url
def reWriteUrl(url):
    f = open('./urls.py', 'r', encoding='utf-8')
    content = f.read()
    f.close()
    f = open('./urls.py', 'w', encoding='utf-8')
    pattern = re.compile('content_url.*\'(.*)\'\n', re.S)
    nowUrl = re.findall(pattern, content)[0]
    content = content.replace(nowUrl, url)
    f.write(content)
    f.close()


def start():
    if state == 1:
        page = getPage(list_url)
        getListFromPage(page)
    else:
        page = getPage(content_url)
        getPageCotent(page)


start()
