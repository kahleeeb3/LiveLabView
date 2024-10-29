import tkinter as tk

class Window:
    def __init__(self, root):
        self.root = root
        self.create_top_frame()
        self.create_left_frame()
        self.create_bottom_left_frame()
        self.create_bottom_right_frame()
        self.create_bottom_frame()

    def create_top_frame(self):
        top_frame = tk.Frame(self.root, bg='red', width=300, height=10)
        top_frame.grid(row=0, column=0, sticky="nsew", columnspan=3)

    def create_left_frame(self):
        left_frame = tk.Frame(self.root, bg='blue', width=10, height=100)
        left_frame.grid(row=1, column=0, sticky="nsew", rowspan=2)
    
    def create_bottom_left_frame(self):
        bottom_left_frame = tk.Frame(self.root, bg='green', width=10, height=10)
        bottom_left_frame.grid(row=1, column=1, sticky="nsew")

    def create_bottom_right_frame(self):
        bottom_right_frame = tk.Frame(self.root, bg='yellow', width=10, height=10)
        bottom_right_frame.grid(row=1, column=2, sticky="nsew")

    def create_bottom_frame(self):
        bottom_frame = tk.Frame(self.root, bg='orange', width=50, height=25)
        bottom_frame.grid(row=2, column=1, sticky="nsew", columnspan=2)


if __name__=="__main__":
    root = tk.Tk()
    window = Window(root)
    root.mainloop()