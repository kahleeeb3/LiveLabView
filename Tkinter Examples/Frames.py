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

root.mainloop()