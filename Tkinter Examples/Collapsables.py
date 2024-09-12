import tkinter as tk

# root
root = tk.Tk()

# top frame
top_frame = tk.Frame(root, bg='red', width=50, height=25)
top_frame.grid(row=0, sticky="ew")

# center frame
center = tk.Frame(root, bg='green', width=50, height=25)
center.grid(row=1, sticky="nsew") # where on root frame

# center left frame
center_left = tk.Frame(center, bg='blue', width=100, height=190)
center_left.grid(row=0, column=0, sticky="nsw")

# center right frame
center_right = tk.Frame(center, bg='yellow', width=250, height=190)
center_right.grid(row=0, column=1, sticky="nse")

class Collapsable():
    def __init__(self, master, row, column, name, width):

        self.body = tk.Frame(master, bg='purple', width=25, height=50)
        self.body.grid(row=row, column=column, sticky="nsew")

        self.width = width
        self.name = name
        self.create_button_frame()
        self.create_collapsed_content_frame()

    def create_collapsed_content_frame(self):
        self.collapsed_content = tk.Frame(self.body, bg='cyan', width=25, height=25)
        self.collapsed_content.grid(row=1, column=0, sticky="nsew")

    def create_button_frame(self):
        self.button_frame = tk.Frame(self.body, bg='grey', width=25, height=25)
        self.button_frame.grid(row=0, column=0, sticky="nsew")

        self.button = tk.Button(self.button_frame, text=f'{self.name} \u25BC', width=self.width, command=self.collapse)
        self.button.grid(row=0, sticky="nsew")        

    def collapse(self):
        if self.collapsed_content.winfo_ismapped():
            self.collapsed_content.grid_remove()
            self.button.config(text=f'{self.name} \u25B6') 
        else:
            self.collapsed_content.grid()
            self.button.config(text=f'{self.name} \u25BC')

# create collapsable
menu1 = Collapsable(master=center_left, row=0, column=0, name="Title 1", width=13)

menu2 = Collapsable(master=center_left, row=1, column=0, name="Title 2", width=13)

# add some content
label1 = tk.Label(menu1.collapsed_content, text='Some Text')
label1.grid(row=0, column=0)

label2 = tk.Label(menu2.collapsed_content, text='Some Text')
label2.grid(row=0, column=0)

root.mainloop()