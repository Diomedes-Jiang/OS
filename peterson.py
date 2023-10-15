import os
import sys
import tkinter as tk
import threading
import random
import time

x0, y0 = 170, 40
class PetersonResource:
    def __init__(self, root):
        self.wantEnter = [False, False]
        self.items = [-1, -1]
        self.txts = [None, None]
        self.peterson_turn = random.randint(0, 1)
        self.root = root

        self.text = tk.Text(root)
        self.text.pack()

        self.dynamicPanel = tk.Canvas(root, width=400, height=200)
        self.dynamicPanel.create_rectangle(x0, y0, x0 + 140, y0 + 30, fill="pink")
        self.dynamicPanel.create_text(x0 + 70, y0 + 10, text="临界区")
        self.dynamicPanel.create_rectangle(x0, y0, x0 + 140, y0 + 120)
        self.dynamicPanel.pack()

def restart_program():
    python = sys.executable
    os.execl(python, python, 'C:\\Users\\diomedes\\Desktop\\os\\tk3.py')

def peterson_thread(root,id, resource):
    while True:

        if resource.items[id] == -1:
            resource.items[id] = resource.dynamicPanel.create_oval(90 * id, 100, 90 * id + 50, 150)
            resource.txts[id] = resource.dynamicPanel.create_text(90*id+25,170,text=f"进程{id}")
        resource.dynamicPanel.itemconfig(resource.items[id],
                                         fill="red")
        try:
            time.sleep(1 + random.randint(0, 2))
        except Exception as e:
            print(e)

        resource.wantEnter[id] = True
        resource.dynamicPanel.itemconfig(resource.items[id], fill="yellow")
        try:
            time.sleep(1.5)
        except Exception as e:
            print(e)

        resource.peterson_turn = 1 - id
        resource.text.insert(tk.END, f"进程 {id}谦让，turn 更新为 {resource.peterson_turn}\n")
        resource.text.see(tk.END)
        while resource.wantEnter[1 - id] and resource.peterson_turn == 1 - id:
            resource.text.insert(tk.END, f"turn为 {resource.peterson_turn}, 进程 {id}谦让对方执行\n")
            resource.text.see(tk.END)
            try:
                time.sleep(0.8)
            except Exception as e:
                print(e)

        try:
            time.sleep(1)
        except Exception as e:
            print(e)

        resource.dynamicPanel.itemconfig(resource.items[id], fill="pink")
        resource.dynamicPanel.coords(resource.items[id], x0 + 70 - 25, y0 + 60 - 25, x0 + 70 + 25, y0 + 60 + 25)
        resource.text.insert(tk.END, f"----进程 {id}正在访问临界区----\n")

        resource.dynamicPanel.coords(resource.txts[id], x0 + 70, y0 + 60 + 45)
        resource.dynamicPanel.itemconfig(resource.txts[id], text=f"进程{id}正在运行ing")
        resource.text.see(tk.END)
        try:
            time.sleep(2 + random.randint(0, 1))
        except Exception as e:
            print(e)
        resource.dynamicPanel.coords(resource.items[id], 90 * id, 100, 90 * id + 50, 150)
        resource.dynamicPanel.coords(resource.txts[id], 90 * id + 25, 170)
        resource.dynamicPanel.itemconfig(resource.txts[id], text=f"进程{id}")
        resource.text.insert(tk.END, f"进程 {id}访问结束！\n")
        resource.text.see(tk.END)
        resource.dynamicPanel.itemconfig(resource.items[id], fill="green")
        resource.wantEnter[id] = False

def main():
    root = tk.Tk()
    root.title("Peterson Algorithm")
    b1 = tk.Button(root, relief='flat', activebackground='orange', bg='lightgreen', overrelief='raised',
                   text='back',
                   command=restart_program)

    b1.place(width=60, height=45, x=80 + 400, y=360)
    resource = PetersonResource(root)

    thread0 = threading.Thread(target=peterson_thread, args=(root,0, resource))
    thread1 = threading.Thread(target=peterson_thread, args=(root,1, resource))
    thread1.daemon = True
    thread0.daemon = True

    thread0.start()
    thread1.start()

    root.mainloop()

if __name__ == "__main__":
    main()