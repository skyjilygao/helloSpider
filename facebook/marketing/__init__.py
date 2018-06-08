from bs4 import BeautifulSoup
import requests
import json
from zhtools.langconv import *

 # 转换繁体到简体
def cht_to_chs(line):
    line = Converter('zh-hans').convert(line)
    line.encode('utf-8')
    return line

def tradition2simple(line):
    # 将繁体转换成简体
    # line = Converter('zh-hans').convert(line)
    line = Converter('zh-hans').convert(line)
    # line = line.encode('utf-8')
    return line
class spider_fb():
    url = 'https://developers.facebook.com/support/faq/'
    # 请求，获取html页面
    def getHtml(self):
        resp = requests.get(self.url)
        text = resp.text
        f = open('fqa.html','w',encoding='utf-8')
        f.write(text)
        return text

    def parseHtml_bs4(self, text):
        soup = BeautifulSoup(text, 'lxml')
        contents = soup.select('._4xit')
        content = contents[0]
        # print('content=',content)
        items = content.select('.devsiteLoggedout ._4oqt')
        item1 = items[1].select('div')
        # print('item=', item1[0])
        # print('item=', item1[1])
        # print('item=', item1[2])
        item2 = item1[3]
        i=0
        for div in item2:
            # print('i=' + str(i), div)
            title = div.select('._3-8q')[0].text
            # print('title', title)
            j = 0
            qa_list = []
            for an in div.select('._1d--'):
                # print('1_an0', an)
                q = an.select('.clearfix')[0].text
                q = tradition2simple(q)
                # print(q)
                a = an.select('._3-8x')[0].text
                # print(a)
                a = tradition2simple(a)
                qa_dic = {'q':q, 'a':a}
                qa_list.append(qa_dic)
                # j+=1
                # if j==2:
                #     break;
            qa_json = json.dumps(qa_list)
            print('qa_json=',qa_json)
            i += 1
            if i==1:
                break;

        # i = 0
        # 标题 ok
        # for div in item3:
        #     print('i=' + str(i), div.text)
        #     i += 1
        item4 = item2.select('._3-8x')
        # print('item4=', item4[1].text)
        # for div in item4:
        #     print('i=' + str(i), div.text)
        #     i += 1


def start():
    print('start...')
    fb = spider_fb()
    text = fb.getHtml()
    fb.parseHtml_bs4(text)

if __name__ == "__main__":
    start()