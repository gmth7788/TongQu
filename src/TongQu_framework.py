#!/usr/bin/evn python3
#coding=utf-8

import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import END
from tkinter import Menu
from tkinter import messagebox

import numpy as np
import matplotlib.pyplot as plt
from pylab import show

from threading import Thread
import time

import tooltip as ttp  #myself tooltip

import queue

from urllib.request import urlopen


import re_search_WF

class TongQu_Gui_framework(object):
    '''
           图形界面
    '''
    def create_label(self, ctn):
        self.name_label = ttk.Label(ctn, text="请输入姓名(输入个over试试看)")
        self.name_label.grid(column=0,row=0, padx=3, pady=3, sticky=tk.W)

    def create_text_box(self, ctn):
        self.name = tk.StringVar()
        self.name_entered = ttk.Entry(ctn, width=12, textvariable=self.name)
        self.name_entered.grid(column=0,row=1, padx=3, pady=3, sticky=tk.W)
        self.name_entered.focus() #set focus
        
    def create_combo_box(self, ctn): 
        self.combo1 = ttk.Label(ctn, text='选择一个数字：')
        self.combo1.grid(column=1, row=0, padx=3, pady=3, sticky=tk.W)
        self.number = tk.StringVar()
        self.number_selected = ttk.Combobox(ctn, width=20, textvariable=self.number, 
                                       state='readonly')
        self.number_selected['value'] = (1,2,4,42,100)
        self.number_selected.grid(column = 1, row= 1, padx=3, pady=3, sticky=tk.W)
        self.number_selected.current(2)

    def create_check_button(self, ctn):
        self.chVarDis = tk.IntVar()
        self.check1 = tk.Checkbutton(ctn, text="Disabled", variable=self.chVarDis, 
                                     state='disabled')
        self.check1.select()
        self.check1.grid(column=0, row=2, padx=3, pady=3, sticky=tk.W)
        
        self.chVarUn = tk.IntVar()
        self.check1 = tk.Checkbutton(ctn, text="Unchecked", variable=self.chVarUn)
        self.check1.deselect()
        self.check1.grid(column=1, row=2, padx=3, pady=3, sticky=tk.W)
        
        self.chVarEn = tk.IntVar()
        self.check2 = tk.Checkbutton(ctn, text="Enabled", variable=self.chVarEn)
        self.check2.select()
        self.check2.grid(column=2, row=2, padx=3, pady=3, sticky=tk.W)
        
    def create_raidio_button(self, ctn):
        #颜色参考： http://www.tcl.tk/man/tcl8.5/TkCmd/colors.htm
        COLOR = ['Blue', 'Gold', 'Gray95']
        
        def radioCall():
            ctn.configure(background=COLOR[self.radVar.get()])
        
        self.radVar = tk.IntVar()
        rad_list = []
        for i in range(len(COLOR)):
            rad_list.append(i)
            rad_list[i] = tk.Radiobutton(ctn, text=COLOR[i], 
                                         variable=self.radVar,
                                         value=i, command=radioCall)
            rad_list[i].grid(column=i, row=3, 
                             padx=3, pady=3, 
                             sticky=tk.W)  #向西对齐
        
    def create_scrolled_text(self, ctn):
        self.scr = scrolledtext.ScrolledText(ctn, wrap=tk.WORD)
        self.scr.grid(column=0, row=4, columnspan = 3, padx=3, pady=3)
        self.scr.insert("insert", "i like python...\n ")
        ttp.createToolTip(self.scr, "这是一个scrolled text控件") #add a ToolTip

    def create_labelframe(self, ctn):
        self.labelsframes = ttk.Labelframe(ctn, text='labels frames')
        self.labelsframes.grid(column=0, row=5, padx=10, pady=10, columnspan=3)
        for i in range(5):
            label = ttk.Label(self.labelsframes, text='labels'+str(i))
            label.grid(column = i, row = 6, padx=10, pady=20)
        
        for child in self.labelsframes.winfo_children():
            child.grid_configure(padx=10, pady=6, sticky=tk.W)
        
    def create_spinbox(self, ctn):
        def _spin():
            value = self.spin.get()
            print(value)
            self.scr.insert(tk.INSERT, value+'\n')
            
        self.spin = tk.Spinbox(ctn, values=('abc',12,"大街上发的", 0.45), 
                          relief=tk.RIDGE, #tk.SUNKEN tk.RAISED tk.FLAT tk.GROOVE tk.RIDGE
                          width=10, bd=8, command=_spin)
        self.spin.grid(column=0, row =6)
        ttp.createToolTip(self.spin, "这是一个spin控件") #add a ToolTip

    def create_button(self, ctn):
        def thread_fun(msg):
            print("thread_fun(): %s\n" % msg)
            for i in range(4):
                time.sleep(1)
                self.fmkQueue.put("thread_fun:"+str(i)+","+msg)
            print("thread_fun() is over!\n")
            
        def createThread(msg):
            runT = Thread(target=thread_fun, args=[msg]) #create thread
            runT.start()
    
        #add a button
        def clickMe():
            val = self.name.get()
            if val == 'over':
                self.action.configure(state='disabled')
            self.action.configure(text="hello，"+self.name.get())
            self.name_label.configure(foreground='blue')
            self.name_entered.focus() #set focus
            
            self.scr.insert('1.0', self.name.get()+","+
                            self.number.get()+","+
                            str(self.chVarDis.get())+","+
                            str(self.chVarUn.get())+","+
                            str(self.chVarEn.get()))
            print("text: {0}".format(self.scr.get('1.0', END)))
            
            createThread("hello，"+self.name.get())
        
        self.action = ttk.Button(ctn, text="click me", command=clickMe)
        self.action.grid(column = 2, row = 1, sticky=tk.W)    

    def create_menu(self, ctn):
        def _quit():
            ctn.quit()
            ctn.destroy()
            exit()
            
        def _msgBox():
            messagebox.showinfo("info", "通衢——我的网络爬虫，v0.01")
            messagebox.showwarning("warning", "警告消息")
            messagebox.showerror("error", "有错误发生啦")
            answer = messagebox.askyesnocancel("ask", "选择yes或no。")
            print("选择了"+str(type(answer))+","+str(answer))
            if answer == True:
                print("Ture")
            elif answer == False:
                print("False")
            else:
                print("None")
                
    
        if type(ctn) != tk.Tk:
            print("init_menu()输入参数与期望的容器类型<class 'tkinter.Tk'>不一致。"+str(type(ctn)))
            exit()
    
        self.menuBar = Menu(ctn)
        ctn.config(menu=self.menuBar)
        
        self.fileMenu = Menu(self.menuBar, tearoff=0) #删除菜单下的第一个虚线
        self.fileMenu.add_command(label="New")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=_quit)
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        
        self.helpMenu = Menu(self.menuBar, tearoff=0)
        self.helpMenu.add_command(label="About", command=_msgBox)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)        
    
    def init_frame(self, ctn):
        #add a label
        self.create_label(ctn)
    
        #add a text box
        self.create_text_box(ctn)
        
        #add combo box
        self.create_combo_box(ctn)
        
        #add check button
        self.create_check_button(ctn)
        
        #add radio button
        self.create_raidio_button(ctn)
        
        #add scrolled text widget
        self.create_scrolled_text(ctn)
    
        #add a LabelFrame
        self.create_labelframe(ctn)
        
        #add spinbox widget
        self.create_spinbox(ctn)
        
        #add button
        self.create_button(ctn)
    
    def monitor(self):
        while True:
            print("mon:"+self.fmkQueue.get())
            
    def createMonitorThread(self):
        runT = Thread(target=self.monitor) #create thread
        runT.setDaemon(True)
        runT.start()
        
    def getWebpage(self, ctn):
        '''
        从网络读取页面文件
        '''
        self.webpage_name_label = ttk.Label(ctn, text="URL：")
        self.webpage_name_label.grid(column=0,row=0, padx=3, pady=3, sticky=tk.W)
        
        #add url text
        self.webpage_url = tk.StringVar()
        self.webpage_url = ttk.Entry(ctn, width=50, textvariable=self.webpage_url)
        self.webpage_url.grid(column=1,row=0, padx=3, pady=3, sticky=tk.W)
        self.webpage_url.focus() #set focus
        
        #add btn
        def click_getWebpage():
            self.webpage = self.webpage_url.get()
            if self.webpage == '':
                self.webpage = 'https://zhidao.baidu.com/question/51570764.html' 
                self.webpage_url.insert("insert", self.webpage)
                
            #尝试多种字符集
            cnt = 0
            encoding_list = ['utf-8', 'gbk', 'gb2312']
            while True:
                try:
                    f = urlopen(self.webpage)
                    html = f.read()
                    html_decoded = html.decode(encoding=encoding_list[cnt], errors="strict") 
                    self.scr_webpage.insert("insert", html_decoded)
                    messagebox.showinfo("info", "下载完成，编码为"+encoding_list[cnt])
                    break
                except Exception as ex:
                    messagebox.showerror("error", "下载失败，编码为"+encoding_list[cnt]+"，错误信息："+str(ex))
                finally:
                    cnt = cnt + 1
                    
                    
        
        self.action_getWebpage = ttk.Button(ctn, text="走起", command=click_getWebpage)
        self.action_getWebpage.grid(column = 2, row = 0, sticky=tk.W) 
        
        #add scrolled text widget
        self.scr_webpage = scrolledtext.ScrolledText(ctn, wrap=tk.WORD)
        self.scr_webpage.grid(column=0, row=1, columnspan = 3, padx=3, pady=3)
        
        

        

    
        
    
    def __init__(self):
        self.win = tk.Tk()
        self.win.title("通衢——我自己的网络爬虫（v0.01）")
        
        #change the main window icon
        self.win.iconbitmap(r'C:\Python34\DLLs\pyc.ico')
        
#        win.withdraw() #remove the debug window 
#        messagebox.showinfo("title", "message")
#        win.resizable(0, 0)  #disable resizing the window

        #add queue
        self.fmkQueue = queue.Queue(10)
        
        #启动队列监听任务
        self.createMonitorThread()
    
        #add menu
        self.create_menu(self.win)
        
        #add tabbed
        tabControl = ttk.Notebook(self.win)
        tab1 = ttk.Frame(tabControl)
        tabControl.add(tab1, text="Tab 1")
        tab2 = ttk.Frame(tabControl)
        tabControl.add(tab2, text="Tab 2")
        tab2 = tk.Frame(tab2, bg="blue")
        tab2.pack()
        for i in range(2):
            canvas = tk.Canvas(tab2, width=150, height=80, 
                               highlightthickness=0, bg='orange')
            canvas.grid(column=i, row= i)
        tabControl.pack(expand=1, fill='both')
        
        #add tab_getWebpage
        tab_getWebpage = ttk.Frame(tabControl)
        tabControl.add(tab_getWebpage, text="从网络读取页面文件")
        self.labelframe_getWebpage = ttk.Labelframe(tab_getWebpage, text='从网络读取页面文件')
        self.labelframe_getWebpage.grid(column=0, row=0, padx=3, pady=3)
        self.getWebpage(self.labelframe_getWebpage)
        
        #add tab_wf
        tab_wf = ttk.Frame(tabControl)
        tabControl.add(tab_wf, text="正则表达式搜索百度网盘地址和提取码")
        self.labelframe_tab_wf = ttk.Labelframe(tab_wf, text='正则表达式搜索百度网盘地址和提取码')
        self.labelframe_tab_wf.grid(column=0, row=0, padx=3, pady=3)
        
        wf = re_search_WF.re_search_WF()
        wf.init_gui(self.labelframe_tab_wf)
        
        #add LabelFrame
        self.labelframe = ttk.Labelframe(tab1, text='通衢——我的网络爬虫')
        self.labelframe.grid(column=0, row=0, padx=3, pady=3)
        self.init_frame(self.labelframe)
        
    def var_test(self):
        '''
        tkinter四种变量类型
        '''
        strVar = tk.StringVar()
        strVar.set("我是字符串")
        print("StringVar(): %s" % strVar.get())
    
        intVar = tk.IntVar()
        intVar.set(1258)
        print("IntVar(): %d" % intVar.get())
    
        doubleVar = tk.DoubleVar()
        doubleVar.set(1258.34354E34)
        print("DoubleVar(): %f" % doubleVar.get())
    
        boolVar = tk.BooleanVar()
        boolVar.set(True)
        print("BooleanVar(): %d" % boolVar.get())
        
        
    
    def matplotlib_test(self):
        '''
        1)wheel
        pip install wheel
        Successfully installed wheel-0.31.1
        
        2)matplotlib
               下载安装包matplotlib-2.2.2-cp34-cp34m-win_amd64.whl (8.3 MB) 
        https://files.pythonhosted.org/packages/46/2f/02958371978f777a99287f7172aa1aaf55fb8bbd9063faceb192e67b10ea/matplotlib-2.2.2-cp34-cp34m-win_amd64.whl
        C:\Python34\Lib\site-packages\matplotlib\
        pip install matplotlib-2.2.2-cp34-cp34m-win_amd64.whl
        
        3)NumPy
        numpy‑1.14.5+mkl‑cp34‑cp34m‑win_amd64.whl
        https://www.lfd.uci.edu/~gohlke/pythonlibs/
        pip install numpy‑1.14.5+mkl‑cp34‑cp34m‑win_amd64.whl
        
        4)Matplotlib documentation
        https://matplotlib.org/users/screenshots.html
        
        '''
        x = np.arange(0, 5, 0.01)
        y = np.sin(x)
        plt.plot(x, y)
        show()

    