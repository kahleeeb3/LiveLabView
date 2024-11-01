import tkinter as tk
from Resizing import Window # see previous example

class Collapsible():
    def __init__(self, master, row, column, name, width):

        self.body = tk.Frame(master, bg='purple', width=width)
        self.body.grid(row=row, column=column, sticky="nsew")
        tk.Grid.rowconfigure(master, row, weight=1)
        
        self.master = master
        self.row = row
        self.width = width
        self.name = name
        self.create_button_frame()
        self.create_collapsed_content_frame()

    def create_button_frame(self):
        self.button_frame = tk.Frame(self.body, bg='grey', width=25, height=25)
        self.button_frame.grid(row=0, column=0, sticky="nsew")

        self.button = tk.Button(self.button_frame, text=f'{self.name} \u25BC', width=self.width, command=self.collapse)
        self.button.grid(row=0, sticky="nsew")

    def create_collapsed_content_frame(self):
        self.collapsed_content = tk.Frame(self.body, bg='cyan')
        self.collapsed_content.grid(row=1, column=0, sticky="nsew")
        tk.Grid.rowconfigure(self.body, 1, weight=1)

    def collapse(self):
        if self.collapsed_content.winfo_ismapped():
            self.collapsed_content.grid_remove()
            self.button.config(text=f'{self.name} \u25B6')
            tk.Grid.rowconfigure(self.master, self.row, weight=0)
        else:
            self.collapsed_content.grid()
            self.button.config(text=f'{self.name} \u25BC')
            tk.Grid.rowconfigure(self.master, self.row, weight=1)

if __name__=="__main__":
    root = tk.Tk()
    window = Window(root)

    # create collapsable
    menu1 = Collapsible(master=window.left_frame, row=0, column=0, name="Title 1", width=25)
    menu2 = Collapsible(master=window.left_frame, row=1, column=0, name="Title 2", width=15)

    # add some content
    label1 = tk.Label(menu1.collapsed_content, text='Some Text')
    label2 = tk.Label(menu2.collapsed_content, text='Some Text')

    # place the content
    label1.grid(row=0, column=0)
    label2.grid(row=0, column=0)

    root.mainloop()