import ctypes
import inspect
import os
from threading import Thread
from time import sleep
from tkinter import *
import threading
from tkinter import messagebox

from tkinter.simpledialog import askinteger

import dekker
import lam
import ex
import peterson

flag = [False, False]
turn = 0
threads = []


def send_msg(msg):
    pass


def draw_process(x0, y0):
    d = 40
    p0 = canvas.create_oval(x0, y0, x0 + d, y0 + d, fill="red")
    process.append(p0)


def draw_critical():
    x0, y0 = 160, 20
    canvas.create_rectangle(x0, y0, x0 + 100, y0 + 30, fill="pink")
    canvas.create_text(x0 + 50, y0 + 10, text="临界区")
    canvas.create_rectangle(x0, y0, x0 + 100, y0 + 100)


def move_item(item, x0, y0, x1, y1):
    canvas.coords(item, x0, y0, x1, y1)


def change_color(item, color):
    canvas.itemconfig(item, fill=color)


# 算法部分 算法要放在show_函数之前
class Dekker(Thread):
    def __init__(self, id):
        super().__init__()
        self.id = id
        self.go = 1

    def visitCritical(self):
        send_msg(f"--进程{self.id}正在访问临界区--")
        move_item(process[self.id], 180, 60, 180 + 40, 60 + 40)
        change_color(process[self.id], "green")
        sleep(1)

    def run(self):
        global turn, flag
        while self.go:
            flag[self.id] = True
            while flag[1 - self.id]:
                if turn == 1 - self.id:
                    flag[self.id] = False
                    while turn == 1 - self.id:
                        pass
                    flag[self.id] = True
            self.visitCritical()
            turn = 1 - self.id
            change_color(process[self.id], "red")
            move_item(process[self.id], 60 + 240 * self.id, 230, 60 + 240 * self.id + 40, 230 + 40)
            send_msg(f'进程{self.id}退出临界区')
            flag[self.id] = False


class Peterson(Thread):
    In = [False, False]
    turn = 0

    def __init__(self, id):
        Thread.__init__(self)
        self.id = id
        self.go = 1

    def visitCritical(self):
        send_msg(f"--进程{self.id}正在访问临界区--")
        move_item(process[self.id], 180, 60, 180 + 40, 60 + 40)
        change_color(process[self.id], "green")
        sleep(1)

    def run(self):

        while self.go:
            self.In[self.id] = True
            self.turn = self.other()
            while self.In[self.other()] and self.turn == self.other():
                pass
            self.visitCritical()
            change_color(process[self.id], "red")
            send_msg(f'进程{self.id}退出临界区')
            self.In[self.id] = False
            move_item(process[self.id], 60 + 240 * self.id, 230, 60 + 240 * self.id + 40, 230 + 40)

    def other(self):
        return 1 - self.id


def show(type):
    if type == 1:
        if threads:
            send_msg("Peterson is Running!!!")
            # stop_thread_func(threads[0].get_ident())
            # stop_thread_func(threads[1].get_ident())
            threads[0].join(1)
            threads[1].join(1)
            threads.pop()
            threads.pop()
        x0, y0, x1 = 60, 230, 300
        draw_process(x0, y0)
        draw_process(x1, y0)
        draw_critical()

        p0 = Peterson(0)
        p1 = Peterson(1)
        threads.append(p0)
        threads.append(p1)
        threads[0].start()
        threads[1].start()
    else:
        if threads:
            send_msg("Dekker is Running!!!")

            threads.pop()
            threads.pop()
        x0, y0, x1 = 60, 230, 300
        draw_process(x0, y0)
        draw_process(x1, y0)
        draw_critical()
        dekker0 = Dekker(0)
        dekker1 = Dekker(1)
        threads.append(dekker0)
        threads.append(dekker1)
        threads[0].start()
        threads[1].start()


def show_warning():
    messagebox.showwarning("警告", "输入数据不合法")


def to_lam():
    var = askinteger("text", prompt="请输入进程数量")
    while var < 0 or var > 10:
        show_warning()
        var = askinteger("text", prompt="请输入进程数量")
    over(0)
    lam.main(var)


def to_ex():
    var = askinteger("text", prompt="请输入进程数量")
    while var < 0 or var > 10:
        show_warning()
        var = askinteger("text", prompt="请输入进程数量")
    over(0)
    ex.main(var)


def to_dekker():
    over(0)
    dekker.main()


def to_peterson():
    over(0)
    peterson.main()


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
    root.geometry("700x450+200+200")
    canvas = Canvas(root, width=500, height=400)

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
