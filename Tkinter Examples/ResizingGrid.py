# https://stackoverflow.com/a/38809894
# https://tkdocs.com/tutorial/grid.html

import tkinter as tk

class Window:
    def __init__(self, root):
        self.root = root
        self.create_top_frame()
        self.create_bottom_frame()
        self.create_bottom_left_frame()
        self.create_bottom_right_frame()

    def create_top_frame(self):
        self.top_frame = tk.Frame(self.root, bg='red', width=50, height=25)
        self.top_frame.grid(row=0, sticky="nsew")
        tk.Grid.columnconfigure(self.root, 0, weight=1)

    def create_bottom_frame(self):
        self.bottom_frame = tk.Frame(self.root, bg='green', width=50, height=25)
        self.bottom_frame.grid(row=1, sticky="nsew")
        tk.Grid.rowconfigure(self.root, 1, weight=1)
    
    def create_bottom_left_frame(self):
        self.bottom_left_frame = tk.Frame(self.bottom_frame, bg='blue', width=100, height=190)
        self.bottom_left_frame.grid(row=0, column=0, sticky="nsew")
        tk.Grid.rowconfigure(self.bottom_frame, 0, weight=1)

    def create_bottom_right_frame(self):
        self.bottom_right_frame = tk.Frame(self.bottom_frame, bg='yellow', width=250, height=190)
        self.bottom_right_frame.grid(row=0, column=1, sticky="nsew")
        tk.Grid.rowconfigure(self.bottom_frame, 0, weight=1)
        tk.Grid.columnconfigure(self.bottom_frame, 1, weight=1)


if __name__=="__main__":
    root = tk.Tk()
    window = Window(root)
    root.mainloop()