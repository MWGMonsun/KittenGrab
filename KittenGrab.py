import inspect
import os
import tkinter
from tkinter import *
from tkinter import ttk
import json
import time
import requests
from searchjson import GetKeyValue
import threading
import time
import datetime
import pytz
import ctypes
headers = ""
post_data1 = None
grab_status = 0
def L1():
    file = open("course_data.txt", 'w').close()
    os.system('start ' + 'course_data.txt')

def Refresh_L():
    global Refresh_label1
    global Refresh_label2
    global Refresh_label3
    global Refresh_label4
    global Refresh_label5
    global Refresh_label6
    global Refresh_label7
    global post_data1
    global post_data2
    global post_data3
    global post_data4
    global post_data5
    global post_data6
    global post_data7

    #---------------------导入课程-----------------------------#
    file = open("course_data.txt",'r',encoding='utf-8')
    f_context=file.read()
    file.close()
    if f_context != "":
        post_data1=f_context
        f_json = GetKeyValue(f_context, mode='s')
        Refresh_label1.configure(text=f_json.search_key('sbjetCd'))
        Refresh_label4.configure(text=f_json.search_key('sbjetNm'))
        Refresh_label5.configure(text=f_json.search_key('sbjetSctnm'))
    else:
        Refresh_label1.configure(text="无")
        Refresh_label4.configure(text="无")
        Refresh_label5.configure(text="无")
    # ---------------------导入课程-----------------------------#



def GET_Headers():
    global warning_change
    localtime = time.asctime(time.localtime(time.time()))
    time_label.configure(text = localtime)
    file = open("headers.txt", 'w').close()
    os.system('start ' + 'headers.txt')
    warning_change.configure(text="警告 : headers格式未转换！")


def Change_Headers():
    global headers
    global warning_change
    file = open("headers.txt", 'r')
    headers = file.read()
    if headers != "":
        headers = headers.strip().split('\n')
        headers = {x.split(':')[0].strip(): ("".join(x.split(':')[1:])).strip().replace('//', "://") for x in headers}
        file.close()
        print(headers)
        warning_change.configure(text="headers已加载成功!")
    else:
        warning_change.configure(text="警告:headers文本为空！")

def thread_it(func, *args):
    # u将函数打包进线程
    t = threading.Thread(target=func, args=args)
    t.setDaemon = True
    t.start()


def Start_grab():
    global headers
    global post_data1
    global post_data2
    global post_data3
    global post_data4
    global post_data5
    global post_data6
    global post_data7
    global grab_status
    global grab_url
    global grab_delay
    global Post_times

    url = grab_url.get()
    delay = grab_delay.get()
    if grab_status == 0:
        Start_post.configure(text="停止抢课")
        grab_status =1
        print("抢课开始")
        if post_data1 != None:
            for i in range(1,200):
                response = requests.request("POST", url, headers=headers, data=post_data1.encode('utf-8'))
                response_listbox.insert("end","["+str(i)+"]"+response.text)
                response_listbox.see("end")
                time.sleep(float(delay))
                Post_times.configure(text = int(Post_times.cget("text"))+1)
                if grab_status == 0:
                    break
        print("抢课结束")
        Start_post.configure(text="开始抢课")
        grab_status=0
    else:
        Start_post.configure(text="开始抢课")
        grab_status = 0

def reset_win():
    global response_listbox
    global Post_times
    Post_times.configure(text = '0')
    response_listbox.delete(0,END)
    response_listbox.see("active")

#-----------猫猫抢课2.0添加内容------------
def dalay_start():
    global grab_status
    thread_it(Start_grab)
    time.sleep(2)
    Start_post.configure(text="开始抢课")
    grab_status=0

def show_time():
    global seoul_tz
    global seoul_time
    global grab_settime
    time_obj = tkinter.StringVar()
    while True:
        seoul_time = datetime.datetime.now(seoul_tz).strftime("%H:%M:%S")
        if seoul_time == grab_settime.get():
            print("时间到开始抢课")
            ttk.Label(mainframe, text="抢课已开始").grid(column=7, row=8, sticky=W)
            thread_it(Start_grab())
            break
        else:
            time_obj.set(seoul_time)
            ttk.Label(mainframe, textvariable=time_obj).grid(column=7, row=8, sticky=W)
            time.sleep(0.5)
#-----------猫猫抢课2.0添加内容------------


if __name__ == "__main__":
    root = Tk()
    root.title("猫猫抢课2.0")
    root.iconbitmap("./robotcat.ico")
    root.resizable(0, 0)
    mainframe = ttk.Frame(root, padding="12 7 15 15")
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mainframe.columnconfigure(0, weight=1)
    mainframe.rowconfigure(0, weight=1)

    # -----------猫猫抢课2.0添加内容------------
    seoul_tz = pytz.timezone('Asia/Seoul')
    seoul_time = datetime.datetime.now(seoul_tz)
    # -----------猫猫抢课2.0添加内容------------

    L1_Button = ttk.Button(mainframe, text="导入课程", command=L1)
    L1_Button.grid(column=6, row=5, sticky=E)

    Refresh_label2 = ttk.Label(mainframe, text="==========")
    Refresh_label2.grid(column=2, row=2, sticky=N, columnspan=2)
    Refresh_label1 = ttk.Label(mainframe, text="未刷新")
    Refresh_label1.grid(column=2, row=3, sticky=N, columnspan=2)
    Refresh_label3 = ttk.Label(mainframe, text="==========")
    Refresh_label3.grid(column=2, row=4, sticky=N, columnspan=2)
    Refresh_label4 = ttk.Label(mainframe, text="未刷新")
    Refresh_label4.grid(column=2, row=5, sticky=N, columnspan=2)

    Refresh_label5 = ttk.Label(mainframe, text="未刷新")
    Refresh_label5.grid(column=2, row=6, sticky=N, columnspan=2)
    Refresh_label6 = ttk.Label(mainframe, text="==========")
    Refresh_label6.grid(column=2, row=7, sticky=N, columnspan=2)

    ttk.Label(mainframe, text="目标网址(url):").grid(column=6, row=1, sticky=E)
    grab_url = ttk.Entry(mainframe)
    grab_url.grid(column=7, row=1, sticky=W)

    ttk.Label(mainframe, text="抢课间隔(秒):").grid(column=6, row=2, sticky=E)
    grab_delay = ttk.Entry(mainframe)
    grab_delay.grid(column=7, row=2, sticky=W)

    ttk.Button(mainframe, text="导入headers", command=GET_Headers).grid(column=6, row=3, sticky=E)
    time_label = ttk.Label(mainframe, text="(在此显示最后一次导入时间)")
    time_label.grid(column=7, row=3, sticky=N)

    change_hd = ttk.Button(mainframe, text="加载headers", command=Change_Headers)
    change_hd.grid(column=6, row=4, sticky=E)
    Start_post = ttk.Button(mainframe, text="开始抢课", command=lambda: thread_it(Start_grab))
    Start_post.grid(column=2, row=1, sticky=W)
    Clear_Status = ttk.Button(mainframe, text="加载课程", command=Refresh_L)
    Clear_Status.grid(column=6, row=6, sticky=W)
    Test_button = ttk.Button(mainframe, text="重置状态", command=reset_win)
    Test_button.grid(column=6, row=7, sticky=W)

    # -----------猫猫抢课2.0添加内容------------
    delay_button = ttk.Button(mainframe, text="定时开抢", command=lambda: thread_it(show_time))
    delay_button.grid(column=2, row=8, sticky=W)
    ttk.Label(mainframe, text="当前时间:").grid(column=6, row=8, sticky=E)
    ttk.Label(mainframe, text="开抢时间(例14:59:55):").grid(column=7, row=8, sticky=E)
    grab_settime = ttk.Entry(mainframe)
    grab_settime.grid(column =8,row=8,sticky=W)
    # -----------猫猫抢课2.0添加内容------------

    warning_change = ttk.Label(mainframe, text="警告 : headers格式未转换！")
    warning_change.grid(column=7, row=4, sticky=N)
    response_Lable = ttk.Label(mainframe, text="=====================")
    response_Lable.grid(column=7, row=5, sticky=N)

    ttk.Label(mainframe, text="封包发送次数(post times)").grid(column=7, row=6, sticky=N)
    Post_times = ttk.Label(mainframe, text="0")
    Post_times.grid(column=7, row=7, sticky=N)

    ttk.Label(mainframe, text="返回封包(response):").grid(column=8, row=1, sticky=W)
    response_listbox = Listbox(mainframe, width=40)
    response_listbox.grid(column=8, row=2, columnspan=2, rowspan=6, sticky=N)

    root.mainloop()




