import os
import sys
import tkinter as tk
import threading
import time
import random
import math


class EisenbergResource:
    def __init__(self, n, root):
        self.flags = [0] * n
        self.NUM_THREADS = n
        self.IDLE = 0
        self.WAITING = 1
        self.ACTIVE = 2
        self.WAIT = 3
        self.turn = random.randint(0, n - 1)

        self.root = root
        self.text = tk.Text(root)
        self.text.pack()
        self.progress_panel = ProgressPanel(n)
        self.progress_panel.pack()
        self.threads = []

    def start_thread(self, id):
        thread = EisenbergThread(id, self)
        self.threads.append(thread)
        thread.start()


class EisenbergThread(threading.Thread):
    def __init__(self, id, resource):
        super().__init__()
        self.id = id
        self.resource = resource

    def run(self):
        while True:
            ra = random.Random()
            m = ra.randint(0, 9)
            if m > 3:

                while True:
                    self.resource.flags[self.id] = self.resource.WAITING
                    self.resource.progress_panel.set_color(self.id, self.resource.WAITING)

                    index = self.resource.turn
                    while index != self.id:
                        if self.resource.flags[index] != self.resource.IDLE:
                            index = self.resource.turn
                        else:
                            index = (index + 1) % self.resource.NUM_THREADS
                        time.sleep(1)

                    self.resource.flags[self.id] = self.resource.ACTIVE

                    index = 0
                    while self.resource.flags[index] != self.resource.ACTIVE:
                        index = (index + 1) % self.resource.NUM_THREADS
                    self.resource.text.insert(tk.END, f"进程{self.id + 1}正在等待.....\n")
                    self.resource.progress_panel.set_color(self.id, self.resource.WAIT)
                    self.resource.text.see(tk.END)
                    time.sleep(1)
                    if index == self.id and (self.resource.turn == self.id or self.resource.flags[
                        self.resource.turn] == self.resource.IDLE):
                        break

                    self.resource.turn = self.id
                time.sleep(1)

                self.resource.text.insert(tk.END, f"---进程{self.id + 1}正在访问临界区---\n")
                self.resource.text.see(tk.END)
                self.resource.progress_panel.set_color(self.id, self.resource.ACTIVE)
                time.sleep(1.5 + ra.uniform(0, 0.5))

                index = (self.resource.turn + 1) % self.resource.NUM_THREADS
                while self.resource.flags[index] == self.resource.IDLE:
                    index = (index + 1) % self.resource.NUM_THREADS
                self.resource.turn = index
                self.resource.flags[self.id] = self.resource.IDLE
                self.resource.progress_panel.set_color(self.id, self.resource.IDLE)
                self.resource.text.insert(tk.END, f"*****进程{self.id + 1}访问结束！*****\n")
                self.resource.text.see(tk.END)
                time.sleep(1)



            else:
                time.sleep(1)
                self.resource.flags[self.id] = self.resource.IDLE
                self.resource.progress_panel.set_color(self.id, self.resource.IDLE)
                self.resource.text.insert(tk.END, f"*****进程{self.id + 1}从现在开始10个时间片不想进入临界区\n")
                self.resource.text.see(tk.END)
                time.sleep(10)


class ProgressPanel(tk.Canvas):
    def __init__(self, NUM_THREADS):
        super().__init__()
        self.NUM_THREADS = NUM_THREADS
        self.change_color = [0] * NUM_THREADS
        self.x0, self.y0 = 170, 130
        self.r = 95

    def set_color(self, id, change_id):
        self.change_color[id] = change_id
        self.draw()

    def jisuan_x(self, id):
        x1 = 50 + (id % 5) * 70
        return int(x1)

    def jisuan_y(self, id):
        y1 = 160 + id // 5 * 70
        return int(y1)

    def draw_critical(self):
        x0, y0 = 130, 20
        self.create_rectangle(x0, y0, x0 + 140, y0 + 30, fill="pink")
        self.create_text(x0 + 70, y0 + 10, text="临界区")
        self.create_rectangle(x0, y0, x0 + 140, y0 + 120)

    def draw(self):
        self.delete("all")
        self.draw_critical()
        for i in range(self.NUM_THREADS):
            x = self.jisuan_x(i)
            y = self.jisuan_y(i)
            if self.change_color[i] == 0:
                color = "red"
            elif self.change_color[i] == 1:
                color = "yellow"
            elif self.change_color[i] == 2:
                color = "pink"
                x = 130 + 70
                y = 20 + 60
            elif self.change_color[i] == 3:
                color = "green"


            self.create_oval(x - 15, y - 15, x + 16, y + 16, fill=color, outline="black")
            self.create_text(x, y, text=str(i + 1))


def restart_program():
    python = sys.executable
    os.execl(python, python, 'C:\\Users\\diomedes\\Desktop\\os\\tk3.py')


def main(n=4):
    root = tk.Tk()
    root.title("Eisenberg算法示例")

    resource = EisenbergResource(n, root)

    for i in range(n):
        thread = EisenbergThread(i, resource)
        resource.threads.append(thread)
        thread.daemon = True  # 设置为附属线程，主线程关闭后自动杀死
        thread.start()
    b1 = tk.Button(root, relief='flat', activebackground='orange', bg='lightgreen', overrelief='raised',
                   text='back',
                   command=restart_program)

    b1.place(width=60, height=45, x=80 + 400, y=360)
    root.mainloop()


if __name__ == "__main__":
    n = int(input('请输入进程数量'))
    main(n)
