# -*- coding:utf-8 -*-

import requests
from html.parser import HTMLParser

# ================ define const ===============
BASEPATH = "I:/"
HTMLURLS = ["http://datachart.500.com/ssq/history/newinc/history.php",
            "http://kaijiang.zhcw.com/lishishuju/jsp/ssqInfoList.jsp"]
HEADERS = [
            {
            "Host": "datachart.500.com",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62."
                          "0.3202.94 Safari/537.36",
            "Referer": "http://datachart.500.com/ssq/history/history.shtml",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Cookie":"ck_RegFromUrl=http%3A//www.500.com/; sdc_session=1533916356798; _jzqy=1.1528606472.1533916357.1."
                     "jzqsr=baidu.-; _jzqckmp=1; seo_key=baidu%7C%7Chttps://www.baidu.com/link?url=MQcB3-er5rK249eCQNw"
                     "G8A4N-hontstLi8HIy9E7H_q&wd=&eqid=fec80b7400019715000000035b6db4d7; bdshare_firstime=15339164028"
                     "59; WT_FPC=id=undefined:lv=1533916553308:ss=1533916402791; _qzja=1.190448226.1533829920533.15338"
                     "29920534.1533916402865.1533916409059.1533916553371.0.0.0.5.2; _qzjc=1; _jzqa=1.20620370185900751"
                     "00.1533829921.1533829921.1533916357.2; _jzqc=1; Hm_lvt_4f816d475bb0b9ed640ae412d6b42cab=15338299"
                     "21,1533916357; Hm_lpvt_4f816d475bb0b9ed640ae412d6b42cab=1533916554; __utma=63332592.612539621.15"
                     "33916358.1533916358.1533916358.1; __utmc=63332592; __utmz=63332592.1533916358.1.1.utmcsr=baidu|u"
                     "tmccn=(organic)|utmcmd=organic; CLICKSTRN_ID=123.98.36.94-1533829945.911636::415C872F9F26292A610C"
                     "843E6BD7FEB2; motion_id=1533920615560_0.37147948464863223",
            },
            {
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding":"gzip, deflate",
            "Accept-Language":"zh-CN,zh;q=0.9",
            "Connection":"keep-alive",
            "Cookie":"JSESSIONID=abci8i7JyQftrfV9SsNuw; Hm_lvt_692bd5f9c07d3ebd0063062fb0d7622f=1533962514,1533962750; Hm"
                    "_lpvt_692bd5f9c07d3ebd0063062fb0d7622f=1533962750; _ga=GA1.2.1837167549.1533962514; _gid=GA1.2.290"
                    "113300.1533962514",
            "Host":"kaijiang.zhcw.com",
            "Referer":"http://kaijiang.zhcw.com/lishishuju/jsp/ssqInfoList.jsp?czId=1&beginIssue=1&endIssue=2018092&"
                      "currentPageNum=1",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0."
                         "3202.94 Safari/537.36",
            },

          ]
PARAMS = [
          {
           'start':'1',
           'end':'18092'
          },
          {
            'czId':'1',
            'beginIssue':'1',
            'endIssue':'2018092',
            'currentPageNum':'1',
          },
         ]
DATAPATHS = ["lot_500_ssq.txt",
             "lot_zhcw_ssq.txt"]


# ================ private parser class ===============
class Parser500ssq(HTMLParser):
    flag_tbody = False
    flag_tr = False
    flag_td = False
    linedata = []
    result = []

    def handle_starttag(self, tag, attrs):    # start tag
        if (str(tag).startswith("tbody")):
            for k,v in attrs:
                if k == 'id' and v == 'tdata':
                    self.flag_tbody = True
                    return
        elif (self.flag_tbody == True):
            if (str(tag).startswith("tr")):
                self.flag_tr = True
            if (str(tag).startswith("td")):
                self.flag_td = True

    def handle_endtag(self, tag):             # end tag
        if (self.flag_tbody == True):
            if (str(tag).startswith("tr")):
                self.result.append(self.linedata)
                self.linedata = []
                self.flag_tr = False
            elif (str(tag).startswith("td")):
                self.flag_td = False
            elif (str(tag).startswith("tbody")):
                self.flag_tbody = False

    def handle_data(self, data):              # <xx>data</xx>
        if (self.flag_td == True):
            if '\xa0' in data:
                self.linedata.append("-".join(data.replace(u'\xa0', u'').split(",")))
            else:
                self.linedata.append("".join(data.split(",")))
'''
    def handle_startendtag(self, tag, attrs): # start and end tag
        print('<%s/>' % tag)

    def handle_comment(self, data):           # <!-->comment<--!>
        print('<!--', data, '-->')

    def handle_entityref(self, name):         # special char: like &nbps
        print('&%s;' % name)

    def handle_charref(self, name):           # special string: like &#
        print('&#%s;' % name)
'''
class ParserZhcwssq(HTMLParser):
    flag_tbody = False
    flag_tr = False
    flag_td = False
    flag_ballnum = False
    flag_nextpage = False
    linedata = []
    result = []
    url_nextpage = []

    def reset_attr(self):
        self.flag_tbody = False
        self.flag_tr = False
        self.flag_td = False
        self.flag_ballnum = False
        self.flag_nextpage = False
        self.linedata = []
        self.result = []
        self.url_nextpage = []

    def handle_starttag(self, tag, attrs):    # start tag
        if (str(tag).startswith("tbody")):
            self.flag_tbody = True
        elif (self.flag_tbody == True):
            if (str(tag).startswith("tr")):
                self.flag_tr = True
            elif (str(tag).startswith("td")):
                self.flag_td = True
                for k,v in attrs:
                    if k == 'class' and v == "kaiHao":
                        self.flag_ballnum = True
        elif self.flag_nextpage == True and str(tag).startswith("a"):
            self.url_nextpage.append(attrs[0][1].split("PageNum=")[1])

    def handle_endtag(self, tag):             # end tag
        if (self.flag_tbody == True):
            if (str(tag).startswith("tr")):
                self.result.append(self.linedata)
                self.linedata = []
                self.flag_tr = False
            elif (str(tag).startswith("td")):
                self.flag_td = False
                self.flag_ballnum = False
            elif (str(tag).startswith("tbody")):
                self.flag_tbody = False

    def handle_data(self, data):              # <xx>data</xx>
        if (self.flag_td == True):
            if self.flag_ballnum == True:
                self.linedata.extend(data.rstrip().split(" "))
            else:
                self.linedata.append("".join(data.split(",")))

    def handle_comment(self, data):  # <!-->comment<--!>
        if(data.strip() == '分页条'):
            self.flag_nextpage = True
# ================ private functions ===============
def parse500ssq(html,datapath):
    print("start grabbing...")
    parser = Parser500ssq()
    parser.feed(html)
    print(parser.result)
    with open(BASEPATH + datapath, 'w') as f:
        for line in parser.result:
            print(line)
            f.write(",".join(line))
            f.write("\n")
    print("finished.")

def parseZhcwssq(html,datapath,htmlurl,method,headers,params):
    print("start grabbing...")
    parser = ParserZhcwssq()
    wmode = 'w'
    while(1):
        parser.feed(html)
        print(parser.result)
        with open(BASEPATH + datapath, wmode) as f:
            for line in parser.result:
                f.write(",".join(line))
                f.write("\n")
        if int(parser.url_nextpage[1]) != int(parser.url_nextpage[3]) - 1:
            print("grabbing nextpage...")
            wmode = 'a'
            params['currentPageNum'] = parser.url_nextpage[2].strip()
            html = getHtml(htmlurl, method, headers,params)
            parser.reset_attr()
        else:
            print("finished.")
            break

# ================ public functions ===============
def getHtml(url, method='get', headers={}, params={}):
    if method == 'get':
        html = requests.get(url, headers=headers,  params=params)
        html.encoding = 'utf-8' #html.apparent_encoding
    else:
        html = requests.post(url, headers=headers, data=params)
        html.encoding = 'utf-8'
    return html.text

# ================ main ===============
if __name__ == "__main__":
    for i in range(len(HTMLURLS)):
        html = getHtml(HTMLURLS[i], 'get', HEADERS[i],PARAMS[i])
        if i == 0:
            parse500ssq(html,DATAPATHS[i])
        elif i == 1:
            parseZhcwssq(html, DATAPATHS[i],HTMLURLS[i],'get',HEADERS[i],PARAMS[i])