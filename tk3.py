import ctypes
import inspect
import os
from threading import Thread
from time import sleep
from tkinter import *
import threading

from tkinter.simpledialog import askinteger
import lam
import ex
import dekker
import peterson

flag = [False, False]
turn = 0
threads = []

def draw_process(x0, y0):
    d = 40
    p0 = canvas.create_oval(x0, y0, x0 + d, y0 + d, fill="red")
    process.append(p0)





def move_item(item, x0, y0, x1, y1):
    canvas.coords(item, x0, y0, x1, y1)


def change_color(item, color):
    canvas.itemconfig(item, fill=color)



def to_dekker():
    over(0)
    dekker.main()


def to_peterson():
    over(0)
    peterson.main()
def to_lam():
    var = askinteger("text", prompt="请输入进程数量")
    over(0)
    lam.main(var)


def to_ex():
    var = askinteger("text", prompt="请输入进程数量")
    over(0)
    ex.main(var)


def over(op=1):  # 退出程序

    root.destroy()
    if op == 1:
        os._exit(0)
    # 销毁root窗口


if __name__ == "__main__":
    # Initialize
    index = 0
    root = Tk()
    root.title("基于软件互斥算法的临界区进程互斥的模拟实现")
    root.geometry("700x400+200+200")
    canvas = Canvas(root, width=500, height=400)
    sb = Scrollbar(root)

    process = []

    b1 = Button(root, relief='flat', activebackground='orange', bg='lightgreen', overrelief='raised',
                text='Dekker',
                command=to_dekker)
    b2 = Button(root, relief='flat', activebackground='orange', bg='lightgreen', overrelief='raised',
                text='Peterson',
                command=to_peterson)
    b3 = Button(root, relief='flat', activebackground='orange', bg='lightgreen', overrelief='raised',
                text='Lamport',
                command=to_lam)
    b4 = Button(root, relief='flat', activebackground='orange', bg='lightgreen', overrelief='raised',
                text='Eisenburg',
                command=to_ex)
    b1.place(width=200, height=150, x=100, y=50)
    b2.place(width=200, height=150, x=100 + 300, y=50)
    b3.place(width=200, height=150, x=100, y=50 + 200)
    b4.place(width=200, height=150, x=100 + 300, y=50 + 200)
    canvas.pack(side="right")
    root.protocol("WM_DELETE_WINDOW", over)
    root.wm_attributes("-topmost", True)
    root.mainloop()

    # Put in background
