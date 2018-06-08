'''
知乎，练习反爬虫
https://www.cnblogs.com/lei0213/p/6957508.html
'''
import time
import requests
class spider_main():
    def login(self):
        url = 'https://www.zhihu.com/api/v3/oauth/sign_in'

        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            "upgrade-insecure-requests": "1",
            'x-udid' : 'AaAgZ7gljg2PThSdpxArkQeDsS83Dmy_S5M=',
            'x-xsrftoken' : 'cf99cf1b-9d4f-4c53-b4f6-302e597ee6bd',
            'authorization' : 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
            'content-type' : 'multipart/form-data; boundary=----WebKitFormBoundaryP0N8JYzceVjAAOTH'
        }
        data = {
            'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
            'grant_type': 'password',
            'timestamp': '1528448486406',
            'source': 'com.zhihu.web',
            'signature': 'b13e12daee45aaa58c7a4d878189be7fab0032c1',
            # 'digits': '573330',
            'username': '1521081015111',
            'password': 'password',
            'captcha': 'vy98',
            'lang': 'en',
            'ref_source': 'settings',
            'utm_source': ''
        }
        response = requests.post(url,data=data,headers=headers)
        print(response)
        print(response.text)

    def getHtml(self, page_no):
        url = 'https://www.zhihu.com'
        print("req url:  "+url)
        # response = requests.get(url)
        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            "upgrade-insecure-requests": "1",
        }
        response = requests.get(url,headers=headers)
        ##    req.encoding = "UTF-8"

        return response.text

    def parse_html_xpath(self, text, index):
        print(text)
def start():
    print('spider start ...')
    startt = time.clock()
    errors = []#存放网页打不开等错误
    zhihu = spider_main()
    i = 25
    while i<=25:
        try:
            text = zhihu.getHtml(i)
        except Exception as e:
            text = False
            errors.append(e)
        finally:
            if text:
                f = open(r'file\fivestart-'+str(i)+'.html', 'w', encoding='utf-8')
                f.write(text)
                f.close()
                zhihu.parse_html_xpath(text, i)
            i +=1
    # zhihu.save2db()
    if errors:
        print("It's bad,there is something wrong waiting for handling!!")
    else:
        print(None,"perfect!!")
    endt = time.clock()
    print("run over!!cost total_time:%s"%(endt - startt))
if __name__ == "__main__":
    zhihu = spider_main()
    # txt = zhihu.getHtml(1)
    # print(txt)
    zhihu.login()
    # start()