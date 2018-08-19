#!/usr/bin/evn python3
#coding=utf-8

import mysql.connector as mysql

'''
    1）下载mysql connector for python
    https://dev.mysql.com/downloads/connector/python/
    Windows (x86, 64-bit), MSI Installer
    Python 3.4    8.0.11    268.0K    

    2） 安装mysql connector for python
          安装目录：
    C:\Python34\Lib\site-packages\mysql\connector
    
    3）mysql connector for python参考手册
    https://dev.mysql.com/doc/connector-python/en/connector-python-reference.html
'''



class MariaDB(object):
    def __init__(self):
        pass
    
    def connect(self):
        '''
        连接MariaDB
        '''
        DB_NAME = 'web_collections'
        dbConfig = {
                'user':'root',
                'password':'',
                'host':'127.0.0.1',
                }
        
        cnt = 0
        while cnt < 3:
            try:
                #建立数据库连接
                self.cnx = mysql.connect(**dbConfig)
                self.cur = self.cnx.cursor()
                
                #创建数据库
                self.cur.execute("SHOW DATABASES")
                ret_list = self.cur.fetchall()
                if ret_list is None or (DB_NAME,) not in ret_list:
                    #创建数据库
                    self.cur.execute("CREATE DATABASE {}".format(DB_NAME))
                #选择数据库
                self.cur.execute("USE {}".format(DB_NAME))
                
                #退出
                break
            except mysql.Error as err:
                print("连接数据库失败：{}".format(err))
            finally:
                cnt = cnt + 1
    
    def disconnect(self): 
        '''
        断开数据库连接
        '''
        try:
            self.cnx.close()
            self.cur.close()   
        except mysql.Error as err:
            print("disconnect failed: {}".format(err))
    
    
    def execute(self, cmd):
        try:
            self.cur.execute(cmd)
        except mysql.Error as err:
            print("disconnect failed: {}".format(err))

    def get_rec(self, cmd):
        try:
            self.cur.execute(cmd)
            ret_list = self.cur.fetchall()
            return ret_list
        except mysql.Error as err:
            print("disconnect failed: {}".format(err))
        