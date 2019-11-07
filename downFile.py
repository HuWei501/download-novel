import urllib.request

url = 'ed2k://|file|[迅雷仓XunLeiCang.Com]越狱.第2季.Prison.Break.2006.S02E17.BD720P.x264.AAC.CHS-4567TV.mp4|1022509910|99515D3D66D6CAB866399F1F8A3457DE|h=QRYMXXBSM2ZD6NHV7CATCNROA6IXSJKC|/'

filename = url[url.rindex('/'):]
print('filename = ' + filename)

downloaded = '0'


def download_listener(a, b, c):
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    new_downloaded = '%.1f' % per
    global downloaded
    if new_downloaded != downloaded:
        downloaded = new_downloaded
        print('download %s%%  %s/%s' % (downloaded, a * b, c))


response = urllib.request.urlretrieve(url, './file' + filename, download_listener)
