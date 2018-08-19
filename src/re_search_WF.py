#!/usr/bin/evn python3
#coding=utf-8

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import time

import urllib.request
import re

from bs4 import BeautifulSoup


import mariadb

'''
用正则表达式提取百度网盘地址和提取码

从百度贴吧上搜索到王菲的专辑，用这个工具摘取链接
【华语】呕心沥血整理出94张王菲专辑
http://tieba.baidu.com/p/5493737812?pn=1

2018-7-13
用beautifulsoup4代替正则表达式处理Html文件
1) pip install beautifulsoup4
2) pip install lxml
3) pip install html5lib
4) https://www.crummy.com/software/BeautifulSoup/bs4/doc/

'''

RE_SEARCH_TABLE_NAME = 'WF_result'

class re_search_WF(object):
    def __init__(self):
        self.db = mariadb.MariaDB()
        self.db.connect()
        self.db.execute('''
            CREATE DEFINER=`root`@`localhost` PROCEDURE `INIT_PROC`()
            BEGIN
                CREATE TABLE WF_result
                            (
                            ID     INT           NOT NULL AUTO_INCREMENT,  
                            NAME   VARCHAR(255)  NULL,                     -- 名称
                            URL    VARCHAR(255)  NOT NULL ,                -- 百度网盘URL
                            CODE   CHAR(4)       NULL,                     -- 提取码
                            PRIMARY KEY (ID)
                            ) ENGINE=Maria CHARSET=utf8;

            END
            ''')
        self.db.execute('''
            CREATE DEFINER=`root`@`localhost` PROCEDURE `GET_REC`()
            BEGIN
                SELECT * FROM WF_result;
            END
        ''')
        self.db.execute('call init_proc();')
        
    def __del__(self):
        self.db.execute('''
            CREATE DEFINER=`root`@`localhost` PROCEDURE `CLEAR_PROC`()
            BEGIN
                DROP TABLE wf_result;
            
            END
            ''')
        self.db.execute('call clear_proc();')
        self.db.disconnect()
    
    def exec_sql_state(self):
        #insert
        self.db.execute('''
            INSERT INTO wf_result VALUES(
            NULL, 'ttt', 'http://www.tiexue.cn', 'a98d');
        ''')
        ret_list = self.db.get_rec('''
            SELECT * FROM wf_result
            WHERE code LIKE '%a%';
        ''')
        print(ret_list)
        
        #update
        self.db.execute('''
            UPDATE wf_result
            SET url = 'http://tiexue.cn'
            WHERE id = 3;
        ''')
        ret_list = self.db.get_rec('''
            SELECT * FROM wf_result
            WHERE code LIKE '%a%';
        ''')
        print(ret_list)
        
        #delete
        self.db.execute('''
            DELETE FROM wf_result
            WHERE url LIKE '%tiexue%';
        ''')
        ret_list = self.db.get_rec('''
            SELECT * FROM wf_result
            WHERE code LIKE '%a%';
        ''')
        print(ret_list)
        
        

    def exec_proc(self):
        '''
        TODO: 如何获得调用存储过程返回的数据集合呢？
        '''
#        self.db.sur.callproc('get_rec')
#        for i in self.db.cur.stored_results():
#            rs = i.fetchall()
#            print(rs)
        pass
        
    def save_one_rec(self, title, name, code):
        sql_state = '''
            INSERT INTO WF_result
            VALUES(NULL, 
              "{0}",
              "{1}",
              "{2}"); 
            '''.format(title, name, code)
        print(sql_state)
        try:
            #insert
            self.db.execute(sql_state)
        except mysql.Error as err:
            print("操作数据库失败：{}".format(err)) 
        
    def process_one_page(self, url):
        '''
        retry_num - 重试次数，若一个url下载失败，则再最多尝试2次
        '''
        webpage = None
        print("下载："+url)
        try:
            webpage = urllib.request.urlopen(url)
        except Exception as e:
            print("下载错误：" + url + e.reason)
            webpage = None
        return webpage


    def search_desired(self, line, f):
        m1 = re.match(r"(.*)(https://pan.baidu.com/(.*))(</a>)(.*)+", line)
        m2 = re.match(r'(.*)20140803" >[：| ]?([0-9a-z]+)(<br>|</div>)', line)  
        m3 = re.match(r'(.*)<br>(([0-9]+.)?(王菲)?《(.*?)》)(.*)', line)  
        if m1 and m2 and m3:
    #    if m1 and m2:
    #        print(m3.group(0))
    #        print(m3.group(1))
    #        print(m3.group(2))
    #        print(m3.group(3))
    #        print(m3.group(4))
    #        print(m3.group(5))
    #        print(m3.group(6))
    #        name = m1.group(2).strip('\n\r')
    #        code = m2.group(2).strip('\n\r')
            name = m1.group(2).strip()
            code = m2.group(2).strip()
            title = m3.group(2).strip()
            print(title+", "+name+", "+code+"\n")
            f.write("<tr align='center'>\n")
            f.write("<td>"+title+"</td><td>"+name+"</td><td>"+code+"</td>\n")
            f.write("</tr>\n")
            self.save_one_rec(title, name, code)

    def process_file(self, reader, f):
        for line in reader:
            line = line.decode("utf-8")
            line = line.strip()
            self.search_desired(line, f)
        
        
        
    def init_gui(self, ctn):
        '''
        todo: 初始化界面
        '''
        self.wf_info = ttk.Label(ctn, text="dsajflkjalf ")
        self.wf_info.grid(column=0,row=0, padx=3, pady=3, sticky=tk.W)

        #add btn
        def click_wf():
            f = open("./result.html", "w")
            f.write("<html>")
            f.write('''
            <head>
            <title>王菲精选集</title>
            <meta charset='GBK'>
            </head>
            <body>
            <table align="center" boder=1 rules="all">
            ''')

            for i in range(15):
                url="http://tieba.baidu.com/p/5493737812?pn=" + str(i+1)
                print(url)
                webpage = self.process_one_page(url)
                if webpage:
                    self.process_file(webpage, f)
                    webpage.close()
                time.sleep(1)
                
            
            f.write('''
            </table>
            </body>
            </html>
            ''')
            f.close()
            messagebox.showinfo("info", "下载完毕")
                    
                    
        
        self.action_getWebpage = ttk.Button(ctn, text="下载", command=click_wf)
        self.action_getWebpage.grid(column = 2, row = 2, sticky=tk.W) 

        #add btn
        def click_soup():
#            f = open(r"E:\wbin\python\workspace\TongQu\src\aa1.html",
#                      mode="w",
#                      encoding="utf8")
#            soup = BeautifulSoup(open(r"E:\wbin\python\workspace\TongQu\src\aa.html", 
#                                      encoding="utf8"),
#                                 'html.parser')
#            f.write(soup.prettify())
#            f.close()
            
            for i in range(15):
                #下载页面
                url="http://tieba.baidu.com/p/5493737812?pn=" + str(i+1)
                print(url)
                resp = urllib.request.urlopen(url)
                html = resp.read()
                #bs4解析页面
                soup = BeautifulSoup(html, 'html.parser')
                tag_list = soup.find_all("a", href=re.compile(r"http://jump.bdimg.com/"))
                print(len(tag_list))
                for i in tag_list:
                    if str(i.parent.contents[4]) != r'<br/>':
                        title = i.parent.contents[4]
                    else:
                        title = i.parent.contents[3]
                    name = i.contents[0]
                    code = i.parent.contents[-1]
                    href = i["href"]
                    print(title, name, code, href)
#                    print(i.contents[0], i["href"], i.parent.contents[-1])
                    self.save_one_rec(title, name, code)
                    time.sleep(1)
            messagebox.showinfo("info", "处理完毕！")


        self.action_getWebpage = ttk.Button(ctn, text="用BeautifulSoup格式化html文件", command=click_soup)
        self.action_getWebpage.grid(column = 2, row = 3, sticky=tk.W) 


