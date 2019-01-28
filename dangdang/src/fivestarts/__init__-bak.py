'''
当当网 5星图书排行 前500名图书
'''
import time
import requests
class spider_main():
    def getHtml(self, page_no):
        url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzUyNDk0MjA2NQ==&scene=126#wechat_redirect'
        # url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-year-2017-0-2-%s' %page_no
        print("req url:  "+url)
        # req = requests.get(url)
        headers = {
            'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E302 MicroMessenger/6.7.1 NetType/4G Language/zh_CN',
            "Content-Type":"application/json",
            "Referer:https":"//servicewechat.com/wxa2ae8810d8157e4b/0/page-frame.html"
        }
        req = requests.get(url,headers=headers)
        ##    req.encoding = "UTF-8"
        return req.text

    def parse_html_xpath(self, text, index):
        print(text)
def start():
    print('spider start ...')
    startt = time.clock()
    errors = []#存放网页打不开等错误
    douban = spider_main()
    i = 1
    while i<=1:
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
                # douban.parse_html_xpath(text, i)
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