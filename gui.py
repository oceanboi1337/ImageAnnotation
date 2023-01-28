from tkinter import *
from tkinter import ttk

class InputBox:
    def __init__(self) -> None:
        self.root = Tk()
        x, y = self.root.winfo_pointerxy()
        self.root.geometry(f'200x50+{x - 100}+{y - 25}')
        self.entry = Entry(self.root, width=200, font=('Arial', 17))
        self.entry.grid(row=0, column=1)
        self.root.bind('<Return>', self.submit)
        self.result = None

    def show(self):
        while not self.result:
            self.root.update()
        self.root.destroy()
        return self.result

    def submit(self, event):
        self.result = self.entry.get()