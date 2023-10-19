import os
import sys
import tkinter as tk
import threading
import random
import time

x0, y0 = 170, 40


def rand_sleep():
    return random.random() + random.randint(0, 2)


def sleep(t):
    time.sleep(t)


class DekkerResource:
    def __init__(self, root):
        self.items = [-1, -1]
        self.txts=[None,None]
        self.wantEnter = [False, False]
        self.seconds = [0, 0]
        self.seconds_txts = [None, None]
        self.dekker_turn = random.randint(0, 1)
        self.root = root

        self.text = tk.Text(root)
        self.text.pack()

        self.dynamicPanel = tk.Canvas(root, width=400, height=200)
        # 画出临界区
        self.dynamicPanel.create_rectangle(x0, y0, x0 + 140, y0 + 30, fill="pink")
        self.dynamicPanel.create_text(x0 + 70, y0 + 10, text="临界区")
        self.dynamicPanel.create_rectangle(x0, y0, x0 + 140, y0 + 120)

        self.dynamicPanel.pack()


def dekker_thread(root, id, resource):
    resource.text.tag_config("tag_red", foreground="red")
    resource.text.tag_config("tag_yellow", background="grey", foreground="yellow")
    resource.text.tag_config("tag_pink", foreground="pink")
    resource.text.tag_config("tag_pink2", background="pink")
    resource.text.tag_config("tag_blue", foreground="blue")
    while True:
        resource.wantEnter[id] = True
        if resource.items[id] == -1:
            resource.items[id] = resource.dynamicPanel.create_oval(90 * id, 100, 90 * id + 50, 150)
            resource.txts[id] = resource.dynamicPanel.create_text(90*id+25,170,text=f"进程{id}")
        resource.dynamicPanel.itemconfig(resource.items[id],
                                         fill="yellow")
        root.update_idletasks()
        time.sleep(1.5)

        while resource.wantEnter[1 - id]:
            if resource.dekker_turn == 1 - id:
                resource.wantEnter[id] = False
                resource.dynamicPanel.itemconfig(resource.items[id],
                                                 fill="red")

                resource.text.insert("end", f"turn为{resource.dekker_turn},进程{id}放弃\n", "tag_red")
                resource.text.see(tk.END)

                while resource.dekker_turn == 1 - id:
                    resource.text.insert(tk.END, f"turn为 {resource.dekker_turn}进程 {id}等待中\n",
                                         "tag_yellow")  # 黄色的时候为wantEnter 只有先黄才能进入
                    resource.text.see(tk.END)
                    time.sleep(0.8)
                resource.wantEnter[id] = True
                resource.dynamicPanel.itemconfig(resource.items[id],
                                                 fill="yellow")
            else:
                resource.text.insert(tk.END, f"turn为{resource.dekker_turn},进程{id}等对方放弃\n")
                resource.text.see(tk.END)
                time.sleep(0.8)

        time.sleep(1)
        resource.dynamicPanel.itemconfig(resource.items[id],
                                         fill="pink")
        resource.dynamicPanel.coords(resource.items[id], x0 + 70 - 25, y0 + 60 - 25, x0 + 70 + 25, y0 + 60 + 25)
        resource.text.insert(tk.END, f"进程{id}正在访问临界区----\n", "tag_pink")
        resource.dynamicPanel.coords(resource.txts[id], x0 + 70, y0 + 60 + 45)
        resource.dynamicPanel.itemconfig(resource.txts[id], text=f"进程{id}正在运行ing")

        t = rand_sleep()
        sleep(t)
        resource.seconds[id] += round(t, 2)
        resource.text.insert(tk.END, f"~~~~进程{id}访问了临界区{t:.2f}秒,共访问临界区{resource.seconds[id]}秒~~~~\n",
                             "tag_pink2")
        resource.text.see(tk.END)
        resource.dynamicPanel.coords(resource.items[id], 90 * id + 20, 100, 90 * id + 70, 150)
        resource.dynamicPanel.coords(resource.txts[id], 90 * id + 40, 170)
        resource.dynamicPanel.itemconfig(resource.txts[id], text=f"进程{id}")
        resource.text.insert(tk.END, f"进程{id}访问结束！\n")
        resource.text.insert(tk.END, f"turn 更新为{resource.dekker_turn}\n", "tag_blue")
        resource.dekker_turn = 1 - id
        resource.text.see(tk.END)
        resource.dynamicPanel.itemconfig(resource.items[id],
                                         fill="green")
        resource.wantEnter[id] = False


def restart_program():
    python = sys.executable
    os.execl(python, python, 'C:\\Users\\diomedes\\Desktop\\os\\tk3.py')


def main():
    root = tk.Tk()

    root.title("Dekker Algorithm")
    b1 = tk.Button(root, relief='flat', activebackground='orange', bg='lightgreen', overrelief='raised',
                   text='back',
                   command=restart_program)

    b1.place(width=60, height=45, x=80 + 400, y=360)
    resource = DekkerResource(root)

    thread0 = threading.Thread(target=dekker_thread, args=(root, 0, resource))
    thread1 = threading.Thread(target=dekker_thread, args=(root, 1, resource))

    thread0.daemon = True
    thread1.daemon = True
    thread0.start()
    thread1.start()

    root.mainloop()


if __name__ == "__main__":

    main()