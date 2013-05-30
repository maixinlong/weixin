# coding=utf-8
import urllib2
import string
import urllib
import re

def baidu_search(keyword):
    p= {'wd': keyword}
    res=urllib2.urlopen("http://www.baidu.com/s?"+urllib.urlencode(p))
    html=res.read()
    content = unicode(html, 'utf-8','ignore')
    arrList = getList(u"<table.*?class=\"result\".*?>.*?<\/a>", content)
    rc_list = []
    try:
        for item in arrList:
            regex = u"<h3.*?class=\"t\".*?><a.*?href=\"(.*?)\".*?>(.*?)<\/a>"
            link = getMatch(regex,item)
            url = link[0]
            title = clearTag(link[1]).encode('utf8')
            rc_list.append(title)
            rc_list.append(url)
            print url
            print title
        return "\n".join(rc_list)
    except Exception,e:
        if len(rc_list)>0:
            return "\n".join(rc_list)
        else:
            return e
        
        
def getList(regex,text):
    arr = []
    res = re.findall(regex, text)
    if res:
        for r in res:
            arr.append(r)
    return arr


def getMatch(regex,text):
    res = re.findall(regex, text)
    if res:
        return res[0]
    return ""


def clearTag(text):
    p = re.compile(u'<[^>]+>')
    retval = p.sub("",text)
    return retval


if __name__ == "__main__":
    baidu_search("rekoo")