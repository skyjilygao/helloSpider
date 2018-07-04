from bs4 import BeautifulSoup
import requests
import json
from zhtools.langconv import *
import pymysql

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
    url = 'https://developers.facebook.com/docs/marketing-api/adgroup/feedback/v3.0'
    # 请求，获取html页面
    def getHtml(self):

        headers = {
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            "upgrade-insecure-requests": "1",
            "accept-language":"zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7"
            # "accept-language":"us-EN,en;q=0.9,en;q=0.8,us-EN;q=0.7"
        }
        resp = requests.get(self.url,headers=headers)
        # resp = requests.get(self.url)
        text = resp.text
        f = open('feedback.html','w',encoding='utf-8')
        f.write(text)
        return text

    def parseHtml_bs4(self, text):
        soup = BeautifulSoup(text, 'lxml')
        contents = soup.select('._5m37')
        content = contents[0]
        # print('content=',content)
        # return
        item2 = content.select('tr')
        # print('item=', item1[0])
        # print('item=', item1[1])
        # print('item=', item1[2])
        # item2 = item1[3]
        i=0
        feedback = []
        for div in item2:
            fb = {
                'key': '',
                'msg':''
            }
            # print('i=' + str(i), div)

            key = div.select('td')[0].text
            msg = div.select('td')[1].text
            # print('key=', key)
            # print('msg=', msg)
            fb['key'] = key
            fb['msg'] = msg
            feedback.append(fb)
            i += 1

        self.feedback = feedback
        print('feedback=',feedback)
        print('feedback-json=',json.dumps(feedback))
        # i = 0
        # 标题 ok
        # for div in item3:
        #     print('i=' + str(i), div.text)
        #     i += 1
        # item4 = item2.select('._3-8x')
        # print('item4=', item4[1].text)
        # for div in item4:
        #     print('i=' + str(i), div.text)
        #     i += 1
    def save2db(self):
        # j = json.dumps(self.feedback, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        # print(j)
        print('insert db start...')
        # 创建链接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', database='pyspider',charset='utf8')
        # 连接数据库
        # conn = pymysql.Connect(host='localhost',port=3306,user='root',passwd='123456',db='pyspider',charset='utf8')
        # 创建游标
        cursor = conn.cursor()

        sql = "insert into ad_review_feedback_definitions(`key`, msg) values(%s, %s)"
        # list = json.dumps(self.feedback, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        list = self.feedback
        for m in list:
            try:
                cursor.execute(sql, (m.get("key"), m.get("msg")))
                conn.commit()
                print('insert one of list ok')
            except Exception as e:
                print('insert error', e)
                conn.rollback()
        conn.close()
        print('insert db end...')

def start():
    print('start...')
    fb = spider_fb()
    text = fb.getHtml()
    fb.parseHtml_bs4(text)
    fb.save2db()

if __name__ == "__main__":
    start()