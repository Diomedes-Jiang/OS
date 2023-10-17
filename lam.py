import os
import sys
import tkinter as tk
import threading
import time
import random


class LamportResource:
    def __init__(self, n, root):
        self.number = [0] * n
        self.choosing = [0] * n
        self.N = n
        self.root = root
        self.text = tk.Text(root)
        self.text.pack()
        self.dynamic_panel = DynamicPanelInLamport(n, self.number)
        self.dynamic_panel.pack()
        self.threads = []

    def get_number(self, id):
        num = max(self.number)

        self.number[id] = num + 1
        return self.number[id]

    def more_priority(self, id, other_id):
        return (self.number[id] != 0) and ((self.number[id] < self.number[other_id]) or (
                self.number[id] == self.number[other_id] and id < other_id))

    def start_thread(self, id):
        thread = LamportThread(id, self)
        self.threads.append(thread)
        thread.start()


class LamportThread(threading.Thread):
    def __init__(self, id, resource):
        super().__init__()
        self.id = id
        self.resource = resource

    def run(self):
        while True:
            self.resource.dynamic_panel.set_color(self.id, 1)
            time.sleep(1 + random.randint(0, 3))

            self.resource.choosing[self.id] = 1
            self.resource.dynamic_panel.set_color(self.id, 5)
            time.sleep(1 + random.randint(0, 1))

            self.resource.get_number(self.id)
            self.resource.text.insert(tk.END, f"进程{self.id} 取到号码：{self.resource.number[self.id]}\n")
            self.resource.text.see(tk.END)
            self.resource.choosing[self.id] = 0
            self.resource.dynamic_panel.set_color(self.id, 2)
            time.sleep(1 + random.randint(0, 2))

            for i in range(self.resource.N):
                while self.resource.choosing[i] != 0:
                    self.resource.text.insert(tk.END, f"当进程 {i} 正在取号，进程 {self.id} 则等待其取完\n")
                    self.resource.text.see(tk.END)
                    time.sleep(1 + random.randint(0, 1))

                while self.resource.more_priority(i, self.id):
                    if random.randint(0, 12) == 0:
                        self.resource.text.insert(tk.END, f"当进程 {i} 更优先，进程 {self.id} 等待\n")
                        self.resource.text.see(tk.END)
                    time.sleep(0.1 + random.uniform(0, 0.2))

            self.resource.text.insert(tk.END, f"进程{self.id}正在访问临界区----\n")
            self.resource.text.see(tk.END)
            self.resource.dynamic_panel.set_color(self.id, 4)
            time.sleep(1 + random.randint(0, 1))

            self.resource.number[self.id] = 0
            self.resource.text.insert(tk.END, f"进程{self.id}访问结束！\n")
            self.resource.text.see(tk.END)
            self.resource.dynamic_panel.set_color(self.id, 3)

            time.sleep(random.uniform(0, 12))


class DynamicPanelInLamport(tk.Canvas):
    def __init__(self, n, numbers):
        super().__init__()
        self.x = [50 + (i % 5) * 70 for i in range(n)]
        self.y = [180 + i // 5 * 70 for i in range(n)]
        self.flag = [1] * n
        self.numbers = numbers
        self.n = n
        self.draw_colors_and_shapes()

    def set_color(self, id, color):
        self.flag[id] = color
        self.draw_colors_and_shapes()

    def draw_critical(self):  # 临界区位置
        x0, y0 = 130, 20
        self.create_rectangle(x0, y0, x0 + 140, y0 + 30, fill="pink")
        self.create_text(x0 + 70, y0 + 10, text="临界区")
        self.create_rectangle(x0, y0, x0 + 140, y0 + 120)

    def draw_colors_and_shapes(self):

        self.delete("all")
        self.draw_critical()
        for i in range(self.n):
            if self.flag[i] != 4:
                color = ""
                if self.flag[i] == 1:
                    color = "red"
                elif self.flag[i] == 2:
                    color = "yellow"
                elif self.flag[i] == 3:
                    color = "green"
                elif self.flag[i] == 5:
                    color = "blue"
                self.create_oval(self.x[i], self.y[i], self.x[i] + 50, self.y[i] + 50, fill=color)
                self.create_text(self.x[i] + 10, self.y[i] + 60, text=f"进程{i}")
                self.create_text(self.x[i] + 20, self.y[i] + 30, text=str(self.numbers[i]))
            else:
                self.draw_in_thread_shape(i)

    def draw_in_thread_shape(self, id):

        self.create_text(190, 60 + 60, text=f"进程 {id} 正在运行ing")
        self.create_oval(180, 60, 180 + 50, 60 + 50, outline="green", fill="pink", width=2)
        # self.create_oval(180, 60, 180 + 50, 60 + 50, )


def restart_program():
    python = sys.executable
    os.execl(python, python, 'C:\\Users\\diomedes\\Desktop\\os\\tk3.py')


def main(n=4):
    # 设置进程数量
    root = tk.Tk()
    root.title("Lamport算法示例")

    resource = LamportResource(n, root)

    for i in range(n):
        thread = LamportThread(i, resource)
        resource.threads.append(thread)
        thread.daemon = True  # 设置为附属线程，主线程关闭后自动杀死
        thread.start()

    b1 = tk.Button(root, relief='flat', activebackground='orange', bg='lightgreen', overrelief='raised',
                   text='back',
                   command=restart_program)

    b1.place(width=60, height=45, x=80 + 400, y=360)
    root.mainloop()


if __name__ == "__main__":
    main()
