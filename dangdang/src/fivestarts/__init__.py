'''
def webscreen():
  url = 'http://www.xxx.com'
  driver = webdriver.PhantomJS()
  driver.set_page_load_timeout(300)
  driver.set_window_size(1280,800)
  driver.get(url)
  imgelement = driver.find_element_by_id('XXXX')
  location = imgelement.location
  size = imgelement.size
  savepath = r'XXXX.png'
  driver.save_screenshot(savepath)
  im = Image.open(savepath)
  left = location['x']
  top = location['y']
  right = left + size['width']
  bottom = location['y'] + size['height']
  im = im.crop((left,top,right,bottom))
  im.save(savepath)
'''
import time
import requests
class spider_main():
    def getHtml(self, page_no):
        url = 'https://www.facebook.com/ads/api/preview_iframe.php?d=AQL_dHmfNvyEP0zQs2tFSpuVwQSj-AyJrL1PrYdt-H7WtiAq7seGnQuTvPjM1FADGmT6B_KbrDXw6nC6HhTVSVF2DIvKMqvjSgnQugfIyiObBv4FqejX3R5HgUZn9j8m-B0CpUD6Ej9deL5rs-tqT2e0IN9AYW0x9s-9Sv86wGEhmI-X4kv2JfKXpDKDJSn6BT94sQ_znG11oHZgCzyHELhHP74DRaiA9ByJuNgAZQFIyt2nkHeqAzTcf3Vu-BaEsVHgCxXtr2sioHwZWdvN1mRG9YvAkr_4WB6eA0sUrpZ9Ng&t=AQI0JNCqwfbVWskZ'
        # url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-year-2017-0-2-%s' %page_no
        print("req url:  "+url)
        # req = requests.get(url)
        headers = {
            'user-agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 11_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E302 MicroMessenger/6.7.1 NetType/4G Language/zh_CN',
            "Content-Type":"application/json",
            "Referer:https":"//servicewechat.com/wxa2ae8810d8157e4b/0/page-frame.html"
        }
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
    i = 1
    while i<=1:
        try:
            text = douban.getHtml(i)
        except Exception as e:
            text = False
            errors.append(e)
        finally:
            if text:
                f = open(r'file\creative-'+str(i)+'.html', 'w', encoding='utf-8')
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