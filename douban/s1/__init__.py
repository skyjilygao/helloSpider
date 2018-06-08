##https://movie.douban.com/top250?start=0&filter=
##https://movie.douban.com/top250?start=25&filter=
##https://movie.douban.com/top250?start=50&filter=
##https://movie.douban.com/top250?start=225&filter=
import time
import requests
from bs4 import BeautifulSoup
import json
import pymysql
##import re
class spider_douban():
    def __init__(self):
        self.href = []#电影链接
        self.movie_name = []#电影名：list中英other
        self.derector_act = []#电影导演和主演等
        self.review = []#简评
        self.comment = []#评分和评价数
        self.errors = []
        self.movies = []
        self.m_list = []
    def getHtml(self,page):
        url = 'https://movie.douban.com/top250?start=%s&filter=' %page
        print("req url:  "+url)
        req = requests.get(url)
        ##    req.encoding = "UTF-8"
        return req.text

    #bs4
    def parseHtml_bs4(self,text, index):

        f = open('text'+str(index)+'.html','w',encoding='utf-8')
        f.write(text)
        f.close()
        soup = BeautifulSoup(text,"lxml")#解析器lxml或者html.parser
        content = soup.select("#wrapper #content")#返回列表，列表内的内容才能select
        title = content[0].select("h1")[0].text#list没有text，所以得[0]先取出
        ##    print(title)
        content2 = content[0].select(".article .grid_view")
        ##        print(len(content2))
        m_list = []
        print('1_size22222-====')
        print(len(content2[0].select("li")))
        ii = 0
        for li in content2[0].select("li"):
            movie_dic = {}
            m = movie()
            try:
                #li>item下主要两个标签pic和info
                ##        pic_href = li.select(".item .pic")#该电影链接和图片，info中也有电影链接
                ##        href = pic_href[0].select("a")[0]["href"]
                #info下主要两个标签hd>a和bd
                hd = li.select(".item .info .hd a")#包括电影链接、中英文名、简评
                self.href.append( hd[0]["href"])#电影链接
                movie_dic["href"] = hd[0]["href"]
                m.href = hd[0]["href"]
                movie_namec_e = hd[0].select(".title")#返回列表[中文名，英文名]
                ##        for i in movie_namec_e:
                ##            print(i)
                ##        break
                zh_name = movie_namec_e[0].text
                try:#可能不存在英文名
                    en_name = movie_namec_e[1].text
                except:
                    en_name = ''
                    ##        print(en_name)
                    ##        break
                try:
                    oth_name = hd[0].select(".other")[0].text
                except:
                    oth_name = ''
                print('1______222------')
                self.movie_name.append([zh_name,en_name,oth_name])
                movie_dic["name"] = zh_name + en_name + oth_name
                m.name = zh_name + en_name + oth_name
                ##        for i in L:
                ##            print (i)
                bd = li.select(".item .info .bd")#包括导演、主演、发行时间国家、电影类型；评星评分和评价数；简评
                ##        print(bd)
                movie_infor = bd[0].select("p")
                derector_act = movie_infor[0].text
                self.derector_act.append(derector_act)
                self.review.append(movie_infor[1].text)#简评

                move = dict.fromkeys((ord(c) for c in u"\xa0\n"))
                output = derector_act.strip().translate(move)
                movie_dic["derector_act"] = output.replace(" ", "")
                movie_dic["review"] = movie_infor[1].text

                m.derector = output
                m.review = movie_infor[1].text
                ##        print(derector_act,comment)
                L2 = []
                for span in bd[0].select(".star"):
                    ##            print(span.text)
                    if span.text :
                        L2.append(span.text.strip("\n"))#评分和评价数
                self.comment.append(L2)
                str1 = ','.join(L2)
                movie_dic["comment"] = str1
                m.comment = str1
                ##        print(L2)
                ##           break
                print('1_movie=')
                print(movie_dic)
                self.movies.append(movie_dic)
                # m_list.append(m)
                print('1____m=')
                print(m)
                self.m_list.append(m)
                print('1_size='+str(ii),self.m_list)
                print(len(self.m_list))
            except Exception as e:
                print('1_eeeeerrrro')
                print(e)
                self.errors.append(e)
            ii += 1

    def save(self):
        print(self.movies)
        j = json.dumps(self.movies)
        print(j)
        if self.errors:#保存error信息
            print("(self.errors)It's bad,there is something wrong waiting for handling!!")
        else:
            print(self)
            print(None,"good")
        ##        for href,movie_name,derector_act,review,comment in\
        ##            zip(self.href,self.movie_name,self.derector_act, self.review, self.comment):
        ##            print(href,movie_name,derector_act,review,comment)
        ##            print("----------------")

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
        list = cursor.execute('select * from top250')
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

    # def page_to_page(self,start,end):
    #     i = 0
    #     while i <=1:
    #         self.getHtml(25*i)
def start():
    startt = time.clock()
    errors = []#存放网页打不开等错误
    i = 0
    demo = spider_douban()
    while i<=0:
        try:
            text = demo.getHtml(25*i)
        except Exception as e:
            text = False
            errors.append(e)
        finally:
            if text:
                demo.parseHtml_bs4(text, i)
            i +=1
    # demo.save()
    demo.save2db()
    if errors:
        print("It's bad,there is something wrong waiting for handling!!")
    else:
        print(None,"perfect!!")
    endt = time.clock()
    print("run over!!cost total_time:%s"%(endt - startt))

class movie():
    id,
    name =''
    derector = ''
    review = ''
    comment = ''
    href = ''


if __name__ =="__main__":
    demo = spider_douban()
    start()
