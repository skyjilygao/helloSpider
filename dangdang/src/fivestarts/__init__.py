'''
当当网 5星图书排行 前500名图书
'''
import time
import requests
class spider_main():
    def getHtml(self, page_no):
        url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-year-2017-0-2-%s' %page_no
        print("req url:  "+url)
        req = requests.get(url)
        ##    req.encoding = "UTF-8"
        return req.text

    def parse_html_xpath(self, text, index):
        print(text)
def start():
    print('spider start ...')
    startt = time.clock()
    errors = []#存放网页打不开等错误
    douban = spider_main()
    i = 25
    while i<=25:
        try:
            text = douban.getHtml(i)
        except Exception as e:
            text = False
            errors.append(e)
        finally:
            if text:
                f = open(r'file\fivestart-'+str(i)+'.html', 'w', encoding='utf-8')
                f.write(text)
                f.close()
                douban.parse_html_xpath(text, i)
            i +=1
    # douban.save2db()
    if errors:
        print("It's bad,there is something wrong waiting for handling!!")
    else:
        print(None,"perfect!!")
    endt = time.clock()
    print("run over!!cost total_time:%s"%(endt - startt))
if __name__ == "__main__":
    start()