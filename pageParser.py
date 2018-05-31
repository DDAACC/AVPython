import urllib.request
import requests
import os
import re
import sys
from htmlWriter import *
from bs4 import BeautifulSoup


req_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
'Accept':'text/html;q=0.9,*/*;q=0.8',
'Accept-Charset':'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
'Accept-Encoding':'gzip',
'Connection':'close',
'Referer':'guibo' 
}

def DownLoadImg(URL,name):
	img=requests.get(URL)
	f=open(name,'ab')
	f.write(img.content)
	f.close()

def getMagnet(search):
    search=search.replace(' ','%20')
    URL='https://m.zhongziso.com/list/%s/1'%(search)
    req=requests.get(URL,headers=req_header)
    if req.encoding == 'ISO-8859-1':
        encodings = requests.utils.get_encodings_from_content(req.text)
        if encodings:
            encoding = encodings[0]
        else:
            encoding = req.apparent_encoding
    text = req.content.decode(encoding, 'replace') 
    #正则匹配磁力链接
    magnetRegex=r'magnet:[^"]+'
    magnetList=re.findall(magnetRegex,text)
    #正则匹配磁力大小
    sizeRegex=r'<dd class="text-size">(.+)</dd>'
    sizeList=re.findall(sizeRegex,text)
    #正则匹配磁力说明
    infoRegex=r'text-success.+>(.+)</a>'
    infoList=re.findall(infoRegex,text)
    for i in range(0,len(infoList)):
        infoList[i]=infoList[i]+"  size:"+sizeList[i]
    return dict(zip(magnetList,infoList))

def pageParser(URL,savePath):
    r=requests.get(URL,headers=req_header)
    text=r.text
    soup=BeautifulSoup(text,'html.parser')
    a=soup.find_all('div',class_='video')

    needInit=True
    if(os.path.exists(savePath+'\\AV.html')):
        needInit=False
    file=open(savePath+'\\AV.html','a+',encoding='utf-8')
    htmlwriter=HtmlWriter(file)
    if needInit==True:
        htmlwriter.initHtml()

    for b in a:
        c=b.find('div',class_='id')
        fanhao=c.string
        c=b.find('a')
        title=c['title']
        imgURL=c['href']
        imgURL='http://www.javlibrary.com/cn'+imgURL.strip('.')
        r=requests.get(imgURL,headers=req_header)
        text=r.text
        soup=BeautifulSoup(text, "html.parser")
        f0=soup.find('table',id='video_jacket_info')
        f1=f0.find('img')
        imgsrc='http:'+f1['src']
        DownLoadImg(imgsrc,savePath+'\\'+fanhao+'.jpg')
        #写入html
        htmlwriter.writeTitle(title)
        htmlwriter.writeImg(fanhao+'.jpg')
        #写入磁链
        magnetList=getMagnet(fanhao)
        for k in magnetList:
            htmlwriter.writeMagnet(k,magnetList[k])
    file.close()
            

#main
pageParser('http://www.javlibrary.com/cn/vl_genre.php?&mode=&g=me&page=5','test')

