#! /usr/bin/python3
# coding: utf-8
# import tkinter
from tkinter import *

win = Tk()
win.title('我的第一个GUI程序')
win.geometry("800x600")
win.minsize(400, 300)

label = Label(win, text='hello,Python')
label.pack()  # 将label组件添b加到窗口中显示

button1 = Button(win, text='取消')
button1.pack(side=LEFT)

button2 = Button(win, text='确定')
button2.pack(side=RIGHT)

win.mainloop()

win2 = Tk()
win2.geometry('200x200+280+280')
win2.title('计算器示例')
# grid布局
L1 = Button(win2, text='1', width=5, bg='yellow')
L2 = Button(win2, text='2', width=5)
L3 = Button(win2, text='3', width=5)
L4 = Button(win2, text='4', width=5)
L5 = Button(win2, text='5', width=5, bg='green')
L6 = Button(win2, text='6', width=5)
L7 = Button(win2, text='7', width=5)
L8 = Button(win2, text='8', width=5)
L9 = Button(win2, text='9', width=5)
L0 = Button(win2, text='0', width=5, bg='yellow')
Lp = Button(win2, text='.')
L1.grid(row=0, column=0)
L2.grid(row=0, column=1)
L3.grid(row=0, column=2)
L4.grid(row=1, column=0)
L5.grid(row=1, column=1)
L6.grid(row=1, column=2)
L7.grid(row=2, column=0)
L8.grid(row=2, column=1)
L9.grid(row=2, column=2)
L0.grid(row=3, column=0, columnspan=2, sticky=E + W)  # 跨两行，左右贴紧
Lp.grid(row=3, column=2, sticky=E + W)
win2.mainloop()

from tkinter import messagebox as msgbox


def ok_clicked():
    msgbox.showinfo("Info", "is OK!")


win3 = Tk()
win3.title("Login")
win3.geometry('200x80')
Label(win3, text="用户名", width=6).place(x=1, y=1)  # 绝对坐标
Entry(win3, width=20).place(x=45, y=1)
Label(win3, text='密码', width=6).place(x=1, y=20)
Entry(win3, width=20, show='*').place(x=45, y=20)
Button(win3, text='登录', width=8, command=ok_clicked).place(x=40, y=40)
Button(win3, text='取消', width=8).place(x=110, y=40)
win3.mainloop()
