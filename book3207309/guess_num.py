# coding: utf-8
import tkinter as tk
import random

number=random.randint(0,1024)
running=True
num=0
nmax=1024
nmin=0

def eBtnClose(event):
    root.destroy()

def eBtnGuess(event):
    global nmax
    global nmin
    global num
    global running

    if running:
        val_a=int(entry_a.get())
        if val_a==number:
            labelqval("恭喜答对了！")
            num+=1
            running=False
            numGuess()
        elif val_a<number:
            if val_a>nmin:
                nmin=val_a
                num+=1
                labelqval("小了，请输入"+str(nmin)+"到"+str(nmax)+"之间的任意整数：")
        else:
            if val_a<nmax:
                nmax=val_a
                num+=1
                labelqval("大了，请输入"+str(nmin)+"到"+str(nmax)+"之间的任意整数：")
    else:
        labelqval('你已经答对了……')

def numGuess():
    if num==1:
        labelqval('一次答对!')
    elif num<10:
        labelqval("==十次以内就答对了，尝试次数："+str(num))
    else:
        labelqval("好吧，你都试了超过10次了...尝试次数："+str(num))

def labelqval(vText):
    label_val_q.config(label_val_q,text=vText)

root=tk.Tk(className="猜数字游戏")
root.geometry("400x90+200+200")
label_val_q=tk.Label(root,width="80")
label_val_q.pack(side="top")

entry_a=tk.Entry(root,width="40")
btnGuess=tk.Button(root,text="猜")
entry_a.pack(side="left")
entry_a.bind('<Return>',eBtnGuess)
btnGuess.bind('<Button-1>',eBtnGuess)
btnGuess.pack(side="left")
btnClose=tk.Button(root,text="关闭")
btnClose.bind('<Button-1>',eBtnClose)
btnClose.pack(side='left')
labelqval("输入0到1024之间的整数")
entry_a.focus_set()
print(number)
root.mainloop()