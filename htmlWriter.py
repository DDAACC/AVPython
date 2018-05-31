import linecache
htmlHead='<!DOCTYPE html>\n<html>\n<head>\n\
	<title>function</title>\n</head>\n<body>\n'
htmlTail='</body>\n</html>'
class HtmlWriter(object):
    def __init__(self,file):
        self.file=file
    def writeMagnet(self,magnet,size):
        write='<a href=\"%s\">%s</a>\n<br>\n'%(magnet,size)
        self.file.write(write)
    def writeTitle(self,title):
        write='<h1>%s</h1>\n<br>\n'%(title)
        self.file.write(write)
    def writeImg(self,imgSrc):
        write='<img src=\"%s\">\n<br>\n'%(imgSrc)
        self.file.write(write)
    def initHtml(self):
        write='<!DOCTYPE html>\n<html>\n<head>\
        \n<title>function</title>\n</head>\n'
        self.file.write(write)
