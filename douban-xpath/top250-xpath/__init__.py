import time
import requests
from lxml import etree
import json
from top250 import *
import pymysql
class spider_main():
    def __init__(self):
        self.m_list = []

    def getHtml(self, page):
        url = 'https://movie.douban.com/top250?start=%s&filter=' %page
        print("req url:  "+url)
        req = requests.get(url)
        ##    req.encoding = "UTF-8"
        return req.text

    def parse_html_xpath(self, text, index):
        html = etree.HTML(text)
        title = html.xpath('/html/head/title/text()')
        print(title)
        contents = html.xpath('//div[@class="info"]')
        i = 0
        for content in contents:
            m = movie()
            # 链接
            href = content.xpath('div[@class="hd"]/a/@href')[0]
            m.href = href
            # name
            names = content.xpath('div[@class="hd"]/a/span/text()')
            namestr =''.join(names)
            m.name = namestr

            # derector
            derectors = content.xpath('div[@class="bd"]/p/text()')
            derector = ''.join(derectors)
            move = dict.fromkeys((ord(c) for c in u"\xa0\n"))
            derector = derector.strip().translate(move)
            # print(derector)

            m.derector = derector
            comment = content.xpath('div[@class="bd"]/div/span[@class="rating_num"]/text()')[0]
            # print(comment)
            m.comment = comment
            review = ''
            review_obj = content.xpath('div[@class="bd"]/p[2]/span/text()')
            if review_obj:
                review = review_obj[0]
            print('1_review',review)
            m.review = review
            j = json.dumps(m, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
            print(j)
            self.m_list.append(m)

            # i +=1
            # if i==1:
            #     break
    def save2db(self):
        j = json.dumps(self.m_list, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        print(j)
        print('insert db start...')
        # 创建链接
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='123456', database='pyspider',charset='utf8')
        # 连接数据库
        # conn = pymysql.Connect(host='localhost',port=3306,user='root',passwd='123456',db='pyspider',charset='utf8')
        # 创建游标
        cursor = conn.cursor()
        # list = cursor.execute('select * from top250')
        sql = "insert into top250(name, derector, review, comment, href) values(%s, %s, %s, %s, %s)"
        list = self.m_list
        for m in list:
            try:
                cursor.execute(sql, (m.name, m.derector, m.review, m.comment, m.href))
                conn.commit()
                print('insert one of list ok')
            except Exception as e:
                print('insert error', e)
                conn.rollback()
        conn.close()
        print('insert db end...')

def start():
    print('spider start ...')
    startt = time.clock()
    errors = []#存放网页打不开等错误
    douban = spider_main()
    i = 0
    while i<=9:
        try:
            text = douban.getHtml(25*i)
        except Exception as e:
            text = False
            errors.append(e)
        finally:
            if text:
                f = open(r'file\top250-'+str(i+1)+'.html', 'w', encoding='utf-8')
                f.write(text)
                f.close()
                douban.parse_html_xpath(text, i)
            i +=1
    # douban.save()
    douban.save2db()
    if errors:
        print("It's bad,there is something wrong waiting for handling!!")
    else:
        print(None,"perfect!!")
    endt = time.clock()
    print("run over!!cost total_time:%s"%(endt - startt))

if __name__ == "__main__":
    start()